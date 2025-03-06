import time
import re
import urllib.parse
from typing import Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from util import Util


class SeleniumAPP:
    def __init__(self):
        # ChromeOptions 객체 생성
        chrome_options = Options()

        # 헤드리스 모드 활성화
        chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_gnb_nav_list(self, use_nested_json=False):
        """
        kt.com에서 메뉴 리스트 가져오기
        :param use_nested_json: True일 경우 계층화된 json 형식으로 리턴
        :return: [{"menu_name" : 메뉴명, "url" : url}, {"menu_name" : 메뉴명, "url" : url}, ...]
        """
        self.driver.get("https://www.kt.com/") # selenium을 사용하여 kt.com 접속
        time.sleep(3)  # 페이지가 완전히 로드될 때까지 대기
        
        # GNB 메뉴 중 "마이" 제외
        self.driver.execute_script("""
            var element = document.querySelector('.navigation');  // GNB element
            var child = element.querySelector('.nav5');  // "마이" element
            if (child) {
                child.remove();  // "마이" element 삭제
            }
        """)

        # GNB element 가져옴
        navigation_element = self.driver.find_element(By.CLASS_NAME, "navigation")
        
        # a 태그 추출
        a_tags = navigation_element.find_elements(By.TAG_NAME, "a")
        
        # {"menu_name" : menu_name, "url" : url} 형식의 dict를 담는 배열
        navigation_list = []
        
        # 메뉴명, url 추출
        for a_tag in a_tags:
            href = a_tag.get_attribute("href")
            match = re.search(r"kt_common\.ktMenuLinkStat\('([^']+)','([^']+)'", href)

            if match:
                url = match.group(1)
                menu_name = urllib.parse.unquote(match.group(2)).replace('^KT-개인_공통^GNB^', '')
                navigation_list.append({"menu_name" : menu_name, "url" : url})

        # 중첩 json 리턴
        if use_nested_json:
            return Util.build_tree(navigation_list)

        return navigation_list
