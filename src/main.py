from util import Util

from selenium_manage import SeleniumAPP
from firecrawl_manage import FirecrawlAPP

def main():
    selenium_app = SeleniumAPP()
    # 메뉴 리스트 가져오기
    menus = selenium_app.get_gnb_nav_list()
    print(menus)

    firecrawl_app = FirecrawlAPP()
    # firecrawl을 사용하여 메인 콘텐츠 스크랩핑 요청(벌크 요청으로 바로 결과를 받아볼 수 없음)
    scraped_result = firecrawl_app.scrape_all_main_content(menus)
    print(scraped_result)

    # 위의 메서드 결과에서 id를 가져와 스크랩 요청한 데이터 받아옴
    scraped_list = firecrawl_app.get_batch_scrape_status(scraped_result["id"])
    print(scraped_list)

    # 메뉴명과 url만 담겨있는 menus에 스크래핑해온 html, markdown 저장
    Util.match_menus_and_scraped_data(menus, scraped_list["data"])



    # 계층별 폴더 생성 및 파일 생성
    Util.create_folders_and_files(menus)

if __name__ == "__main__":
    main()
