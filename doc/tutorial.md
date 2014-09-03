Tutorial
=======================================================================

Installation
-----------------------------------------------------------------------

    pip install knitter


Preconditions
-----------------------------------------------------------------------

+ Support Python 2.7, NOT support Python 3.

+ Depends on selenium, xlrd, xlwt packages, which will be installed while installing knitter.

+ Chrome/IE Driver: 

    - [https://github.com/hww712/Knitter/tree/master/examples/DemoProject/drivers](https://github.com/hww712/Knitter/tree/master/examples/DemoProject/drivers)

    - Official download link for Chrome driver: [http://chromedriver.storage.googleapis.com/index.html](http://chromedriver.storage.googleapis.com/index.html)

    - Official download link for IE driver: [http://selenium-release.storage.googleapis.com/index.html](http://selenium-release.storage.googleapis.com/index.html)



Start Testing
-----------------------------------------------------------------------

+ Test Page: ([http://sleepycat.org/static/knitter/KnitterDemo.html](http://sleepycat.org/static/knitter/KnitterDemo.html))

+ Demo Project: ([https://github.com/hww712/Knitter/tree/master/examples/DemoProject](https://github.com/hww712/Knitter/tree/master/examples/DemoProject))


#### 1). Create project folder structure.

    test project folder structure:

    DemoProject\
               |data\...   (Excel Data Files, such as "TestData.xlsx")
               |page\
                     __init__.py
                     DemoPage.py
                     ...
               |testcase\
                     __init__.py
                     demo_module.py
                     ...
               conf.ini
               runner.py


#### 2). Add test page module "DemoPage.py" under "page/"

+ All element class must inherit from "WebElement".


    # -*- coding: utf-8 -*-

    from knitter.webelement import WebElement
    from selenium.webdriver.common.by import By

    class SubmitButton(WebElement):
        (by, value) = (By.XPATH, '//button[@onclick="do_submit();"]')

    class ResetButton(WebElement):
        (by, value) = (By.XPATH, '//button[@onclick="do_reset();"]')

    class Gender:
        class Male(WebElement):
            (by, value) = (By.ID, 'male')

        class Female(WebElement):
            (by, value) = (By.ID, 'female')



#### 3). Add test case module "demo_module.py" under "testcase/"

+ Just import the page you need, and use it directly.


    # -*- coding: utf-8 -*-

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


#### 4). Configure "conf.ini"

    DRIVER_CHROME: where the Chrome driver locates.
    DRIVER_IE:     where the IE driver locates.
    TESTING_URL:   start up URL for testing.

    TESTING_BROWSERS: Multi browsers divided by "|", will run test case one time on each browser.


#### 5) Configure "runner.py", and run it.

    # Will run all test cases of module "testcase/demo_module.py".
    executer.run_module("demo_module") 
    
    # Run specified test case of test module.
    executer.run_case("demo_module", "TestCase001_Normal_Input_Test") 

run "runner.py", check result in "result/" folder.







