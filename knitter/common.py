# -*- coding: utf-8 -*-

import datetime, os, sys, inspect

import env


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
    fn = unicode(fn)
    
    if not os.path.exists(fn):
        return fn

    path, name = os.path.split(fn)
    name, ext = os.path.splitext(name)

    make_fn = lambda i: os.path.join(path, '%s__%d%s' % (name, i, ext))

    for i in xrange(2, sys.maxint):
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
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)



def get_value_from_conf(key):
    conf_file = u"%s\\conf.ini" % env.PROJECT_PATH
    
    if not os.path.exists(conf_file):
        return ""
    
    if not os.path.isfile(conf_file):
        return ""
    
    try:
        with open(conf_file, 'r') as f:
            while True:
                data = f.readline()
                
                if not data:
                    return ""
                
                if len(data.split('=')) < 2:
                    continue
                
                if data.strip()[0] == "#":
                    continue
                
                if data.split('=')[0].strip() == key:
                    return str(data.split('=', 1)[1].strip())
    except IOError:
        return ""










if __name__ == "__main__":
    pass






