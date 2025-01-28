-- テーブル作成
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    user_name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fish_records (
    record_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    photo BYTEA,
    fish_name TEXT,
    length REAL CHECK (length > 0),
    location TEXT,
    date DATE DEFAULT CURRENT_DATE,
    memo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (photo IS NOT NULL OR fish_name IS NOT NULL)
);

-- ダミーデータ挿入
INSERT INTO users (user_name, password) VALUES
('user1', 'password1'),
('user2', 'password2'),
('user3', 'password3');

INSERT INTO fish_records (user_id, photo, fish_name, length, location, date, memo, created_at, updated_at) VALUES
(1, NULL, 'サクラマス', 50.0, '北海道', '2021-01-01', 'メモ1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, NULL, 'ニジマス', 30.0, '北海道', '2021-01-02', 'メモ2', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, NULL, 'マンボウ', 60.0, '北海道', '2021-01-03', 'メモ3', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, NULL, 'サメ', 40.0, '北海道', '2021-01-04', 'メモ4', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, NULL, 'ながぐつ', 70.0, '北海道', '2021-01-05', 'メモ5', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, NULL, 'タイヤ', 50.0, '北海道', '2021-01-06', 'メモ6', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);