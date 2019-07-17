
from setuptools import setup


setup(
    name='knitter',
    version='1.0.0',
    
    author='Henry Wang',
    author_email='outsidematrix@126.com',
    maintainer='Henry Wang',
    maintainer_email='outsidematrix@126.com',
    
    url='https://github.com/hw712/knitter',

    description='A Web Automation Test Framework Based On Selenium WebDriver',
    long_description="Knitter['nitə] is a web automation test framework, with which you can develop "
                     "the web ui automation with good maintainability and extendability.",

    # https://pypi.org/classifiers/
    classifiers=['License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Topic :: Software Development :: Testing',
                 'Topic :: Software Development :: Quality Assurance',
                 'Topic :: Software Development :: Libraries :: Application Frameworks'],

    platforms=['linux', 'windows'],

    license='BSD License',
    
    packages=['knitter'],
    
    install_requires=['selenium', 'xlrd'],
)











