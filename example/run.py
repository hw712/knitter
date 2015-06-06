# -*- coding: utf-8 -*-

from knitter import executer
from demoprj import conf, testcase


executer.run(conf.ChromeDemo, testcase.validations.TestCase001_NormalInputTest)
executer.run(conf.MSWindows, testcase.validations.TestCase002_Data_In_Excel)


executer.run(conf.MultiBrowsersDemo, testcase.validations)









