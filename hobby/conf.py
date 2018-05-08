from knitter.configure import Browser, General


def windows():
    # Chrome
    Browser.Chrome.Driver = "driver/chromedriver.exe"
    Browser.AvailableBrowsers.append(Browser.Chrome)

    # If True, not open real chrome, just run chrome in memory
    Browser.HeadlessMode = False

    # URL
    Browser.StartURL = "http://sleepycat.org/static/knitter/hobby.html"

    # Result Path
    General.Path.Result = "C:/Archive/results"
