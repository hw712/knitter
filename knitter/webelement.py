import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException
from selenium.common.exceptions import ElementClickInterceptedException

from knitter.configure import Browser
from knitter import logger


class CompatibleMethod(object):
    """If the first argument(self. is a class, set/use properties of the class. If the
    first argument is a instance, set/use properties of the instance.

    This is an extention version for "@classmethod", used for multi-thread issues
    of the framework.

    EXAMPLE

        class A:
            a = 0

            @CompatibleMethod
            def test(self, aaa):
                self.a = aaa

            @CompatibleMethod
            def get(self):
                print "get ", self.a


    """
    def __init__(self, method):
        self._method = method

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)

        # this is the different part with "classmethod"
        if isinstance(obj, klass):
            klass = obj
            klass.__name__ = klass.__class__.__name__

        def newfunc(*args, **kws):
            return self._method(klass, *args, **kws)

        return newfunc


class WebBrowser:

    @CompatibleMethod
    def Wait(self, seconds):
        logger.step_normal("Element [%s]: Wait for [%s] seconds." % (self.__name__, seconds))
        time.sleep(seconds)

    @CompatibleMethod
    def ScrollTo(self, x, y):
        logger.step_normal("Element [%s]: Scroll To [%s, %s]" % (self.__name__, x, y))
        Browser.RunningBrowser.execute_script("window.scrollTo(%s, %s);" % (x, y))

    @CompatibleMethod
    def Refresh(self, times=4):
        logger.step_normal("Element [%s]: Browser Refresh" % (self.__name__,))

        for i in range(times):
            action = webdriver.ActionChains(Browser.RunningBrowser)
            action.key_down(Keys.CONTROL).send_keys(Keys.F5).key_up(Keys.CONTROL).perform()
            time.sleep(5)

    @CompatibleMethod
    def DeleteAllCookies(self):
        logger.step_normal("Element [%s]: Browser Delete All Cookies" % (self.__name__,))
        Browser.RunningBrowser.delete_all_cookies()

        time.sleep(3)

    @CompatibleMethod
    def NavigateTo(self, url):
        logger.step_normal("Element [%s]: Navigate To [%s]" % (self.__name__, url))
        Browser.RunningBrowser.get(url)

        time.sleep(3)

    @CompatibleMethod
    def IESkipCertError(self):
        logger.step_normal("IE Skip SSL Cert Error.")
        Browser.RunningBrowser.get("javascript:document.getElementById('overridelink').click();")

    @CompatibleMethod
    def AlertAccept(self):
        logger.step_normal("AlertAccept()")

        time.sleep(2)
        try:
            logger.step_normal("switch_to_alert()")
            alert = Browser.RunningBrowser.switch_to_alert()
            alert.accept()
        except NoAlertPresentException:
            logger.step_normal("Alert Not Found. ")

        try:
            logger.step_normal("switch_to_default_content()")
            Browser.RunningBrowser.switch_to_default_content()
        except:
            pass

    @CompatibleMethod
    def AlertDismiss(self):
        logger.step_normal("AlertDismiss()")

        time.sleep(2)
        try:
            logger.step_normal("switch_to_alert()")
            alert = Browser.RunningBrowser.switch_to_alert()
            alert.dismiss()
        except NoAlertPresentException:
            logger.step_normal("Alert Not Found.")

        try:
            logger.step_normal("switch_to_default_content()")
            Browser.RunningBrowser.switch_to_default_content()
        except Exception as e:
            logger.step_normal(e)
            pass

    @CompatibleMethod
    def AlertSendKeys(self, value):
        logger.step_normal("AlertSendKeys [%s]" % value)
        try:
            Browser.RunningBrowser.switch_to.alert.send_keys(value)
            Browser.RunningBrowser.switch_to.default_content()
        except Exception as e:
            logger.step_normal(e)
            logger.step_warning(str(sys.exc_info()))

    @CompatibleMethod
    def AlertTextHave(self, txt_value):
        logger.step_normal("AlertTextHave [%s]" % txt_value)
        alert_text = Browser.RunningBrowser.switch_to_alert().text()

        if txt_value in alert_text:
            logger.step_pass("pass")
        else:
            logger.step_fail("fail")

        Browser.RunningBrowser.switch_to_default_content()

    @CompatibleMethod
    def SwitchToNewPopWindow(self):
        logger.step_normal("SwitchToNewPopWindow()")

        t = 0
        while t < 10:
            t = t + 1
            time.sleep(3)

            if len(Browser.RunningBrowser.window_handles) < 2:
                logger.step_normal("Pop Window Not Found. Wait 3 Seconds then Try Again!")
            else:
                break

        Browser.RunningBrowser.switch_to.window(Browser.RunningBrowser.window_handles[-1])

        logger.step_normal("Switch To The New Window of : %s" % str(Browser.RunningBrowser.window_handles))

    @CompatibleMethod
    def SwitchToDefaultWindow(self):
        logger.step_normal("SwitchToDefaultWindow()")

        logger.step_normal("Switch To The Default Window of: %s" % str(Browser.RunningBrowser.window_handles))

        try:
            Browser.RunningBrowser.switch_to.window(Browser.RunningBrowser.window_handles[0])
        except Exception as e:
            logger.step_normal(e)
            logger.step_warning("Browser.RunningBrowser.switch_to.window(Browser.RunningBrowser.window_handles[0])")

    @CompatibleMethod
    def SwitchToFrame(self, frame):
        logger.step_normal("SwitchToFrame()")

        Browser.RunningBrowser.switch_to.frame(frame)

    @CompatibleMethod
    def SwitchToDefaultContent(self):
        logger.step_normal("SwitchToDefaultContent()")

        try:
            Browser.RunningBrowser.switch_to.default_content()
        except Exception as e:
            logger.step_normal(e)
            logger.step_warning("Browser.RunningBrowser.switch_to.default_content()")


