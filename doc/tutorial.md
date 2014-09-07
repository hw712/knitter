Tutorial
=======================================================================

1. Installation
-----------------------------------------------------------------------

    pip install knitter


2. Preconditions
-----------------------------------------------------------------------

+ Python 2.7

+ Depends on "selenium", "xlrd", "xlwt" packages, which will be installed while installing knitter.

+ Drivers

    - [Chrome Driver](http://chromedriver.storage.googleapis.com/index.html)

    - [IE Driver](http://selenium-release.storage.googleapis.com/index.html)

    - You can also find drivers [here](https://github.com/hww712/Knitter/tree/master/examples/DemoProject/drivers).



3. Start Demo Project
-----------------------------------------------------------------------

+ [Demo Project Test Script](https://github.com/hww712/Knitter/tree/master/examples/DemoProject))

+ [Demo Project Test Page](http://sleepycat.org/static/knitter/KnitterDemo.html))


#### Step 1. Create project folder structure.

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


#### Step 2. Add test page module "DemoPage.py" under "page/"


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


+ All element class must inherit from "WebElement".



#### Step 3. Add test case module "demo_module.py" under "testcase/"


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


+ Just import the page you need, and use it directly.


#### Step 4. Configure "conf.ini"

    DRIVER_CHROME: where the Chrome driver locates.
    DRIVER_IE:     where the IE driver locates.
    TESTING_URL:   start up URL for testing.

    TESTING_BROWSERS: Multi browsers divided by "|", will run test case one time on each browser.


#### Step 5. Configure "runner.py", and run it.

    # -*- coding: utf-8 -*-
    
    from knitter import executer

    # Run specified test case of test module "testcase/demo_module.py".
    executer.run_case("demo_module", "TestCase001_Normal_Input_Test") 

run "runner.py", check result in "result/" folder.







