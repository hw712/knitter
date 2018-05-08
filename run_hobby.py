from knitter import executor
from hobby import conf
from hobby.testcase import module1_inputs, module2_combine

executor.run(conf.windows, module1_inputs, module2_combine)

"""
# You can run your specified modules or test cases, just append them as the next parameters.
executor.run(conf.windows, module1_inputs.TestCase01_BasicVerify)
executor.run(conf.windows, module1_inputs.TestCase01_BasicVerify, module2_combine)

"""
