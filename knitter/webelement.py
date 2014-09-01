# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
import env, log


class WebBrowser:
    
    @classmethod
    def ScrollTo(cls, x, y):
        log.step_normal(u"Element [%s]: Scroll To [%s, %s]" % (cls.__name__, x, y))
        env.BROWSER.execute_script("window.scrollTo(%s, %s);" % (x, y))
        
        time.sleep(3)
    
    @classmethod
    def Refresh(cls):
        log.step_normal(u"Element [%s]: Browser Refresh" % (cls.__name__,))
        env.BROWSER.refresh()
        
        time.sleep(3)
    
    @classmethod
    def NavigateTo(cls, url):
        log.step_normal(u"Element [%s]: Navigate To [%s]" % (cls.__name__, url))
        env.BROWSER.get(url)
        time.sleep(5)
    
    
    @classmethod
    def IESkipCertError(cls):
        log.step_normal("IE Skip SSL Cert Error.")
        env.BROWSER.get("javascript:document.getElementById('overridelink').click();")
    
    
    @classmethod
    def AlertAccept(cls):
        log.step_normal("AlertAccept.")
        env.BROWSER.switch_to_alert().accept()
        
        env.BROWSER.switch_to_default_content()
    
    
    @classmethod
    def AlertDismiss(cls):
        log.step_normal("AlertDismiss.")
        env.BROWSER.switch_to_alert().dismiss()
        
        env.BROWSER.switch_to_default_content()
    
    
    @classmethod
    def AlertSendKeys(cls, value):
        log.step_normal("AlertSendKeys [%s]" % value)
        env.BROWSER.switch_to_alert().send_keys(value)
        
        env.BROWSER.switch_to_default_content()
    
    
    @classmethod
    def AlertTextHave(cls, txt_value):
        log.step_normal("AlertTextHave [%s]" % txt_value)
        alert_text = env.BROWSER.switch_to_alert().text()
        
        if txt_value in alert_text:
            log.step_pass("pass")
        else:
            log.step_fail("fail")
        env.BROWSER.switch_to_default_content()






