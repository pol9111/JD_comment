from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from config import *


class Action():
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "SM_G9500",
            "appPackage": "com.jingdong.app.mall",
            "appActivity": "main.MainActivity",
            "noReset": True
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def comments(self):
        # 点击进入搜索页面
        search = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jingdong.app.mall:id/a3p')))
        search.click()
        # 输入搜索文本
        box = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search:id/search_text')))
        box.set_text(KEYWORD)
        # 点击搜索按钮
        button = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jingdong.app.mall:id/awc')))
        button.click()
        # 点击进入商品详情
        view = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search:id/product_item_name')))
        view.click()
        # 进入评论详情
        ac = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.productdetail:id/detail_desc_description')))
        if ac:
            TouchAction(self.driver).long_press(x=806, y=2500, duration=600).move_to(x=806, y=50).release().perform()
            # 进入评论详情
            tab = self.wait.until(
                EC.presence_of_element_located((By.ID, 'com.jd.lib.productdetail:id/pd_comment_goodper')))
            tab.click()

    def scroll(self):
        self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.shareorder:id/comment_list_item_root')))
        while True:
            # 模拟拖动
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            sleep(SCROLL_SLEEP_TIME)

    def main(self):
        self.comments()
        self.scroll()


if __name__ == '__main__':
    action = Action()
    action.main()




