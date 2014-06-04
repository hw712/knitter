# -*- coding: utf-8 -*-

from selenium import webdriver

import time
import environment, log


class WebElement(object):
    (by, value) = (None, None)
    
    
    @classmethod
    def Set(cls, value):
        log.step_normal(u"Element [%s]: Set Value [%s]." % (cls.__name__, value))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        element.clear()
        action = webdriver.ActionChains(environment.BROWSER)
        action.send_keys_to_element(element, value)
        action.perform()
    
    
    @classmethod
    def IsEnabled(cls):
        log.step_normal(u"Element [%s]: Is Enabled?" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        if element.is_enabled():
            log.step_normal(u"Yes!")
            return True
        else:
            log.step_normal(u"No!")
            return False
    
    
    @classmethod
    def TypeIn(cls, value):
        '''
        input value without clear existed values
        '''
        
        log.step_normal(u"Element [%s]: TypeIn Value [%s]." % (cls.__name__, value))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.send_keys_to_element(element, value)
        action.perform()
    
    '''
    @classmethod
    def GetInnerHTML(cls):
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        return element.get_attribute('innerHTML')
    
    
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
    def IsExist(cls):
        log.step_normal("Element [%s]: IsExist?" % (cls.__name__))
        
        cls.__wait_for_exist(cls.by, cls.value)
        
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        log.step_normal("Element [%s]: IsExist? Count=[%s]" % (cls.__name__, len(elements)))
        
        
        if len(elements) > 0:
            return True
        else:
            return False
    
    
    @classmethod
    def VerifyExistence(cls, trueORfalse):
        log.step_normal("Element [%s]: Verify Existence [%s]." % (cls.__name__, trueORfalse))
        
        cls.__wait_for_exist(cls.by, cls.value)
        
        elements = environment.BROWSER.find_elements(cls.by, cls.value)
        log.step_normal("Element [%s]: Exist Count=[%s]" % (cls.__name__, len(elements)))
        
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
    def DoubleClick(cls):
        log.step_normal("Element [%s]: Do DoubleClick()" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.double_click(element)
        action.perform()
        
        
        time.sleep(2)
    
    
    
    @classmethod
    def Click(cls):
        log.step_normal("Element [%s]: Do Click()" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.click(element)
        action.perform()
    
    
    
    @classmethod
    def IEClick(cls):
        log.step_normal("Element [%s]: Do IEClick()" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.click_and_hold(element)
        action.release(element)
        action.perform()
        
    
    @classmethod
    def MouseOver(cls):
        log.step_normal("Element [%s]: Do MouseOver()" % (cls.__name__))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        action = webdriver.ActionChains(environment.BROWSER)
        action.move_to_element(element)
        action.perform()
        
    
    
    @classmethod
    def ULSelectByOrder(cls, order):
        log.step_normal("Element [%s]: Do Select [%s]" % (cls.__name__, order))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        lis = element.find_elements_by_tag_name('li')
        
        if order > 0:
            t = 0
            while (len(lis) == 0):
                lis = element.find_elements_by_tag_name('li')
                time.sleep(3)
                t = t + 1
                
                if t == 2:
                    return
            
            log.step_normal("Element [%s]: List Count = [%s]." % (cls.__name__, len(lis)))
            
            if (order > len(lis)):
                log.step_normal("Element [%s]: Not su many lists. [%s]" % (cls.__name__, len(lis)))
            else:
                log.step_normal("Element [%s]: Do Click [%s]" % (cls.__name__, order))
                action = webdriver.ActionChains(environment.BROWSER)
                action.click(lis[order-1])
                action.perform()
                
                
        
        #for li in lis:
        #    pass
#             if option.get_attribute('selected') != None:
#                 print "Default Selection: ", option.get_attribute('selected'), option.text
#             
#             if option.is_selected():
#                 print "option.is_selected():", option.text
            
            #if li.text == value:
            #    li.click()
    
    
    @classmethod
    def Select(cls, value):
        log.step_normal("Element [%s]: Do Select [%s]." % (cls.__name__, value))
        
        cls.__wait(cls.by, cls.value)
        element = environment.BROWSER.find_element(cls.by, cls.value)
        
        options = element.find_elements_by_tag_name('option')
        
        for option in options:
#             if option.get_attribute('selected') != None:
#                 print "Default Selection: ", option.get_attribute('selected'), option.text
#             
#             if option.is_selected():
#                 print "option.is_selected():", option.text
            
            if option.text == value:
                option.click()
    
    @classmethod
    def __wait(cls, test_by, test_value):
        
        t = 0
        while t < 60:
            t = t + 1
            
            elements = environment.BROWSER.find_elements(test_by, test_value)
            if len(elements) == 0:
                time.sleep(3)
                log.step_normal("Element [%s]: Wait 3 Seconds." % cls.__name__)
            else:
                break
        
        if len(elements) > 1:
            log.step_fail("Element [%s]: Element NOT Unique! There are [%s] Elements!" % (cls.__name__, len(elements)))
        

    
    @classmethod
    def __wait_for_exist(cls, test_by, test_value):
        
        t = 0
        while t < 20:
            t = t + 1
            
            elements = environment.BROWSER.find_elements(test_by, test_value)
            if len(elements) == 0:
                time.sleep(3)
            else:
                log.step_normal("Element [%s]: Found [%s] Element. Tried [%s] Times." % (cls.__name__, len(elements), t))
                break









