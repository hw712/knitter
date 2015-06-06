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

    - You can also find both driver files [here](https://github.com/hww712/Knitter/tree/master/examples/DemoProject/drivers).



3. Demo project
-----------------------------------------------------------------------

+ Demo project source code:

    - [https://github.com/hww712/Knitter/tree/master/example](https://github.com/hww712/Knitter/tree/master/example)

+ Demo project test page:

    - [http://sleepycat.org/static/knitter/KnitterDemo.html](http://sleepycat.org/static/knitter/KnitterDemo.html)


#### Step 1. Create a source code package "demoprj".


    demoprj/
           page/
                 __init__.py
                 KintterDemo.py   # elements of test page
                 ...
           
           testcase/
                 __init__.py
                 validations.py   # test cases
                 ...
           
           __init__.py
           conf.py                # configurations


#### Step 2. Add page elements to "page/KnitterDemo.py"


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




#### Step 3. Add cases to "testcase/validations.py"

    # -*- coding: utf-8 -*-
    
    from knitter import datadriver, log
    from demoprj.page import KnitterDemo
    
    
    def TestCase001_NormalInputTest():
        #### Name ###
        KnitterDemo.Name.Title.Select("Mr.")
        KnitterDemo.Name.Name.Set("Henry.Wang")
        
        ### Gender ###
        KnitterDemo.Gender.Male.Click()
        
        ### Hobbies ###
        KnitterDemo.Hobby.Music.Click()
        KnitterDemo.Hobby.Travel.Click()
        
        ###### Result ######
        KnitterDemo.SubmitButton.Click()
        
        KnitterDemo.Result.VerifyInnerHTMLContains("Henry.Wang")
        KnitterDemo.Result.VerifyAttribute("innerHTML", "Music", method="contain")
        



#### Step 4. Add configurations to "conf.py"

    # -*- coding: utf-8 -*-
    
    
    class MSWindows:
        BASE_URL = 'http://sleepycat.org/static/knitter/KnitterDemo.html'
        TESTING_BROWSERS = 'Firefox'




#### Step 5. Setup "run.py", and run it.

    # -*- coding: utf-8 -*-
    
    from knitter import executer
    from demoprj import conf, testcase
    
    
    executer.run(conf.ChromeDemo, testcase.validations.TestCase001_NormalInputTest)




#### Step 6. Check result of HTML report.

    result/index.html
    




