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

    - [Chrome driver](http://chromedriver.storage.googleapis.com/index.html)

    - [IE driver](http://selenium-release.storage.googleapis.com/index.html)

    - You can also find both driver files [here](https://github.com/hww712/Knitter/tree/master/examples/DemoProject/drivers).



3. Start Demo Project
-----------------------------------------------------------------------

+ [Demo project test script](https://github.com/hww712/Knitter/tree/master/examples/DemoProject)

+ [Demo project test page](http://sleepycat.org/static/knitter/KnitterDemo.html)


#### Step 1. Create Project Folder Structure.


    DemoProject/
               data/...   (Excel Data Files, such as "TestData.xlsx")
               page/
                     __init__.py
                     DemoPage.py
                     ...
               testcase/
                     __init__.py
                     demo_module.py
                     ...
               conf.ini
               runner.py


#### Step 2. Add Test Page Module "DemoPage.py" under "page/"


    # -*- coding: utf-8 -*-
    # All element class must inherit from "WebElement".

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






#### Step 3. Add Test Case Module "demo_module.py" under "testcase/"


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

**Run "runner.py", check result in "result/" folder.**







