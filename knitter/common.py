# -*- coding: utf-8 -*-

import datetime, os, sys, xlrd, inspect

import environment, log


def stamp_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def stamp_datetime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def stamp_datetime_coherent():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")


def exception_error():
    error_message = u"""Error!
======================================== Error Message ====================================
    File:          %s
    Line:          %s
    Function:      %s
    Statement:     %s
    Error Message: %s
-------------------------------------------------------------------------------------------
    File:          %s
    Line:          %s
    Function:      %s
    Statement:     %s
======================================== Error Message ======================================================""" % (
    inspect.trace()[-1][1], 
    inspect.trace()[-1][2],
    inspect.trace()[-1][3],
    inspect.trace()[-1][4],
    sys.exc_info(),
    inspect.trace()[-2][1], 
    inspect.trace()[-2][2],
    inspect.trace()[-2][3],
    inspect.trace()[-2][4],
    )
    
    
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



def setconf(arg, value):
    conf_file = u"%s\\conf.ini" % environment.PROJECT_PATH
    data_all  = ""
    arg_exist = False
    
    if os.path.exists(conf_file):
        if os.path.isfile(conf_file):
            try:
                with open(conf_file, 'r') as f:
                    while True:
                        data = f.readline()
                        
                        if not data:
                            break
                        
                        if data.split('=')[0] == arg:
                            arg_exist = True
                            data = u"%s=%s\n" % (data.split('=')[0], value)
                        else:
                            data = u"%s=%s\n" % (data.split('=')[0], data.split('=')[1].splitlines()[0])
                        
                        data_all = u"%s%s" % (data_all, data)
                
                if arg_exist == False:
                    data_all = u"%s%s=%s\n" % (data_all, arg, value)
            
            except:
                log.handle_error()
        else:
            data_all = u"%s%s=%s\n" % (data_all, arg, value)
    else:
        data_all = u"%s%s=%s\n" % (data_all, arg, value)
    
    try:
        with open(conf_file, 'w') as f:
            f.write(data_all.encode('utf-8'))
    except:
        log.handle_error()


def getconf(arg):
    conf_file = u"%s\\conf.ini" % environment.PROJECT_PATH
    
    if os.path.exists(conf_file):
        if os.path.isfile(conf_file):
            try:
                with open(conf_file, 'r') as f:
                    while True:
                        data = f.readline()
                        
                        if not data:
                            break
                        
                        if data.split('=')[0].strip() == arg:
                            return str(data.split('=', 1)[1].splitlines()[0].strip())
                
            except IOError:
                return ""
    
    return ""


def excel_get_nrows(xls_path, sheet_name):
    excel = xlrd.open_workbook(xls_path)
    sheet = excel.sheet_by_name(sheet_name)
    
    return sheet.nrows


def excel_get_value_by_position(xls_path, sheet_name, x, y):
    excel = xlrd.open_workbook(xls_path)
    sheet = excel.sheet_by_name(sheet_name)
    
    return unicode(sheet.cell(x, y).value)

def excel_get_value_by_row_number(xls_path, sheet_name, x, colname):
    excel = xlrd.open_workbook(xls_path)
    sheet = excel.sheet_by_name(sheet_name)
    
    collist = []
    
    for col in range(0, sheet.ncols):
        collist.append(excel_get_value_by_position(xls_path, sheet_name, x, col))
    
    return excel_get_value_by_position(xls_path, sheet_name, x, collist.index(colname))






if __name__ == "__main__":
    pass






