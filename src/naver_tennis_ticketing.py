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

# 로그인 기능 이용시, loginTry = True 및 아이디와 패스워드를 여기에 입력
# macOS는 불가 (loginTry = True 로 설정 금지)
# 개발 및 테스트용 ( 터미널에 start 쳐서 하는게 더 정확하고 빠름)
loginTry = False
ID = ""
PW = ""
TEST = False


############사용자 설정 내용 #############
# URL 주소 ( 현재 : 양재 테니스장)
# 1. 양재
URL = "https://booking.naver.com/booking/10/bizes/210031"
# 2. 내곡
# URL = "https://booking.naver.com/booking/10/bizes/217811"

# AMPM 이 0 이면 AM, 1 이면 PM
AMPM = 0

# TIME 시간값으로 입력 : 0,1,2,3,4,5,6,7,8,9,10,11
# 0 일 경우 12:00
TIME = 10
# 보통 주말 예약은 최대 두시간 이므로 10 으로 설정하면 10:00 ~ 12:00 (2시간) 예약이 됩니다.

# 예약 사이트의 예약하고자 하는 테니스코트 순서(왼쪽 상단 0부터 시작!!)
RESER_COURT = 0

# 내가 선택할 일자 입력 (앞에 일자 부터 입력 권장 - "YYYY-MM-DD" 형식이여야 함!)
myReserveDate = [
    "2021-11-07",  # 0번째 값
    "2021-11-14",  # 1번째 값
    "2021-11-21",  # 2번째 값
    "2021-11-28",  # 3번째 값
]
date_rank = [
    0,  # myReserverDate 0번째 값 선택
    1,  # myReserverDate 4번째 값 선택
    2,  # myReserverDate 3번째 값 선택
    3,  # myReserverDate 1번째 값 선택
]
# date_rank는 0부터 (myReserveDate 의 원소 갯수 -1) 의 값을 가져야하며,
# myReserverDate의 원소와 쌍을 이루며 순서를 설정함

# ex ) date_rank 의 첫번째 값이 0 => myReserveDate의 0번째에 값이 진행됨 (가장 먼저)
#      => 2021-07-04 의 날짜를 가장 먼저 예약 시도함
#      date_rank 의 두번째 값이 4 => myReserveDate의 4번째에 값이 진행됨
#      => 2021-07-31 의 날짜로 예약 시도함 (0,1,2,3,4 이니 가장 마지막!!)
#      date_rank 의 세번째 값이 3 => myReserveDate의 3번째 값이 진행됨
#      => 2021-07-25의 날짜로 예약 시도함
#          ....
#     예약 시도하는 순서 -->  2021-07-04 -> 2021-07-31 -> 2021-07-25 -> 2021-07-18 -> 2021-07-24


############사용자 설정 내용 완료 #############

# 6월 테스트 테스트 테스트 테스트 테스트 테스트 테스트 테스트
# 실제 할때는 반드시 TEST = False 로 바꾸고 위 '사용자 설정 내용' 에 있는 값을 바꿀것
if TEST == True:
    RESER_COURT = 5
    myReserveDate = [
        "2021-11-07",  # 0번째 값
        "2021-11-14",  # 1번째 값
        "2021-11-21",  # 2번째 값
        "2021-11-28",  # 3번째 값
        "2021-11-13",  # 4번째 값
    ]
    date_rank = [
        4,  # myReserverDate 4번째 값 선택
        1,  # myReserverDate 1번째 값 선택
        3,  # myReserverDate 3번째 값 선택
        2,  # myReserverDate 2번째 값 선택
        0,  # myReserverDate 0번째 값 선택
    ]
# 6월 테스트 테스트 테스트 테스트 테스트 테스트 테스트 테스트

idx = 0

# OS 버전에 따른 크롬 드라이버 설정
cwdPath = ""
clientOS = ""
if platform.platform()[0:5] == "macOS":
    cwdPath = os.path.dirname(os.path.realpath(__file__)) + "/macOS/chromedriver"
    clientOS = "macOS"
else:
    cwdPath = (
        os.path.dirname(os.path.realpath(__file__)) + "//Windows//chromedriver.exe"
    )
    clientOS = "Windows"

now = datetime.now()
options = Options()
options.headless = False
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# executable_path 부분에 브라우저 드라이버 파일 경로를 입력
driver = webdriver.Chrome(executable_path=cwdPath, options=options)
wait = WebDriverWait(driver, 10)
driver.get(URL)
time.sleep(5)


