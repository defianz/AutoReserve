import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import pause
import pyperclip
import platform
import os

# 아이디와 패스워드를 여기에 입력 (macOS는 미입력 )
ID = ""
PW = ""
# URL 주소 ( 현재 : 양재 테니스장)
# URL = "https://booking.naver.com/booking/10/bizes/210031" //양재
URL = "https://booking.naver.com/booking/10/bizes/217811"
#내곡

# OS 버전에 따른 크롬 드라이버 설정
cwdPath = ""
clientOS = ""
if(platform.platform()[0:5] == "macOS"):
    cwdPath =  os.path.dirname(os.path.realpath(__file__)) + "/macOS/chromedriver"
    clientOS = "macOS"
else:
    cwdPath = os.path.dirname(os.path.realpath(__file__)) + "//window//chromedriver.exe"
    clientOS = "Windows"

# AMPM 이 0 이면 AM, 1 이면 PM
AMPM = 0
# TIME 시간값으로 입력 : 0,1,2,3,4,5,6,7,8,9,10,11
# 0 일 경우 12:00
TIME = 10
# 예약 사이트의 예약하고자 하는 테니스코트 순서(왼쪽 상단 0부터 시작!!)
RESER_COURT = 0


now = datetime.now()
options = Options()
options.headless = False
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# executable_path 부분에 브라우저 드라이버 파일 경로를 입력
driver = webdriver.Chrome(
    executable_path=cwdPath,
    options=options
    )
wait = WebDriverWait(driver, 10)
driver.get(URL)
time.sleep(5)

# 로그인 함수
# 아이디 창과 패스워드 입력 창을 찾아서 클릭할 수 있을때까지 기다린 다음 자동으로 입력을 합니다

satcnt = 0
MAXSATCNT = 4

suncnt = 0
MAXSUNCNT = 4


def login():

    loginBtn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "gnb_btn_login"))).click()

    id_box = wait.until(EC.element_to_be_clickable((By.ID, "id")))
    pw_box = driver.find_element_by_id("pw")

    id_box.click()
    pyperclip.copy(ID)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(
        Keys.CONTROL).perform()

    pw_box.click()
    pyperclip.copy(PW)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(
        Keys.CONTROL).perform()

    login = wait.until(EC.element_to_be_clickable(
        (By.ID, "log.login"))).click()

    time.sleep(0.5)


def wait_booking():

    booking_btn = 0

    while True:

        try:
            print("try")
            more_info = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'span[ng-bind-html="bizItemInfo.name | newlines"]')))
            booking_btn = driver.find_elements_by_css_selector(
                'span[ng-bind-html="bizItemInfo.name | newlines"]')
        except:
            driver.refresh()
            print("REFRESH")
            time.sleep(0.5)
        if booking_btn != 0:
            break

    booking_btn[RESER_COURT].click()


def get_calender():

    calendar = wait.until(EC.element_to_be_clickable((By.ID, "calendar")))

    month = calendar.find_element_by_css_selector(
        'span[ng-bind="$ctrl.baseDate.get(\'month\') + 1"]')

    nobth_sel_btn_R = calendar.find_element_by_css_selector(
        'a[ng-click="$ctrl.nextMonth()"]')
    nobth_sel_btn_L = calendar.find_element_by_css_selector(
        'a[ng-click="$ctrl.prevMonth()"]')

    if month.text == str(now.month):
        nobth_sel_btn_R.click()

    return calendar


