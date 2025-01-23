## 魚図鑑  
This is Fish record app.  

## ターミナル操作メモ  
```bash
# イメージのビルド&コンテナの起動  
docker compose up -d  

# Webアプリに接続
http://localhost:3000/  

# 更新
docker compose up --build -d  

# イメージとコンテナを削除  
docker compose down --rmi all  

# ボリュームを削除  
docker compose down --volume
```

## .envファイルの作成
fish-record/.env  
内容を以下のように記入  
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