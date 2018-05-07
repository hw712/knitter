import os
import inspect
import datetime
import sys
import shutil

from knitter.configure import General
from knitter import logger

def get_sub_folder_names(full_path):
    return [ name for name in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, name)) ]


def get_value_from_conf(conf_file, key):

    if not os.path.exists(conf_file):
        return ""

    if not os.path.isfile(conf_file):
        return ""

    try:
        with open(conf_file, 'r') as f:
            while True:
                data = f.readline()

                if not data:
                    break

                if len(data.split('=')) < 2:
                    continue

                if data.strip()[0] == "#":
                    continue

                if data.split('=')[0].strip() == key:
                    return str(data.split('=', 1)[1].strip())
    except IOError:
        return ""


def version_info():
    from knitter import __version__ as knitter_version
    from selenium import __version__ as selenium_version
    from sys import version as python_version

    browser_version = ""
    for k, v in General.VersionInfo.items():
        browser_version += "%s %s, " % (k, v)

    return "Python %s, %sKnitter %s, Selenium %s" % (python_version.split(" ")[0],
                                                                   browser_version, knitter_version, selenium_version)


def timestamp_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def timestamp_date_and_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def timestamp_for_file_name():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")


def exception_error():
    error_message = ""
    for i in range(len(inspect.trace())):
        error_line = """
File:      %s - [%s]
Function:  %s
Statement: %s
-------------------------------------------------------------------------------------------""" % \
                     (inspect.trace()[i][1], inspect.trace()[i][2], inspect.trace()[i][3], inspect.trace()[i][4])

    error_message = "%s%s" % (error_message, error_line)
    error_message = """Error!
%s
%s
======================================== Error Message ====================================%s

======================================== Error Message ======================================================""" % \
                    (sys.exc_info()[0], sys.exc_info()[1], error_message)

    return error_message


def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


def delete_file_or_folder(file_full_path):
    if os.path.exists(file_full_path):
        if os.path.isdir(file_full_path):
            delete_folder(file_full_path)
        else:
            os.remove(file_full_path)


def copy(src, destination):
    try:
        if os.path.isdir(src):
            shutil.copytree(src, destination)
        else:
            shutil.copy(src, destination)
    except Exception as e:
        logger.handle_exception(e)


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    version_info()
