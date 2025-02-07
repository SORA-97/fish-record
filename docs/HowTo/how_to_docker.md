
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