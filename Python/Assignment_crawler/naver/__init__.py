import os
import requests
from bs4 import BeautifulSoup


class NaverWebtoonCrawler:
    _url_list_base = 'http://comic.naver.com/webtoon/list.nhn'  # 웹툰 리스트 url 베이스
    _url_detail_base = 'http://comic.naver.com/webtoon/detail.nhn'  # 웹툰 뷰어 url 베이스

    def __init__(self, webtoon_id, webtoon_title = None, webtoon_author = None):
        self.webtoon_id = webtoon_id
        self._webtoon_title = webtoon_title
        self._webtoon_author = webtoon_author

    def params_episode_list(self, webtoon_id, page):
        '''웹툰 리스트 url 파라메터'''
        return {'titleId': webtoon_id, 'page': page}

    def params_episode_num(self, webtoon_id, epi_num):
        '''웹툰 뷰어 url 파라메터'''
        return {'titleId': webtoon_id, 'no': epi_num}

    def get_html_from_url(self, url, params):
        '''해당 url주소 웹페이지의 HTML 태그를 텍스트로 반환'''
        self.response = requests.get(url, params=params)
        return self.response.text

    def get_url(self, url, params):
        '''해당 url주소 웹페이지의 HTML 태그를 텍스트로 반환'''
        self.response = requests.get(url, params=params)
        return self.response.url

    def crawl_list_page(self, *page_number):
        '''크롤링할 페이지 번호 또는 시작/끝 번호를 받아 episode class 인스턴스를 리스트에 넣어 반환'''
        specified_episode_list = []  # 지정한 페이지의 episode instance를 저장하기 위한 list 생성(초기화)
        cur_page_episode_list = []  # 해당 페이지에 있는 만화 정보를 episode class instance로 생성해 저장할 list 생성(초기화)

        if len(page_number) == 2:
            start_page_number = page_number[0]
            end_page_number = page_number[1]
        elif len(page_number) == 1:
            start_page_number = page_number[0]
            end_page_number = page_number[0]
        elif len(page_number) == 0:
            start_page_number = 1
            end_page_number = 100
        else:
            print('페이지 번호를 잘못 적었습니다.')
            return None

        for page_num in range(start_page_number, end_page_number + 1):  # start_page_number~end_page_number 페이지까지 순환
            html = self.get_html_from_url(self._url_list_base, self.params_episode_list(self.webtoon_id, page_num))

            soup = BeautifulSoup(html, 'html.parser')
            episode_tr = soup.find('table', class_="viewList").find_all('tr')

            before_page_episode_list = cur_page_episode_list
            # 다음 페이지로 넘어오면, cur_page_episode에는 전 페이지의 list가 남는다. 따라서 비교를 위해 before로 옮겨준다.
            cur_page_episode_list = []
            # 다음 페이지로 넘어오면, cur_page_episode_list를 초기화시킨다.

            for episode in episode_tr:
                if not episode.find('td', class_='title'):
                    continue
                tr_episode = episode
                # episode_thumbnail = tr_episode.img['src']
                episode_title = tr_episode.find('td', class_="title").a.text
                # episode_link = tr_episode.find('td', class_="title").a['href']
                # episode_rating = tr_episode.find('div', class_="rating_type").find('strong').text
                # episode_num = tr_episode.find('td', class_="num").text
                # cur_page_episode_list.insert(0,(episode_thumbnail, episode_title,episode_link, episode_rating, episode_num))
                cur_page_episode_list.insert(0,episode_title)
                # print(cur_page_episode_list)

            if not page_num == start_page_number:
            # 페이지 번호가 시작번호인 경우 페이지의 리스트를 비교할 before_cur_page_episode_list가 비어있기때문에 비교하지않는다.
                if not before_page_episode_list[0] == cur_page_episode_list[0]:
                    specified_episode_list[0:0] = cur_page_episode_list
                    # 이전 페이지 첫 화의 제목과 이번 페이지 첫 화의 제목이 같지 않으면 cur_page_episode_list를 episode_list 앞에 삽입

                else:
                # 이전 페이지 첫 화의 제목과 이번 페이지 첫 화의 제목이 같으면 cur_page_episode_list를 episode_list에 추가하지않고 break
                    break
            else:
                specified_episode_list = cur_page_episode_list
                # 첫페이지의 리스트는 비교대상이 없으므로 바로 episode_list에 넣어준다

        return specified_episode_list

    def crawl_episode(self, episode_num=None):
        """
        webtoon_id에 해당하는 웹툰의 episode_num화 내부의 이미지를 저장
        :param episode_num:
        :return:
        """
        if episode_num is None:
            episode_num = len(self.crawl_list_page(1, 100))

        dir_path = '{}/{:03}'.format(self.webtoon_title, episode_num)

        # 이미지를 저장할 디렉터리 생성
        os.makedirs(dir_path, exist_ok=True)

        def get_img_tag_list():
            """
            디테일페이지에서 img Tag(bs4)의 리스트를 반환
            :return:
            """
            # 디테일 페이지의 html을 가져와 img의 href를 출력
            # print(url_detail)
            # requests를 이용해서 url_detail에 get요청을 보냄
            response = requests.get(url_detail)
            # 응답(Response)에서 .text를 이용해 내용을 가져옴
            # 가져온 응답내용을 이용해 BeautifulSoup인스턴스를 생성 (soup)
            soup = BeautifulSoup(response.text, 'html.parser')
            # soup인스턴스에서 select_one메서드를 사용해 웹툰뷰어 태그를 리턴
            div_wt_viewer = soup.select_one('div.wt_viewer')
            # 웹튠뷰어 태그에서 img태그들을 전부 찾아 리스트로 반환
            img_list = div_wt_viewer.find_all('img')
            return img_list

        url_detail = self.get_url(self._url_detail_base, self.params_episode_num(self.webtoon_id, episode_num))
        # 웹툰 에피소드 뷰어 url

        # 이미지 태그 목록 가져오기
        img_list = get_img_tag_list()

        # 리스트를 순회하며 각 img태그의 src속성을 출력 및 다운로드
        for index, img in enumerate(img_list):
            # 이미지 주소에 get요청
            headers = {'Referer': url_detail}
            response = requests.get(img['src'], headers=headers)

            # 요청 결과 (이미지파일)의 binary데이터를 파일에 쓴다
            img_path = '{}/{:02}.jpg'.format(
                dir_path,
                index
            )
            with open(img_path, 'wb') as f:
                f.write(response.content)

        # 해당 에피소드를 볼 수 있는 HTML파일을 생성
        with open('{}/{:03}.html'.format(self.webtoon_title, episode_num), 'wt') as f:
            f.write('<html>\n')
            for i in range(len(img_list)):
                f.write('\t<img src="{:03}/{:02}.jpg"><br>\n'.format(episode_num, i))
            f.write('</html>')

        print('에피소드 {}화 저장 완료'.format(episode_num))



    def crawl_all_episode(self):
        episode_num = len(self.crawl_list_page(1,100))
        for i in range(1,episode_num+1):
            self.crawl_episode(i)
        print('')
        print('모든 에피소드 저장완료')


    def get_info(self):
        html = self.get_html_from_url(self._url_list_base, self.params_episode_list(self.webtoon_id, 1))
        soup = BeautifulSoup(html, 'html.parser')
        webtoon_info = soup.select_one('div.comicinfo').find('div',class_='detail').find('h2')
        webtoon_title = webtoon_info.contents[0].strip()
        webtoon_author = webtoon_info.find('span',class_="wrt_nm").text.strip()
        return [webtoon_title, webtoon_author]

    @property
    def webtoon_title(self):
        return self._webtoon_title

    @webtoon_title.setter
    def webtoon_title(self,new_webtoon_title):
        self._webtoon_title = new_webtoon_title

    @property
    def webtoon_author(self):
        return self._webtoon_author

    @webtoon_author.setter
    def webtoon_author(self, new_webtoon_author):
        self._webtoon_author = new_webtoon_author



            #
        #
        # class NaverWebtoon:
        #     def __init__(self, webtoon_id):
        #         self.webtoon_id = webtoon_id
        #         self.episode_list = []
        #
        #     def get_info(self):
        #         return '정보 리턴'
        #
        #     def view_last_episode(self):
        #         return ''
        #
        #     def view_episode_list(self, num=1):
        #         return ''
        #
        #     def save_webtoon(self, create_html=False):
        #         if create_html:
        #             return '다운받은 웹툰을 볼 수 있는 html까지 생성해서 저장'
        #         return '특정 경로에 웹툰 전체를 다운받아서 저장'











































# class Episode:
#     def __init__(self, thumbnail, title, link, rating, date):
#         self.thumbnail = thumbnail
#         self.__title = title
#         self.link = link
#         self.rating = rating
#         self.date = date
#
#     @property
#     def show_info(self):
#         print('[ 제목:  {} ]  [ 평점:  {}  ]  [ 날짜:  {} ]'.format(self.title, self.rating, self.date))
#         return [self.title, self.rating, self.date]
#
#     @property
#     def show_link(self):
#         return ('http://comic.naver.com/' + self.link)
#
#     @property
#     def title(self):
#         return self.__title
