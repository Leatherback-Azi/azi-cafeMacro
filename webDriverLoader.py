from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

class BrowserNotFoundError(Exception):
    def __init__(self, browser=None):
        self.browser = browser

    def __str__(self):
        if self.browser == None:
            return "\nBrowser Not Found\n"
        else:
            return "\n{} Browser Not Found".format(self.browser)

class BrowserNotLoadableError(Exception):
    def __str__(self):
        return "\nBrowser Not Loadable"

class WebDriverLoader:
    def __init__(self, path):
        self.path = path

    def getAvailableDriver(self):
        try:
            return self.getChromeDriver()
        except BrowserNotFoundError:
            chromeNotFound = True
        except:
            chromeNotFound = False

        if chromeNotFound:
            raise BrowserNotFoundError
        else:
            raise BrowserNotLoadableError

    def getChromeDriver(self):
        try:
            driver = webdriver.Chrome(ChromeDriverManager(path=self.path).install())
            return driver
        except ValueError:
            raise BrowserNotFoundError("Chrome")
        except Exception as error:
            raise error
