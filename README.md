## <span style="color:rgb(93, 185, 182); ">このファイルは何？</span>
環境構築などの手順と、アプリの概要について記述するファイルです。開発環境の操作方法などについては、`docs/references`を閲覧してください!  

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

## <span style="color:rgb(93, 185, 182); ">ファイル構成</span>
ファイル構成を以下に示します。ファイルに欠け等あって起動できない場合は、リポジトリのオーナーにご確認ください。  

<details><summary>ファイル構成</summary>

```
.env
.gitignore
app/
    __init__.py
    __pycache__/
        __init__.cpython-311.pyc
        main.cpython-311.pyc
        models.cpython-311.pyc
    Dockerfile
    main.py
    models.py
    requirements.txt
    static/
        css/
            account.css
            authentication.css
            create_record.css
            edit_record.css
            index.css
            styles.css
            view_record.css
        js/
            preview.js
            record-list-manager.js
            validate-form.js
        uploads/
    templates/
        account.html
        authentication.html
        create_record.html
        edit_record.html
        index.html
        view_record.html
compose.yml
db/
    Dockerfile
    init-sql/
        create-record.sql
        init-pgcrypto.sql
docs/
    desktop.ini
    figures/
        persona.png
        storyboard.png
    references/
        how_to_docker.md
        links.md
        plan.md
        plan_example.md
README.md
```
</details>

## <span style="color:rgb(93, 185, 182); ">リンク集</span>  
### リモートリポジトリ  
https://github.com/SORA-97/fish-record  

### カンバンボード
https://github.com/users/SORA-97/projects/1/views/1

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