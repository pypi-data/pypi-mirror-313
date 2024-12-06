import logging, traceback, random, requests
import time
from io import BytesIO
from PIL import Image
from curl_cffi import requests as cffi_requests
import tls_client
import warnings
warnings.filterwarnings('ignore')

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class fctrequest:
    def __init__(self, use_session=False, use_cffi=False, use_tls=False, use_proxy=False):
        self.truncate_nbre = 40
        self.use_proxy = use_proxy
        self.use_session = use_session
        self.use_cffi = use_cffi
        self.use_tls = use_tls
        if self.use_cffi:
            if self.use_session:
                self.session = cffi_requests.Session()
            else:
                self.session = cffi_requests

        elif self.use_tls:
            client_identifier = ['safari_ios_15_5', 'safari_ios_15_6', 'safari_ios_16_0', 'okhttp4_android_7',
                                 'okhttp4_android_8', 'okhttp4_android_9', 'okhttp4_android_10', 'okhttp4_android_11',
                                 'okhttp4_android_12', 'okhttp4_android_13']
            self.session = tls_client.Session(client_identifier=random.choice(client_identifier), random_tls_extension_order=True)

        else:
            if self.use_session:
                self.session = requests.session()
            else:
                self.session = requests


    def generate_proxy(self, proxies=None):
        dict_proxy = {}
        if proxies and self.use_proxy:
            try:
                random_proxy = proxies[random.randint(0, len(proxies) - 1)]
                if self.use_cffi:
                    random_proxy = random_proxy.replace('http://', '').strip()
                    dict_proxy = {"http": random_proxy, "https": random_proxy}

                else:
                    random_proxy = f'http://{random_proxy.strip()}'
                    dict_proxy = {"http": random_proxy, "https": random_proxy}
            except:
                logging.exception(traceback.format_exc())
        return dict_proxy


    def request(self, method='', link='', params=None, data=None, json=None, headers={}, cookies={}, proxies=[], verify=False, allow_redirects=True, timeout=30, sleep=0, tries=3, path_file='', is_image=False):
        response = None
        if method == 'GET':
            response = self.get(link, params=params, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep, tries=tries)

        elif method == 'POST':
            response = self.post(link, data=data, json=json, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep, tries=tries)

        elif method == 'PUT':
            response = self.put(link, data=data, json=json, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep, tries=tries)

        elif method == 'DGET':
            response = self.download(method=method, link=link, params=params, data=data, json=json, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep, tries=tries, path_file=path_file, is_image=is_image)

        elif method == 'DPOST':
            response = self.download(method=method, link=link, params=params, data=data, json=json, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep, tries=tries, path_file=path_file, is_image=is_image)

        else:
            logging.warning(f'Method {method} Not Supported in request function')

        return response


    def get(self, link, params=None, headers={}, cookies={}, proxies=[], verify=False, allow_redirects=True, timeout=30, sleep=0, tries=3):
        response = None
        try:
            i = 0
            status_code = 0
            while status_code not in range(200, 300) and i < tries:
                i += 1
                try:
                    response = self.get_simple(link, params=params, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep)
                    status_code = response.status_code
                except:
                    logging.exception(traceback.format_exc())

                logging.info(f'Request Get: {i}/{tries} | status_code: {status_code} | {link}')

        except:
            logging.exception(traceback.format_exc())

        return response


    def get_simple(self, link, params=None, headers={}, cookies={}, proxies=[], verify=False, allow_redirects=True, timeout=30, sleep=0):
        response = None
        try:
            proxies = self.generate_proxy(proxies)
            if self.use_cffi:
                response = self.session.request(method='GET', url=link, params=params, impersonate="chrome", proxies=proxies, verify=verify, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout)

            else:
                response = self.session.get(link, params=params, proxies=proxies, verify=verify, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout)

            self.log_request(method='GET', link=link, sleep=sleep)

        except:
            logging.exception(traceback.format_exc())

        return response


    def post(self, link, data=None, json=None, headers={}, cookies={}, proxies=[], verify=False, allow_redirects=True, timeout=30, sleep=0, tries=3):
        response = None
        try:
            i = 0
            status_code = 0
            while status_code not in range(200, 300) and i < tries:
                i += 1
                try:
                    response = self.post_simple(link, data=data, json=json, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep)
                    status_code = response.status_code
                except:
                    logging.exception(traceback.format_exc())

                logging.info(f'Request Post: {i}/{tries} | status_code: {status_code} | {link}')

        except:
            logging.exception(traceback.format_exc())

        return response


    def post_simple(self, link, data=None, json=None, headers={}, cookies={}, proxies=[], verify=False, allow_redirects=True, timeout=30, sleep=0):
        response = None
        try:
            proxies = self.generate_proxy(proxies)
            if self.use_cffi:
                response = self.session.request(method='POST', url=link, data=data, json=json, impersonate="chrome", proxies=proxies, verify=verify, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout)

            else:
                response = self.session.post(link, data=data, json=json, proxies=proxies, verify=verify, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout)

            self.log_request(method='POST', link=link, data=data, json=json, sleep=sleep)

        except:
            logging.exception(traceback.format_exc())

        return response


    def put(self, link, data=None, json=None, headers={}, cookies={}, proxies=[], verify=False, allow_redirects=True, timeout=30, sleep=0, tries=3):
        response = None
        try:
            i = 0
            status_code = 0
            while status_code not in range(200, 300) and i < tries:
                i += 1
                try:
                    response = self.put_simple(link, data=data, json=json, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep)
                    status_code = response.status_code
                except:
                    logging.exception(traceback.format_exc())

                logging.info(f'Request Put: {i}/{tries} | status_code: {status_code} | {link}')

        except:
            logging.exception(traceback.format_exc())

        return response


    def put_simple(self, link, data=None, json=None, headers={}, cookies={}, proxies=[], verify=False, allow_redirects=True, timeout=30, sleep=0):
        response = None
        try:
            proxies = self.generate_proxy(proxies)
            if self.use_cffi:
                response = self.session.request(method='PUT', url=link, data=data, json=json, impersonate="chrome", proxies=proxies, verify=verify, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout)

            else:
                response = self.session.put(link, data=data, json=json, proxies=proxies, verify=verify, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=timeout)

            self.log_request(method='PUT', link=link, data=data, json=json, sleep=sleep)

        except:
            logging.exception(traceback.format_exc())

        return response

    def download(self, method='', link='', params=None, data=None, json=None, headers={}, cookies={}, proxies=[], verify=False, allow_redirects=True, timeout=30, sleep=0, tries=3, path_file='', is_image=False):
        file_size = 0
        try:
            i = 0
            status_code = 0
            while status_code not in range(200, 300) and i < tries:
                i += 1
                try:
                    if method == 'DGET':
                        response = self.get_simple(link, params=params, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep)

                    elif method == 'DPOST':
                        response = self.post_simple(link, data=data, json=json, headers=headers, cookies=cookies, proxies=proxies, verify=verify, allow_redirects=allow_redirects, timeout=timeout, sleep=sleep)

                    else:
                        logging.warning(f'Method {method} Not Supported in download function')
                        return file_size

                    if response:
                        body = response.content

                        file_size = len(body)
                        status_code = response.status_code
                        if status_code:
                            if is_image:
                                im = Image.open(BytesIO(body))
                                im.save(path_file)  # Save the image as a JPEG file
                            else:
                                with open(path_file, 'wb') as file:
                                    file.write(body)
                except:
                    logging.exception(traceback.format_exc())

                logging.info(f'Request Download: {i}/{tries} | status_code: {status_code} | file_size = {file_size} | {link}')

        except:
            logging.exception(traceback.format_exc())

        return file_size

    def log_request(self, method=None, link=None, data=None, json=None, sleep=0):
        if sleep:
            library = ''
            if self.use_cffi:
                library = 'Cffi '

            elif self.use_tls:
                library = 'tls '

            link_display = f"| link: {link[:self.truncate_nbre]}..." if link else ""
            data_display = f"| data: {str(data)[:self.truncate_nbre]}..." if data else ""
            json_display = f"| json: {str(json)[:self.truncate_nbre]}..." if json else ""
            if isinstance(sleep, list):
                if len(sleep) >= 2:
                    _sleep = int(random.uniform(sleep[0], sleep[1]))
                    logging.info(f'{library}Request {method} | sleep: {_sleep}s {link_display} {data_display} {json_display}')
                    time.sleep(_sleep)
            elif isinstance(sleep, int):
                logging.info(f'{library}Request {method} | sleep: {sleep}{link_display}{data_display}{json_display}')
                time.sleep(sleep)


# if __name__ == '__main__':
#     proxies = ["EDoqoyPZeB9Mmw00-country-US:dmkJoq6JAxe5uMw@res-v2.pr.plainproxies.com:8080"]
#     use_proxy = True
#     fctrequest = fctrequest(use_session=False, use_cffi=False, use_tls=True, use_proxy=use_proxy)
#
#     headers = {
#         'accept': '*',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
#     }
#
#     response = fctrequest.request(method='GET', link='https://www.searchpeoplefree.com/address/ca/trabuco-canyon/brassie-ln/36', headers=headers, proxies=proxies, tries=5)
#     print(response.text)
#     # response = fctrequest.request(method='POST', link=link, data=param, headers=headers, proxies=proxies, tries=5)
#     # image_size = fctrequest.request(method='DGET', link=image_link, path=image_path, is_image=True, proxies=proxies, tries=5)
#     # image_size = fctrequest.request(method='DPOST', link=image_link, path=image_path, is_image=True, proxies=proxies, tries=5)
