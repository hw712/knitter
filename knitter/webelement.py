# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

import time
import environment, log


class WebElement(object):
    (by, value) = (None, None)
    index       = 0
    
    
    @classmethod
    def Set(cls, value):
        log.step_normal(u"Element [%s]: Set Value [%s]." % (cls.__name__, value))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        elements[cls.index].clear()
        action = webdriver.ActionChains(environment.BROWSER)
        action.send_keys_to_element(elements[cls.index], value)
        action.perform()
        
        cls.__clearup()
    
    
    
    @classmethod
    def IsEnabled(cls):
        log.step_normal(u"Element [%s]: Is Enabled?" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        if elements[cls.index].is_enabled():
            log.step_normal(u"Yes!")
            return True
        else:
            log.step_normal(u"No!")
            return False
        
        cls.__clearup()
    
    
    @classmethod
    def TypeIn(cls, value):
        '''
        input value without clear existed values
        '''
        
        log.step_normal(u"Element [%s]: TypeIn Value [%s]." % (cls.__name__, value))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.send_keys_to_element(elements[cls.index], value)
        action.perform()
        
        cls.__clearup()
    
    
    @classmethod
    def GetFocus(cls):
        log.step_normal(u"Element [%s]: GetFocus()" % (cls.__name__, ))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        elements[cls.index].send_keys(Keys.NULL)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.send_keys_to_element(elements[cls.index], Keys.NULL)
        action.perform()
        
        cls.__clearup()
        
    
    @classmethod
    def GetInnerHTML(cls):
        log.step_normal(u"Element [%s]: GetInnerHTML." % (cls.__name__, ))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        #log.step_normal(u"Element [%s]: InnerHTML = [%s]" % (cls.__name__, elements[cls.index].get_attribute('innerHTML')))
        
        cls.__clearup()
        return elements[cls.index].get_attribute('innerHTML')
    
    
    @classmethod
    def GetAttribute(cls, attr):
        log.step_normal(u"Element [%s]: Get Attribute [%s]." % (cls.__name__, attr))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        return elements[cls.index].get_attribute(attr)
    
    '''
    @classmethod
    def VerifyInnerHTML(cls, verify_html):
        log.step_normal("Element [%s]: Verify Inner HTML [%s]." % (cls.__name__, verify_html))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        inner_html = element.get_attribute('innerHTML')
        
        if inner_html == verify_html:
            log.step_pass("Equal. Real inner_hmtl=[%s]" % inner_html)
        else:
            log.step_fail("NOT Equal. Real inner_hmtl=[%s]" % inner_html)
    
    
    @classmethod
    def GetValue(cls):
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        return element.get_attribute('value')
    
    
    
    @classmethod
    def VerifyValue(cls, verify_value):
        log.step_normal("Element [%s]: VerifyValue [%s]." % (cls.__name__, verify_value))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        page_value = element.get_attribute('value')
        
        if page_value == verify_value:
            log.step_pass("Equal. page_value=[%s]" % page_value)
        else:
            log.step_fail("NOT Equal. page_value=[%s]" % page_value)
    '''
    
    @classmethod
    def WaitForExist(cls):
        log.step_normal("Element [%s]: WaitForExist." % (cls.__name__))
        
        cls.__wait_for_exist(cls.by, cls.value)
        
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        if len(elements) == 0:
            log.step_fail("Element [%s]: Not Exist. Count=[%s]" % (cls.__name__, len(elements)))
        
        cls.__clearup()
    
    
    @classmethod
    def WaitForDisappear(cls):
        log.step_normal("Element [%s]: WaitForNotExist." % (cls.__name__))
        
        if cls.__wait_for_not_exist(cls.by, cls.value) == True:
            log.step_pass("Element [%s]: Not Exist." % (cls.__name__))
        
        cls.__clearup()
    
    
    @classmethod
    def GetObjectsCount(cls):
        log.step_normal("Element [%s]: GetObjectsCount." % (cls.__name__))
        
        cls.__wait_for_exist(cls.by, cls.value)
        
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        log.step_normal("Element [%s]: GetObjectsCount = [%s]" % (cls.__name__, len(elements)))
        
        cls.__clearup()
        return len(elements)
    
    
    @classmethod
    def IsExist(cls):
        log.step_normal("Element [%s]: IsExist?" % (cls.__name__))
        
        cls.__wait_for_exist(cls.by, cls.value)
        
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        log.step_normal("Element [%s]: IsExist? Count = [%s]" % (cls.__name__, len(elements)))
        
        cls.__clearup()
        if len(elements) > 0:
            return True
        else:
            return False
    
    
    @classmethod
    def VerifyExistence(cls, trueORfalse):
        log.step_normal("Element [%s]: Verify Existence [%s]." % (cls.__name__, trueORfalse))
        
        cls.__wait_for_exist(cls.by, cls.value)
        
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        log.step_normal("Element [%s]: Count = [%s]" % (cls.__name__, len(elements)))
        
        
        cls.__clearup()
        if len(elements) > 0:
            if trueORfalse == True:
                log.step_pass("Exist!")
            else:
                log.step_fail("Exist!")
        else:
            if trueORfalse == False:
                log.step_pass("Not Exist!")
            else:
                log.step_fail("Not Exist!")
    
    
    @classmethod
    def VerifyInnerHTMLContains(cls, contain_content):
        log.step_normal("Element [%s]: VerifyInnerHTMLContains [%s]." % (cls.__name__, contain_content))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        inner_html = elements[cls.index].get_attribute('innerHTML')
        
        if contain_content in inner_html:
            log.step_pass("Real inner_hmtl=[%s]" % inner_html)
        else:
            log.step_fail("Real inner_hmtl=[%s]" % inner_html)
        
        cls.__clearup()
    
    @classmethod
    def VerifyAttribute(cls, attr, contain_content):
        log.step_normal("Element [%s]: Verify Attribute [%s] == [%s]." % (cls.__name__, attr, contain_content))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        attr_value = elements[cls.index].get_attribute(attr)
        
        if contain_content == attr_value:
            log.step_pass("Real attr_value=[%s]" % attr_value)
        else:
            log.step_fail("Real attr_value=[%s]" % attr_value)
        
        cls.__clearup()
    
    @classmethod
    def VerifyAttributeContains(cls, attr, contain_content):
        log.step_normal("Element [%s]: Verify [%s] Contains [%s]." % (cls.__name__, attr, contain_content))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        attr_value = elements[cls.index].get_attribute(attr)
        
        if contain_content in attr_value:
            log.step_pass("Real attr_value=[%s]" % attr_value)
        else:
            log.step_fail("Real attr_value=[%s]" % attr_value)
        
        cls.__clearup()
    
    @classmethod
    def DoubleClick(cls):
        log.step_normal("Element [%s]: Do DoubleClick()" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.double_click(elements[cls.index])
        action.perform()
        
        cls.__clearup()
    
    
    
    @classmethod
    def Click(cls):
        log.step_normal("Element [%s]: Do Click()" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.click(elements[cls.index])
        action.perform()
        
        cls.__clearup()
        
        time.sleep(1)
    
    
    @classmethod
    def MouseOver(cls):
        log.step_normal("Element [%s]: Do MouseOver()" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.move_to_element(elements[cls.index])
        action.perform()
        
        cls.__clearup()
    
    
    @classmethod
    def ClickAndHold(cls):
        log.step_normal("Element [%s]: Do ClickAndHold()" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.click_and_hold(elements[cls.index])
        action.perform()
        
        cls.__clearup()
    
    
    @classmethod
    def ReleaseClick(cls):
        log.step_normal("Element [%s]: Do ReleaseClick()" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.release(elements[cls.index])
        action.perform()
        
        cls.__clearup()
    
    
    @classmethod
    def SelectByOrder(cls, order):
        log.step_normal("Element [%s]: Do Select by Order [%s]" % (cls.__name__, order))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        #### ul ################
        if elements[cls.index].tag_name == "ul":
            lis = elements[cls.index].find_elements_by_tag_name('li')
            
            if order > 0:
                
                ### Wait and try more times if NO item found. ###
                t = 0
                while (len(lis) == 0):
                    lis = elements[cls.index].find_elements_by_tag_name('li')
                    time.sleep(3)
                    t = t + 1
                    log.step_normal("Element [%s]: Wait 3 Seconds for [li]")
                    
                    if t == 8 and len(lis) == 0:
                        log.step_fail("Element [%s]: List Count = [%s]." % (cls.__name__, len(lis)))
                        return
                
                
                log.step_normal("Element [%s]: List Count = [%s]." % (cls.__name__, len(lis)))
                
                if (order > len(lis)):
                    log.step_normal("Element [%s]: Not so many lists. [%s]" % (cls.__name__, len(lis)))
                else:
                    log.step_normal("Element [%s]: Do Click [%s]" % (cls.__name__, order))
                    action = webdriver.ActionChains(environment.BROWSER)
                    action.click(lis[order-1])
                    action.perform()
            else:
                log.step_fail("Order = [%s], Value Error." % order)
                
                
        
        #for li in lis:
        #    pass
#             if option.get_attribute('selected') != None:
#                 print "Default Selection: ", option.get_attribute('selected'), option.text
#             
#             if option.is_selected():
#                 print "option.is_selected():", option.text
            
            #if li.text == value:
            #    li.click()
        
        cls.__clearup()
    
    
    @classmethod
    def Select(cls, value):
        log.step_normal("Element [%s]: Do Select [%s]." % (cls.__name__, value))
        
        cls.__wait(cls.by, cls.value)
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        
        
        #### select ################
        if elements[cls.index].tag_name == "select":
            options = elements[cls.index].find_elements_by_tag_name('option')
            
            for option in options:
                # if option.get_attribute('selected') != None:
                #     print "Default Selection: ", option.get_attribute('selected'), option.text
                #  
                # if option.is_selected():
                #     print "option.is_selected():", option.text
                
                if option.text == value:
                    option.click()
        
        
        
        #### select ################
        elif elements[cls.index].tag_name == "ul":
            pass
        
        
        
        
        #### NOT Supported ################
        else:
            log.step_fail("Element [%s]: Tag Name [%s] Not Supported." % (cls.__name__, elements[cls.index].tag_name))
        
        cls.__clearup()
    
    @classmethod
    def __wait(cls, test_by, test_value):
        t = 0
        while t < 60:
            t = t + 1
            
            try:
                elements = environment.BROWSER.find_elements(test_by, test_value)
            except NoSuchElementException:
                log.step_normal("Element [%s]: NoSuchElementException." % cls.__name__)
                elements = []
            
            if len(elements) == 0:
                time.sleep(3)
                log.step_normal("Element [%s]: Wait 3 Seconds, By [%s]" % (cls.__name__, test_value))
            else:
                break
        
        if len(elements) < cls.index + 1:
            log.step_fail("Element [%s]: Element Index Issue! There are [%s] Elements! Index=[%s]" % (cls.__name__, len(elements), cls.index))
        
    
    @classmethod
    def __wait_for_not_exist(cls, test_by, test_value):
        
        t = 0
        while t < 40:
            t = t + 1
            
            try:
                elements = environment.BROWSER.find_elements(test_by, test_value)
            except NoSuchElementException:
                log.step_normal("Element [%s]: NoSuchElementException." % cls.__name__)
                elements = []
            
            if len(elements) == 0:
                return True
            else:
                time.sleep(3)
                log.step_normal("Element [%s]: Found [%s] Element. Tried [%s] Times." % (cls.__name__, len(elements), t))
        
        return False
    
    @classmethod
    def __wait_for_exist(cls, test_by, test_value):
        
        t = 0
        while t < 5:
            t = t + 1
            
            try:
                elements = environment.BROWSER.find_elements(test_by, test_value)
            except NoSuchElementException:
                log.step_normal("Element [%s]: NoSuchElementException." % cls.__name__)
                elements = []
            
            if len(elements) == 0:
                time.sleep(3)
            else:
                log.step_normal("Element [%s]: Found [%s] Element. Tried [%s] Times." % (cls.__name__, len(elements), t))
                break
    
    
    @classmethod
    def __clearup(cls):
        if cls.index != 0:
            log.step_normal("Element [%s]: Last Element Index = [%s]." % (cls.__name__, cls.index))
        
        cls.index = 0







