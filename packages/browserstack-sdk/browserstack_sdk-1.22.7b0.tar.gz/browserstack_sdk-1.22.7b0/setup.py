from os.path import abspath, join, dirname
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(join(dirname(abspath(__file__)), 'LICENSE.txt'), encoding='utf8') as f:
    LICENSE = f.read()

# this provides the __version__ attribute at setup.py run time
exec(open('browserstack_sdk/_version.py').read())

setup(
    name='browserstack_sdk',
    packages=['browserstack_sdk', 'browserstack_sdk.sdk_cli', 'pytest_browserstackplugin', 'bstack_utils'],
    version=__version__,
    description='Python SDK for browserstack selenium-webdriver tests',
    long_description='Python SDK for browserstack selenium-webdriver tests',
    author='BrowserStack',
    author_email='support@browserstack.com',
    keywords=['browserstack', 'selenium', 'python'],
    classifiers=[],
    install_requires=[
        'psutil',
        'pyyaml',
        'browserstack-local>=1.2.5',
        'packaging',
        'requests',
        'percy-appium-app',
        'python-dotenv',
        'requests_toolbelt',
        'pypac',
        'GitPython',
        'pytest-xdist',
        'grpcio==1.62.3',
        'protobuf==4.21.6',
    ],
    license=LICENSE,
    entry_points = {
        'console_scripts': [
            'browserstack-sdk = browserstack_sdk.__init__:run_on_browserstack'
            ],
        'pytest11': [
            'myplugin = pytest_browserstackplugin.plugin',
            ],
        'bstack_utils11': [
            'browserstack_utils = bstack_utils'
            ]
        }
)
