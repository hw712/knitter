Tutorial
=======================================================================

1. Installation
-----------------------------------------------------------------------

    pip install knitter


2. Preconditions
-----------------------------------------------------------------------

+ Python 2.7

+ depends on "selenium", "xlrd", "xlwt" packages, which will be installed while installing knitter.

+ drivers

    - [Chrome driver](http://chromedriver.storage.googleapis.com/index.html)

    - [Ie driver](http://selenium-release.storage.googleapis.com/index.html)

    - You can also find both driver files [here](https://github.com/hww712/Knitter/tree/master/examples/DemoProject/drivers).



3. Test demo project
-----------------------------------------------------------------------

+ [demo project](https://github.com/hww712/Knitter/tree/master/examples/DemoProject)

+ [demo project test page](http://sleepycat.org/static/knitter/KnitterDemo.html)


#### [Step 1] Create project folder structure.


    DemoProject/
               data/
                    ...               # excel data files, such as "TestData.xlsx"
               page/
                     __init__.py
                     DemoPage.py      # elements of test page
                     ...
               testcase/
                     __init__.py
                     demo_module.py   # test cases
                     ...
               conf.ini
               runner.py


#### [Step 2] Add page/DemoPage.py


    # -*- coding: utf-8 -*-
    # All element class must inherit from "WebElement".

    from knitter.webelement import WebElement
    from selenium.webdriver.common.by import By
    
    class Name:
        class Title(WebElement):
            (by, value) = (By.ID, 'title')
        
        class Name(WebElement):
            (by, value) = (By.ID, 'name')
    
    class Gender:
        class Male(WebElement):
            (by, value) = (By.ID, 'male')
        
        class Female(WebElement):
            (by, value) = (By.ID, 'female')
    
    class Hobby:
        class Music(WebElement):
            (by, value) = (By.ID, 'music')
        
        class Sport(WebElement):
            (by, value) = (By.ID, 'sport')
        
        class Travel(WebElement):
            (by, value) = (By.ID, 'travel')
    
    
    class SubmitButton(WebElement):
        (by, value) = (By.XPATH, '//button[@onclick="do_submit();"]')
    
    class ResetButton(WebElement):
        (by, value) = (By.XPATH, '//button[@onclick="do_reset();"]')
    
    
    class Result(WebElement):
        (by, value) = (By.ID, 'result')




#### [Step 3] Add testcase/demo_module.py


    # -*- coding: utf-8 -*-
    # Just import the page you need, and use it directly.

    from page import DemoPage

    def TestCase001_Normal_Input_Test():

        #### Name ###
        DemoPage.Name.Title.Select("Mr.")
        DemoPage.Name.Name.Set("Henry.Wang")

        ### Gender ###
        DemoPage.Gender.Male.Click()

        ### Hobbies ###
        DemoPage.Hobby.Music.Click()
        DemoPage.Hobby.Travel.Click()

        ###### Result ######
        DemoPage.SubmitButton.Click()

        DemoPage.Result.VerifyInnerHTMLContains("Henry.Wang")
        DemoPage.Result.VerifyInnerHTMLContains("Gender: male")
        DemoPage.Result.VerifyInnerHTMLContains("Hobbies: Music Travel")




#### [Step 4] Configure conf.ini
    
    DRIVER_CHROME       = E:\Knitter\examples\DemoProject\drivers\chromedriver_win32\chromedriver.exe
    DRIVER_IE           = E:\Knitter\examples\DemoProject\drivers\IEDriverServer_Win32_2.42.0\IEDriverServer.exe
    
    TESTING_URL         = http://sleepycat.org/static/knitter/KnitterDemo.html
    
    
    # divided by "|", run test case one time for each browser.
    TESTING_BROWSERS    = Chrome|IE|Firefox

    



#### [Step 5] Configure runner.py

    # -*- coding: utf-8 -*-
    
    from knitter import executer

    # Run specified test case of testcase/demo_module.py
    executer.run_case("demo_module", "TestCase001_Normal_Input_Test") 




#### [Step 6] Run runner.py

    result/
          summary.log     # summary result
          result.xls      # summary result in excel.
          screenshort/
                     ...  # screen shorts of error test cases.
        
          testcase/
                  ...     # detailed log of each test case
    