def make_booking(calendar):

    global satcnt, suncnt, MAXSATCNT, MAXSUNCNT
    time.sleep(0.5)
    try:
        calendar_table = calendar.find_element_by_class_name("tb_body")
        weeks = calendar_table.find_elements_by_tag_name("tr")

        sat_date = []
        sun_date = []
        etc_date = []

        for item in weeks:
            days = item.find_elements_by_tag_name("td")
            for item2 in days:
                class_attribute = item2.get_attribute("class")
                if class_attribute == "calendar-sat":
                    sat_date.append(item2)
                elif class_attribute == "calendar-sat calendar-selected start-day end-day":
                    sat_date.append(item2)
                elif class_attribute == "calendar-sun":
                    sun_date.append(item2)
                elif class_attribute == "calendar-sun calendar-selected start-day end-day":
                    sun_date.append(item2)
                else:
                    etc_date.append(item2)

        MAXSATCNT = len(sat_date)
        MAXSUNCNT = len(sun_date)

        if satcnt == MAXSATCNT:
            print("Click Date : SUNDAY of :", suncnt+1, " weeks")
            if(suncnt == 4):
                driver.find_element_by_css_selector(
                    "a[ng-click='$event.preventDefault();$ctrl.isShow = false;']").click()
            sun_date[suncnt].click()
        else:
            print("Click Date : SATURDAY of :", satcnt+1, " weeks")
            sat_date[satcnt].click()

        time.sleep(0.1)
        customer_selector = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ly_time_booking")))
        time_select_am = customer_selector.find_element_by_css_selector(
            'div[class="am"]'
        ).find_elements_by_css_selector('span[ng-bind="$ctrl.getStartTime(timeSchedule)"]')
        time_select_pm = customer_selector.find_element_by_css_selector(
            'div[class="pm"]'
        ).find_elements_by_css_selector('span[ng-bind="$ctrl.getStartTime(timeSchedule)"]')

        time_select = [time_select_am, time_select_pm]

        print("Click TIME : AMPM : ", AMPM, " TIME : ", TIME)
        time_select[AMPM][TIME].click()
        time_select[AMPM][TIME+1].click()

        select_time_btn = driver.find_element_by_css_selector(
            "button[ng-click='$event.preventDefault(); $ctrl.close()']").click()

        next_step_btn = driver.find_element_by_css_selector(
            "button[ng-click='$ctrl.nextStep($event)']").click()

        gogo_payment_btn = driver.find_element_by_css_selector(
            "span[ng-bind='$ctrl.getSubmitButtonTitle()']").click()

        time.sleep(3)
        agree_btn = driver.find_element_by_xpath(
            "//*[@id='orderForm']/div/div[5]/div[1]/div[2]/div/strong/label"
        ).click()

        do_payment_btn = driver.find_element_by_css_selector(
            'button[class="btn_payment _click(nmp.front.order.order_sheet.account()) _stopDefault _doPayButton"]').click()

        print("[Booking] Success to Booking, Please try to do payment!")
        number = 1
        while number == 1:
            time.sleep(10000)
    except Exception as e:
        print("[BOOKING - ERROR]", e)

        driver.refresh()
        print("refresh @ END Variabe - satcnt : ", satcnt, " / MAXSATCNT : ",
              MAXSATCNT-1, " | suncnt : ", suncnt, " / MAXSUNCNT : ", MAXSUNCNT-1)
        time.sleep(0.5)
        calendar2 = wait.until(EC.element_to_be_clickable((By.ID, "calendar")))
        if(satcnt < MAXSATCNT):
            satcnt = satcnt + 1
        else:
            suncnt = suncnt + 1

        if(suncnt >= MAXSUNCNT):
            return 0

        print("Refresh @ START Variabe - satcnt : ", satcnt, " / MAXSATCNT : ",
              MAXSATCNT-1, " | suncnt : ", suncnt, " / MAXSUNCNT : ", MAXSUNCNT-1)
        make_booking(calendar2)


def main():
    while input() != "start":
        print("waiting")
        time.sleep(0.5)

    print("[START] Program Start")
    print(clientOS)
    if clientOS == "macOS":
        # print(driver.find_element_by_id("gnb_name1").get_attribute('innerHTML'))
        # while driver.find_element_by_id("gnb_name1").get_attribute('innerHTML') == "":
        #     print("waiting")
            time.sleep(0.5)
    else:
        print("[Login] Start to Login")
        login()
    print("[Login] Success to Login")
    wait_booking()
    calendar = get_calender()
    print("[Booking] Start to Booking")
    make_booking(calendar)
    # while result != 1:
    #     result = make_booking(calendar)
    print("[END] Program Ends")


if __name__ == "__main__":
    main()