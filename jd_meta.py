from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from pymongo import MongoClient
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from two import *

class Action():
    def __init__(self):
        self.desired_caps = {
          "platformName": "Android",
          "deviceName": "SM_G9500",
          "appPackage": "com.jingdong.app.mall",
          "appActivity": "main.MainActivity",
          "noReset": True
            }
        self.driver = webdriver.Remote(DRIVER_SERVER,  self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

    def entry(self):
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
        view = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search:id/product_list_item')))
        view.click()
        # 确认进入商品详情
        ac = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.productdetail:id/detail_desc_description')))
        if ac:
            TouchAction(self.driver).long_press(x=806, y=2500, duration=1000).move_to(x=806, y=50).release().perform()
            # 进入评论详情
            tab = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.productdetail:id/pd_comment_goodper')))
            tab.click()


    def comments(self):
        while True:
            items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@resource-id="com.jd.lib.shareorder:id/comment_list_item_root"]')))
            for item in items:
                try:
                    nickname = item.find_element_by_id('com.jd.lib.shareorder:id/tv_name').get_attribute('text')
                    pub_time = item.find_element_by_id('com.jd.lib.shareorder:id/tv_pub_time').get_attribute('text')
                    content = item.find_element_by_id('com.jd.lib.shareorder:id/tv_expand_content').get_attribute('text')
                    # score = item.find_element_by_id('com.jd.lib.shareorder:id/rb_score')
                    buy_date = item.find_element_by_id('com.jd.lib.shareorder:id/tv_buy_date').get_attribute('text')
                    useful_count = item.find_element_by_id('com.jd.lib.shareorder:id/tv_comment_useful_count').get_attribute('text')
                    reply_count = item.find_element_by_id('com.jd.lib.shareorder:id/tv_comment_reply_count').get_attribute('text')
                    print(nickname)
                    print(content)
                    print(pub_time)
                    # print(useful_count)
                    # print(reply_count)
                    images = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.jd.lib.shareorder:id/ll_images_container]')))
                    # images_list = []
                    # for image in images:
                    #     image = images.find_element_by_id('//*[@resource-id="com.jd.lib.shareorder:id/comment_list_img]')
                    #     images_list.append(image)
                    image = images.find_element_by_id('//*[@resource-id="com.jd.lib.shareorder:id/comment_list_img]')
                    data = {
                        '买家昵称': nickname,
                        '发表时间': pub_time,
                        '评论内容': content,
                        # '评分': score,
                        # '购买时间': buy_date,
                        # '按赞数': useful_count,
                        # '回复数': reply_count,
                        # '评论图片': images_list,
                        '评论图片': image,
                    }
                    print(data)
                    self.collection.update({'买家昵称': nickname, '评论内容': content}, {'$set': data}, True)
                    sleep(SCROLL_SLEEP_TIME)
                    self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
                except NoSuchElementException:
                    pass


    def main(self):
        self.entry()
        self.comments()


if __name__ == '__main__':
    action = Action()
    action.main()















