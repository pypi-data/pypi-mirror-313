'初始信息'
import gettext
import locale
import os

APP_NAME = 'lfy'
APP_ID = 'cool.ldr.lfy'
VERSION = '0.0.11'
PACKAGE_URL_BUG = 'https://github.com/ldrfy/lfy/issues'
PACKAGE_URL = 'https://github.com/ldrfy/lfy'
RES_PATH = '/cool/ldr/lfy'

PKGDATA_DIR = '/usr/share/cool.ldr.lfy'
SCHEMAS_DIR = '/usr/share'
PYTHON_DIR = '/usr/lib'
LOCALE_DIR = '/usr/share/locale'

if not os.path.exists(f"{LOCALE_DIR}/zh_CN/LC_MESSAGES/{APP_ID}.mo"):
    LOCALE_DIR = os.path.join(os.path.dirname(__file__),
                              "resources/locale/")
    print("new LOCALE_DIR", LOCALE_DIR)

try:
    locale.bindtextdomain(APP_ID, LOCALE_DIR)
    locale.textdomain(APP_ID)
except AttributeError as e:
    print(f"Some gettext/locale translations will not work. Error:\n{e}")

try:
    gettext.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.textdomain(APP_ID)
except AttributeError as e:
    print(f"Some gettext translations will not work. Error:\n{e}")
