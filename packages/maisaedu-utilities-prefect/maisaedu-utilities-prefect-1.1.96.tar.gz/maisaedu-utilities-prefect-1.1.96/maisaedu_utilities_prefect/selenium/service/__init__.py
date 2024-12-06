from pydantic import BaseModel
from typing import Optional, Any

from selenium import webdriver 

from fake_useragent import UserAgent

from maisaedu_utilities_prefect.constants.selenium import (
    SELENIUM_HUB_URL
)

class ScraperService(BaseModel):
    options: Any
    driver: Any
    
    def __init__(self, options: Optional[webdriver.ChromeOptions] = None, url = SELENIUM_HUB_URL):
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument("profile-directory=MaisAEduPartialSales") 
            options.add_argument("user-data-dir=/home/seluser/.cache/selenium/chrome")
            options.add_argument("start-maximized")

        driver = webdriver.Remote(
            command_executor=url,
            options=options
        )

        super().__init__(options=options, driver=driver)

    def quit(self):
        self.driver.quit()
