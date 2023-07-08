import pytchat
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

#使用ツール : pytchat
#URL : https://github.com/taizan-hokuto/pytchat
#pip install pytchat　を使用してインストールできます。

#使用ツール : selenium
#URL : https://www.selenium.dev/ja/documentation/
#pip install selenium　を使用してインストールできます。
#また、自動操作にfirefoxを使用して自動化しています。
#firefoxをインストールし、seleeniumの記事を参考にWebDriverを取得してください。

def main():
    #以下のIDは配信ごとに変更してください。
    #
    video_id = "cz9wZFxJ9g4"

    #モデレーターアクション ボタンの表示テキストで判定しています。
    # (Youtubeの表示が変わった場合は、この文字列を編集すると使えるはず)
    delStr = "削除"
    timeoutStr = "ユーザーをタイムアウトにする"
    blockStr = "このチャンネルのユーザーを表示しない"


    #seleniumの準備
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    #channelURLを開く
    strURL = "https://www.youtube.com/watch?v=" + video_id
    #print(f"{strURL} ")
    print(f"{strURL}")
    driver.get(str(strURL))

    #あらかじめcookieを用意し、読み込んで使用することでログインする
    #cookieの取得方法は以下の方法を参考にしています。
    #https://self-development.info/%E3%80%90python%E3%80%91selenium%E3%81%A7%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BC%EF%BC%88%E3%83%AD%E3%82%B0%E3%82%A4%E3%83%B3%E6%83%85%E5%A0%B1%EF%BC%89%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B/
    json_open = open('youtube_cookie.txt', 'r')
    cookies = json.load(json_open)
    for cookie in cookies:
        tmp = {"name": cookie["name"], "value": cookie["value"]}
        driver.add_cookie(tmp)

    #チャット表示URLに遷移する(こうしないとチャット操作エレメントが取れない)
    strChatURL = "https://www.youtube.com/live_chat?is_popout=1&v=" + video_id
    driver.get(str(strChatURL))

    #表示を上位チャットからチャットに切り替える
    selectChatType = '/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/yt-live-chat-header-renderer/div[1]/span[2]/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/div/tp-yt-paper-button/div'
    driver.find_element(By.XPATH, selectChatType).click()
    time.sleep(3)
    chatNormal = '/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/yt-live-chat-header-renderer/div[1]/span[2]/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/tp-yt-iron-dropdown/div/div/tp-yt-paper-listbox/a[2]'
    driver.find_element(By.XPATH, chatNormal).click()

    livechat = pytchat.create(video_id)
    while livechat.is_alive():

        # チャットデータの取得
        chatdata = livechat.get()
        for c in chatdata.items:
            #以下の文は自分の好きなようにアルゴリズムを作成してください。
            #例として、コメントが150文字以上を削除しています。
            if len(c.message)>150:   #コメントが150文字以上
                #情報確認用
                #print(f"{c.id} {c.author.channelUrl} {c.datetime} {c.author.name} {c.messageEx} {c.amountString}"

                #対象のコメントに対してidを検索してエレメントを取得する
                comment_id = '//*[@id=\"' + c.id + '\"]'
                num_of_comment = driver.find_element(By.XPATH, comment_id).click()

                #actionStr = '//*[@id="items"]/ytd-menu-navigation-item-renderer' #『チャンネル』へを押したい場合はこのXPathを取得してください
                actionStr = '/html/body/yt-live-chat-app/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer'
                action_elements =  driver.find_elements(By.XPATH, actionStr)
                for action_element in action_elements:
                    #ボタンの中から削除ボタンを選んで押しています。
                    if(action_element.text == delStr):
                        action_element.click()
                    """非表示にしたい場合は上2行のif文を以下のように変更することで実現できます
                    if(action_element.text == blockStr):
                        action_element.click()
                    """
                    """タイムアウトにしたい場合はこちら
                    if(action_element.text == timeoutStr):
                        action_element.click()
                    """


        time.sleep(3)
    print("自動ブロック終了")
    driver.quit()
    return 0


main()