def login():

    loginBtn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "gnb_btn_login"))
    ).click()

    id_box = wait.until(EC.element_to_be_clickable((By.ID, "id")))
    pw_box = driver.find_element_by_id("pw")

    id_box.click()
    pyperclip.copy(ID)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("v").key_up(
        Keys.CONTROL
    ).perform()

    pw_box.click()
    pyperclip.copy(PW)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("v").key_up(
        Keys.CONTROL
    ).perform()

    login = wait.until(EC.element_to_be_clickable((By.ID, "log.login"))).click()

    time.sleep(0.5)


def wait_booking():

    booking_btn = 0

    while True:

        try:
            print("try")
            more_info = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        'span[ng-bind-html="bizItemInfo.name | newlines"]',
                    )
                )
            )
            booking_btn = driver.find_elements_by_css_selector(
                'span[ng-bind-html="bizItemInfo.name | newlines"]'
            )
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
        "span[ng-bind=\"$ctrl.baseDate.get('month') + 1\"]"
    )

    nobth_sel_btn_R = calendar.find_element_by_css_selector(
        'a[ng-click="$ctrl.nextMonth()"]'
    )
    nobth_sel_btn_L = calendar.find_element_by_css_selector(
        'a[ng-click="$ctrl.prevMonth()"]'
    )

    if month.text == str(now.month):
        nobth_sel_btn_R.click()

    return calendar


def make_booking(calendar):

    global myReserveDate, idx, date_rank
    time.sleep(0.5)
    try:
        calendar_table = calendar.find_element_by_class_name("tb_body")
        weeks = calendar_table.find_elements_by_tag_name("tr")

        my_date = []
        etc_date = []

        for item in weeks:
            days = item.find_elements_by_tag_name("td")
            for item2 in days:
                class_attribute = item2.get_attribute("data-tst_cal_datetext")
                if class_attribute in myReserveDate:
                    my_date.append(item2)
                else:
                    etc_date.append(item2)

        print("Click Date :", myReserveDate[date_rank[idx]], " ")
        driver.find_element_by_css_selector(
            "a[ng-click='$event.preventDefault();$ctrl.isShow = false;']"
        ).click()
        my_date[date_rank[idx]].click()

        time.sleep(0.1)
        customer_selector = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ly_time_booking"))
        )
        time_select_am = customer_selector.find_element_by_css_selector(
            'div[class="am"]'
        ).find_elements_by_css_selector(
            'span[ng-bind="$ctrl.getStartTime(timeSchedule)"]'
        )
        time_select_pm = customer_selector.find_element_by_css_selector(
            'div[class="pm"]'
        ).find_elements_by_css_selector(
            'span[ng-bind="$ctrl.getStartTime(timeSchedule)"]'
        )

        time_select = [time_select_am, time_select_pm]

        print("Click TIME : AMPM : ", AMPM, " TIME : ", TIME)
        time_select[AMPM][TIME].click()
        time_select[AMPM][TIME + 1].click()

        select_time_btn = driver.find_element_by_css_selector(
            "button[ng-click='$event.preventDefault(); $ctrl.close()']"
        ).click()

        next_step_btn = driver.find_element_by_css_selector(
            "button[ng-click='$ctrl.nextStep($event)']"
        ).click()

        gogo_payment_btn = driver.find_element_by_css_selector(
            "span[ng-bind='$ctrl.getSubmitButtonTitle()']"
        ).click()

        time.sleep(3)
        agree_btn = driver.find_element_by_xpath(
            "//*[@id='orderForm']/div/div[5]/div[1]/div[2]/div/strong/label"
        ).click()

        do_payment_btn = driver.find_element_by_css_selector(
            'button[class="btn_payment _click(nmp.front.order.order_sheet.account()) _stopDefault _doPayButton"]'
        ).click()

        print("[Booking] Success to Booking, Please try to do payment!")
        number = 1
        while number == 1:
            time.sleep(10000)
    except Exception as e:
        print("[BOOKING - ERROR]", e)

        driver.refresh()
        print("refresh @ END Variabe - data : ", myReserveDate[date_rank[idx]])
        time.sleep(0.5)
        calendar2 = wait.until(EC.element_to_be_clickable((By.ID, "calendar")))
        idx = idx + 1
        if idx >= len(date_rank):
            print("예약에 모두 실패했습니다. 수동으로 진행해주세요")
            while True:
                time.sleep(1000000)
        print("Refresh @ START Variabe - date : ", myReserveDate[date_rank[idx]])
        make_booking(calendar2)


def main():
    print("waiting for Inputing 'start' , Please Login the Reserving page")
    while input() != "start":
        print("waiting for Inputing 'start' , Please Login the Reserving page")
        time.sleep(0.5)

    print("[START] Program Start")
    print(clientOS)
    if clientOS == "macOS":
        time.sleep(0.5)
    else:
        if loginTry:
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
