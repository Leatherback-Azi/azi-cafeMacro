''' Please Read '''
# 1. this program is made for "양아지(dkwl025)"'s naver Cafe.
# 2. this program requires "Chrome (WebBrowser)" to run.


from config import config
from userDataBase import userDataBase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os, pyperclip, time
import webDriverLoader


def clearConsole():
    # 콘솔 클리어. OS별 다른 커맨드
    if config.OS == 'Windows':
        os.system('cls')
    elif config.OS == 'Darwin' or config.OS == 'Linux':
        os.system('clear')

class barCodeChecker:
    def __init__(self):
        clearConsole()
        print('이 프로그램을 사용하기 위해서 Chrome이 필수적으로 설치 되어 있어야 합니다!\n\n')
        print('Ctrl + C 를 눌러서 프로그램을 강제로 종료합니다.\n')
        self.isitActive = True
        self.total_member = 0
        self.initDriver()
        self.barCodeChecker_main()

    # 프로그램 종료 시 사용되는 메서드
    def __del__(self):
        print('프로그램을 종료합니다.')
        print('종료중...')
        self.isitActive = False
        time.sleep(3)
        # raise KeyboardInterrupt

    # main 메서드
    def barCodeChecker_main(self):
        self.login()
        time.sleep(2)
        clearConsole()
        self.findMemberTab()
        self.getUserPendigCount()
        self.checkMemberLeft()
        if self.total_member <= 100:
            self.allowLogic_UnderHundred()
        else:
            self.allowLogic_OverHundred()

        print('추가적으로', end=' ')
        self.getUserPendigCount()
        if self.total_member != 0:
            print('\n\n매크로 실행 중 추가적인 멤버가 가입신청을 하였습니다.\n')
            if self.total_member <= 100:
                self.allowLogic_UnderHundred()
            else:
                self.allowLogic_OverHundred()
            print('추가적으로 대기중인 멤버가 없습니다.\n')
            raise KeyboardInterrupt
        else:
            print('대기중인 멤버가 없습니다.\n')
            raise KeyboardInterrupt

    # 클릭 가능할 때 까지 기다린 후 클릭 (css selector)
    def click_element_by_css_selector(self, elem):
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, str(elem))))
        element.click()

    # 클릭 가능할 때 까지 기다린 후 클릭 (XPath)
    def click_element_by_xpath(self, elem):
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, str(elem))))
        element.click()

    # text 값 가져올 수 있을때까지 기다린 후 text 값 가져오기 (XPath)
    def getValue_element_by_xpath(self, elem):
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, str(elem))))
        return element.text

    def getUserNickname(self, process_complete):
        # get Barcode + (nickname) info. (바코드 + 닉네임 정보 가져오기)
        memberName = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div[2]/div[1]/form/table/tbody/tr[' + str(process_complete) + ']/td[2]/div/a')
        memberName = memberName.text
        print(memberName)
        # crop barcode part (바코드 부분만 자르기)
        # -> nickname part will be deleted (닉네임 부분은 삭제됨.)
        membername = memberName.split(' ')[0]
        return membername

    # check barcode does correct in form (바코드닉이 형식에 맞는지 확인)
    # if correct, return 1, else return 0. (맞으면 1, 틀리면 0을 리턴함)
    def checkname_barcode(self, membername):
        # >= 15 : dkwl025 / == 20 : bighead033
        if len(membername) >= 15:
            count_number = membername.count('l')
            count_number += membername.count('i')
            count_number += membername.count('I')
            if count_number == len(membername):
                return 1
            else:
                return 0
        else:
            return 0

    # check "membercnt"'s order checkbox (membercnt번째 멤버 체크박스 선택)
    def checkname_element(self, membercnt):
        self.driver.find_element_by_css_selector(
            "._click\(ManageJoinApplication\|Member\|member" + str(membercnt) + "\)").send_keys(Keys.SPACE)

    def loadWebDriver(self):
        try:
            self.loader = webDriverLoader.WebDriverLoader(config.DRIVER_PATH)  # Parameter - Driver Path
            self.driver = self.loader.getAvailableDriver()  # Chromedriver 가져오기
            self.driver.implicitly_wait(10)  # 로딩까지 10초간 기다린다는 뜻.
            self.driver.get(config.baseURL)
        except Exception as E:
            print(f'{str(E)}\n\nChromedriver를 설치 또는 가져오는 중 에러가 발생함!')

    def initDriver(self):
        # 현재 디렉토리, Chromedriver 디렉토리 출력
        print('현재 디렉토리 :\n' + config.PROJECT_ROOT + '/')
        print('Chromedriver 경로 :\n' + config.DRIVER_PATH + '/')
        print('ID, 비밀번호 저장 경로 :\n' + config.DB_FILE)
        print('잠시만 기다려 주세요...')
        self.loadWebDriver()
        self.wait = WebDriverWait(self.driver, 10)

    # check barcode nickname. (바코드 닉네임 확인)
    def checkname_correct(self, process_complete):
        barcode = self.getUserNickname(process_complete)
        checker = self.checkname_barcode(barcode)

        if checker == 1:
            print('수락됨 - 형식에 맞음.\n')
            self.checkname_element(process_complete)
            return 1
        else:
            print('스킵됨 - 잘못된 형식.\n')
            return 0

    def checkname_incorrect(self, processed_count):
        barcode = self.getUserNickname(processed_count)
        checker = self.checkname_barcode(barcode)
        if checker == 0:
            print('거부됨 - 잘못된 형식.\n')
            self.checkname_element(processed_count)
        else:
            print('에러가 발생함.')

            print(
                '사유 : 확인 된 멤버 수 보다 실제 신청된 멤버 수가 많거나 적습니다.\n')
            print("'Enter'를 눌러 프로그램을 종료합니다.")
            input()
            raise KeyboardInterrupt

    def login(self):
        # login button
        self.click_element_by_xpath(config.xpath_logIn_Button)
        userInfo = userDataBase()
        while True:
            userSelection = input(
                '\n\n1 - 직접 웹에 입력하여 로그인.\n2 - 저장된 ID, 비밀번호 사용하기. (저장된 값이 없을 시 생성)\n3 - 저장된 ID 삭제\n입력 : ')
            clearConsole()
            if userSelection == '1':
                print('로그인 후 현재 창에서 \'Enter\'를 눌러 주세요.')
                input()
                break
            elif userSelection == '2':
                input('로그인 중 복사해 놓은 값이 사라질 수 있습니다. 진행하기 전에 복사한 값을 먼저 저장해 주세요.\n\'Enter\'를 입력하여 계속하기.\n')
                clearConsole()
                if userInfo.isDataExist:
                    print('저장된 ID : ' + userInfo.ID)
                    if config.OS == 'Windows' or config.OS == 'Linux':
                        pyperclip.copy(userInfo.ID)
                        self.driver.find_element_by_xpath('//*[@id="id"]').send_keys(Keys.LEFT_CONTROL, 'v')
                        pyperclip.copy(userInfo.PW)
                        self.driver.find_element_by_xpath('//*[@id="pw"]').send_keys(Keys.LEFT_CONTROL, 'v')
                    elif config.OS == 'Darwin':
                        pyperclip.copy(userInfo.ID)
                        self.driver.find_element_by_xpath('//*[@id="id"]').send_keys(Keys.COMMAND, 'v')
                        pyperclip.copy(userInfo.PW)
                        self.driver.find_element_by_xpath('//*[@id="pw"]').send_keys(Keys.COMMAND, 'v')
                    pyperclip.copy(
                        '아지짱짱 - 이 복사된 값은 아지랜드 가입승인 매크로 실행 중 로그인 캡차(로봇이 아님을 인증하세요)를 회피하기 위해 비밀번호를 복사한 것을 덮어쓰기 위해 복사한 값입니다.')
                    self.driver.find_element_by_xpath('//*[@id="log.login"]').click()
                    print('로그인 되었습니다.')
                    break
                else:
                    answer = 'y'
                    while True:
                        if answer == 'y' or answer == 'Y':
                            newID = input('ID를 입력해 주세요. -\n')
                            newPW = input('비밀번호를 입력해 주세요. -\n')
                        clearConsole()
                        answer = input('ID : ' + newID + '\nPW : ' + newPW + '\n입력하신 정보가 맞습니까? (Y/N)\n')
                        clearConsole()
                        if answer == 'y' or answer == 'Y':
                            userInfo.saveFile(newID, newPW)
                            break
                        elif answer == 'n' or answer == 'N':
                            answer = 'y'
                            continue
                        else:
                            print('잘못된 입력입니다. 다시 선택해 주세요.')
            elif userSelection == '3':
                answer = 'y'
                while True:
                    if answer == 'y' or answer == 'Y':
                        print('저장된 ID : ' + userInfo.ID)
                    answer = input('정말로 삭제하시겠습니까? (Y/N)\n')
                    if answer == 'y' or answer == 'Y':
                        userInfo.deleteFileData()
                        cnt = 3
                        for i in range(3):
                            clearConsole()
                            print('성공적으로 삭제 되었습니다. ' + str(cnt) + '초 후 선택창으로 돌아갑니다.')
                            cnt -= 1
                            time.sleep(1)
                        clearConsole()
                        break
                    elif answer == 'n' or answer == 'N':
                        break
                    else:
                        print('잘못된 입력입니다. 다시 선택해 주세요.')



    # 가입승인 페이지 열기
    def findMemberTab(self):
        # cafe management (카페 관리 클릭)
        self.click_element_by_xpath(config.xpath_cafeManagement_Button)
        # 다른 창이 전체화면일 시, 작동하지 않음. - 전체화면 기준 : 새 데스크톱 또는 화면을 혼자 먹는 전체화면
        self.click_element_by_css_selector(config.css_manageJoin_Button)
        self.click_element_by_xpath(config.xpath_manageApplicant)

    # 가입승인 대기중인 멤버 수 가져오기
    def getUserPendigCount(self):
        self.total_member = self.getValue_element_by_xpath(config.xpath_usersPendingCount)
        # 대기중인 멤버 수 출력
        print("대기중인 멤버 : " + str(self.total_member))
        # tot_member는 char class이므로, int class로 변환.
        self.total_member = int(self.total_member)

    def checkMemberLeft(self):
        if self.total_member:
            Select(self.driver.find_element_by_xpath(config.xpath_selectPerPageCount)).select_by_value('100')
        else:
            print('더이상 대기중인 멤버가 없습니다.')
            self.isitActive = False
            raise KeyboardInterrupt

    # 가입 승인 메서드
    def allow_check(self, process_now):
        process_complete = 1
        allowed_count = 0
        while process_now > 0:
            temp = self.checkname_correct(process_complete)
            allowed_count += temp
            process_complete += 1
            process_now -= 1
        self.click_element_by_xpath(config.xpath_allowButton)
        return allowed_count

    def deny_check(self, process_now):
        process_complete = 1
        while process_now > 0:
            self.checkname_incorrect(process_complete)
            process_complete += 1
            process_now -= 1
        self.click_element_by_xpath(config.xpath_denyButton)
        return process_complete - 1

    # 대기중인 멤버가 100명 이하일 때 실행되는 코드
    def allowLogic_UnderHundred(self):
        process_now = self.total_member
        print('가입승인 처리중...\n\n')
        process_complete = self.allow_check(process_now)

        print('\'확인\' 버튼을 누른 후, 현재 창에서 \'Enter\'를 눌러 주세요.')
        input()
        clearConsole()
        self.total_member -= process_complete
        process_now -= process_complete

        if self.total_member == 0:
            print('\n가입승인 작업이 끝났습니다!')
            return

        print('가입거부 처리중...\n\n')
        temp = process_complete
        process_complete = self.deny_check(process_now)
        process_complete += temp
        print('\n가입승인 및 거부 작업이 끝났습니다!')
        print('\'확인\' 버튼을 누른 후, 현재 창에서 \'Enter\'를 눌러 주세요.')
        input()
        clearConsole()

    # 대기중인 멤버가 100명 초과일 시 실행
    def allowLogic_OverHundred(self):
        process_first = self.total_member % 100
        self.allowLogic_UnderHundred(process_first)
        self.total_member -= process_first
        loop_page = self.total_member // 100
        int(loop_page)
        while loop_page > 0:
            loop_page -= 1
            self.allowLogic_UnderHundred()


if __name__ == '__main__':
    try:
        program = barCodeChecker()
    except KeyboardInterrupt:
        quit()
    except Exception as E:
        print('Unknown Error! Terminating Program...\n' + str(E))
