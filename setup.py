# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name                    = 'knitter',
    version                 = '0.4.1',
    
    author                  = 'Henry Wang',
    author_email            = 'skymatrix@126.com',
    maintainer              = 'Henry Wang',
    maintainer_email        = 'skymatrix@126.com',
    
    url                     = 'https://github.com/hww712/Knitter',
    description             = 'Python Web Automation Test Framework with Selenium WebDriver',
    long_description        = 'This is a web testing framework based on Selenium WebDriver. The object is to develop web testing automation project with good implementation, maintainance and extendability.',
    
    classifiers             = ['Topic :: Software Development :: Testing', 'Topic :: Software Development :: Quality Assurance'],
    platforms               = ['linux', 'windows'],
    license                 = 'BSD License',
    
    packages                = ['knitter'],
    
    install_requires        = ['selenium', 'xlrd', 'xlwt'],
)











