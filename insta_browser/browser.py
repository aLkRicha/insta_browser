from selenium import webdriver
import pickle
import time


class Browser:

    def __init__(self, debug=False, chrome=False):
        if chrome:
            self.chrome = chrome
            self.browser = webdriver.Chrome()
        else:
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            for key, value in headers.items():
                webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = headers.get('User-Agent')

            self.browser = webdriver.PhantomJS()
            self.browser.command_executor._commands['executePhantomScript']=('POST', '/session/$sessionId/phantom/execute')
            self.resource_requested_logic()
        self.mouse = webdriver.ActionChains(self.browser)
        self.debug = debug

    def clear_driver_cache(self):
        self.browser.execute('executePhantomScript', {'script': '''
            var page = this;
            page.clearMemoryCache();
        ''', 'args': []})

    def resource_requested_logic(self):
        self.browser.execute('executePhantomScript', {'script': '''
            var page = this;
            page.onResourceRequested = function(request, networkRequest) {
                if (/\.(jpg|jpeg|png|mp3|css|mp4)/i.test(request.url))
                {
                    //console.log('Final with css! Suppressing image: ' + request.url);
                    networkRequest.abort();
                    return;
                }
            }
        ''', 'args': []})

    def auth(self, login, password):
        br = self.browser
        self.get("https://www.instagram.com/accounts/login/")
        self.browser.save_screenshot('var/screenshots/login.png')
        time.sleep(2)
        try:
            self.log('try to auth with cookies')
            cookies = pickle.load(open('var/cookies/{}.pkl'.format(login), "rb"))
            for cookie in cookies:
                br.add_cookie(cookie)

        except:
            self.log('regular login')
            login_field = br.find_element_by_name("username")
            login_field.clear()
            self.log(u'Login fill')
            login_field.send_keys(login)
            password_field = br.find_element_by_name("password")
            password_field.clear()
            self.log(u'Password fill')
            password_field.send_keys(password)
            submit = br.find_element_by_css_selector("form button")
            self.log(u'Form submit')
            submit.submit()
            time.sleep(3)
            pickle.dump([br.get_cookie('sessionid')], open('var/cookies/{}.pkl'.format(login), "wb"))
            self.log('auth complete')
        br.refresh()

    def get(self, url):
        self.browser.get(url)
        self.log(u'Open ' + self.browser.current_url)
        return self

    def close_all(self):
        self.browser.save_screenshot('var/screenshots/close_all.png')
        self.browser.close()
        self.browser.quit()
        self.log(u'Browser process was ended')
        self.log(u'')

    def is_last_post_in_feed_not_liked(self):
        try:
            self.browser.find_element_by_css_selector('article:last-child .coreSpriteLikeHeartOpen')
            return True
        except:
            return False

    def scroll_feed_to_last_not_liked(self):
        while self.is_last_post_in_feed_not_liked():
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.log('scroll down')

    def like_found_posts(self):
        br = self.browser
        articles = br.find_elements_by_tag_name('article')
        for post in articles:
            self.mouse.move_to_element(post).perform()
            time.sleep(1)
            heart = post.find_element_by_css_selector('div:nth-child(3) section a:first-child')
            if 'coreSpriteLikeHeartOpen' in heart.find_element_by_css_selector('span').get_attribute("class"):
                self.log('need to be liked ♥️')
                self.mouse.move_to_element(heart).perform()
                heart.click()
            else:
                self.log('no need to be liked 🍔')

    def log(self, text):
        if self.debug:
            print(text)
