import pytchat
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import emoji
import PySimpleGUI as sg

#使用ツール : pytchat
#URL : https://github.com/taizan-hokuto/pytchat
#pip install pytchat　を使用してインストールできます。

#使用ツール : selenium
#URL : https://www.selenium.dev/ja/documentation/
#pip install selenium　を使用してインストールできます。
#また、自動操作にfirefoxを使用して自動化しています。
#firefoxをインストールし、seleeniumの記事を参考にWebDriverを取得してください。


# 空文字かどうかを確認する関数
# notを使うことで、str型をbool型として判定する
def is_empty_string(string):
    return not string

def main(videoID, actType, strActCount, strRepeat, strTimeInterval):
    #以下のIDは配信ごとに変更してください。
    #
    video_id = videoID

    #モデレーターアクション ボタンの表示テキストで判定しています。
    # (Youtubeの表示が変わった場合は、この文字列を編集すると使えるはず)
    delStr = "削除"
    timeoutStr = "ユーザーをタイムアウトにする"
    blockStr = "このチャンネルのユーザーを表示しない"
    SlectActStr = ""
    match actType:
        case -1:
            print("選択ができませんでした。アプリを終了します。")
            driver.quit()
            return 0
        case 0:
            SlectActStr = delStr
        case 1:
            SlectActStr = timeoutStr
        case 2:
            SlectActStr = blockStr
    print("次の処理を実行します：" + SlectActStr)
    print("実行文字数："+ str(strActCount))

    #seleniumの準備
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    #channelURLを開く
    #strURL = "https://www.youtube.com/watch?v=" + video_id

    strChatURL = "https://www.youtube.com/live_chat?is_popout=1&v=" + video_id
    #print(f"{strURL} ")
    print(f"{strChatURL}")
    driver.get(str(strChatURL))
    driver.implicitly_wait(5)

    #あらかじめcookieを用意し、読み込んで使用することでログインする
    #cookieの取得方法は以下の方法を参考にしています。
    #https://self-development.info/%E3%80%90python%E3%80%91selenium%E3%81%A7%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BC%EF%BC%88%E3%83%AD%E3%82%B0%E3%82%A4%E3%83%B3%E6%83%85%E5%A0%B1%EF%BC%89%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B/
    json_open = open('youtube_cookie.txt', 'r')
    cookies = json.load(json_open)
    for cookie in cookies:
        tmp = {"name": cookie["name"], "value": cookie["value"]}
        driver.add_cookie(tmp)
    driver.implicitly_wait(5)

    #チャット表示URLに遷移する(こうしないとチャット操作エレメントが取れない)
    driver.get(str(strChatURL))
    driver.implicitly_wait(5)


    #表示を上位チャットからチャットに切り替える
    selectChatType = '/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/yt-live-chat-header-renderer/div[1]/span[2]/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/div/tp-yt-paper-button/div'
    try:
        driver.find_element(By.XPATH, selectChatType).click()
    except:
        print("チャットを使用できないため、アプリを終了します。ライブ中のVideoIDを正しく入力しているか、確認してください")
        driver.quit()
        return 0

    time.sleep(2)
    chatNormal = '/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/yt-live-chat-header-renderer/div[1]/span[2]/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/tp-yt-iron-dropdown/div/div/tp-yt-paper-listbox/a[2]'
    driver.find_element(By.XPATH, chatNormal).click()

    actUser_dict = {}
    livechat = pytchat.create(video_id)
    while livechat.is_alive():
        #ブラウザが閉じられたかどうかを検知し、ブラウザが閉じられたら終了する。
        #コメント欄にあるチャット表示を参照し、存在しない場合は操作用ブラウザが存在しないと判断し、終了する。
        try:
            driver.find_element(By.XPATH, selectChatType)
        except:
            print("操作用ブラウザが存在しないため、プログラムを終了します。")
            break

        # チャットデータの取得
        chatdata = livechat.get()
        for c in chatdata.items:
            #以下の文は自分の好きなようにアルゴリズムを作成してください。
            #例として、コメントが150文字以上を削除しています。

            #絵文字も1文字としてカウントする
            messageStr = emoji.emojize(c.message)
            if len(messageStr)>strCount:   #コメントが150文字以上
                #情報確認用
                #print(f"{c.id} {c.author.channelUrl} {c.datetime} {c.timestamp} {c.author.name} {messageStr} {c.amountString} {is_empty_string(c.amountString)}")

                #コメントの内容がスーパーチャットの時は無視する(以下の処理がなくても削除はされないが、処理に時間がかかる)
                if(is_empty_string(c.amountString) == False):
                    continue

                #検索して存在するか
                if c.author.channelUrl not in actUser_dict:
                    actUser_dict[c.author.channelUrl] = [int(1),c.timestamp]
                    #print(f"キー追加：{actUser_dict[c.author.channelUrl]}")
                else:
                    #前回の間隔を超えていたら1カウント、間隔ないなら+カウント
                    beforeData = actUser_dict[c.author.channelUrl]
                    #print(f"前キー確認：{beforeData},{beforeData[0]},{beforeData[1]}")
                    if  c.timestamp - int(beforeData[1]) < strTimeInterval*1000:
                        cnt = beforeData[0] + 1
                        actUser_dict[c.author.channelUrl] = [cnt,c.timestamp]
                        print(f"{cnt}回目の更新：{c.author.name}")
                    else:
                        actUser_dict[c.author.channelUrl] = [int(1),c.timestamp]
                        #print(f"キー再設定：{actUser_dict[c.author.channelUrl]}")

                #回数を超えていない場合はペナルティを発生せずに続ける。
                actCount = actUser_dict[c.author.channelUrl]
                #print(f"キー確認：{actUser_dict[c.author.channelUrl]},{actCount},{strRepeat}")
                if strRepeat > int(actCount[0]):
                    continue
                else:
                    #ペナルティが発生したら辞書から削除する
                    print(f"ペナルティ発生：{c.author.name} {c.author.channelUrl}に対してペナルティを実施します")
                    actUser_dict.pop(c.author.channelUrl)

                #対象のコメントに対してidを検索してエレメントを取得する
                comment_id = '//*[@id=\"' + c.id + '\"]/div[2]/yt-icon-button/button/yt-icon/yt-icon-shape/icon-shape/div'
                #TODO クリックする位置を変えてやる必要がある。(コメントを直接クリックしているが、3点リーダー部分をクリックする必要ある
                existComment = False
                for _ in range(5):  #ブラウザに表示される前に選択する場合があるため、待つ
                    try:
                        # 最下部までスクロール
                        try:
                            scrollXPathStr="/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/div[1]/div[3]/div[1]/yt-live-chat-item-list-renderer/div/yt-icon-button/button/yt-icon/yt-icon-shape/icon-shape/div"
                            driver.find_element(By.XPATH, scrollXPathStr).click()
                        except:
                            pass
                        num_of_comment = driver.find_element(By.XPATH, comment_id).click()
                        existComment = True
                    except:
                        time.sleep(1)       #エレメントが実際に表示されるまでは待つ
                    else:
                        break  # 失敗しなかった時はループを抜ける

                if(existComment):
                    #actionStr = '//*[@id="items"]/ytd-menu-navigation-item-renderer' #『チャンネル』へを押したい場合はこのXPathを取得してください
                    actionStr = '/html/body/yt-live-chat-app/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer'
                    action_elements =  driver.find_elements(By.XPATH, actionStr)
                    clickFlag = False
                    for action_element in action_elements:
                        if(action_element.text == delStr):
                            action_element.click()
                            #クリックした場合はフラグをTrueに設定してください。
                            clickFlag = True

                    if(clickFlag == False):
                        #クリックできなかった場合は、ESCキーを入力してポップアップを終了させる
                        #(これがないと次のエレメントが取れない)
                        try:
                            action_element.send_keys(Keys.ESCAPE)
                            print(f"esc")
                        except:
                            print(f"escできませんでした")

                else:
                    print(f"コメントが見つかりませんでした")
        time.sleep(3)
    print("自動ブロック終了")
    driver.quit()
    return 0


