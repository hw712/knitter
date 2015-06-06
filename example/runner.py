# -*- coding: utf-8 -*-

import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__name__)))

print sys.path

from knitter import executer

#executer.run_case("demo_module", "TestCase001_Normal_Input_Test")
#executer.run_case("demo_module", "TestCase002_Data_In_Excel")


executer.run_module("demo_module")


print "end"

