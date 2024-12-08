import binascii
import time
import traceback

import pyotp
from retrying import retry  # type: ignore
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import Chrome

from quantplay.exception.exceptions import (
    BrokerException,
    InvalidArgumentException,
    RetryableException,
)
from quantplay.utils.selenium_utils import Selenium


class AliceblueLogin:
    @staticmethod
    def check_error(page_source: str):
        for error_message in [
            "User profile not found",
            "Invalid username or password",
            "Invalid TOTP",
        ]:
            if error_message in page_source:
                raise InvalidArgumentException(error_message)

        if "Invalid" in page_source:
            start_index = page_source.find("Invalid")
            print(page_source[start_index : min(start_index + 20, len(page_source))])

        if "Invalid" in page_source and "api_key":
            raise InvalidArgumentException("Invalid API Key")

    @staticmethod
    def click_on_login(driver: Chrome):
        login = '//*[@id="login_card_inital"]/div[6]/button'
        login = driver.find_element("xpath", login)
        login.click()

    @staticmethod
    def enter_user_id(driver: Chrome, user_id: str):
        time.sleep(0.5)
        user_id_xpath = '//*[@id="userid_inp"]'
        driver.find_element("xpath", user_id_xpath).send_keys(user_id)  # type: ignore

        time.sleep(0.5)
        next_xpath = '//*[@id="userId_btn_label"]'
        driver.find_element("xpath", next_xpath).click()

    @staticmethod
    def enter_password(driver: Chrome, password: str):
        time.sleep(0.5)
        password_xpath = '//*[@id="password_inp"]'
        driver.find_element("xpath", password_xpath).send_keys(password)  # type: ignore

        time.sleep(0.5)
        next_xpath = '//*[@id="password_btn"]'
        driver.find_element("xpath", next_xpath).click()

    @staticmethod
    def enter_totp(driver: Chrome, totp: str):
        time.sleep(1.5)
        totp_xpath = '//*[@id="totp_otp_inp"]'
        driver.find_element("xpath", totp_xpath).send_keys(totp)  # type: ignore

        # time.sleep(0.5)
        # next_xpath = '//*[@id="totp_btn"]'
        # driver.find_element("xpath", next_xpath).click()

    @staticmethod
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def login(user_id: str, password: str, totp: str):
        try:
            driver = Selenium().get_browser(headless=True)

            driver.get("https://ant.aliceblueonline.com/")
            AliceblueLogin.click_on_login(driver)
            AliceblueLogin.enter_user_id(driver, user_id)
            AliceblueLogin.enter_password(driver, password)
            AliceblueLogin.enter_totp(driver, pyotp.TOTP(str(totp)).now())

        except binascii.Error:
            raise InvalidArgumentException("Invalid TOTP key provided")

        except InvalidArgumentException:
            raise

        except NoSuchElementException:
            raise BrokerException(
                "Login to Aliceblue failed. Please log in manually to generate a new token"
            )

        except WebDriverException:
            traceback.print_exc()
            raise RetryableException("Selenium setup need to be fixed")

        except Exception as e:
            traceback.print_exc()
            raise RetryableException(str(e))
