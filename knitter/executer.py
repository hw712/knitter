# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import types, importlib, time, inspect, os
import log, environment, common



def launch_browser():
    
    if environment.RUNNING_BROWSER == "Firefox":
        #os.popen("TASKKILL /F /IM firefox.exe")
        
        binary_path = common.getconf("BinaryPath_Firefox")
        
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        fp = FirefoxProfile()
        fp.native_events_enabled = False
        
        if binary_path == "":
            environment.BROWSER = webdriver.Firefox(firefox_profile=fp)
        else:
            fb = FirefoxBinary(firefox_path=binary_path)
            environment.BROWSER = webdriver.Firefox(firefox_profile=fp, firefox_binary=fb)
    
    
    elif environment.RUNNING_BROWSER == "Chrome":
        #os.popen("TASKKILL /F /IM chrome.exe")
        os.popen("TASKKILL /F /IM chromedriver.exe")
        
        binary_path  = common.getconf("BinaryPath_Chrome")
        chromedriver = common.getconf("DriverPath_Chrome")
        
        if binary_path == "":
            os.environ["webdriver.chrome.driver"] = chromedriver
            environment.BROWSER = webdriver.Chrome(executable_path=chromedriver)
        else:
            opts = Options()
            opts.binary_location = binary_path
            
            os.environ["webdriver.chrome.driver"] = chromedriver
            environment.BROWSER = webdriver.Chrome(executable_path=chromedriver, chrome_options=opts)
    
    
    elif environment.RUNNING_BROWSER == "IE":
        #os.popen("TASKKILL /F /IM iexplore.exe")
        os.popen("TASKKILL /F /IM IEDriverServer.exe")
        
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        dc = DesiredCapabilities.INTERNETEXPLORER.copy()
        
        dc['acceptSslCerts'] = True
        dc['nativeEvents']   = True
        
        iedriver = common.getconf("DriverPath_IE")
        os.environ["webdriver.ie.driver"] = iedriver
        environment.BROWSER = webdriver.Ie(executable_path=iedriver, capabilities=dc)
    
    
    else:
        return False
    
    
    environment.TEST_URL = common.getconf("Testing_URL")
    
    
    environment.BROWSER.get(environment.TEST_URL)
    environment.BROWSER.maximize_window()
    
    time.sleep(3)
    
    return True



def testcase_windingup():
    time.sleep(3)
    environment.BROWSER.quit()
    
    os.popen("TASKKILL /F /IM IEDriverServer.exe")
    os.popen("TASKKILL /F /IM chromedriver.exe")




def run_module(module_name):
    testmodule = importlib.import_module("testcase.%s" % module_name)
    
    environment.MODULE_NAME = module_name.split('.')[-1]
    testcases = [testmodule.__dict__.get(a).__name__ for a in dir(testmodule)
           if isinstance(testmodule.__dict__.get(a), types.FunctionType)]
    
    environment.PROJECT_PATH = inspect.stack()[1][1].rsplit("\\", 1)[0]
    environment.TESTING_BROWSERS = common.getconf("Testing_Browsers")
    
    
    for testcase in testcases:
        if testcase == "before_each_testcase" or testcase == "after_each_testcase" or testcase == "before_launch_browser":
            continue
        
        for browser in environment.TESTING_BROWSERS.split('|'):
            environment.RUNNING_BROWSER = browser
            
            
            ##### Launch Browser
            if "before_launch_browser" in testcases:
                getattr(testmodule, "before_launch_browser")()
            
            if launch_browser() == False:
                continue
            
            
            ##### Run Test Case.
            try:
                log.start_test(testcase)
                
                if "before_each_testcase" in testcases:
                    getattr(testmodule, "before_each_testcase")()
                
                getattr(testmodule, testcase)()
            except:
                log.handle_error()
            finally:
                if "after_each_testcase" in testcases:
                    getattr(testmodule, "after_each_testcase")()
                
                log.stop_test()
            
            
            ##### Clear Environment. Quite Browser, Kill Driver Processes.
            testcase_windingup()





def run_case(module_name, case_name):
    testmodule = importlib.import_module("testcase.%s" % module_name)
    
    environment.MODULE_NAME = module_name.split('.')[-1]
    testcases = [testmodule.__dict__.get(a).__name__ for a in dir(testmodule)
           if isinstance(testmodule.__dict__.get(a), types.FunctionType)]
    
    environment.PROJECT_PATH     = inspect.stack()[1][1].rsplit("\\", 1)[0]
    environment.TESTING_BROWSERS = common.getconf("Testing_Browsers")
    
    if not case_name in testcases:
        return
    
    
    
    for browser in environment.TESTING_BROWSERS.split('|'):
        environment.RUNNING_BROWSER = browser
        
        
        ##### Launch Browser
        if "before_launch_browser" in testcases:
            getattr(testmodule, "before_launch_browser")()
        
        if launch_browser() == False:
            continue
        
        ##### Run Test Case.
        try:
            log.start_test(case_name)
            
            if "before_each_testcase" in testcases:
                getattr(testmodule, "before_each_testcase")()
            
            getattr(testmodule, case_name)()
        except:
            log.handle_error()
        finally:
            if "after_each_testcase" in testcases:
                getattr(testmodule, "after_each_testcase")()
            
            log.stop_test()
        
        
        ##### Clear Environment. Quite Browser, Kill Driver Processes.
        testcase_windingup()







