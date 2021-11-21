import json
import logging
import os
from time import sleep

import selenium
import selenium.webdriver
from schedule import Scheduler
from selenium.common.exceptions import NoSuchElementException


class Login:
    def __init__(self):
        self.__url = "https://gw.buaa.edu.cn/"
        options = selenium.webdriver.FirefoxOptions()
        options.add_argument('-headless')
        self.__browser = selenium.webdriver.Firefox(
            executable_path=os.path.abspath("geckodriver"),
            options=options)
        # time limitation, 3 seconds is enough to load all assets in BUAA-WiFi
        # If exceed, there must be some connection errors.
        self.__browser.implicitly_wait(5)
        logging.basicConfig(
            level=logging.DEBUG,
            filename="daemon.log",
            filemode='w',
            format="%(asctime)s [%(name)s] %(levelname)-9s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")
        self.__schedule = Scheduler()
        self.__schedule.every(2).hours.do(self.__run_once)

    def __login(self) -> int:
        data = None
        try:
            with open("config.json", 'r', encoding="utf-8") as cfg:
                data = json.load(cfg)
        except FileNotFoundError:
            logging.error("cannot find config file")
            return 1

        ret = 0
        self.__browser.get(self.__url)
        loaded = False

        try:
            # Check whether page is loaded or not by checking logo
            self.__browser.find_element_by_id("logo")
            loaded = True
            username_input = self.__browser.find_element_by_id("username")
            username_input.send_keys(data["username"])
            password_input = self.__browser.find_element_by_id("password")
            password_input.send_keys(data["password"])
            login_btn = self.__browser.find_element_by_id("login")
            login_btn.click()

            logging.info("login successfully")
        except NoSuchElementException as e:
            if not loaded:
                logging.error("cannot login, some key element cannot be found")
                logging.exception(e)
                ret = 1
            else:
                logging.error("cannot load page, check network connection")
                ret = 2

        # self.__browser.close()
        return ret

    def __check_alive(self) -> int:
        ret = 0
        self.__browser.get(self.__url)
        loaded = False

        try:
            self.__browser.find_element_by_id("logo")
            loaded = True
            # FIXME: text of lavel cannot be got
            # user_flow_label = self.__browser.find_element_by_id("used_flow")
            # logging.info("network flow remains: %s" % user_flow_label.text)
        except NoSuchElementException:
            if loaded:
                ret = 1
            else:
                ret = 2

        # self.__browser.close()
        return ret

    def __logout(self) -> int:
        ret = 0
        self.__browser.get(self.__url)

        try:
            self.__browser.find_element_by_id("logo")
            logout_btn = self.__browser.find_element_by_id("logout-dm")
            logout_btn.click()
        except NoSuchElementException:
            ret = 1

        # self.__browser.close()
        return ret

    def __run_once(self):
        logging.info("checking alive ...")
        ret = self.__check_alive()
        if ret > 0:
            logging.info("not alive, trying connect ...")
            ret = self.__login()
        return ret

    def run(self):
        self.__run_once()
        while True:
            self.__schedule.run_pending()
            sleep(1)
