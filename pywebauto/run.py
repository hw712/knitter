#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types, importlib, time, inspect, os

import selenium.webdriver as webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import log, env, function



def launch_browser():
    env.PROJECT_PATH = inspect.stack()[2][1].rsplit("\\", 1)[0]
    
    
    if env.RUNNING_BROWSER == "Firefox":
        os.popen("TASKKILL /F /IM firefox.exe")
        
        binary_path = function.getconf("BinaryPath_Firefox")
        
        if binary_path == "":
            env.BROWSER = webdriver.Firefox()
        else:
            fb = FirefoxBinary(firefox_path=binary_path)
            env.BROWSER = webdriver.Firefox(firefox_binary=fb)
    
    
    elif env.RUNNING_BROWSER == "Chrome":
        os.popen("TASKKILL /F /IM chrome.exe")
        os.popen("TASKKILL /F /IM chromedriver.exe")
        
        chromedriver = function.getconf("DriverPath_Chrome")
        os.environ["webdriver.chrome.driver"] = chromedriver
        env.BROWSER = webdriver.Chrome(chromedriver)
    
    
    elif env.RUNNING_BROWSER == "IE":
        os.popen("TASKKILL /F /IM iexplorer.exe")
        os.popen("TASKKILL /F /IM IEDriverServer.exe")
        
        iedriver = function.getconf("DriverPath_IE")
        os.environ["webdriver.ie.driver"] = iedriver
        env.BROWSER = webdriver.Ie(iedriver)
    
    
    else:
        return False
    
    
    env.TEST_URL = function.getconf("Testing_URL")
    
    
    env.BROWSER.get(env.TEST_URL)
    env.BROWSER.maximize_window()
    
    time.sleep(3)
    
    return True



def testcase_tail_cleaning():
    time.sleep(3)
    env.BROWSER.quit()
    
    os.popen("TASKKILL /F /IM IEDriverServer.exe")
    os.popen("TASKKILL /F /IM chromedriver.exe")




def run_module(module_name):
    testmodule = importlib.import_module(module_name)
    
    env.MODULE_NAME = module_name.split('.')[-1]
    testcases = [testmodule.__dict__.get(a).__name__ for a in dir(testmodule)
           if isinstance(testmodule.__dict__.get(a), types.FunctionType)]
    
    env.PROJECT_PATH = inspect.stack()[1][1].rsplit("\\", 1)[0]
    env.TESTING_BROWSERS = function.getconf("Testing_Browsers")
    
    
    for testcase in testcases:
        if testcase == "before_each_testcase" or testcase == "after_each_testcase" or testcase == "before_launch_browser":
            continue
        
        for browser in env.TESTING_BROWSERS.split('|'):
            env.RUNNING_BROWSER = browser
            
            
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
            testcase_tail_cleaning()





def run_case(module_name, case_name):
    testmodule = importlib.import_module(module_name)
    
    env.MODULE_NAME = module_name.split('.')[-1]
    testcases = [testmodule.__dict__.get(a).__name__ for a in dir(testmodule)
           if isinstance(testmodule.__dict__.get(a), types.FunctionType)]
    
    env.PROJECT_PATH     = inspect.stack()[1][1].rsplit("\\", 1)[0]
    env.TESTING_BROWSERS = function.getconf("Testing_Browsers")
    
    if not case_name in testcases:
        return
    
    
    
    for browser in env.TESTING_BROWSERS.split('|'):
        env.RUNNING_BROWSER = browser
        
        
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
        testcase_tail_cleaning()







