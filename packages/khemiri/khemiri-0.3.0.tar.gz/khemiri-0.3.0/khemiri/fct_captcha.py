from amazoncaptcha import AmazonCaptcha
from scrapy.selector import Selector
from twocaptcha import TwoCaptcha
import traceback, logging, base64, time
from pathlib import Path
from unicaps import CaptchaSolver, CaptchaSolvingService
from khemiri import fct_core

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

def solve_azcaptcha_image_base64(**kwargs):
    base64_data = kwargs.get('base64_data')
    key_azcaptcha = kwargs.get('key_azcaptcha')

    solution_captcha = ''
    try:
        # Decode the base64 data to bytes
        image_bytes = base64.b64decode(base64_data.split('base64,')[-1])

        with CaptchaSolver(CaptchaSolvingService.AZCAPTCHA, key_azcaptcha) as solver:
            solved = solver.solve_image_captcha(
                image_bytes,  # Provide image_bytes directly
                is_phrase=False,
                is_case_sensitive=True
            )
            solution_captcha = solved.solution.text.upper()
    except:
        logging.error(traceback.format_exc())

    return solution_captcha

def solve_azcaptcha_image(**kwargs):
    path = kwargs.get('path')
    key_azcaptcha = kwargs.get('key_azcaptcha')

    solution_captcha = ''
    try:
        with CaptchaSolver(CaptchaSolvingService.AZCAPTCHA, key_azcaptcha) as solver:
            solved = solver.solve_image_captcha(
                Path(path),
                is_phrase=False,
                is_case_sensitive=True
            )
            solution_captcha = solved.solution.text.upper()
    except:
        logging.error(traceback.format_exc())

    return solution_captcha

def solve_azcaptcha_recaptcha(**kwargs):
    url = kwargs.get('url')
    sitekey = kwargs.get('sitekey')
    key_azcaptcha = kwargs.get('key_azcaptcha')

    solution_captcha = ''
    c=0
    while not solution_captcha and c<5:
        c += 1
        logging.info(f'solve_azcaptcha_recaptcha: {c}/5')
        try:
            with CaptchaSolver(CaptchaSolvingService.AZCAPTCHA, key_azcaptcha) as solver:
                solved = solver.solve_recaptcha_v2(
                    site_key=sitekey,
                    page_url=url,
                    # data_s='<data-s value>',  # optional
                    # api_domain='<"google.com" or "recaptcha.net">'  # optional
                )
                solution_captcha = solved.solution.token
        except:
            logging.error(traceback.format_exc())

    return solution_captcha

def solve_2captcha_image_base64(**kwargs):
    base64_data = kwargs.get('base64_data')
    key2captcha = kwargs.get('key2captcha')

    solution_captcha = ''
    try:
        # Decode the base64 data to bytes
        image_bytes = base64.b64decode(base64_data.split('base64,')[-1])

        solver = TwoCaptcha(key2captcha)
        result1 = solver.normal(image_bytes)  # Provide image_bytes directly

        try:
            solution_captcha = str(result1["code"])
        except:
            logging.error(traceback.format_exc())
    except:
        logging.error(traceback.format_exc())

    return solution_captcha

def solve_2captcha_image(**kwargs):
    path = kwargs.get('path')
    key2captcha = kwargs.get('key2captcha')

    solution_captcha = ''
    try:
        solver = TwoCaptcha(key2captcha)
        result1 = solver.normal(path)
        try:
            solution_captcha = str(result1["code"])
        except:
            logging.error(traceback.format_exc())
    except:
        logging.error(traceback.format_exc())

    return solution_captcha


def solve_2captcha_recaptcha(**kwargs):
    url = kwargs.get('url')
    sitekey = kwargs.get('sitekey')
    key2captcha = kwargs.get('key2captcha')

    recaptcha_response = ''
    try:
        solver = TwoCaptcha(key2captcha)
        result1 = solver.recaptcha(sitekey=sitekey, url=url)
        try:
            recaptcha_response = str(result1["code"])
        except:
            logging.error(traceback.format_exc())
    except:
        logging.error(traceback.format_exc())

    return recaptcha_response

# recaptcha_response = solve_2captcha.solve_hcaptcha(url=index_url, key_hcaptcha='ec6e1672b32462483d95d1319c15f6dd',
#                                                    sitekey='33f96e6a-38cd-421b-bb68-7806e1764460')


def solve_amazon_captcha(driver):
    try:
        str1 = driver.inner_html('html')
        html1 = Selector(text=str1)

        src_image = fct_core.parse_field('//form[@action="/errors/validateCaptcha"]//img/@src', html1)
        if src_image:
            h=0
            while src_image and h<4:
                logging.info(f'src_image: {src_image}')

                captcha = AmazonCaptcha.fromlink(src_image)
                solution = captcha.solve()
                logging.info(f'solution: {solution}')

                try:
                    driver.type('xpath=//form[@action="/errors/validateCaptcha"]//input[@id="captchacharacters"]', solution)
                    time.sleep(3)
                    driver.click('xpath=//form[@action="/errors/validateCaptcha"]//button[@type="submit"]')
                    time.sleep(10)
                except:
                    ''

                str1 = driver.inner_html('html')
                html1 = Selector(text=str1)
                src_image = fct_core.parse_field('//form[@action="/errors/validateCaptcha"]//img/@src', html1)

                h=h+1
    except:
        logging.error(traceback.format_exc())

    return driver

