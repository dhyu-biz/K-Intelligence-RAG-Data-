from firecrawl import FirecrawlApp
import time


class FirecrawlAPP:
    def __init__(self):
        self.app = FirecrawlApp(api_key="fc-5e038ceec6064ccb9cd916e0cac4d923")
        
    def scrape_main_content(self, menu):
        '''
        1개의 url에 대해 스크래핑
        :param menu:
        :return:
        '''
        # {"menu_name" : "메뉴명1", "result" : "스크랩 결과물"}
        scraped_data = {
                        "menu_name" : menu["menu_name"],
                        "result": self.app.scrape_url(url=menu["url"],
                                                    params={
                                                        "formats": ["markdown", "html"],
                                                        "includeTags": ["#cfmClContents"],
                                                        "excludeTags": [".location"],
                                                    })
                        }

        return scraped_data

    def scrape_all_main_content(self, menus):
        '''
        firecrawl을 이용하여 batch 스크래핑 요청(요청하는 url이 많아 결과를 바로 받아 볼 수 없음 "get_batch_scrape_status()"를 통해 결과 요청해야 함)
        비동기 요청

        :param menus: [{"menu_name" : 메뉴명, "url" : url}, {"menu_name" : 메뉴명, "url" : url}, ...]
        :return: {'success': True, 'id': '912a7128-71de-48a1-b846-d397e5701f4c', 'url': 'https://api.firecrawl.dev/v1/batch/scrape/912a7128-71de-48a1-b846-d397e5701f4c'}
        '''
        # 스크랩 결과를 담을 배열
        scraped_data_list = []

        # batch scrape를 위한 url만 담긴 배열
        url_list = self.extract_urls(menus)
        return self.app.async_batch_scrape_urls(url_list,
                                           {
                                                    "formats": ["markdown", "html"],
                                                    "includeTags": ["#cfmClContents"],
                                                    "excludeTags": [".location"],
                                                   })

    def get_batch_scrape_status(self, batch_id: str):
        '''
        batch 스크래핑 요청 결과를 받아옴 (스크랩 요청이 비동기 방식으로 순서가 뒤섞임
        :param batch_id: scrape_all_main_content()의 결과의 id값을 전달
        :return: {
                  "status": "completed",
                  "total": 36,
                  "completed": 36,
                  "creditsUsed": 36,
                  "expiresAt": "2024-00-00T00:00:00.000Z",
                  "next": "https://api.firecrawl.dev/v1/batch/scrape/123-456-789?skip=26",
                  "data": [
                    {
                      "markdown": "[Firecrawl Docs home page![light logo](https://mintlify.s3-us-west-1.amazonaws.com/firecrawl/logo/light.svg)!...",
                      "html": "<!DOCTYPE html><html lang=\"en\" class=\"js-focus-visible lg:[--scroll-mt:9.5rem]\" data-js-focus-visible=\"\">...",
                      "metadata": {
                        "title": "Build a 'Chat with website' using Groq Llama 3 | Firecrawl",
                        "language": "en",
                        "sourceURL": "https://docs.firecrawl.dev/learn/rag-llama3",
                        "description": "Learn how to use Firecrawl, Groq Llama 3, and Langchain to build a 'Chat with your website' bot.",
                        "ogLocaleAlternate": [],
                        "statusCode": 200
                      }
                    },
                    ...
                  ]
                }
        '''
        while True:
            # 결과 요청 status가 complete 될 때까지 5초 마다 요청
            result = self.app.check_batch_scrape_status(batch_id)
            print(result)
            if result["status"] == 'completed':
                return result
            else:
                time.sleep(5)

    @staticmethod
    def extract_urls(menus):
        '''
        scrape_all_main_content() 호출 시 url 리스트가 필요하기에 menus에서 url만 따옴
        :param dict_array_menu: [{"menu_name" : 메뉴명, "url" : url}, {"menu_name" : 메뉴명, "url" : url}, ...]
        :return: ['url', 'url', 'url', ...]
        '''
        url_list = []
        for menu in menus:
            url_list.append(menu["url"])

        return url_list


