# -*- coding: utf-8 -*-

from platform import python_version_tuple
import datetime, os, sys, inspect, stat, shutil

try:
    # Python 3
    from knitter import log
    from knitter import env
except ImportError:
    # Python 2
    import log
    import env



def is_python_2():
    if python_version_tuple()[0] == '2':
        return True
    else:
        return False

def is_python_3():
    if python_version_tuple()[0] == '3':
        return True
    else:
        return False


def stamp_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def stamp_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def stamp_datetime_coherent():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")


def exception_error():
    error_message = ""
    for i in range(len(inspect.trace())):
        error_line = u"""
File:      %s - [%s]
Function:  %s
Statement: %s
-------------------------------------------------------------------------------------------""" % (
        inspect.trace()[i][1], 
        inspect.trace()[i][2], 
        inspect.trace()[i][3], 
        inspect.trace()[i][4])
        
        error_message = "%s%s" % (error_message, error_line)
    
    
    error_message = """Error!
%s
%s
======================================== Error Message ====================================%s

======================================== Error Message ======================================================""" % (sys.exc_info()[0], sys.exc_info()[1], error_message)
    
    return error_message


def add_unique_postfix(fn):
    '''
    __author__ = 'Denis Barmenkov <denis.barmenkov@gmail.com>'
    __source__ = 'http://code.activestate.com/recipes/577200-make-unique-file-name/'
    
    '''
    if is_python_2():
        fn = unicode(fn)
    
    if not os.path.exists(fn):
        return fn

    path, name = os.path.split(fn)
    name, ext = os.path.splitext(name)

    make_fn = lambda i: os.path.join(path, '%s__%d%s' % (name, i, ext))

    for i in range(2, sys.maxint):
        uni_fn = make_fn(i)
        if not os.path.exists(uni_fn):
            return uni_fn

    return None


def force_delete_file(file_path):
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            return file_path
        except:
            '''
            print "delete fail. Kill Processes."
            os.popen("TASKKILL /F /IM excel.exe")
            time.sleep(2)
            '''
            return add_unique_postfix(file_path)
    else:
        return file_path



def mkdirs(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except:
        log.step_warning(str(sys.exc_info()))


def remove_readonly(fn, path, excinfo):
    if os.path.exists(path):
        try:
            if fn is os.rmdir:
                os.chmod(path, stat.S_IWRITE)
                os.rmdir(path)
            elif fn is os.remove:
                os.chmod(path, stat.S_IWRITE)
                os.remove(path)
        except:
            log.step_warning(str(sys.exc_info()))

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
    except:
        log.step_warning(str(sys.exc_info()))


def delete_file_or_folder(file_full_path):
    if os.path.exists(file_full_path):
        if os.path.isdir(file_full_path):
            delete_folder(file_full_path)
        else:
            os.remove(file_full_path)

def copy(src, dst):
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)
    except:
        log.step_warning(str(sys.exc_info()))


def delete_then_mkdir(dir_path):
    if os.path.exists(dir_path):
        delete_folder(dir_path)
    os.makedirs(dir_path)

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


def parse_conf_class(conf_class):
    '''
    Parse the configure class, get all the properties of the class, then set
    their corresponding value in module "env".
    
    AUTHOR
        Henry.Wang, 2015-02-11
    '''
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    new_conf = []
    for var in dir(conf_class):
        if (not var.startswith("__")) and (not var.endswith("__")):
            new_conf.append(var)
    
    def_conf = []
    for var in dir(env):
        if (not var.startswith("__")) and (not var.endswith("__")):
            def_conf.append(var)
    
    for conf in new_conf:
        if conf in def_conf:
            setattr(env, conf, getattr(conf_class, conf))
        else:
            log.step_warning("conf [%s] not found in module env." % conf)
    
    # if result path not set in conf, set where the "run.py" file locates.
    if env.RESULT_PATH == "":
        env.RESULT_PATH = os.path.dirname(os.path.abspath(inspect.stack()[-1][1]))


def get_sub_folder_names(full_path):
    return [ name for name in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, name)) ]

def get_version_info():
    from knitter import __version__ as knitter_version
    from selenium import __version__ as selenium_version
    from sys import version as python_version
    
    browser_version = ""
#     for k, v in env.BROWSER_VERSION_INFO.iteritems():
    for k, v in env.BROWSER_VERSION_INFO.items():
        browser_version += "%s - %s, " % (k, v)
    
    return "Version Info:  Python %s, %sKnitter %s, Selenium %s" % (python_version.split(" ")[0],
                                                             browser_version, 
                                                             knitter_version,
                                                             selenium_version)
    

if __name__ == "__main__":
    pass

#     env.BROWSER_VERSION_INFO = {"Firefox": "22.0"}
#     print get_version_info()

#     thedir = r"E:\EclipseWorkspace\claims-qa-test\result"
#     print [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
    
    #copy(r"E:\EclipseWorkspace\claims-qa-test\result\testcase", r"E:\EclipseWorkspace\claims-qa-test\result\2015-03-10_160248_2015-03-10_160320\testcase")







