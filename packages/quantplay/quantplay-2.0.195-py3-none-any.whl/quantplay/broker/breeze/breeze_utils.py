import binascii
import time
import traceback

import pyotp
from retrying import retry  # type: ignore
from selenium.common.exceptions import WebDriverException

from quantplay.exception.exceptions import (
    InvalidArgumentException,
    RetryableException,
    TokenException,
    WrongLibrarySetup,
    retry_exception,
)
from quantplay.utils.selenium_utils import Selenium


class BreezeUtils:
    user_id_xpath = '//*[@id="txtuid"]'
    password_xpath = '//*[@id="txtPass"]'
    i_agree_xpath = '//*[@id="chkssTnc"]'

    login_xpath = '//*[@id="btnSubmit"]'
    totp_xpath = '//*[@id="pnlOTP"]/div[2]/div[2]/div[3]/div/div[{}]/input'
    submit_xpath = '//*[@id="Button1"]'

    @staticmethod
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def get_session_code(api_key: str, user_id: str, password: str, totp: str):
        try:
            driver = Selenium().get_browser()

            icici_direct_url = (
                f"https://api.icicidirect.com/apiuser/login?api_key={api_key}"
            )

            driver.get(icici_direct_url)
            time.sleep(2)

            user_id_element = driver.find_element("xpath", BreezeUtils.user_id_xpath)
            password_element = driver.find_element("xpath", BreezeUtils.password_xpath)
            i_agree_element = driver.find_element("xpath", BreezeUtils.i_agree_xpath)
            login_element = driver.find_element("xpath", BreezeUtils.login_xpath)

            user_id_element.send_keys(user_id)
            password_element.send_keys(password)
            i_agree_element.click()
            time.sleep(0.5)
            login_element.click()
            time.sleep(2)
            totp_code = pyotp.TOTP(str(totp)).now()
            for i in range(1, 7):
                entry = totp_code[i - 1]
                totp_pin = driver.find_element(
                    "xpath", BreezeUtils.totp_xpath.replace("{}", str(i))
                )
                totp_pin.send_keys(entry)
            submit_element = driver.find_element("xpath", BreezeUtils.submit_xpath)
            submit_element.click()

            time.sleep(2)

            url = driver.current_url
            print("got icici redirect url {}".format(url))
            session_token = url.split("apisession=")[1].split("&")[0]

            driver.close()

            return session_token

        except binascii.Error:
            raise InvalidArgumentException("Invalid TOTP key provided")

        except (InvalidArgumentException, TokenException) as e:
            raise e

        except WebDriverException:
            raise WrongLibrarySetup(
                "ICICI login failed, please contact support team or generate token from Dashboard page"
            )

        except Exception as e:
            traceback.print_exc()
            raise RetryableException(str(e))
