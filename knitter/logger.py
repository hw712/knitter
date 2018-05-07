from datetime import datetime
import os
import sys

from knitter.configure import Browser, General
from knitter import library
from knitter import reportor


def start_project():
    General.TestCase.Browser = None
    General.TestCase.Name = ""
    General.TestCase.Pass = True
    General.TestCase.Warnings = 0
    General.TestCase.StartTime = ""
    General.TestCase.EndTime = ""

    General.TestModule.Name = ""

    General.Total.NumberOfTestCasePass = 0
    General.Total.NumberOfTestCaseFail = 0
    General.Total.StartTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    General.HTMLReporterLines[:] = []

    library.delete_folder(os.path.join(General.Path.Result, "testcase"))
    library.delete_folder(os.path.join(General.Path.Result, "screenshots"))

    reportor.generate_html_report([General.Total.StartTime, "N/A", "N/A", "N/A", "N/A", "N/A"], [])

    print(">>>>>>  [%s]  =>  Start Testing......       <<<<<<" % General.Total.StartTime)


def end_project():
    General.Total.EndTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(">>>>>>  [%s]  =>  Test End. Duration [%s], All [%s], Pass [%s], Fail [%s]       <<<<<<" % (
        General.Total.EndTime,
        datetime.strptime(General.Total.EndTime, "%Y-%m-%d %H:%M:%S") - datetime.strptime(General.Total.StartTime,
                                                                                          "%Y-%m-%d %H:%M:%S"),
        General.Total.NumberOfTestCasePass + General.Total.NumberOfTestCaseFail,
        General.Total.NumberOfTestCasePass,
        General.Total.NumberOfTestCaseFail
    ))

    reportor.generate_html_report([General.Total.StartTime, General.Total.EndTime,
                                   datetime.strptime(General.Total.EndTime, "%Y-%m-%d %H:%M:%S") - datetime.strptime(General.Total.StartTime, "%Y-%m-%d %H:%M:%S"),
                                   General.Total.NumberOfTestCasePass + General.Total.NumberOfTestCaseFail,
                                   General.Total.NumberOfTestCasePass,
                                   General.Total.NumberOfTestCaseFail], General.HTMLReporterLines, countdown=False)
    reportor.save_current_report_to_repository()
    reportor.generate_report_history()
    reportor.generate_html_report([General.Total.StartTime, General.Total.EndTime,
                                   datetime.strptime(General.Total.EndTime, "%Y-%m-%d %H:%M:%S") - datetime.strptime(General.Total.StartTime, "%Y-%m-%d %H:%M:%S"),
                                   General.Total.NumberOfTestCasePass + General.Total.NumberOfTestCaseFail,
                                   General.Total.NumberOfTestCasePass,
                                   General.Total.NumberOfTestCaseFail], General.HTMLReporterLines, countdown=True)

    print("")
    print(library.version_info())


def handle_exception(e):
    if General.TestCase.Pass is False:
        return

    if e is not None:
        step_normal(e)

        if General.QuickTest is True:
            print(library.timestamp_date_and_time() + "                Warning: " + str(e))

    if sys.exc_info()[0] is not None:
        step_warning(library.exception_error())

        if Browser.RunningBrowser is not None:
            image = "Fail__%s__%s__%s.png" % (library.timestamp_for_file_name(), General.TestCase.Name,
                                              Browser.RunningBrowser.name)
            save_screen_shot(image)
            step_normal("Screen short: [%s]" % image)
        else:
            step_normal("No screen shot for browser because browser is not running.")

        General.TestCase.Pass = False


def start_test_case(name, browser):
    General.TestCase.Name = name + "-" + browser.__name__
    General.TestCase.StartTime = datetime.now().replace(microsecond=0)
    General.TestCase.Pass = True
    General.TestCase.Warnings = 0

    write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
              "\n**************  Test Case [%s] [%s]  ***************\n" % (name, browser.__name__))


