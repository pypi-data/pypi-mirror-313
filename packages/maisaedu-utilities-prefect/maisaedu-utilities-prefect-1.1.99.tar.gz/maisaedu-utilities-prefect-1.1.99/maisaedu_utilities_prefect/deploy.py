try:
    from prefect.engine import signals

    prefect_2 = False
except Exception as e:
    prefect_2 = True

if prefect_2 is False:

    import prefect
    import os
    import subprocess
    import psycopg2
    import re

    from prefect import task, case, Task
    from prefect.engine import signals
    from prefect.engine.state import Failed
    from prefect.utilities.notifications import slack_notifier

    from typing import Dict, Tuple, List, Generator, Optional
    from hashlib import sha256
    from enum import Enum

    from maisaedu_utilities_prefect.secrets import download_secret, get_dsn

    notify = slack_notifier(only_states=[Failed])

    @task
    def get_last_successful_deploy(repo_name: str, current_hash: str) -> Optional[str]:
        with psycopg2.connect(get_dsn()) as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                -- Bypasses ownership requirement of CREATE TABLE IF NOT EXISTS:
                do $$
                    begin
                        if not exists (
                            select *
                            from information_schema.tables
                            where table_schema = 'meta' and table_name = 'prefect_deploys'
                        ) then
                            create table if not exists meta.prefect_deploys (
                                repository text not null,
                                deployed_at timestamp not null default current_timestamp,
                                commit_hash text not null,
                                deploy_flow_hash text
                            );
                            grant all on table meta.prefect_deploys to public;
                            comment on table meta.prefect_deploys is
                                'Records the automatic Prefect deploys and their commit hashes';
                        end if;
                    end;
                $$;
                
                select
                    commit_hash
                from
                    meta.prefect_deploys
                where
                    repository = %s and commit_hash != %s
                order by
                    deployed_at desc
                limit 1
                """,
                [repo_name, current_hash],
            )
            rows = cursor.fetchall() or [(None,)]
            return rows[0][0] if len(rows) > 0 else None

    def run_command(args: List[str], show=True) -> str:
        # A pretty name for humans to read:
        pretty_name = " ".join(arg if " " not in arg else f'"{arg}"' for arg in args)
        logger = prefect.context.logger

        if show:
            logger.info(f"Running {pretty_name}")

        # Do the running thing:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        returncode = process.returncode

        # Fail on command failure:
        if returncode != 0:
            logger.error(stderr.decode("utf8"))
            if show:
                raise signals.FAIL(
                    f"Command {pretty_name} exited with returncode {returncode}"
                )
            else:
                raise signals.FAIL
        else:
            return stdout.decode("utf8")

    @task
    def clone_repository(repo_name: str, origin: memoryview) -> str:
        prefect.context.logger.info("Cloning repository")
        run_command(
            ["git", "clone", bytes(origin).decode("utf8"), repo_name], show=False
        )
        os.chdir(repo_name)
        current_hash = run_command(["git", "rev-parse", "HEAD"]).strip()

        return current_hash

    def exclude_folder(folder: str) -> bool:
        return folder.startswith("./.git/") or folder == "./.git"

    def folder_hashes() -> Dict[str, bytes]:
        hashers: Dict[str, sha256] = {}

        for folder, subfolders, files in os.walk("."):
            if exclude_folder(folder):
                continue

            hasher = hashers.setdefault(folder, sha256())

            for filename in sorted(files):
                with open(f"{folder}/{filename}", "rb") as f:
                    hasher.update(f.read())

        return {folder: hasher.digest() for folder, hasher in hashers.items()}

    @task
    def calculate_hashes(
        last_commit_hash: Optional[str],
    ) -> Tuple[Dict[str, bytes], Dict[str, bytes]]:
        if last_commit_hash is not None:
            run_command(["git", "checkout", last_commit_hash])
            last_hashes = folder_hashes()
            run_command(["git", "switch", "-"])
        else:
            last_hashes = {}

        current_hashes = folder_hashes()

        return last_hashes, current_hashes

    @task
    def find_changed_flows(
        hash_comparison: Tuple[Dict[str, bytes], Dict[str, bytes]],
        force_deploy_all_flows,
    ) -> List[str]:
        class FolderStatus(Enum):
            NEW = 1
            CHANGED = 2
            UNCHANGED = 3
            DELETED = 4

        def parents(folder: str) -> Generator[str, None, None]:
            split = folder.split("/")
            for i, _ in enumerate(split):
                yield "/".join(split[: i + 1])

        last_hashes, current_hashes = hash_comparison

        status = {}

        # Find what happened to folders that exist now:
        for folder, current_hash in current_hashes.items():
            last_hash = last_hashes.get(folder)
            if last_hash is None:
                folder_status = FolderStatus.NEW
            elif last_hash != current_hash:
                folder_status = FolderStatus.CHANGED
            else:
                if force_deploy_all_flows is None or force_deploy_all_flows == False:
                    folder_status = FolderStatus.UNCHANGED
                else:
                    folder_status = FolderStatus.CHANGED

            status[folder] = folder_status

        # Find what happened to folders that existed earlier:
        for folder in last_hashes.keys():
            current_hash = current_hashes.get(folder)
            if current_hash is None:
                status[folder] = FolderStatus.DELETED

        # Select folders that changed:
        changed_folders = (
            folder
            for folder, folder_status in status.items()
            if folder_status == FolderStatus.CHANGED
            or folder_status == FolderStatus.NEW
        )

        # Select folders and their parents:
        folder_candidates = {
            parent for folder in changed_folders for parent in parents(folder)
        }

        # Generate hypothetical flow files in this location:
        flow_candidates = (f"{folder}/flow.py" for folder in folder_candidates)

        # From the hypothetical flow, return the ones that do exist:
        return [flow for flow in flow_candidates if os.path.exists(flow)]

    # Challenge for you: decipher this!
    find_pip_packages = re.compile(
        '(?:"EXTRA_PIP_PACKAGES"|'
        "'EXTRA_PIP_PACKAGES'"
        '|"""EXTRA_PIP_PACKAGES"""|'
        "'''EXTRA_PIP_PACKAGES'''"
        ')\s*:\s*(""".*?"""|".*?"|'
        "'.*?'|"
        "'''.*?'''"
        ")",
        re.MULTILINE | re.DOTALL,
    )

    def install_pip_packages(filename: str = "flow.py") -> None:
        with open(filename) as flow_file:
            flow = flow_file.read()

        try:
            packages_quoted = find_pip_packages.search(flow).group(1)
            # !!! DANGER !!!
            packages = eval(packages_quoted)
        except Exception as e:
            prefect.context.logger.warn(f"Failed to get pip packages: {e}")
            return

        package_list = packages.split()

        if len(packages):
            run_command(["python3.7", "-m", "pip", "install", *package_list])

    @task(task_run_name="deploying {flowpath}", state_handlers=[notify])
    def run_flow(flowpath: str) -> None:
        cwd = os.getcwd()
        logger = prefect.context.logger

        try:
            os.chdir(flowpath[: -len("/flow.py")])

            # Last chance!
            if os.path.exists(".nodeploy"):
                return
            install_pip_packages()
            run_command(["python3.7", "flow.py"])
        finally:
            os.chdir(cwd)

    @task
    def deploy_hash_changed(repo_name: str) -> bool:
        with open(f"deploy.py", "rb") as deploy_flow_file:
            deploy_flow_hash = sha256(deploy_flow_file.read()).hexdigest()

        with psycopg2.connect(get_dsn()) as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                select
                    deploy_flow_hash
                from
                    meta.prefect_deploys
                where
                    repository = %s
                order by
                    deployed_at desc
                limit 1
                """,
                [repo_name],
            )
            rows = cursor.fetchall() or [(None,)]

            return rows[0][0] != deploy_flow_hash

    @task
    def self_deploy() -> None:
        prefect.context.logger.info("deploy hash changed. Self-redeploying")
        logger = prefect.context.logger
        install_pip_packages("deploy.py")
        run_command(["python3.7", "deploy.py"])

    @task(skip_on_upstream_skip=False)
    def mark_deployed(repo_name: str) -> None:
        commit_hash = run_command(["git", "rev-parse", "HEAD"]).strip()

        with open(f"deploy.py", "rb") as deploy_flow_file:
            deploy_flow_hash = sha256(deploy_flow_file.read()).hexdigest()

        with psycopg2.connect(get_dsn()) as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                insert into
                    meta.prefect_deploys (repository, commit_hash, deploy_flow_hash)
                select
                    %s,
                    %s,
                    %s
                """,
                [repo_name, commit_hash, deploy_flow_hash],
            )

    def deploy_repository(
        repo_name: str,
        repo_secret: str,
        force_deploy_all_flows,
        upstream_tasks: Optional[List[Task]] = None,
    ) -> Task:
        """Creates the deploy flow. Only call this function inside a flow definition context."""
        # Get location of the repository
        origin_secret = download_secret(
            repo_secret, upstream_tasks=upstream_tasks or []
        )
        # Clone repository
        current_hash = clone_repository(repo_name, origin_secret)
        # Get the last time you were able to deploy
        last_commit_hash = get_last_successful_deploy(repo_name, current_hash)
        # Compare files hashes
        hash_comparison = calculate_hashes(
            last_commit_hash, upstream_tasks=[current_hash]
        )
        # From the hash comparison, get the flows that actually changed
        changed_flows = find_changed_flows(hash_comparison, force_deploy_all_flows)

        # Run flows that changed
        deployed_flows = run_flow.map(changed_flows)

        with case(deploy_hash_changed(repo_name), True):
            self_deployed = self_deploy()

        # Mark this as a successful deploy
        deployed = mark_deployed(
            repo_name, upstream_tasks=[deployed_flows, self_deployed]
        )

        return deployed
