import time
import pyperclip
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from json import load

secrets = load(open("secrets.json"))

ID = secrets["ID"]
PW = secrets["PW"]

class NaverLoginService():

    def __init__(self):
        self.driver = None
        self.title = None
        self.content = None

    def open_web_mode(self):
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(10)

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def login(self, id , pw):
        self.driver.get("https://nid.naver.com/nidlogin.login")
        time.sleep(2)  # 페이지 로딩 대기

        test_id = id
        test_passwd = pw

        # 아이디 입력
        id_input = self.driver.find_element(By.ID, "id")
        id_input.click()
        pyperclip.copy(test_id)
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(1)  # 입력 후 잠시 대기

        # 패스워드 입력
        pw_input = self.driver.find_element(By.ID, "pw")
        pw_input.click()
        pyperclip.copy(test_passwd)
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(1)  # 입력 후 잠시 대기

        # 로그인 버튼 클릭
        self.driver.find_element(By.ID, "log.login").click()

        # 로그인 후 '새로운 환경' 알림에서 '등록안함' 버튼 클릭
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.btn_cancel"))
            )
            element.click()
        except:
            print("기기 등록 '등록안함' 버튼을 찾을 수 없습니다.")

    def route_to_cafe_page(self, cafe_url, index):
        self.driver.get(f"https://cafe.naver.com/{cafe_url}/{index}")

    def switch_to_frame(self):
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "cafe_main"))

    def get_title_text(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'ArticleTitle')
        self.title = ' '.join([element.text for element in elements])

    def get_content_text(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'se-component-content')
        self.content = ' '.join([element.text for element in elements])

if __name__ == "__main__":
    naver_service = NaverLoginService()
    naver_service.open_web_mode()
    
    naver_service.login(ID, PW)
    time.sleep(5)

    naver_service.route_to_cafe_page("directwedding","6876240")
    time.sleep(5)

    naver_service.switch_to_frame()

    naver_service.get_title_text()
    print(naver_service.title)
    time.sleep(5)

    naver_service.get_content_text()
    print(naver_service.content)
    time.sleep(5)

    naver_service.close_browser()