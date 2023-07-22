# YoutubeAutoModerator
Youtube配信で
コメント内容から判定して、自動で削除・ブロック・タイムアウトできるプログラムです。

GUIで以下のことを実施すると、Seleniumによって自動でペナルティを実施します。
・削除、ブロック・タイムアウトのどのペナルティを実施するか選択
・ペナルティになる条件(文字数、連投時間、連投回数)を決める
・モデレータ開始ボタンを押す

#事前設定
公開プログラムはFireFoxを使用して自動操作を行っています。
その為、実行するためにはFireFoxをインストールしてください。
https://www.mozilla.org/ja/firefox/new/

またモデレータ権限でログインするため、
cookie情報を取得する必要があります。
以下のサイトを参考にcookie.txtを作成し、ファイル名をyoutube_cookie.txtと変更したうえで実行ファイルと同フォルダに格納してください。
https://self-development.info/%E3%80%90python%E3%80%91selenium%E3%81%A7%E3%82%AF%E3%83%83%E3%82%AD%E3%83%BC%EF%BC%88%E3%83%AD%E3%82%B0%E3%82%A4%E3%83%B3%E6%83%85%E5%A0%B1%EF%BC%89%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B/


#Requirements
pytchat(https://github.com/taizan-hokuto/pytchat)
Selenium(https://www.selenium.dev/)
emoji(https://github.com/carpedm20/emoji/)


#License
MIT



