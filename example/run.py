# -*- coding: utf-8 -*-

import sys

# from platform import python_version_tuple
# from platform import python_version
# 
# print(python_version())
# 
# if python_version()[0] == '2':
#     print("haha")
# elif  python_version()[0] == '3':
#     print("333")
# else:
#     print('hhhhhh')
# 
# print(python_version_tuple()[0])

 
from knitter import executer
from demoprj import conf, testcase
# 
# print(dir(testcase))
# print(testcase.__loader__)
executer.run(conf.MSWindows, testcase.validations.TestCase001_NormalInputTest)
executer.run(conf.MSWindows, testcase.validations.TestCase002_Data_In_Excel)
# print(dir(testcase.validations))

# executer.run(conf.MultiBrowsersDemo, testcase.validations)