class WebElement:
    (by, value) = (None, None)
    index       = 0
    
    @classmethod
    def Set(cls, value):
        log.step_normal(u"Element [%s]: Set Value [%s]." % (cls.__name__, value))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        
        if elements[cls.index].tag_name == "select" or elements[cls.index].tag_name == "ul":
            cls.Select(value)
        
        else:
            elements[cls.index].clear()
            action = webdriver.ActionChains(env.BROWSER)
            action.send_keys_to_element(elements[cls.index], value)
            action.perform()
            
            cls._clearup()
    
    
    @classmethod
    def VerifyEnabled(cls, trueOrfalse):
        log.step_normal(u"Element [%s]: Verify Enabled = [%s]" % (cls.__name__, trueOrfalse))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        if elements[cls.index].is_enabled():
            if trueOrfalse == True:
                log.step_pass("Pass")
            else:
                log.step_fail("Fail")
        else:
            if trueOrfalse == True:
                log.step_fail("Fail")
            else:
                log.step_pass("Pass")
        
        cls._clearup()
    
    
    @classmethod
    def IsEnabled(cls):
        log.step_normal(u"Element [%s]: Is Enabled?" % (cls.__name__))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        if elements[cls.index].is_enabled():
            log.step_normal(u"Yes!")
            cls._clearup()
            return True
        else:
            log.step_normal(u"No!")
            cls._clearup()
            return False
    
    
    @classmethod
    def TypeIn(cls, value):
        '''
        input value without clear existed values
        '''
        
        log.step_normal(u"Element [%s]: TypeIn Value [%s]." % (cls.__name__, value))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(env.BROWSER)
        action.send_keys_to_element(elements[cls.index], value)
        action.perform()
        
        cls._clearup()
    
    
    @classmethod
    def GetFocus(cls):
        log.step_normal(u"Element [%s]: GetFocus()" % (cls.__name__, ))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        elements[cls.index].send_keys(Keys.NULL)
        
        action = webdriver.ActionChains(env.BROWSER)
        action.send_keys_to_element(elements[cls.index], Keys.NULL)
        action.perform()
        
        cls._clearup()
    
    @classmethod
    def SendEnter(cls):
        log.step_normal(u"Element [%s]: SendEnter()" % (cls.__name__, ))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(env.BROWSER)
        action.send_keys_to_element(elements[cls.index], Keys.ENTER)
        action.perform()
        
        cls._clearup()
    
    
    
    
    @classmethod
    def GetInnerHTML(cls):
        log.step_normal(u"Element [%s]: GetInnerHTML." % (cls.__name__, ))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        #log.step_normal(u"Element [%s]: InnerHTML = [%s]" % (cls.__name__, elements[cls.index].get_attribute('innerHTML')))
        
        cls._clearup()
        return elements[cls.index].get_attribute('innerHTML')
    
    
    @classmethod
    def GetAttribute(cls, attr):
        log.step_normal(u"Element [%s]: Get Attribute [%s]." % (cls.__name__, attr))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        attr_value = elements[cls.index].get_attribute(attr)
        log.step_normal(u"Element [%s]: Attribute Value = [%s]." % (cls.__name__, attr_value))
        
        cls._clearup()
        return attr_value
    
    
    @classmethod
    def AppearingWait(cls):
        log.step_normal("Element [%s]: AppearingWait." % (cls.__name__))
        
        cls._wait_for_appearing()
        cls._clearup()
    
    
    @classmethod
    def DisappearingWait(cls):
        log.step_normal("Element [%s]: DisappearingWait." % (cls.__name__))
        
        cls._wait_for_disappearing()
        cls._clearup()
    
    
    @classmethod
    def GetObjectsCount(cls):
        log.step_normal("Element [%s]: GetObjectsCount." % (cls.__name__))
        
        cls._wait_for_appearing()
        
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        log.step_normal("Element [%s]: GetObjectsCount = [%s]" % (cls.__name__, len(elements)))
        
        cls._clearup()
        return len(elements)
    
    
    @classmethod
    def IsExist(cls):
        log.step_normal("Element [%s]: IsExist?" % (cls.__name__))
        
        time.sleep(5)
        
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        log.step_normal("Element [%s]: IsExist? Count = [%s]" % (cls.__name__, len(elements)))
        
        cls._clearup()
        if len(elements) > 0:
            return True
        else:
            return False
    
    
    @classmethod
    def VerifyExistence(cls, trueORfalse):
        log.step_normal("Element [%s]: Verify Existence = [%s]." % (cls.__name__, trueORfalse))
        
        if trueORfalse == True:
            cls._wait_for_appearing()
        else:
            cls._wait_for_disappearing()
        
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        log.step_normal("Element [%s]: Count = [%s]" % (cls.__name__, len(elements)))
        
        
        cls._clearup()
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
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        inner_html = elements[cls.index].get_attribute('innerHTML')
        
        if contain_content in inner_html:
            log.step_pass("Real inner_hmtl=[%s]" % inner_html)
        else:
            log.step_fail("Real inner_hmtl=[%s]" % inner_html)
        
        cls._clearup()
    
    
    @classmethod
    def VerifyAttribute(cls, attr, contain_content):
        log.step_normal("Element [%s]: Verify Attribute [%s] == [%s]." % (cls.__name__, attr, contain_content))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        attr_value = elements[cls.index].get_attribute(attr)
        
        if contain_content == attr_value:
            log.step_pass("Real attr_value=[%s]" % attr_value)
        else:
            log.step_fail("Real attr_value=[%s]" % attr_value)
        
        cls._clearup()
    
    
    @classmethod
    def VerifyAttributeContains(cls, attr, contain_content):
        log.step_normal("Element [%s]: Verify [%s] Contains [%s]." % (cls.__name__, attr, contain_content))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        attr_value = elements[cls.index].get_attribute(attr)
        
        log.step_normal("Element [%s]: attr_value = [%s]." % (cls.__name__, attr_value))
        
        if contain_content in attr_value:
            log.step_pass("Real attr_value=[%s]" % attr_value)
        else:
            log.step_fail("Real attr_value=[%s]" % attr_value)
        
        cls._clearup()
    
    
    @classmethod
    def DoubleClick(cls):
        log.step_normal("Element [%s]: Do DoubleClick()" % (cls.__name__))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(env.BROWSER)
        action.double_click(elements[cls.index])
        action.perform()
        
        cls._clearup()
    
    
    @classmethod
    def Click(cls):
        log.step_normal("Element [%s]: Do Click()" % (cls.__name__))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(env.BROWSER)
        action.click(elements[cls.index])
        action.perform()
        
        cls._clearup()
    
    
    @classmethod
    def MouseOver(cls):
        log.step_normal("Element [%s]: Do MouseOver()" % (cls.__name__))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(env.BROWSER)
        action.move_to_element(elements[cls.index])
        action.perform()
        
        cls._clearup()
        
        time.sleep(1)
    
    
    @classmethod
    def ClickAndHold(cls):
        log.step_normal("Element [%s]: Do ClickAndHold()" % (cls.__name__))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(env.BROWSER)
        action.click_and_hold(elements[cls.index])
        action.perform()
        
        cls._clearup()
    
    
    @classmethod
    def ReleaseClick(cls):
        log.step_normal("Element [%s]: Do ReleaseClick()" % (cls.__name__))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        action = webdriver.ActionChains(env.BROWSER)
        action.release(elements[cls.index])
        action.perform()
        
        cls._clearup()
    
    
    @classmethod
    def SelectByOrder(cls, order):
        log.step_normal("Element [%s]: Do Select by Order [%s]" % (cls.__name__, order))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
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
                    log.step_normal("Element [%s]: Wait 3 Seconds for [li]" % cls.__name__)
                    
                    if t == 8 and len(lis) == 0:
                        log.step_fail("Element [%s]: List Count = [%s]." % (cls.__name__, len(lis)))
                        return
                
                
                log.step_normal("Element [%s]: List Count = [%s]." % (cls.__name__, len(lis)))
                
                if (order > len(lis)):
                    log.step_normal("Element [%s]: Not so many lists. [%s]" % (cls.__name__, len(lis)))
                else:
                    log.step_normal("Element [%s]: Do Click [%s]" % (cls.__name__, order))
                    action = webdriver.ActionChains(env.BROWSER)
                    action.click(lis[order-1])
                    action.perform()
            else:
                log.step_fail("Order = [%s], Value Error." % order)
                
                
        
        
        cls._clearup()
    
    
    @classmethod
    def Select(cls, value):
        log.step_normal("Element [%s]: Do Select [%s]." % (cls.__name__, value))
        
        cls._wait()
        elements = env.BROWSER.find_elements(cls.by, cls.value)
        
        
        #### select ################
        if elements[cls.index].tag_name == "select":
            options = elements[cls.index].find_elements_by_tag_name('option')
            
            for option in options:
                if option.text == value:
                    option.click()
                    break
        
        
        
        #### ul ################
        elif elements[cls.index].tag_name == "ul":
            lis = elements[cls.index].find_elements_by_tag_name('li')
            
            for li in lis:
                if li.text == value:
                    li.click()
                    break
        
        
        
        
        #### NOT Supported ################
        else:
            log.step_fail("Element [%s]: Tag Name [%s] Not Supported." % (cls.__name__, elements[cls.index].tag_name))
        
        cls._clearup()
    
    
    
    
    @classmethod
    def _wait(cls):
        t = 0
        while t < 60:
            t = t + 1
            
            try:
                elements = env.BROWSER.find_elements(cls.by, cls.value)
            except NoSuchElementException:
                log.step_normal("Element [%s]: NoSuchElementException." % cls.__name__)
                elements = []
            
            if len(elements) == 0:
                time.sleep(3)
                log.step_normal("Element [%s]: Wait 3 Seconds, By [%s]" % (cls.__name__, cls.value))
            else:
                break
        
        if len(elements) < cls.index + 1:
            log.step_fail("Element [%s]: Element Index Issue! There are [%s] Elements! Index=[%s]" % (cls.__name__, len(elements), cls.index))
    
    
    @classmethod
    def _wait_for_disappearing(cls):
        
        t = 0
        while t < 15:
            t = t + 1
            
            try:
                elements = env.BROWSER.find_elements(cls.by, cls.value)
            except NoSuchElementException:
                log.step_normal("Element [%s]: NoSuchElementException." % cls.__name__)
                elements = []
            
            if len(elements) == 0:
                return True
            else:
                time.sleep(3)
                log.step_normal("Element [%s]: WairForDisappearing... Found [%s] Element. Tried [%s] Times." % (cls.__name__, len(elements), t))
        
        return False
    
    
    @classmethod
    def _wait_for_appearing(cls):
        
        t = 0
        while t < 15:
            t = t + 1
            
            try:
                elements = env.BROWSER.find_elements(cls.by, cls.value)
            except NoSuchElementException:
                log.step_normal("Element [%s]: NoSuchElementException." % cls.__name__)
                elements = []
            
            if len(elements) == 0:
                time.sleep(3)
                log.step_normal("Element [%s]: WaitForAppearing... Wait 3 Seconds, By [%s]" % (cls.__name__, cls.value))
            else:
                log.step_normal("Element [%s]: Found [%s] Element. Tried [%s] Times." % (cls.__name__, len(elements), t))
                break
    
    
    @classmethod
    def _clearup(cls):
        if cls.index != 0:
            log.step_normal("Element [%s]: Last Element Index = [%s]." % (cls.__name__, cls.index))
        
        cls.index = 0