def stop_test_case():
    General.TestCase.EndTime = datetime.now().replace(microsecond=0)
    General.Total.EndTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if General.TestCase.Warnings > 0:
        warning_message = ", has [%s] warning(s)!" % General.TestCase.Warnings
    else:
        warning_message = ""

    if General.TestCase.Pass is True:
        print(u"%s    [Pass]  =>  [%s] [%s] [%s] [%s]%s" % (library.timestamp_date_and_time(),
                                                            General.TestCase.EndTime - General.TestCase.StartTime,
                                                            General.TestModule.Name,
                                                            General.TestCase.Name,
                                                            Browser.RunningBrowser.name,
                                                            warning_message))
        General.Total.NumberOfTestCasePass += 1

        General.HTMLReporterLines.append(["%s =&gt; %s" % (General.TestCase.StartTime.strftime("%m-%d %H:%M:%S"),
                                                           General.TestCase.EndTime.strftime("%m-%d %H:%M:%S")),
                                         '<a href="testcase/%s.log">[%s] - %s</a>' % (General.TestCase.Name,
                                                                                      General.TestModule.Name,
                                                                                      General.TestCase.Name),
                                          General.TestCase.EndTime - General.TestCase.StartTime,
                                          Browser.RunningBrowser.name,
                                          '<td>Pass</td>'])

    else:
        print(u"%s    [Fail]  =>  [%s] [%s] [%s] [%s]%s" % (library.timestamp_date_and_time(),
                                                            General.TestCase.EndTime - General.TestCase.StartTime,
                                                            General.TestModule.Name,
                                                            General.TestCase.Name,
                                                            Browser.RunningBrowser.name,
                                                            warning_message))
        General.Total.NumberOfTestCaseFail += 1

        General.HTMLReporterLines.append(["%s =&gt; %s" % (General.TestCase.StartTime.strftime("%m-%d %H:%M:%S"),
                                                           General.TestCase.EndTime.strftime("%m-%d %H:%M:%S")),

                                         '<a href="testcase/%s.log">[%s] - %s</a>' % (General.TestCase.Name,
                                                                                      General.TestModule.Name,
                                                                                      General.TestCase.Name),

                                          General.TestCase.EndTime - General.TestCase.StartTime,
                                          Browser.RunningBrowser.name,

                                          '<td class="tfail"><a href="screenshots/%s">Fail</a></td>' %
                                          General.TestCase.ScreenShot
                                          ])

    reportor.generate_html_report([General.Total.StartTime, General.Total.EndTime,
                                   datetime.strptime(General.Total.EndTime, "%Y-%m-%d %H:%M:%S") -
                                   datetime.strptime(General.Total.StartTime, "%Y-%m-%d %H:%M:%S"),
                                   General.Total.NumberOfTestCasePass + General.Total.NumberOfTestCaseFail,
                                   General.Total.NumberOfTestCasePass,
                                   General.Total.NumberOfTestCaseFail], General.HTMLReporterLines, countdown=True)

    General.TestCase.Pass = True
    General.TestCase.Warnings = 0


def write_log(path, message):
    if General.QuickTest is True:
        return

    log = os.path.join(General.Path.Result, path)
    library.create_folder(os.path.dirname(log))

    with open(log, 'a') as f:
        f.write(message)


def save_screen_shot(image_name):
    if General.QuickTest is True:
        return

    image_path = os.path.join(General.Path.Result, "screenshots")
    library.create_folder(image_path)

    try:
        Browser.RunningBrowser.save_screenshot(os.path.join(image_path, image_name))
        General.TestCase.ScreenShot = image_name
    except Exception as e:
        handle_exception(e)


def step_section(message):
    write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
              "\n%s    Section: %s\n" % (library.timestamp_date_and_time(), message))


def step_normal(message):
    write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
              "%s    Step: %s\n" % (library.timestamp_date_and_time(), message))


def step_pass(message):
    write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
              "%s    Pass: %s\n" % (library.timestamp_date_and_time(), message))


def step_fail(message):
    if Browser.RunningBrowser is not None:
        image_name = "Fail__%s__%s__%s.png" % (library.timestamp_for_file_name(), General.TestCase.Name,
                                               Browser.RunningBrowser.name)

        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "------------ Fail [%s] -------------------\n" % library.timestamp_date_and_time())
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "%s    Fail: %s, Check ScreenShot [%s]\n" % (library.timestamp_date_and_time(), message, image_name))
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "------------ Fail [%s] ---------------------------------------\n" % library.timestamp_date_and_time())

        save_screen_shot(image_name)
    else:
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "------------ Fail [%s] -------------------\n" % library.timestamp_date_and_time())
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "%s    Fail: %s. And the browser not open.\n" % (library.timestamp_date_and_time(), message))
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "------------ Fail [%s] ---------------------------------------\n" % library.timestamp_date_and_time())

    General.TestCase.Pass = False

    if General.QuickTest is True:
        print(library.timestamp_date_and_time() + "                Fail Step: " + message)

    raise AssertionError(message)


def step_warning(message):
    if Browser.RunningBrowser is not None:
        image_name = "Fail__%s__%s__%s.png" % (library.timestamp_for_file_name(), General.TestCase.Name,
                                               Browser.RunningBrowser.name)
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "------------ Warning [%s] -------------------\n" % library.timestamp_date_and_time())
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "%s    Fail: %s, Check ScreenShot [%s]\n" % (library.timestamp_date_and_time(), message, image_name))
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "------------ Warning [%s] ---------------------------------------\n" % library.timestamp_date_and_time())

        save_screen_shot(image_name)
    else:
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "------------ Warning [%s] -------------------\n" % library.timestamp_date_and_time())
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "%s    Fail: %s. And the browser not open.\n" % (library.timestamp_date_and_time(), message))
        write_log(os.path.join("testcase", "%s.log" % General.TestCase.Name),
                  "------------ Warning [%s] ---------------------------------------\n" % library.timestamp_date_and_time())

    General.TestCase.Warnings += 1









