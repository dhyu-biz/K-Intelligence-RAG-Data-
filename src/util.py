import os
from datetime import datetime

class Util:
    APP_NAME = "MyApp"
    VERSION = "1.0.0"

    @staticmethod
    def match_menus_and_scraped_data(menus, scraped_list):
        rs = Util.make_useful_data(scraped_list)
        for menu in menus:
            for r in rs:
                if r["url"] == menu["url"]:
                    menu["html"] = r["html"]
                    menu["markdown"] = r["markdown"]

    @staticmethod
    def make_useful_data(scraped_data: list):
        '''
        batch 스크래핑 결과들 중 필요한 데이터(url, html, markdown)만 추출하여 리스트에 담아 리턴
        :param scraped_data:
        :return: [
                    {
                        "url" : datum["metadata"]["sourceURL"],
                        "html" : datum["html"],
                        "markdown" : datum["markdown"]
                    }, ...
                ]
        '''
        result = []
        for datum in scraped_data:
            result.append({
                "url" : datum["metadata"]["sourceURL"],
                "html" : datum["html"],
                "markdown" : datum["markdown"]
            })
        return result

    @staticmethod
    def build_tree(menus):
        '''
        GNB 메뉴 계층형 json 변환기
        :param menus: [{"menu_name" : 메뉴명, "url" : url}, {"menu_name" : 메뉴명, "url" : url}, ...]
        :return: {
                  "Shop": {
                    "url": "https://shop.kt.com",
                    "요고다이렉트": {
                      "url": "https://shop.kt.com/unify/yogoEvent.do",
                      "요고가입혜택": {
                        "url": "https://shop.kt.com/unify/yogoEvent.do"
                      },
                      "요고가입": {
                        "url": "https://shop.kt.com/direct/directUsim.do",
                        "USIM가입": {
                          "url": "https://shop.kt.com/direct/directUsim.do"
                        },
                        "eSIM가입": {
                          "url": "https://shop.kt.com/direct/directEsim.do"
                        }
                      },
                      "핸드폰등록및요금제변경": {
                        "url": "https://shop.kt.com/direct/directChangeRate.do"
                      }
                    },
        '''
        tree = {}

        for item in menus:
            parts = item['menu_name'].split('^')
            node = tree

            for part in parts:
                if part not in node:
                    node[part] = {}
                node = node[part]

            node['url'] = item['url']

        return tree

    # 파일 저장 함수
    @staticmethod
    def save_files(path, menu):
        # url 파일 저장
        with open(os.path.join(path, 'url.txt'), 'w', encoding='utf-8') as url_file:
            url_file.write(menu['url'])

        # html 파일 저장 (빈 HTML 내용으로 저장)
        with open(os.path.join(path, 'html.html'), 'w', encoding='utf-8') as html_file:
            html_file.write(str(menu.get('html', {})))  # 기본값으로 빈 dict 저장

        # markdown 파일 저장 (빈 Markdown 내용으로 저장)
        with open(os.path.join(path, 'markdown.md'), 'w', encoding='utf-8') as md_file:
            md_file.write(str(menu.get('markdown', {})))  # 기본값으로 빈 dict 저장

    # 디렉토리 생성 함수
    @staticmethod
    def create_folders_and_files(menu_data, base_path=f"rag_data {datetime.now()}"):
        '''
        계층별 폴더 생성 및 파일(html, markdown, url) 생성
        :param menu_data: match_menus_and_scraped_data()의 결과
        :param base_path: 저장할 base 폴더 경로명 + 현재 시간
        :return: None
        '''
        for menu in menu_data:
            # menu_name을 기반으로 디렉토리 경로를 생성
            folders = menu['menu_name'].split('^')
            folder_path = os.path.join(base_path, *folders)

            # 디렉토리가 존재하지 않으면 생성
            os.makedirs(folder_path, exist_ok=True)

            # 해당 디렉토리에 url, html, markdown 파일을 저장
            Util.save_files(folder_path, menu)

    def __new__(cls, *args, **kwargs):
        raise TypeError("이 클래스는 인스턴스화할 수 없습니다.")


