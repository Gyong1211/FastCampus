from naver import *

# webtoon = NaverWebtoonCrawler('678499')
# # webtoon.crawl_episode()
# print(webtoon.get_info())


while True:
    print('\n\n=======Naver Webtoon Crawler=======\n\n')
    webtoon_id = input('수집하실 웹툰의 titleId를 입력해주세요 (종료:0)\n>>>>')
    print('\n\n')
    if webtoon_id == '0':
        print('===== 종료합니다 =====\n')
        break
    webtoon = NaverWebtoonCrawler(webtoon_id)
    [webtoon.webtoon_title, webtoon.webtoon_author] = webtoon.get_info()
    print('선택하신 웹툰의 정보\n[제목 : {}    작가: {}]'.format(webtoon.webtoon_title, webtoon.webtoon_author))

    while True:
        choice = input("\n\n======== 기능 선택 메뉴 ========\n"
                       "1. 전체 에피소드 리스트 보기\n"
                       "2. 특정 페이지의 에피소드 리스트 보기\n"
                       "3. 전체 에피소드 저장\n"
                       "4. 특정 에피소드 저장\n"
                       "0. 웹툰 선택으로 되돌아가기\n")
        if choice == '0':
            break

        elif choice =='1':
            print('\n전체 에피소드 리스트를 출력합니다.\n')
            all_episode_list = webtoon.crawl_list_page()
            for episode in all_episode_list:
                print(episode)
            input('\n기능 선택 메뉴로 돌아가시려면 아무 문자나 입력하세요.\n')

        elif choice =='2':
            page_num_input = input('\n에피소드 리스트를 출력할 페이지를 입력하세요.\n'
                                  '숫자를 하나만 입력하면 해당하는 페이지의 에피소드 리스트를,\n'
                                  '1,3과 같이 입력하면 1~3페이지의 에피소드 리스트를 불러옵니다.\n')
            if ',' in page_num_input:
                page_number = page_num_input.split(',')
                start_page_number = int(page_number[0])
                end_page_number = int(page_number[1])
                print('\n==== {} ~ {} 페이지의 에피소드 리스트 ====\n'.format(start_page_number,end_page_number))
                specific_page_episode_list = webtoon.crawl_list_page(start_page_number,end_page_number)

            else:
                page_number = int(page_num_input)
                print('\n==== {} 페이지의 에피소드 리스트 ====\n'.format(page_number))
                specific_page_episode_list = webtoon.crawl_list_page(page_number)

            for episode in specific_page_episode_list:
                print(episode)
            input('\n기능 선택 메뉴로 돌아가시려면 아무 문자나 입력하세요.\n')

        elif choice == '3':
            print('\n전체 에피소드를 저장합니다.\n')
            webtoon.crawl_all_episode()

        elif choice == '4':
            episode_number = int(input('\n저장하실 에피소드를 입력하세요.\n>>>'))
            print('\n지정한 에피소드 {}화를 저장합니다.\n'.format(episode_number))
            webtoon.crawl_episode(episode_number)


        else:
            print('\n잘못된 입력입니다.\n')