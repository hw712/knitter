from knitter.configure import Browser, General


def windows():
    # Chrome
    Browser.Chrome.Driver = "driver/chromedriver.exe"
    Browser.AvailableBrowsers.append(Browser.Chrome)

    # FireFox
    Browser.FireFox.Driver = "driver/geckodriver.exe"
    Browser.AvailableBrowsers.append(Browser.FireFox)

    # Only for Chrome. If True, will just run in memory.
    Browser.HeadlessMode = False

    # URL
    Browser.StartURL = "http://sleepycat.org/static/knitter/hobby.html"

    # Result
    General.Path.Result = "results"
