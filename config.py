import os, platform

class config:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    DRIVER_PATH = PROJECT_ROOT.replace('\\', '/') + '/webdriver'
    DB_ROOT = PROJECT_ROOT
    DB_FILE = DB_ROOT + "/data.tl"
    OS = platform.system()

    baseURL = 'https://cafe.naver.com/azi025'

    xpath_logIn_Button = '//*[@id="gnb_login_button"]/span[3]'
    xpath_cafeManagement_Button = '//*[@id="ia-info-data"]/ul/li[3]/a[1]'
    css_manageJoin_Button = '#joinAndGrade'
    xpath_manageApplicant = '//*[@id="application"]'
    xpath_usersPendingCount = '//*[@id="joinapplication"]/p/em'
    xpath_selectPerPageCount = '//*[@id="joinapplication"]/div[1]/div[2]/p/select'
    xpath_allowButton = '//*[@id="joinapplication"]/div[2]/div/a[1]'
    xpath_denyButton = '//*[@id="joinapplication"]/div[2]/div/a[2]'
