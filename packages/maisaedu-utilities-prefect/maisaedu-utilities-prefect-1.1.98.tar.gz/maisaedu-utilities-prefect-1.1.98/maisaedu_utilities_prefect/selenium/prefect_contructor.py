import subprocess

from prefect import task, get_run_logger

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from maisaedu_utilities_prefect.constants.env import (
    LOCAL,
    PROD,
)

@task
def build_environment(env = PROD):
    if env == LOCAL:
        get_run_logger().info("You are running locally, you need prepare your environment manually. Install chrome and chromedriver")
    elif(env == PROD):
        get_run_logger().info("Preparing environment for selenium")
        result = subprocess.run(["apt", "update", "-y"], capture_output=True, text=True)
        result = subprocess.run(["apt", "install", "wget", "-y"], capture_output=True, text=True)
        result = subprocess.run(["wget", "-nc", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], capture_output=True, text=True)
        result = subprocess.run(["apt", "install", "-f", "./google-chrome-stable_current_amd64.deb", "-y"], capture_output=True, text=True)
        get_run_logger().info("Environment prepared")

@task
def build_driver(env = PROD):
    options = Options()
    options.page_load_strategy = "normal"
    if env == PROD:
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver