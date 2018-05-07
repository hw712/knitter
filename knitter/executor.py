
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

import types
import os
import importlib

from knitter.configure import Browser, General
from knitter import logger


def launch_browser(browser, url):
    """
    Launch and init a new browser, start with the 'url'

    """

    if browser == Browser.FireFox:
        logger.step_normal("Launch Browser FireFox. URL = " + url)

        firefox_capabilities = DesiredCapabilities.FIREFOX

        # disable the download dialogue
        fp = webdriver.FirefoxProfile()
        fp.set_preference('browser.download.manager.showWhenStarting', False)

        try:
            if Browser.FireFox.Binary == "":
                Browser.RunningBrowser = webdriver.Firefox(executable_path=Browser.FireFox.Driver, firefox_profile=fp,
                                                           capabilities=firefox_capabilities,
                                                           log_path=os.path.join(General.Path.Result, "firefox.log"))
            else:
                Browser.RunningBrowser = webdriver.Firefox(executable_path=Browser.FireFox.Driver, firefox_profile=fp,
                                                           firefox_binary=FirefoxBinary(firefox_path=
                                                                                        Browser.FireFox.Binary),
                                                           log_path=os.path.join(General.Path.Result, "firefox.log"))

            if Browser.FireFox.__name__ not in General.VersionInfo:
                General.VersionInfo[Browser.FireFox.__name__] = Browser.RunningBrowser.capabilities['browserVersion']

        except Exception as e:
            logger.handle_exception(e)
            return False

    elif browser == Browser.Chrome:
        try:
            chrome_options = Options()

            if Browser.HeadlessMode is True:
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--window-size=1920x1080")
                chrome_options.add_argument("--no-sandbox")

            Browser.RunningBrowser = webdriver.Chrome(chrome_options=chrome_options,
                                                      executable_path=Browser.Chrome.Driver)

            if Browser.Chrome.__name__ not in General.VersionInfo:
                General.VersionInfo[Browser.Chrome.__name__] = Browser.RunningBrowser.capabilities['version']
        except Exception as e:
            logger.handle_exception(e)
            return False

    elif browser == Browser.IE:
        '''
        os.popen('TASKKILL /F /IM IEDriverServer.exe')
        dc = DesiredCapabilities.INTERNETEXPLORER.copy()
        dc['nativeEvents'] = False
        dc['acceptSslCerts'] = True
        '''

        try:
            Browser.RunningBrowser = webdriver.Ie(executable_path=Browser.IE.Driver)

            Browser.RunningBrowser.capabilities['acceptInsecureCerts'] = True
            # Browser.RunningBrowser.capabilities['nativeEvents'] = False
            # Browser.RunningBrowser.capabilities['ignoreProtectedModeSettings'] = True

            # print(Browser.RunningBrowser.capabilities)
            if Browser.IE.__name__ not in General.VersionInfo:
                General.VersionInfo[Browser.IE.__name__] = Browser.RunningBrowser.capabilities['browserVersion']
        except Exception as e:
            logger.handle_exception(e)
            return False

    Browser.RunningBrowser.set_window_size(1366, 758)
    Browser.RunningBrowser.set_window_position(0, 0)
    Browser.RunningBrowser.maximize_window()
    Browser.RunningBrowser.set_page_load_timeout(300)
    Browser.RunningBrowser.implicitly_wait(0)

    Browser.RunningBrowser.get(url)

    return True


def quit_browser():
    if Browser.RunningBrowser is not None:
        Browser.RunningBrowser.quit()
        Browser.RunningBrowser = None


def __run_test_module(test_module):
    General.TestModule.Name = test_module.__name__.split('.')[-1]

    cases = []
    for fun in dir(test_module):
        if (not fun.startswith("__")) and (not fun.endswith("__")) and (isinstance(test_module.__dict__.get(fun),
                                                                                   types.FunctionType)):
            if test_module.__dict__.get(fun).__module__ == test_module.__name__:
                cases.append(fun)

    for case in cases:
        if case == 'before_each_case' or case == 'after_each_case' or case == 'before_launch_browser':
            return

        for browser in Browser.AvailableBrowsers:
            try:
                logger.start_test_case(case, browser)

                if hasattr(test_module, 'before_launch_browser'):
                    getattr(test_module, 'before_launch_browser')()

                if hasattr(test_module, 'before_each_case'):
                    getattr(test_module, 'before_each_case')()

                if launch_browser(browser, Browser.StartURL) is False:
                    raise AssertionError("Launch Browser [" + browser.__name__ + "] Fails!")

                getattr(test_module, case)()

                if hasattr(test_module, 'after_each_case'):
                    getattr(test_module, 'after_each_case')()

            except Exception as e:
                logger.handle_exception(e)

                if General.QuickTest is True:
                    return
            finally:
                logger.stop_test_case()
                quit_browser()


def __run_test_case(case):
    test_module = importlib.import_module(case.__module__)
    General.TestModule.Name = case.__module__.split('.')[-1]

    for browser in Browser.AvailableBrowsers:
        try:
            logger.start_test_case(case.__name__, browser)

            if hasattr(test_module, 'before_launch_browser'):
                getattr(test_module, 'before_launch_browser')()

            if hasattr(test_module, 'before_each_case'):
                getattr(test_module, 'before_each_case')()

            if launch_browser(browser, Browser.StartURL) is False:
                raise AssertionError("Launch Browser [" + browser.__name__ + "] Fails!")

            case()

            if hasattr(test_module, 'after_each_case'):
                getattr(test_module, 'after_each_case')()

        except Exception as e:
            logger.handle_exception(e)

            if General.QuickTest is True:
                return
        finally:
            logger.stop_test_case()
            quit_browser()


def wrapper():
    def handle_func(func):
        def handle_args(*args):
            try:
                # args[0] should be a conf definition function.
                args[0]()

                # remove duplicated items.
                Browser.AvailableBrowsers = list(set(Browser.AvailableBrowsers))

                logger.start_project()

                func(*args)

                logger.end_project()

            except Exception as e:
                logger.handle_exception(e)

        return handle_args
    return handle_func


@wrapper()
def run(*args):
    if len(args) < 2:
        print("At least 2 args needed for run(), first as configuration, others are test object(s).")

    for i in range(1, len(args)):
        run_test_object(args[i])


def run_test_object(obj):
    if General.QuickTest is True and General.Total.NumberOfTestCaseFail > 0:
        return

    if isinstance(obj, list):
        for o in obj:
            run_test_object(o)

    elif isinstance(obj, types.ModuleType):
        __run_test_module(obj)

    elif isinstance(obj, types.FunctionType):
        __run_test_case(obj)

    else:
        print("knitter.executor: function [run_test_objects] code error: objects = " + obj)







