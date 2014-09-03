Tutorial
-----------------------------------------------------------------------

### Install

    pip install knitter


### Preconditions

+ Support Python 2.7, NOT support Python 3.

+ Knitter depends on selenium/xlrd/xlwt packages, which will be installed while installing knitter.

+ You need to have ChromeDriver and IDDriver to run test on Chrome and IE. I put the driver files in folder: [https://github.com/hww712/Knitter/tree/master/examples/DemoProject/drivers](https://github.com/hww712/Knitter/tree/master/examples/DemoProject/drivers)

    - Download Chrome Driver: [http://chromedriver.storage.googleapis.com/index.html](http://chromedriver.storage.googleapis.com/index.html)

    - Download IE Driver: [http://selenium-release.storage.googleapis.com/index.html](http://selenium-release.storage.googleapis.com/index.html)



### How to Start

** Let's take page [http://sleepycat.org/static/knitter/KnitterDemo.html](http://sleepycat.org/static/knitter/KnitterDemo.html) as an example test page for a demo. **

#### 1) Create project folder structure.

Consult [https://github.com/hww712/Knitter/tree/master/examples/DemoProject](https://github.com/hww712/Knitter/tree/master/examples/DemoProject).

    test project folder structure:

    DemoProject\
               |data\...   (Excel Data Files, such as "TestData.xlsx")
               |page\
                     __init__.py  ("page" is a Python package, which includes all real test pages.)
                     DemoPage.py  (This file is for the demo page, which includes all elements on page "http://sleepycat.org/static/knitter/KnitterDemo.html"
                     ...
               |testcase\
                     __init__.py    ("testcase" is a Python package, which includes all test cases.)
                     demo_module.py (This file contains a group of test cases for the demo)
                     ...
               conf.ini             (Configure running environment)
               runner.py            (Configure which case or module to run, and run)


#### 2) add page modules under "page/"

Create file for each page, add elements according to the syle like below. The only thing that need to concern is By and Value.

All element class must inherit from "WebElement".

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



#### 3) add test case under "testcase/"

Just import the page you need, and use it directly.

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


#### 4) configure "conf.ini"

    DRIVER_CHROME: is where the Chrome driver locates.
    DRIVER_IE:     is where the IE driver locates.
    TESTING_URL:   is the start up URL for testing.

    TESTING_BROWSERS: Set the browsers you want to run. Multi browsers divided by "|", and will run test case one time on each browser.


#### 5) configure "runner.py"

    executer.run_module("demo_module") # Will run all test cases of module "testcase/demo_module.py".

run "runner.py", check result in "result/" folder.













