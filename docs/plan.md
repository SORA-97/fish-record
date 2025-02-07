# 魚記録アプリ

## 機能

**会員登録/ログイン画面**
- 会員登録
- ログイン

**ホーム画面**
- 分類方法の選択
- 分類の選択
- 順序の選択
- 昇順・降順の変更

**アカウント画面**
- パスワード変更
- ログアウト
- アカウント消去

**詳細画面**
- 記録の編集
- 記録の削除

**記録（編集）画面**
- 画像のアップロード・削除
- 名称編集
- 体長編集
- 日付編集
- 場所編集
- メモ編集

## プルダウンボタン内容

**分類方法**
- 全ての記録（分類の設定不可）
- 魚の種類
- 場所
- 時期（1月～12月）

**分類**
- （ユーザが登録した魚・場所、または月）
- 未設定

**順序**
- 新着順
- 名前順
- サイズ順

## テーブル

**ユーザテーブル**
```
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY, -- 自動インクリメントの一意なID
    username TEXT UNIQUE NOT NULL, -- ユニークなユーザー名
    password TEXT NOT NULL        -- パスワード
);
```

**魚テーブル**
```
CREATE TABLE fish_records (
    record_id SERIAL PRIMARY KEY, -- 自動インクリメントの一意なID
    user_id INTEGER NOT NULL REFERENCES users(user_id), -- 外部キー
    photo BYTEA,                -- 画像データ
    fish_name TEXT,             -- 魚の名称
    length REAL CHECK (length > 0), -- 魚の体長（0より大きい場合のみ許可）
    location TEXT,              -- 捕獲場所
    date DATE DEFAULT CURRENT_DATE, -- 日付（デフォルトで現在日）
    memo TEXT,                  -- メモ

    -- CHECK制約: 画像または魚の名前のどちらかは必須
    CHECK (photo IS NOT NULL OR fish_name IS NOT NULL)
);
```