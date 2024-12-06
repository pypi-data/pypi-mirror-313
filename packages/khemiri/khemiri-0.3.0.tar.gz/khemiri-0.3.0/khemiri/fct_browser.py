import logging, traceback, shutil, time, random, coloredlogs, os
from os.path import dirname, abspath
from urllib.parse import quote
from khemiri import fct_core

# playwright
from undetected_playwright.sync_api import sync_playwright
# from playwright.sync_api import sync_playwright

# DrissionPage
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Actions

# seleniumBase
from seleniumbase import Driver as SeleniumBaseDriver

coloredlogs.install()
start_dt = time.time()

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class Browser:
    def __init__(
            self,
            library='P',
            use_proxy=False,
            proxies=[],
            cookies={},
            block_imgs=False,
            cloudflare=False,
            cloudflare_title='just a moment',
            recaptcha=False,
            press_hold=False,
            extension_path='',
            window_position='960,0',  # Set the browser's starting window position: "X,Y"
            window_size='960,1020',  # Set the browser's starting window size: "Width,Height"
            port=False,
            maximized=False,
    ):

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.cloudflare = cloudflare
        self.cloudflare_title = cloudflare_title
        self.recaptcha = recaptcha
        self.press_hold = press_hold
        self.library = library
        self.driver = None
        self.context = None
        self.browser = None
        self.playwright = None
        self.use_proxy = use_proxy
        self.proxies = proxies
        self.cookies = cookies
        self.block_imgs = block_imgs

        if port:
            self.port = port
        else:
            self.port = random.randint(9600, 19600)
            # self.port = random.randint(1, 20)

        self.window_position = window_position
        self.window_size = window_size
        self.maximized = maximized

        self.path_browser_data = os.path.join(dirname(abspath(__file__)), 'browser_data')
        self.path_browser_proxies = os.path.join(self.path_browser_data, 'proxies', f'extension_{self.port}')

        self.extension_path = None
        if extension_path:
            self.extension_path = os.path.join(self.current_dir, extension_path)

    def open(self):
        try:
            arguments = [
                # "--start-maximized",
                # "--no-first-run",
                # "--force-color-profile=srgb",
                # "--metrics-recording-only",
                # "--password-store=basic",
                # "--use-mock-keychain",
                # "--export-tagged-pdf",
                # "--no-default-browser-check",
                # "--disable-background-mode",
                # "--enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
                # "--disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
                # "--deny-permission-prompts",
                # "--disable-gpu",
                #
                # "--disable-popup-blocking",
                # "--disable-notifications",
                # "--disable-infobars",
                # "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            ]

            if self.library == 'P':
                arguments = []
                self.playwright = sync_playwright().start()

                if self.extension_path:
                    arguments.append(f"--disable-extensions-except={self.extension_path}")
                    arguments.append(f"--load-extension={self.extension_path}")
                    if self.use_proxy:
                        self.context = self.playwright.chromium.launch_persistent_context(
                            user_data_dir=self.path_browser_data,
                            headless=False,
                            proxy=self.generate_proxy_playwright(),
                            channel='chrome',
                            # viewport={"width": 375, "height": 667},
                            args=arguments
                        )
                    else:
                        self.context = self.playwright.chromium.launch_persistent_context(
                            user_data_dir=self.path_browser_data,
                            headless=False,
                            channel='chrome',
                            # viewport={"width": 375, "height": 667},
                            args=arguments
                        )

                    self.driver = self.context.pages[0]

                else:
                    if self.use_proxy:
                        self.browser = self.playwright.chromium.launch(
                            headless=False,
                            channel='chrome',
                            args=arguments,
                            proxy=self.generate_proxy_playwright(),
                        )
                    else:
                        self.browser = self.playwright.chromium.launch(
                            headless=False,
                            channel='chrome',
                            args=arguments,
                        )

                    self.context = self.browser.new_context(ignore_https_errors=True, no_viewport=self.maximized)
                    self.driver = self.context.new_page()
                    self.driver.set_default_timeout(0)

                if self.cookies:
                    cookie_list = [
                        {key: cookie[key] for key in ("name", "value", "domain", "path", "secure", "httpOnly")} for
                        cookie in self.cookies]
                    self.context.add_cookies(cookie_list)

                if self.block_imgs:
                    # self.driver.route(re.compile(r"\.(jpg|png|svg)$"), lambda route: route.abort())
                    # self.driver.route(re.compile(r"google"), lambda route: route.abort())
                    # excluded_resource_types = ["stylesheet", "script", "image", "font"]
                    excluded_resource_types = ["stylesheet", "image", "font"]

                    def block_aggressively(route):
                        if (route.request.resource_type in excluded_resource_types):
                            route.abort()
                        else:
                            route.continue_()

                    self.driver.route("**/*", block_aggressively)


            elif self.library == 'D':
                arguments = []
                if self.maximized: arguments.append("--start-maximized")

                options_chrome = ChromiumOptions().set_tmp_path(self.path_browser_data).auto_port(True)
                if self.block_imgs:
                    options_chrome.no_imgs(True).mute(True)

                if self.use_proxy:
                    self.generate_extension_proxies()
                    if self.use_proxy:
                        options_chrome.add_extension(f'{self.path_browser_proxies}')

                for argument in arguments:
                    options_chrome.set_argument('-' + argument.lstrip('--'))

                self.driver = ChromiumPage(addr_or_opts=options_chrome)
                # self.driver.set.window.size(1200, 800)
                # self.driver.set.window.location(400, 100)

                if self.cookies:
                    cookie_list = [
                        {key: cookie[key] for key in ("name", "value", "domain", "path", "secure", "httpOnly")} for
                        cookie in self.cookies]
                    self.driver.set.cookies(cookie_list)


            elif self.library == 'SB':
                if self.use_proxy:
                    # self.generate_extension_proxies()
                    self.driver = SeleniumBaseDriver(
                        uc=True,  # Use undetected-chromedriver to evade bot-detection.
                        # extension_dir=self.path_browser_proxies,
                        proxy=random.choice(self.proxies),
                        # Use proxy. Format: "SERVER:PORT" or "USER:PASS@SERVER:PORT".
                        locale_code='en',  # Set the Language Locale Code for the web browser.
                        incognito=True,  # Enable Chromium's Incognito mode.
                        # window_position=self.window_position,  # Set the browser's starting window position: "X,Y"
                        # window_size=self.window_size,  # Set the browser's starting window size: "Width,Height"
                    )

                else:
                    self.driver = SeleniumBaseDriver(
                        uc=True,  # Use undetected-chromedriver to evade bot-detection.
                        locale_code='en',  # Set the Language Locale Code for the web browser.
                        incognito=True,  # Enable Chromium's Incognito mode.
                        # window_position=self.window_position,  # Set the browser's starting window position: "X,Y"
                        # window_size=self.window_size,  # Set the browser's starting window size: "Width,Height"
                    )

                if self.maximized: self.driver.maximize_window()

                # options_chrome = ChromiumOptions()
                # options_chrome.set_local_port(self.port)
                # if self.block_imgs:
                #     options_chrome.no_imgs(True).mute(True)
                #
                # if self.use_proxy:
                #     self.generate_extension_proxies()
                #     if self.use_proxy:
                #         options_chrome.add_extension(f'{self.path_browser_proxies}')
                #
                # for argument in arguments:
                #     options_chrome.set_argument('-'+argument.lstrip('--'))
                #
                # self.driver = ChromiumPage(addr_or_opts=options_chrome)
                # self.driver.set.window.size(1200, 800)
                # self.driver.set.window.location(400, 100)
                #
                # if self.cookies:
                #     cookie_list = [{key: cookie[key] for key in ("name", "value", "domain", "path", "secure", "httpOnly")} for cookie in self.cookies]
                #     self.driver.set.cookies(cookie_list)

            else:
                logging.warning(f'The library "{self.library}" is not supported in the "open()" function.')

        except:
            logging.error(traceback.format_exc())

    def close(self):
        try:
            if self.library == 'P':
                self.context.close()
                if self.browser:
                    self.browser.close()
                self.playwright.stop()

            elif self.library == 'D':
                self.driver.close()
                self.driver.quit()

            elif self.library == 'SB':
                self.driver.quit()

            else:
                logging.warning(f'The library "{self.library}" is not supported in the "close()" function.')

        except:
            logging.error(traceback.format_exc())

    def request(self, method='GET', method_request='GET', link='', data=[], headers={}, timeout=5, file_path='',
                response_length=20, check_if_title_not_exist='', check_if_keywords_not_exist=[]):
        str1 = ''
        if link:
            if method == 'GET':
                str1 = self.send_get(link, timeout=timeout)

            elif method == 'LGET':
                str1 = self.local_or_request(method_request=method_request, link=link, data=data, headers=headers,
                                             timeout=timeout, file_path=file_path, response_length=response_length,
                                             check_if_title_not_exist=check_if_title_not_exist,
                                             check_if_keywords_not_exist=check_if_keywords_not_exist)

            elif method == 'XGET':
                str1 = self.xhr_get(link, headers=headers, timeout=timeout)


            elif method == 'XPOST':
                str1 = self.xhr_post(link, data=data, headers=headers, timeout=timeout)

            else:
                logging.warning(f'The library "{self.library}" is not supported in the "request()" function.')

        else:
            logging.warning(f'No link provided. Please provide a valid link.')

        return str1

    def local_or_request(self, method_request='GET', link='', data=[], headers={}, timeout=5, file_path='',
                         response_length=20, check_if_title_not_exist='', check_if_keywords_not_exist=[]):
        response = ''
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    response = f.read()
            else:
                response = self.request(method=method_request, link=link, data=data, headers=headers, timeout=timeout)

                title = ""
                try:
                    title = self.driver.title.lower()
                except:
                    ''

                if response:
                    if len(response) > response_length:
                        if check_if_title_not_exist.lower() != title:
                            if not any(keyword.lower() in fct_core.preg_repace(patt='\s+', repl=' ',
                                                                              subj=response).strip().lower() for keyword
                                       in check_if_keywords_not_exist):
                                with open(file_path, 'w', encoding="utf-8") as f:
                                    f.write(str(response))
                            else:
                                logging.warning(f'{check_if_keywords_not_exist} in response in link: {link}')
                        else:
                            logging.warning(f'check_if_title_not_exist == {title} in link: {link}')
                    else:
                        logging.warning(f'len(response) < {response_length} in link: {link}')
                else:
                    logging.warning(f'no response found in link: {link}')

        except:
            logging.error(traceback.format_exc())

        return response

    def send_get(self, link, timeout=5):
        response = ''
        try:
            if self.library == 'P':
                self.driver.goto(link, wait_until="domcontentloaded")
                self.driver.wait_for_load_state("domcontentloaded")
                self.driver.wait_for_timeout(timeout * 1000)
                time.sleep(timeout)
                response = self.content()

            elif self.library == 'D':
                self.driver.get(link)
                time.sleep(timeout)

                if self.cloudflare and self.cloudflare_title.lower() in self.get_title():
                    CloudflareBypasser_DrissionPage(self.cloudflare_title, self.driver).bypass()

                if self.recaptcha:
                    RecaptchaBypasser_DrissionPage(self.driver).bypass()

                response = self.content()

            elif self.library == 'SB':
                # self.driver.uc_open_with_reconnect(link, timeout)
                self.driver.get(link)
                time.sleep(timeout)

                if self.cloudflare:
                    self.driver.uc_gui_click_captcha()

                if self.recaptcha:
                    self.driver.uc_gui_handle_captcha(frame="iframe")  # (Auto-detects the CAPTCHA)
                    self.driver.uc_gui_click_captcha()

                response = self.content()

            else:
                logging.warning(f'The library "{self.library}" is not supported in the "send_get()" function.')

        except:
            logging.error(traceback.format_exc())

        return response

    def get_title(self):
        title = ""
        try:
            title = self.driver.title.lower()
        except:
            ''
        return title

    def xhr_get(self, link, headers={}, timeout=5):
        response = ''
        try:
            headers_js = self.generate_headers(headers)
            command_js = f'''
                            return new Promise((resolve, reject) => {{
                                let xhr = new XMLHttpRequest();
                                xhr.withCredentials = true;
                                xhr.open("GET", "{link}");

                                {headers_js}

                                xhr.timeout = {timeout * 1000}; //with ms
                                xhr.onload = function() {{
                                    if (xhr.status >= 200 && xhr.status < 300) {{
                                        resolve(xhr.responseText);
                                    }}
                                }};
                                xhr.send(null);
                            }})
                            .then(response => {{
                                return response;
                            }});
                    '''

            response = self.execute_js(command_js)

        except:
            logging.error(traceback.format_exc())

        return response

    def encode_data(self, data):
        query_string = ''

        for key, value in data.items():
            if isinstance(value, list):
                # If value is a list, encode each item with the same key
                for item in value:
                    query_string += f"{quote(key)}={quote(item)}&"
            else:
                # Otherwise, just encode the key-value pair
                query_string += f"{quote(key)}={quote(value)}&"

        # Remove the trailing '&'
        return query_string.rstrip('&')

    def xhr_post(self, link, data=[], headers={}, timeout=5):
        response = ''
        try:
            headers_js = self.generate_headers(headers)
            data_js = self.encode_data(data)

            # f'''const data = new URLSearchParams({data})'''

            command_js = f'''
                            const data = "{data_js}";
                            return new Promise((resolve, reject) => {{
                                let xhr = new XMLHttpRequest();
                                xhr.withCredentials = true;
                                xhr.open("POST", "{link}");

                                {headers_js}

                                xhr.timeout = {timeout * 1000}; //with ms
                                xhr.onload = function() {{
                                    if (xhr.status >= 200 && xhr.status < 300) {{
                                        resolve(xhr.responseText);
                                    }}
                                }};
                                xhr.send(data);
                            }});
                    '''

            command_js = f'''
            const data = "{data_js}";

            // Function to fetch data and return the Promise result
            async function fetchData() {{
                try {{
                    const result = await new Promise((resolve, reject) => {{
                        let xhr = new XMLHttpRequest();
                        xhr.withCredentials = true;
                        xhr.open("POST", "{link}");

                        {headers_js}

                        xhr.timeout = 10000; // Timeout in ms
                        xhr.onload = function () {{
                            if (xhr.status >= 200 && xhr.status < 300) {{
                                resolve(xhr.responseText);
                            }} else {{
                                reject(`Request failed with status ${{xhr.status}}`);
                            }}
                        }};

                        xhr.onerror = function () {{
                            reject('Request failed due to an error.');
                        }};

                        xhr.ontimeout = function () {{
                            reject('Request timed out.');
                        }};

                        xhr.send(data);
                    }});

                    return result; // Returns the resolved result directly
                }} catch (error) {{
                    return error; // If an error occurs, it will be thrown
                }}
            }}

            // Usage of fetchData to return the result
            fetchData()
            '''

            print(command_js)
            response = self.execute_js(command_js)

        except:
            ''  # logging.error(traceback.format_exc())

        return response

    def generate_proxy_playwright(self):
        proxy_str = self.proxies[random.randint(0, len(self.proxies) - 1)]
        if '@' in proxy_str:
            auth, server = proxy_str.split('@')
            username, password = auth.split(':')
        else:
            username = None
            password = None
            server = proxy_str

        ip_proxy, port_proxy = server.split(':')

        proxy_dict = {
            "server": f"http://{ip_proxy}:{port_proxy}",
            "username": username,
            "password": password
        }

        return proxy_dict

    def generate_extension_proxies(self):
        if self.proxies:
            proxy_str = random.choice(self.proxies)
            if '@' in proxy_str:
                auth, server = proxy_str.split('@')
                username, password = auth.split(':')
            else:
                username = None
                password = None
                server = proxy_str

            ip_proxy, port_proxy = server.split(':')

            manifest_json = """{"version": "1.0.0", "manifest_version": 2, "name": "Chrome Proxy", "permissions": ["proxy", "tabs", "unlimitedStorage", "storage", "<all_urls>", "webRequest", "webRequestBlocking"], "background": {"scripts": ["background.js"]}, "minimum_chrome_version":"22.0.0"}"""
            background_js = """var config = {mode: "fixed_servers", rules: {singleProxy: {scheme: "http", host: "%s", port: parseInt(%s)}, bypassList: ["localhost"]}}; chrome.proxy.settings.set({value: config, scope: "regular"}, function() {}); function callbackFn(details) {return {authCredentials: {username: "%s", password: "%s"}};}; chrome.webRequest.onAuthRequired.addListener(callbackFn, {urls: ["<all_urls>"]}, ['blocking']);""" % (
                ip_proxy, port_proxy, username, password)

            if os.path.exists(self.path_browser_proxies):
                shutil.rmtree(self.path_browser_proxies)
                os.makedirs(self.path_browser_proxies)
            else:
                os.makedirs(self.path_browser_proxies)

            with open(os.path.join(".", self.path_browser_proxies, 'manifest.json'), "w", encoding="utf-8") as f:
                f.write(manifest_json)

            with open(os.path.join(".", self.path_browser_proxies, 'background.js'), "w", encoding="utf-8") as f:
                f.write(background_js)

    def generate_headers(self, headers):
        js_code = "\n"
        for key, value in headers.items():
            key_lower = key.lower()
            if not key_lower.startswith(
                    'sec-') and key_lower != "user-agent" and key_lower != "origin" and key_lower != "referer":
                js_code += f'xhr.setRequestHeader("{key}", "{value}");\n'
        return js_code

    def find_element(self, xpath=None):
        if self.library == 'P':
            return self.driver.query_selector(f'xpath={xpath}')

        elif self.library == 'D':
            return self.driver.ele(f'xpath:{xpath}')

        elif self.library == 'SB':
            return self.driver.find_element(xpath)

        else:
            logging.warning(f'The library "{self.library}" is not supported in the "find_element()" function.')

    def get_attribute(self, xpath=None, attr=None):
        if self.library == 'P':
            logging.warning(f'The library "{self.library}" is not supported in the "get_attribute()" function.')

        elif self.library == 'D':
            logging.warning(f'The library "{self.library}" is not supported in the "get_attribute()" function.')

        elif self.library == 'SB':
            return self.driver.get_attribute(xpath, attr, by='xpath')

        else:
            logging.warning(f'The library "{self.library}" is not supported in the "get_attribute()" function.')

    def set_attribute(self, xpath=None, attr=None, value=None, scroll=False):
        if self.library == 'P':
            logging.warning(f'The library "{self.library}" is not supported in the "get_attribute()" function.')

        elif self.library == 'D':
            logging.warning(f'The library "{self.library}" is not supported in the "get_attribute()" function.')

        elif self.library == 'SB':
            self.driver.set_attribute(xpath, attr, value, by='xpath', scroll=scroll)

        else:
            logging.warning(f'The library "{self.library}" is not supported in the "get_attribute()" function.')

    def wait(self, xpath=None, delay=10):
        start_dt = time.time()
        while True:
            if not self.find_element(xpath=xpath):
                break
            elif time.time() - start_dt > delay:
                break
            else:
                time.sleep(1)

        return round(time.time() - start_dt, 2)

        # if self.library == 'P':
        #     self.driver.locator(f'xpath={xpath}').wait_for(timeout=delay*1000)
        #
        # elif self.library == 'D':
        #     self.driver.wait.ele_displayed(f'xpath:{xpath}', timeout=delay)
        #
        # else:
        #     logging.warning(f'The library "{self.library}" is not supported in the "wait()" function.')

    def execute_js(self, js):
        response = None
        if self.library == 'P':
            response = self.driver.evaluate(f'''async () => {{
                    {js}
                }}
            ''')

        elif self.library == 'D':
            response = self.driver.run_js(js)

        elif self.library == 'SB':
            response = self.driver.execute_script(js)

        else:
            logging.warning(f'The library "{self.library}" is not supported in the "execute_js()" function.')

        return response

    def click(self, xpath=None, delay=10):
        if self.library == 'P':
            self.driver.click(f'xpath={xpath}')
            time.sleep(delay)

        elif self.library == 'D':
            self.driver.ele(f'xpath:{xpath}').click()
            time.sleep(delay)

        elif self.library == 'SB':
            self.driver.click(xpath)
            time.sleep(delay)

        else:
            logging.warning(f'The library "{self.library}" is not supported in the "click()" function.')

    def type(self, xpath=None, text=None, delay=2):
        if self.library == 'P':
            self.driver.type(f'xpath={xpath}', text)
            time.sleep(delay)

        elif self.library == 'D':
            self.driver.ele(f'xpath:{xpath}').input(text)
            time.sleep(delay)

        elif self.library == 'SB':
            self.driver.type(xpath, text)
            time.sleep(delay)

        else:
            logging.warning(f'The library "{self.library}" is not supported in the "type()" function.')

    def select(self, css=None, value=None, delay=2):
        self.execute_js('document.querySelector(\'' + css + '\').value = \'' + str(value) + '\';')
        time.sleep(delay)

    def datepicker(self, css=None, value=None, delay=2):
        value_formatted = fct_core.convert_string_to_date_format(date_str=value, date_format='%Y-%m-%d')
        self.execute_js('document.querySelector(\'' + css + '\').value = \'' + str(value_formatted) + '\';')
        time.sleep(delay)

    def content(self):
        # response = None
        # if self.library == 'P':
        #     # response = self.driver.content()
        #     # response = self.driver.inner_html('html')
        #     response = self.execute_js("return document.getElementsByTagName('html')[0].innerHTML")
        #
        # elif self.library == 'D':
        #     # response = self.driver.html
        #     response = self.execute_js("return document.getElementsByTagName('html')[0].innerHTML")
        #
        # else:
        #     logging.warning(f'The library "{self.library}" is not supported in the "content()" function.')

        response = self.execute_js("return document.getElementsByTagName('html')[0].innerHTML")
        return response

    def get_cookies(self):
        cookies = None
        if self.library == 'P':
            cookies = {cookie["name"]: cookie["value"] for cookie in self.context.cookies()}

        elif self.library == 'D':
            cookies = {cookie["name"]: cookie["value"] for cookie in self.driver.cookies()}

        elif self.library == 'SB':
            cookies = {cookie["name"]: cookie["value"] for cookie in self.driver.get_cookies()}

        else:
            logging.warning(f'The library "{self.library}" is not supported in the "get_cookies()" function.')

        return cookies

    def get_current_url(self):
        current_url = None
        if self.library == 'P':
            current_url = self.driver.url

        elif self.library == 'D':
            current_url = self.driver.url

        elif self.library == 'SB':
            current_url = self.driver.get_current_url()

        else:
            logging.warning(f'The library "{self.library}" is not supported in the "get_current_url()" function.')

        return current_url

    def zoom_document(self, zoom=0.25, delay=1):
        _ = self.execute_js(f"document.body.style.zoom={zoom};")
        time.sleep(delay)

    def scroll_to_bottom(self, delay=5):
        if self.library == 'D':
            self.driver.set.scroll.smooth(on_off=True)
            self.driver.scroll.to_bottom()

        else:
            _ = self.execute_js("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(delay)

    def scroll_to_element(self, xpath=None, delay=2):
        if self.library == 'D':
            ele = self.find_element(xpath=xpath)
            self.driver.scroll.to_see(ele)

            # self.driver.scroll.to_see(f'xpath://div[@id="flagging-button"]')

        else:
            logging.warning(f'The library "{self.library}" is not supported in the "get_current_url()" function.')
        time.sleep(delay)


class CloudflareBypasser_DrissionPage:
    def __init__(self, cloudflare_title, driver):
        self.cloudflare_title = cloudflare_title
        self.driver = driver
        self.max_retries = 5
        self.log = True

    def search_recursively_shadow_root_with_iframe(self, ele):
        if ele.shadow_root:
            if ele.shadow_root.child().tag == "iframe":
                return ele.shadow_root.child()
        else:
            for child in ele.children():
                result = self.search_recursively_shadow_root_with_iframe(child)
                if result:
                    return result
        return None

    def search_recursively_shadow_root_with_cf_input(self, ele):
        if ele.shadow_root:
            if ele.shadow_root.ele("tag:input"):
                return ele.shadow_root.ele("tag:input")
        else:
            for child in ele.children():
                result = self.search_recursively_shadow_root_with_cf_input(child)
                if result:
                    return result
        return None

    def locate_cf_button(self):
        button = None
        eles = self.driver.eles("tag:input")
        for ele in eles:
            if "name" in ele.attrs.keys() and "type" in ele.attrs.keys():
                if "turnstile" in ele.attrs["name"] and ele.attrs["type"] == "hidden":
                    button = ele.parent().shadow_root.child()("tag:body").shadow_root("tag:input")
                    break

        if button:
            return button
        else:
            # If the button is not found, search it recursively
            self.log_message("Basic search failed. Searching for button recursively.")
            ele = self.driver.ele("tag:body")
            iframe = self.search_recursively_shadow_root_with_iframe(ele)
            if iframe:
                button = self.search_recursively_shadow_root_with_cf_input(iframe("tag:body"))
            else:
                self.log_message("Iframe not found. Button search failed.")
            return button

    def log_message(self, message):
        if self.log:
            logging.warning(message)

    def click_verification_button(self):
        try:
            button = self.locate_cf_button()
            if button:
                self.log_message("Verification button found. Attempting to click.")
                button.click()
            else:
                self.log_message("Verification button not found.")

        except Exception as e:
            self.log_message(f"Error clicking verification button: {e}")

    def is_bypassed(self):
        try:
            title = self.driver.title.lower()
            logging.warning(f"Title: {title}")
            return self.cloudflare_title.lower() not in title
        except Exception as e:
            self.log_message(f"Error checking page title: {e}")
            return False

    def bypass(self):

        try_count = 0

        while not self.is_bypassed():
            if 0 < self.max_retries + 1 <= try_count:
                self.log_message("Exceeded maximum retries. Bypass failed.")
                break

            self.log_message(f"Attempt {try_count + 1}: Verification page detected. Trying to bypass...")
            self.click_verification_button()

            try_count += 1
            time.sleep(10)

        if self.is_bypassed():
            self.log_message("Bypass successful.")
        else:
            self.log_message("Bypass failed.")


class RecaptchaBypasser_DrissionPage:
    def __init__(self, driver):
        self.driver = driver
        self.captcha_iframe = '//iframe[@title="reCAPTCHA"]'
        self.captcha_checkbox = '//span[@id="recaptcha-anchor"]'
        self.captcha_bypassed = '//span[contains(@class, "recaptcha-checkbox-checked")]'

    def clickCycle(self):
        try:
            if self.driver.get_frame(f'xpath:{self.captcha_iframe}').ele(f'xpath:{self.captcha_checkbox}', timeout=2):
                time.sleep(2)
                self.driver.get_frame(f'xpath:{self.captcha_iframe}').ele(f'xpath:{self.captcha_checkbox}',
                                                                          timeout=3).click()
        except:
            ''

    def isBypassed(self):
        try:
            if self.driver.get_frame(f'xpath:{self.captcha_iframe}').ele(
                    f'xpath:{self.captcha_bypassed}') and not self.driver.get_frame(f'xpath:{self.captcha_iframe}').ele(
                f'xpath://div[@id="rc-imageselect"]'):
                return True
            return False
        except:
            return False

    def bypass(self):
        i = 0
        while not self.isBypassed() and i < 5:
            i += 1
            logging.info(f"RecaptchaBypasser: {i}/5 | Recaptcha Verification page detected. Trying to bypass...")
            time.sleep(10)
            self.clickCycle()


class PressHoldBypasser_DrissionPage:
    def __init__(self, driver):
        self.driver = driver

    def clickCycle(self):
        try:
            if self.driver.wait.ele_displayed('#px-captcha', timeout=1.5):
                time.sleep(1.5)
                action = Actions(self.driver)
                element = self.driver.ele('#px-captcha')
                print('element = ', element)
                print('click_and_hold')
                action.hold('#px-captcha')
                print('sleep 10')
                time.sleep(10)
                print('release')
                action.release('#px-captcha')
                print('sleep 5')
                time.sleep(5)
        except:
            logging.error(traceback.format_exc())

    def isBypassed(self):
        if 'Press & Hold to confirm you are' in self.driver.html:
            return False
        return True

    def bypass(self):
        i = 0
        while not self.isBypassed() and i < 5:
            i += 1
            logging.info(f"Press & Hold: {i}/5 | Press & Hold Verification page detected. Trying to bypass...")
            time.sleep(10)
            self.clickCycle()

# if __name__ == '__main__':
#     use_proxy = True
#     proxies = ["nvuoqcqz-rotate:00bb3er9drua@p.webshare.io:80"]
#
# self.cookies = {
#     'visid_incap_2712217': 'PLjJjfe+Tt2/6whGuk7ZyEooy2YAAAAAQUIPAAAAAAD4VCbXaWjGEDXygjGXDU0z',
#     'pa_privacy': '%22optin%22',
#     'TCPID': '124801349194451461676',

#     fctbrowser = Browser(library='P', use_proxy=use_proxy, proxies=proxies, cookies=self.cookies, block_imgs=False)
#     fctbrowser.open()
#
#     str1 = fctbrowser.request(method='GET', link='https://quotes.toscrape.com/login', timeout=5)
#     response = fctbrowser.content()
#
#     logging.info(f'response: {response}')
#
#     logging.info('wait')
#     fctbrowser.wait(xpath='//input[@id="username"]', delay=5)
#     logging.info('type username')
#     fctbrowser.type(xpath='//input[@id="username"]', text='hello username', delay=2)
#     logging.info('type password')
#     fctbrowser.type(xpath='//input[@id="password"]', text='hello password', delay=2)
#     logging.info('click password Login')
#     fctbrowser.click(xpath='//input[@value="Login"]', delay=10)
#
#     logging.info('Finished scraping')
#     time.sleep(2000)
#
# #     headers = {
# #         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
# #         'accept-language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ar;q=0.6',
# #         'cache-control': 'no-cache',
# #         'pragma': 'no-cache',
# #         'priority': 'u=0, i',
# #         'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
# #         'sec-ch-ua-mobile': '?0',
# #         'sec-ch-ua-platform': '"Windows"',
# #         'sec-fetch-dest': 'document',
# #         'sec-fetch-mode': 'navigate',
# #         'sec-fetch-site': 'same-origin',
# #         'sec-fetch-user': '?1',
# #         'upgrade-insecure-requests': '1',
# #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
# #     }
# #
# #     fctbrowser = Browser(library='D', use_proxy=use_proxy, proxies=proxies, block_imgs=False)
# #     fctbrowser.open()
# #
# #     str1 = fctbrowser.request(method='GET', link='https://www.buzzfile.com/business/US-Lawns-of-Fort-Myers-239-690-1725', timeout=5)
# #     logging.info(f'str1: {str1}')
# #
# #
# #     # str1 = fctbrowser.request(method='GET', link='https://www.zillow.com/pfs/api/v1/client-data', timeout=5)
# #     # logging.info(f'str1: {str1}')
# #     #
# #     # str1 = fctbrowser.request(method='XGET', link='https://www.zillow.com/profile/bndzumbo', headers=headers, timeout=5)
# #     # logging.info(f'str1: {str1}')
# #     #
# #     # str1 = fctbrowser.request(method='XGET', link='https://httpbin.org/get', headers=headers, timeout=5)
# #     # logging.info(f'str1: {str1}')
# #     #
# #     # str1 = fctbrowser.request(method='XPOST', link='https://httpbin.org/post', data=[], headers=headers, timeout=5)
# #     # logging.info(f'str1: {str1}')
# #
# #     time.sleep(2000)
# #     fctbrowser.close()
# #
# #     logging.info(f'script take {round(time.time() - start_dt, 2)} sec to finished')


# str1 = self.fctbrowser.request(method='LGET', method_request='GET', link=link, timeout=5, file_path=file_path, response_length=20, check_if_title_not_exist='Just a moment...', check_if_keywords_not_exist=['cloudflare'])

