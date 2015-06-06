# -*- coding: utf-8 -*-
import threading

# driver of web browser, such as: webdriver.Firefox()
BROWSER             = None


# path where to save the result log.
RESULT_PATH         = ""
EXCEL_DATA_PATH     = ""

# test case/module variables.
#===============================================================================
# CASE_START_TIME     = "N/A"
# CASE_STOP_TIME      = "N/A"
# CASE_NAME           = "N/A"
# CASE_PASS           = "N/A"
# CASE_WARNINGS       = 0
# 
# MODULE_NAME         = ""
#===============================================================================



# multi-threading
threadlocal = threading.local()




# start/stop time of the whole test
TOTAL_START_TIME    = "N/A"
TOTAL_STOP_TIME     = "N/A"

TOTAL_TESTCASE_PASS = 0
TOTAL_TESTCASE_FAIL = 0


# initial URL of the testing page.
BASE_URL            = ""


# TESTING_BROWSER is one of TESTING_BROWSERS
TESTING_BROWSER     = ""
TESTING_BROWSERS    = ""


# Data of test result, for generate report in excel.
EXCEL_REPORT_DATA   = []

HTMLREPORT_TESTCASES = []
HTMLREPORT_SCREENSHOT_NAME = ""


FIREFOX_BINARY          = ""
RESERVED_FIREFOX_BINARY = ""

DRIVER_OF_CHROME     = ""
DRIVER_OF_IE         = ""


FAST_FAIL            = False
EXIT_STATUS          = 0


BROWSER_VERSION_INFO = {}


THREAD_LOCK          = threading.Lock()

RESTART_BROWSER      = True


SUPPORT_ANGULARJS    = True
