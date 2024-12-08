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
from quantplay.utils.constant import Constants
from quantplay.utils.selenium_utils import Selenium


class FlatTradeUtils:
    user_id_xpath = '//*[@id="input-19"]'
    password_xpath = '//*[@id="pwd"]'
    totp_xpath = '//*[@id="pan"]'

    login_xpath = '//*[@id="sbmt"]'
    error_xpath = '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/form/div[5]/div'

    @staticmethod
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def get_request_code(api_key: str, user_id: str, password: str, totp: str):
        try:
            pyotp.TOTP(str(totp)).now()
            driver = Selenium().get_browser()

            flattrade_url = f"https://auth.flattrade.in/?app_key={api_key}"

            driver.get(flattrade_url)
            time.sleep(2)

            user_id_element = driver.find_element("xpath", FlatTradeUtils.user_id_xpath)
            password_element = driver.find_element("xpath", FlatTradeUtils.password_xpath)

            user_id_element.send_keys(user_id)
            password_element.send_keys(password)

            totp_pin = driver.find_element("xpath", FlatTradeUtils.totp_xpath)
            totp_pin.send_keys(pyotp.TOTP(str(totp)).now())

            time.sleep(1)

            login_attempt = driver.find_element("xpath", FlatTradeUtils.login_xpath)
            login_attempt.click()

            time.sleep(2)

            url = driver.current_url

            if url.split("/")[2] == flattrade_url.split("/")[2]:
                error_message = ""

                try:
                    error_attempt = driver.find_element(
                        "xpath", FlatTradeUtils.error_xpath
                    )
                    error_message = error_attempt.text

                    if error_message.lower() in [
                        "invalid input : wrong password",
                        "invalid api key",
                        "resetpassword",
                        "user blocked due to multiple wrong attempts",
                    ]:
                        raise InvalidArgumentException(
                            f"Flattrade Login Failed: {error_message}"
                        )

                except Exception as e:
                    Constants.logger.info(f"Flattrade Error: {e}")
                    traceback.print_exc()
                    raise TokenException(str(e))

                finally:
                    Constants.logger.info(f"Flattrade Error : {error_message}")
                    raise TokenException(f"Flattrade Error : {error_message}")

            try:
                request_token = url.split("code=")[1].split("&")[0]
            except Exception as e:
                Constants.logger.info(f"Flattrade Error for {url}")
                traceback.print_exc()
                raise TokenException(str(e))

            driver.close()

            return request_token

        except binascii.Error:
            raise InvalidArgumentException("Invalid TOTP key provided")

        except (InvalidArgumentException, TokenException) as e:
            raise e

        except WebDriverException:
            raise WrongLibrarySetup(
                "Flattrade login failed, please contact support team or generate token from Dashboard page"
            )

        except Exception as e:
            traceback.print_exc()
            raise RetryableException(str(e))
