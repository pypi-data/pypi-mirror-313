import binascii
import time
import traceback

import pyotp
from retrying import retry  # type: ignore
from selenium.common.exceptions import WebDriverException

from quantplay.exception.exceptions import (
    InvalidArgumentException,
    RetryableException,
    retry_exception,
)
from quantplay.utils.selenium_utils import Selenium


class KiteUtils:
    zerodha_username = "zerodha_username"
    zerodha_password = "zerodha_password"
    zeordha_totp_unique_id = "zerodha_totp_unique_id"

    user_id_xpath = '//*[@id="container"]/div/div/div[2]/form/div[1]/input'
    password_xpath = '//*[@id="container"]/div/div/div[2]/form/div[2]/input'
    login_xpath = '//*[@id="container"]/div/div/div[2]/form/div[4]/button'
    kite_pin_xpath = (
        "/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/input"
    )
    authorize_xpath = "/html/body/div[1]/div/div[1]/div/div/form/div/button"

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
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def get_request_token(
        api_key: str | None = None,
        user_id: str | None = None,
        password: str | None = None,
        totp: str | None = None,
    ):
        if totp is None:
            raise InvalidArgumentException("TOTP Key is Missing")

        if api_key is None:
            raise InvalidArgumentException("TOTP Key is Missing")

        if user_id is None:
            raise InvalidArgumentException("User ID Key is Missing")

        if password is None:
            raise InvalidArgumentException("Password Key is Missing")

        try:
            pyotp.TOTP(str(totp)).now()
            driver = Selenium().get_browser()

            kite_url = "https://kite.trade/connect/login?api_key={}&v=3".format(api_key)
            print("Kite Url {}".format(kite_url))

            driver.get(kite_url)
            time.sleep(2)
            page_source = driver.page_source
            KiteUtils.check_error(page_source)

            user_id_element = driver.find_element("xpath", KiteUtils.user_id_xpath)
            password_element = driver.find_element("xpath", KiteUtils.password_xpath)

            user_id_element.send_keys(user_id)
            password_element.send_keys(password)

            login_attempt = driver.find_element("xpath", KiteUtils.login_xpath)
            login_attempt.submit()
            time.sleep(2)

            page_source = driver.page_source
            KiteUtils.check_error(page_source)

            kite_pin = driver.find_element("xpath", KiteUtils.kite_pin_xpath)
            kite_pin.send_keys(pyotp.TOTP(str(totp)).now())
            time.sleep(1)

            page_source = driver.page_source
            KiteUtils.check_error(page_source)
            if "Authorize" in page_source:
                print(f"Authorizing {api_key}")
                authorize = driver.find_element("xpath", KiteUtils.authorize_xpath)
                authorize.submit()

            url = driver.current_url
            print("got kite url {}".format(url))
            request_token = url.split("token=")[1].split("&")[0]

            driver.close()

            return request_token
        except binascii.Error:
            raise InvalidArgumentException("Invalid TOTP key provided")
        except InvalidArgumentException:
            raise
        except WebDriverException:
            raise RetryableException("Selenium setup need to be fixed")
        except Exception as e:
            traceback.print_exc()
            raise RetryableException(str(e))
