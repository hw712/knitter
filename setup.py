
from setuptools import setup


setup(
    name='knitter',
    version='1.0.0',
    
    author='Henry Wang',
    author_email='skymatrix@126.com',
    maintainer='Henry Wang',
    maintainer_email='skymatrix@126.com',
    
    url='https://github.com/hw712/Knitter',

    description='Python Web Automation Test Framework with Selenium WebDriver',
    long_description='This is a web testing framework based on Selenium WebDriver. '
                     'The target is to develop web testing automation project with good implementation, '
                     'maintainability and extendability.',

    # https://pypi.org/classifiers/
    classifiers=['License :: OSI Approved :: BSD License',
                 'Topic :: Software Development :: Testing',
                 'Topic :: Software Development :: Quality Assurance',
                 'Topic :: Software Development :: Libraries :: Application Frameworks'],

    platforms=['linux', 'windows'],

    license='BSD License',
    
    packages=['knitter'],
    
    install_requires=['selenium', 'xlrd'],
)











