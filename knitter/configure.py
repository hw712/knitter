

class Browser:
    StartURL = ""
    RunningBrowser = None
    AvailableBrowsers = []
    HeadlessMode = False

    class FireFox:
        Driver = ""
        Binary = ""

    class Chrome:
        Driver = ""

    class IE:
        Driver = ""


class General:
    class TestCase:
        Name = ""
        Pass = True
        Warnings = ""
        StartTime = ""
        EndTime = ""
        ScreenShot = ""

    class TestModule:
        Name = ""

    class Total:
        StartTime = ""
        EndTime = ""
        NumberOfTestCasePass = 0
        NumberOfTestCaseFail = 0

    class Path:
        Result = ""

    VersionInfo = {}

    HTMLReporterLines = []

    # Only show log in the console, and exit all testing when any case fail.
    QuickTest = False