class WebElement:
    (by, value) = (None, None)
    index = 0

    @CompatibleMethod
    def __init__(self, by=None, value=None):
        self.by = by
        self.value = value

    @CompatibleMethod
    def ScrollIntoView(self):
        logger.step_normal("Element [%s]: ScrollToView()" % self.__name__)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        i = 0
        while not elements[self.index].is_displayed():
            WebBrowser.ScrollTo(0, i)
            i = i + 10

            if i == 1000:
                logger.step_normal("still not displayed. break out.")

    @CompatibleMethod
    def Set(self, value):
        logger.step_normal("Element [%s]: Set [%s]." % (self.__name__, value))

        value = str(value)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        if elements[self.index].tag_name == "select" or elements[self.index].tag_name == "ul":
            self.Select(value)

        else:
            elements[self.index].clear()
            elements[self.index].send_keys(value)

            """
            elements[self.index].clear()
            action = webdriver.ActionChains(Browser.RunningBrowser)
            action.send_keys_to_element(elements[self.index], value)
            action.perform()
            """

            self.__clearup()


    @CompatibleMethod
    def SelectByPartText(self, value):
        logger.step_normal("Element [%s]: Select [%s]." % (self.__name__, value))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        is_selected = False

        # select
        if elements[self.index].tag_name == "select":
            options = elements[self.index].find_elements_by_tag_name('option')

            for option in options:
                if value in option.text:
                    option.click()
                    is_selected = True
                    break

        # ul
        elif elements[self.index].tag_name == "ul":
            lis = elements[self.index].find_elements_by_tag_name('li')

            for li in lis:
                if value in li.text:
                    li.click()
                    is_selected = True
                    break

        # not support
        else:
            logger.step_fail("Element [%s]: Tag [%s] NOT support [Select] method" % (self.__name__, elements[self.index].tag_name))

        if is_selected is False:
            logger.step_fail("No item selected!")

        self.__clearup()

    @CompatibleMethod
    def Select(self, value):
        logger.step_normal("Element [%s]: Select [%s]." % (self.__name__, value))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        is_selected = False

        # select
        if elements[self.index].tag_name == "select":
            options = elements[self.index].find_elements_by_tag_name('option')

            for option in options:
                logger.step_normal("Element [%s]: option [%s]" % (self.__name__, option.text))

                if option.text == value:
                    option.click()
                    is_selected = True
                    break

        # ul
        elif elements[self.index].tag_name == "ul":
            lis = elements[self.index].find_elements_by_tag_name('li')

            for li in lis:
                logger.step_normal("Element [%s]: li [%s]" % (self.__name__, li.text))

                if li.text == value:
                    li.click()
                    is_selected = True
                    break

        # not support
        else:
            logger.step_fail("Element [%s]: Tag [%s] NOT support [Select] method" % (self.__name__, elements[self.index].tag_name))

        if is_selected is False:
            logger.step_fail("No item selected!")

        self.__clearup()


    @CompatibleMethod
    def SelectByOrder(self, order):
        logger.step_normal("Element [%s]: Select by Order [%s]" % (self.__name__, order))

        order = int(order)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        # ul
        if elements[self.index].tag_name == "ul":
            lis = elements[self.index].find_elements_by_tag_name('li')

            if order > 0:

                # wait and try more times if NO item found.
                t = 0
                while len(lis) == 0:
                    lis = elements[self.index].find_elements_by_tag_name('li')
                    time.sleep(3)
                    t = t + 1
                    logger.step_normal("Element [%s]: Wait 3 Seconds for [li]" % self.__name__)

                    if t == 20 and len(lis) == 0:
                        logger.step_fail("Element [%s]: List Count = [%s]." % (self.__name__, len(lis)))
                        return

                logger.step_normal("Element [%s]: List Count = [%s]." % (self.__name__, len(lis)))

                if order > len(lis):
                    logger.step_fail("Element [%s]: Not so many lists. [%s]" % (self.__name__, len(lis)))
                else:
                    logger.step_normal("Element [%s]: Do Click [%s]" % (self.__name__, order))
                    action = webdriver.ActionChains(Browser.RunningBrowser)

                    # Added to avoid error: "Element is no longer attached to the DOM"
                    elements = Browser.RunningBrowser.find_elements(self.by, self.value)
                    lis = elements[self.index].find_elements_by_tag_name('li')

                    action.click(lis[order-1])
                    action.perform()

            else:
                logger.step_fail("Order = [%s], Value Error." % order)


        # select
        # if elements[self.index].tag_name == "select":
        else:
            options = elements[self.index].find_elements_by_tag_name('option')

            if order > 0:

                # wait and try more times if NO item found.
                t = 0
                while len(options) == 0:
                    options = elements[self.index].find_elements_by_tag_name('option')
                    time.sleep(3)
                    t = t + 1
                    logger.step_normal("Element [%s]: Wait 3 Seconds for [option]" % self.__name__)

                    if t == 20 and len(lis) == 0:
                        logger.step_fail("Element [%s]: options Count = [%s]." % (self.__name__, len(options)))
                        return

                logger.step_normal("Element [%s]: options Count = [%s]." % (self.__name__, len(options)))

                if order > len(options):
                    logger.step_fail("Element [%s]: Not so many options. [%s]" % (self.__name__, len(options)))
                else:
                    logger.step_normal("Element [%s]: Do Click [%s]" % (self.__name__, order))
                    action = webdriver.ActionChains(Browser.RunningBrowser)
                    action.click(options[order-1])
                    action.perform()
            else:
                logger.step_fail("Order = [%s], Value Error." % order)

        self.__clearup()


    @CompatibleMethod
    def MouseOver(self):
        logger.step_normal("Element [%s]: MouseOver()" % self.__name__)

        time.sleep(1)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        action = webdriver.ActionChains(Browser.RunningBrowser)
        action.move_to_element(elements[self.index])
        action.perform()

        self.__clearup()

        time.sleep(1)


    @CompatibleMethod
    def Click(self):
        logger.step_normal("Element [%s]: Click()" % self.__name__)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        try:
            elements[self.index].click()
        except ElementClickInterceptedException:
            self.Wait(3)
            action = webdriver.ActionChains(Browser.RunningBrowser)
            action.click(elements[self.index])
            action.perform()

        self.__clearup()

    @CompatibleMethod
    def DoubleClick(self):
        logger.step_normal("Element [%s]: DoubleClick()" % self.__name__)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        action = webdriver.ActionChains(Browser.RunningBrowser)
        action.double_click(elements[self.index])
        action.perform()

        self.__clearup()

    @CompatibleMethod
    def ClickAndHold(self):
        logger.step_normal("Element [%s]: ClickAndHold()" % self.__name__)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        action = webdriver.ActionChains(Browser.RunningBrowser)
        action.click_and_hold(elements[self.index])
        action.perform()

        self.__clearup()

    @CompatibleMethod
    def DragAndDropByOffset(self, xoffset, yoffset):
        """
        Holds down the left mouse button on the source element,
        then moves to the target offset and releases the mouse button.
        """
        logger.step_normal("Element [%s]: drag_and_drop_by_offset()" % self.__name__)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        action = webdriver.ActionChains(Browser.RunningBrowser)
        action.drag_and_drop_by_offset(elements[self.index],xoffset, yoffset)
        action.perform()

        self.__clearup()

    @CompatibleMethod
    def ReleaseClick(self):
        logger.step_normal("Element [%s]: ReleaseClick()" % self.__name__)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        action = webdriver.ActionChains(Browser.RunningBrowser)
        action.release(elements[self.index])
        action.perform()

        self.__clearup()

    @CompatibleMethod
    def TypeInWithoutClear(self, value):
        """Input value without clear existing values"""

        logger.step_normal("Element [%s]: TypeInWithoutClear [%s]." % self.__name__, value)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        elements[self.index].send_keys(value)

        self.__clearup()

    @CompatibleMethod
    def SendEnter(self):
        logger.step_normal("Element [%s]: SendEnter()" % self.__name__, )

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        action = webdriver.ActionChains(Browser.RunningBrowser)
        action.send_keys_to_element(elements[self.index], Keys.ENTER)
        action.perform()

        self.__clearup()

    @CompatibleMethod
    def GetRepetition(self):
        logger.step_normal("Element [%s]: GetRepetition()." % self.__name__)

        self.__wait_for_appearing()

        elements = Browser.RunningBrowser.find_elements(self.by, self.value)
        logger.step_normal("Element [%s]: repetition = [%s]" % (self.__name__, len(elements)))

        self.__clearup()
        return len(elements)


    @CompatibleMethod
    def GetRepetitionWithoutWaiting(self):
        """ Get real time obj counts, without waiting."""
        logger.step_normal("Element [%s]: GetRepetitionWithoutWaiting()." % self.__name__)

        elements = Browser.RunningBrowser.find_elements(self.by, self.value)
        logger.step_normal("Element [%s]: repetition = [%s]" % (self.__name__, len(elements)))

        self.__clearup()
        return len(elements)

    @CompatibleMethod
    def GetInnerHTML(self):
        logger.step_normal("Element [%s]: GetInnerHTML()" % self.__name__)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        logger.step_normal("Element [%s]: InnerHTML = [%s]" % (self.__name__, elements[self.index].get_attribute('innerHTML')))

        self.__clearup()
        return elements[self.index].get_attribute('innerHTML')

    @CompatibleMethod
    def GetAttribute(self, attr):
        logger.step_normal("Element [%s]: GetAttribute [%s]." % (self.__name__, attr))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        attr_value = elements[self.index].get_attribute(attr)
        logger.step_normal("Element [%s]: Attribute Value = [%s]." % (self.__name__, attr_value))

        self.__clearup()
        return attr_value

    @CompatibleMethod
    def GetParentElement(self):
        logger.step_normal("Element [%s]: GetParentElement()" % self.__name__)

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        return elements[self.index].parent()

    @CompatibleMethod
    def GetText(self):
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)
        logger.step_normal("Element [%s]: Get text of the element = %s." % (self.__name__,
                                                                                          elements[self.index].text))
        return elements[self.index].text

    @CompatibleMethod
    def FetchSubElementOfXPath(self, layer):
        return WebElement(self.by, "/".join(self.value.split("/")[:layer+2]))


    @CompatibleMethod
    def WaitForAttribute(self, name, value, comparator="equal"):
        '''

        Example:
            NewClaim.Dates.ReminderDate.WaitForAttribute('ng-model', 'hello', comparator='equal')
            NewClaim.Dates.ReminderDate.WaitForAttribute('ng-model', 'hello', comparator='contain')
            NewClaim.Dates.ReminderDate.WaitForAttribute('ng-model', 'hello', comparator='not contain')
            NewClaim.Dates.ReminderDate.WaitForAttribute('ng-model', 'hello', comparator='in')
            NewClaim.Dates.ReminderDate.WaitForAttribute('ng-model', 'hello', comparator='not equal')

        Description for "method":
            equal  => real value is 'hello'
            has    => real value contains 'hello', e.g. 'hello world'.
            in     => real value in 'hello', e.g. 'he'
            differ => real value not equal to 'hello', e.g. 'hehe'

        '''
        logger.step_normal("Element [%s]: WaitForAttribute [%s] <%s> [%s]." % (self.__name__, name, method, value))

        i = 0
        while True:
            self.__wait()
            elements = Browser.RunningBrowser.find_elements(self.by, self.value)

            realvalue = elements[self.index].get_attribute(name)

            if method.lower() == 'equal':
                if value.lower() == realvalue.lower():
                    logger.step_normal("Yes! real value=[%s]" % realvalue)
                    break
                else:
                    logger.step_normal("No! real value=[%s]" % realvalue)

            elif method.lower() == 'contain':
                if value.lower() in realvalue.lower():
                    logger.step_normal("Yes! real value=[%s]" % realvalue[:150])
                    break
                else:
                    logger.step_normal("No! real value=[%s]" % realvalue[:150])

            elif method.lower() == 'not contain':
                if value.lower() in realvalue.lower():
                    logger.step_normal("Yes! real value=[%s]" % realvalue[:150])
                else:
                    logger.step_normal("No! real value=[%s]" % realvalue[:150])
                    break

            elif method.lower() == 'in':
                if realvalue.lower() in value.lower():
                    logger.step_normal("Yes! real value=[%s]" % realvalue[:150])
                    break
                else:
                    logger.step_normal("No! real value=[%s]" % realvalue[:150])

            elif method.lower() == 'not equal':
                if value.lower() == realvalue.lower():
                    logger.step_normal("No! real value=[%s]" % realvalue)
                else:
                    logger.step_normal("Yes! real value=[%s]" % realvalue)
                    break

            else:
                logger.step_fail("code error.")


            i = i + 1
            if i > 90:
                logger.step_fail("Not Found Expected Value! real value=[%s]" % realvalue)
                break

            time.sleep(1)


        self.__clearup()


    #===========================================================================
    # @compatiblemethod
    # def WaitForAttributeContains(self, attr_name, attr_value):
    #     logger.step_normal("Element [%s]: WaitForAttribute [%s] = [%s]." % (self.__name__, attr_name, attr_value))
    #
    #     i = 0
    #     while True:
    #         self.__wait()
    #         elements = Browser.RunningBrowser.find_elements(self.by, self.value)
    #
    #         real_value = elements[self.index].get_attribute(attr_name)
    #
    #
    #         if not isinstance(real_value, unicode):
    #             print "not !!"
    #             real_value = real_value.encode('utf-8')
    #
    #
    #         if attr_value.upper() in real_value.upper():
    #             logger.step_normal("Yes! real_value=[%s]" % real_value)
    #             break
    #         else:
    #             logger.step_normal("No! real_value=[%s]" % real_value)
    #
    #         i = i + 1
    #         if i > 60:
    #             logger.step_fail("Not Found Expected Value! real_value=[%s]" % real_value)
    #             break
    #
    #         time.sleep(3)
    #
    #
    #     self.__clearup()
    #===========================================================================


    @CompatibleMethod
    def WaitForAppearing(self):
        logger.step_normal("Element [%s]: WaitForAppearing..." % (self.__name__))

        self.__wait_for_appearing()
        self.__clearup()


    @CompatibleMethod
    def WaitForDisappearing(self):
        logger.step_normal("Element [%s]: WaitForDisappearing..." % (self.__name__))

        self.__wait_for_disappearing()
        self.__clearup()


    @CompatibleMethod
    def WaitForVisible(self):
        logger.step_normal("Element [%s]: WaitForVisible..." % (self.__name__))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        t = 0
        while(t < 90):
            if elements[self.index].is_displayed():
                logger.step_normal("Element [%s]: IS visible now." % (self.__name__))
                break
            else:
                logger.step_normal("Element [%s]: Still NOT visible, wait 1 second." % (self.__name__))
                time.sleep(1)

        self.__clearup()


    @CompatibleMethod
    def WaitForEnabled(self):
        logger.step_normal("Element [%s]: WaitForEnabled..." % (self.__name__))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        t = 0
        while(t < 90):
            if elements[self.index].is_enabled():
                logger.step_normal("Element [%s]: is enabled now." % (self.__name__))
                break
            else:
                logger.step_normal("Element [%s]: still NOT enabled, wait 1 second." % (self.__name__))
                time.sleep(1)

            t = t + 1

        self.__clearup()


    @CompatibleMethod
    def IsEnabled(self):
        logger.step_normal("Element [%s]: Is Enabled?" % (self.__name__))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        if elements[self.index].is_enabled():
            logger.step_normal("Yes!")
            self.__clearup()
            return True
        else:
            logger.step_normal("No!")
            self.__clearup()
            return False


    @CompatibleMethod
    def IsExist(self):
        logger.step_normal("Element [%s]: IsExist?" % (self.__name__))

        time.sleep(2)

        elements = Browser.RunningBrowser.find_elements(self.by, self.value)
        logger.step_normal("Element [%s]: IsExist? Count = [%s]" % (self.__name__, len(elements)))

        self.__clearup()

        if len(elements) > 0:
            return True
        else:
            return False


    @CompatibleMethod
    def IsVisible(self):
        logger.step_normal("Element [%s]: IsVisible?" % (self.__name__))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        if elements[self.index].is_displayed():
            self.__clearup()
            return True
        else:
            self.__clearup()
            return False


    @CompatibleMethod
    def IsAttribute(self, name, value, comparator="contain"):
        logger.step_normal("Element [%s]: IsAttribute [%s] <%s> [%s]." % (self.__name__, name, method, value))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)
        realvalue = elements[self.index].get_attribute(name)

        if method.lower() == 'equal':
            if value == realvalue:
                self.__clearup()
                return True
            else:
                self.__clearup()
                return False

        elif method.lower() == 'not equal':
            if not value == realvalue:
                self.__clearup()
                return True
            else:
                self.__clearup()
                return False

        elif method.lower() == 'contain':
            if value in realvalue:
                self.__clearup()
                return True
            else:
                self.__clearup()
                return False

        elif method.lower() == 'not contain':
            if not value in realvalue:
                self.__clearup()
                return True
            else:
                self.__clearup()
                return False

        elif method.lower() == 'in':
            if realvalue in value:
                self.__clearup()
                return True
            else:
                self.__clearup()
                return False


        else:
            logger.step_fail("code error.")

        self.__clearup()



    @CompatibleMethod
    def VerifyExistence(self, trueORfalse):
        logger.step_normal("Element [%s]: Verify Existence = [%s]." % (self.__name__, trueORfalse))

        if trueORfalse == True:
            self.__wait_for_appearing()
        else:
            self.__wait_for_disappearing()

        elements = Browser.RunningBrowser.find_elements(self.by, self.value)
        logger.step_normal("Element [%s]: Count = [%s]" % (self.__name__, len(elements)))


        self.__clearup()
        if len(elements) > 0:
            if trueORfalse == True:
                logger.step_pass("Exist!")
            else:
                logger.step_fail("Exist!")
        else:
            if trueORfalse == False:
                logger.step_pass("Not Exist!")
            else:
                logger.step_fail("Not Exist!")


    @CompatibleMethod
    def VerifyVisible(self, trueORfalse):
        logger.step_normal("Element [%s]: Verify Visible = [%s]." % (self.__name__, trueORfalse))

        self.__wait()

        elements = Browser.RunningBrowser.find_elements(self.by, self.value)
        logger.step_normal("Element [%s]: Count = [%s]" % (self.__name__, len(elements)))

        if elements[self.index].is_displayed():
            if trueORfalse == True:
                logger.step_pass("Visible!")
            else:
                logger.step_fail("Visible!")
        else:
            if trueORfalse == False:
                logger.step_pass("Not Visible!")
            else:
                logger.step_fail("Not Visible!")

        self.__clearup()


    @CompatibleMethod
    def VerifyEnabled(self, trueOrfalse):
        logger.step_normal("Element [%s]: Verify Enabled = [%s]" % (self.__name__, trueOrfalse))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        is_disabled = elements[self.index].get_attribute("disabled")
        logger.step_normal("Element [%s]: attribute 'is_disabled' = [%s]" % (self.__name__, is_disabled))

        if is_disabled == "true":
            if trueOrfalse == False:
                logger.step_pass("Pass...")
            else:
                logger.step_fail("Fail...")

        elif elements[self.index].is_enabled():
            if trueOrfalse == True:
                logger.step_pass("Pass")
            else:
                logger.step_fail("Fail")

        else:
            logger.step_fail("Not verified.")


        self.__clearup()


    @CompatibleMethod
    def VerifyInnerHTMLContains(self, contain_content):
        logger.step_normal("Element [%s]: VerifyInnerHTMLContains [%s]." % (self.__name__, str(contain_content)))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)
        inner_html = elements[self.index].get_attribute('innerHTML')

        if isinstance(contain_content, list):
            for content in contain_content:
                if content in inner_html:
                    logger.step_pass("Real inner_hmtl=[%s]" % inner_html)
                else:
                    logger.step_fail("Real inner_hmtl=[%s]" % inner_html)

        else:
            if contain_content in inner_html:
                logger.step_pass("Real inner_hmtl=[%s]" % inner_html)
            else:
                logger.step_fail("Real inner_hmtl=[%s]" % inner_html)

        self.__clearup()


    @CompatibleMethod
    def VerifyAttribute(self, name, value, comparator='equal'):
        '''
        Example:
            NewClaim.Dates.ReminderDate.VerifyAttribute('ng-model', 'hello', comparator='equal')
            NewClaim.Dates.ReminderDate.VerifyAttribute('ng-model', 'hello', comparator='contain')
            NewClaim.Dates.ReminderDate.VerifyAttribute('ng-model', 'hello', comparator='in')
            NewClaim.Dates.ReminderDate.VerifyAttribute('ng-model', 'hello', comparator='not equal')

        Description for "method":
            equal  => real value is 'hello'
            has    => real value contains 'hello', e.g. 'hello world'.
            in     => real value in 'hello', e.g. 'he'
            differ => real value not equal to 'hello', e.g. 'hehe'

        '''
        logger.step_normal("Element [%s]: VerifyAttribute [%s] <%s> [%s]." % (self.__name__, name, method, value))

        self.__wait()
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)
        realvalue = elements[self.index].get_attribute(name)

        if method.lower() == 'equal':
            if value == realvalue:
                logger.step_pass("real value=[%s]" % realvalue)
            else:
                logger.step_fail("real value=[%s]" % realvalue)

        elif method.lower() == 'not equal':
            if not value == realvalue:
                logger.step_pass("real value=[%s]" % realvalue)
            else:
                logger.step_fail("real value=[%s]" % realvalue)

        elif method.lower() == 'contain':
            if value in realvalue:
                logger.step_pass("real value=[%s]" % realvalue)
            else:
                logger.step_fail("real value=[%s]" % realvalue)

        elif method.lower() == 'not contain':
            if not value in realvalue:
                logger.step_pass("real value=[%s]" % realvalue)
            else:
                logger.step_fail("real value=[%s]" % realvalue)

        elif method.lower() == 'in':
            if realvalue in value:
                logger.step_pass("real value=[%s]" % realvalue)
            else:
                logger.step_fail("real value=[%s]" % realvalue)

        else:
            logger.step_fail("code error.")

        self.__clearup()


    @CompatibleMethod
    def __wait_for_enabled(self):
        elements = Browser.RunningBrowser.find_elements(self.by, self.value)

        if elements[self.index].is_enabled():
            return
        else:
            t = 0
            while t < 90:
                if elements[self.index].is_enabled():
                    break

                logger.step_normal("Element [%s]: __wait_for_enabled for 1 second, By [%s :: %s :: %s]" % (self.__name__, self.by, self.value, self.index))
                time.sleep(0.5)


    @CompatibleMethod
    def __wait(self):
        t = 0
        while t < 300:
            t = t + 1

            try:
                elements = Browser.RunningBrowser.find_elements(self.by, self.value)
            except NoSuchElementException:
                logger.step_normal("Element [%s]: NoSuchElementException." % self.__name__)
                elements = []
            except UnexpectedAlertPresentException:
                logger.step_warning("Element [%s]: UnexpectedAlertPresentException." % self.__name__)


            if len(elements) == 0:
                time.sleep(0.5)
                logger.step_normal("Element [%s]: Wait 0.5 second, By [%s :: %s :: %s]" % (self.__name__, self.by, self.value, self.index))
            else:
                if len(elements) > 1:
                    logger.step_normal("Element [%s]: There are [%s] Elements!" % (self.__name__, len(elements)))

                break


        if len(elements) < self.index + 1:
            logger.step_fail("Element [%s]: Element Index Issue! There are [%s] Elements! Index=[%s]" % (self.__name__, len(elements), self.index))




    @CompatibleMethod
    def __wait_for_disappearing(self):

        t = 0
        while t < 120:
            t = t + 1

            try:
                elements = Browser.RunningBrowser.find_elements(self.by, self.value)
            except NoSuchElementException:
                logger.step_normal("Element [%s]: NoSuchElementException." % self.__name__)
                elements = []
                continue
            except UnexpectedAlertPresentException:
                logger.step_warning("Element [%s]: UnexpectedAlertPresentException." % self.__name__)

            if len(elements) == 0:
                return True
            else:
                time.sleep(0.5)
                logger.step_normal("Element [%s]: WairForDisappearing... Found [%s] Element. Tried [%s] Times." % (self.__name__, len(elements), t))


        return False


    @CompatibleMethod
    def __wait_for_appearing(self):

        t = 0
        while t < 120:
            t = t + 1

            try:
                elements = Browser.RunningBrowser.find_elements(self.by, self.value)
            except NoSuchElementException:
                logger.step_normal("Element [%s]: NoSuchElementException." % self.__name__)
                elements = []
                continue
            except UnexpectedAlertPresentException:
                logger.step_warning("Element [%s]: UnexpectedAlertPresentException." % self.__name__)


            if len(elements) == 0:
                time.sleep(0.5)
                logger.step_normal("Element [%s]: WaitForAppearing... Wait 1 second, By [%s]" % (self.__name__, self.value))
            else:
                logger.step_normal("Element [%s]: Found [%s] Element. Tried [%s] Times." % (self.__name__, len(elements), t))
                break



    @CompatibleMethod
    def __clearup(self):
        if self.index != 0:
            logger.step_normal("Element [%s]: The Operation Element Index = [%s]." % (self.__name__, self.index))

#         self.index = 0