#テーマを決めます。
#テーマの種類は、sg.preview_all_look_and_feel_themes()で確認できます。
sg.theme("DarkBlue")
#表示する画面の設定をします。"初期値"はGUIを起動したときにテキストボックスに表示される値です。
layout=[[sg.Text("VideoID(URLの○○○部分[https://www.youtube.com/watch?v=○○○])を入力してください")],
        [sg.Text("VideoID"),sg.InputText("",key="text")],
        [sg.Radio('削除',group_id='action', key='actDel'),sg.Radio('タイムアウト',group_id='action', key='actTimeout', default=True),sg.Radio('非表示',group_id='action', key='actHidden')],
        [sg.Text("コメント文字数条件"),sg.Combo(values=['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '110','120','130','140','150','160','170','180','190'], default_value="150", size=(10, 1), key='strCount', enable_events=True)],
        [sg.Text("繰り返し条件回数    "),sg.Combo(values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], default_value='3', size=(10, 1), key='repeat', enable_events=True)],
        [sg.Text("コメント間隔(秒)     "),sg.Combo(values=['1', '2', '3', '4','5','8','10','15','20','25','30'], default_value='5', size=(10, 1), key='timeInterval', enable_events=True)],
        [sg.Button("モデレーター開始",key="ok")]]

window=sg.Window("YTAutoModerator",layout)

#無限ループで画面を表示します。×ボタンかOKボタンで無限ループを抜けます。OKボタンの場合はテキストボックスの値も取得します。
while True:
    event,values=window.read()
    if event==sg.WIN_CLOSED:
        break
    elif event=="ok":
        videoID=values["text"]
        print("処理中...")
        #ラジオボタンで選択したアクションを行う
        actType = -1
        if values['actDel']==True:
            actType = 0
        if values['actTimeout']==True:
            actType = 1
        if values['actHidden']==True:
            actType = 2
        strCount=int(values['strCount'])
        strRepeat=int(values['repeat'])
        strTimeInterval=int(values['timeInterval'])

        main(videoID,actType,strCount,strRepeat,strTimeInterval)
        break

#画面を閉じます。
window.close()
