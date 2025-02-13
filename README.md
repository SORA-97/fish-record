## <span style="color:rgb(93, 185, 182); ">このファイルは何？</span>
環境構築などの手順と、アプリの概要について記述するファイルです。
アプリケーションの操作は`docs/fish-record-demo.mp4`で解説しています。  
開発環境の操作方法などについては、`docs/references`を閲覧してください!  

## <span style="color:rgb(93, 185, 182); ">魚の記録帳</span>  
日々の釣果を記録する、おさかな特化の日記アプリです。
* 記録の作成・編集・削除ができる！
* 記録にタグをつけて管理できる！
* ユーザごとに記録を閲覧できる！

## <span style="color:rgb(93, 185, 182); ">起動方法(Windows 11環境で検証済)</span>  
0. 事前にDocker Desktopのインストールをお願いします。  
参考:  
https://qiita.com/zembutsu/items/a98f6f25ef47c04893b3

1. `.env`の作成（下記項目を参照）  

2. `fish-record`（このファイルが入っているフォルダ）をターミナルで開く

3. ターミナルで以下のDockerコマンドを実行：  
```bash
docker compose up -d  
```
4. http://localhost:3000/home をブラウザで開き、Webアプリにアクセスする

5. 初回はログインを求められるので、新規会員登録をするか、以下のサンプルユーザでログインする：

```
ID   : user1
pass : password1

ID   : user2
pass : password2

ID   : user3
pass : password3
```

6. 終了するときは、ターミナルで以下のDockerコマンドを実行：
```bash
# イメージとコンテナを削除（記録データは残る）  
docker compose down --rmi all  

# ボリュームを削除（データをリセットしたいなら追加で実行する）  
docker compose down --volume
```

## <span style="color:rgb(93, 185, 182); ">.envファイルの作成</span>
`.env`を`fish-record`の下（このファイルと同じ階層）に作成する必要があります。

内容を以下のように記入してください。  
```
# COMMON
API_PORT=3000
DB_PORT=5432

# PostgreSQL Settings
POSTGRES_USER=guest
POSTGRES_PASSWORD=password
POSTGRES_DB=guest
POSTGRES_HOST=db
```

## <span style="color:rgb(93, 185, 182); ">リンク集</span>  
### リモートリポジトリ  
https://github.com/SORA-97/fish-record  

### カンバンボード
https://github.com/users/SORA-97/projects/1/views/1

### Figma
デザインエディタ（閲覧のみ可能）  
https://www.figma.com/design/sJIGsQbKKmvAbIuJBbLvTl/%E9%AD%9A%E5%9B%B3%E9%91%91?node-id=0-1&t=nmH5fwbsboVWyCrS-1  
プロトタイプ  
https://www.figma.com/proto/sJIGsQbKKmvAbIuJBbLvTl/%E9%AD%9A%E5%9B%B3%E9%91%91?node-id=0-1&t=nmH5fwbsboVWyCrS-1  

### 参考:写真から探せる魚図鑑
サンプルデータにて画像を引用   
https://fishai.jp/  

### 参考:ハウツー長靴釣り - デイリーポータルZ
サンプルデータにて画像を引用  
https://dailyportalz.jp/kiji/150622193882  

### 参考:【作って学ぼう】Flask Webアプリ開発入門 ~課題メモアプリ~  
サンプルを流用  
https://zenn.dev/urassh/books/fec2793bf80acd  


## <span style="color:rgb(93, 185, 182); ">クレジット</span>
### プロジェクトマネージャー 廣橋空
https://github.com/SORA-97

### テクニカルリーダー 河野元要
https://github.com/earcra0106

### ドキュメントリーダー 横山海都
https://github.com/kaison302

### テストリーダー 宇治雅貴
https://github.com/masa785

リリース：2025年2月7日