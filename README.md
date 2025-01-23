## このファイルは何？
環境構築などの手順と、アプリの概要について記述するファイルです。  開発環境の操作方法などについては、`docs/HowTo`を閲覧してください!  

## 魚図鑑  
This is Fish record app.  

## .envファイルの作成
`.env`  

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