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
    photo_path TEXT NOT NULL DEFAULT 'default.jpg',
    fish_name TEXT NOT NULL DEFAULT '無銘の魚',
    length REAL NOT NULL DEFAULT 999999 CHECK (length > 0),
    location TEXT NOT NULL DEFAULT 'NoData',
    date DATE NOT NULL DEFAULT '0001-01-01',
    memo TEXT NOT NULL DEFAULT 'NoData',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ダミーデータ挿入
INSERT INTO users (user_name, password) VALUES
('user1', 'password1'),
('user2', 'password2'),
('user3', 'password3');

INSERT INTO fish_records (user_id, photo_path, fish_name, length, location, date, memo, created_at, updated_at) VALUES
(1, DEFAULT, 'サクラマス', 50.0, '北海道', '2021-01-01', 'メモ1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, DEFAULT, 'ニジマス', 30.0, '北海道', '2021-01-02', 'メモ2', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, DEFAULT, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, DEFAULT, 'マンボウ', 60.0, '北海道', '2021-01-03', 'メモ3', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, DEFAULT, 'サメ', 40.0, '北海道', '2021-01-04', 'メモ4', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, DEFAULT, 'ながぐつ', 70.0, '北海道', '2021-01-05', 'メモ5', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, DEFAULT, 'タイヤ', 50.0, '北海道', '2021-01-06', 'メモ6', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

UPDATE users SET password = 'scrypt:32768:8:1$TB4EdHmyhKDTEXDv$121dace93d5193d1e7ea38bd82e17ad2768a2a3240e0f0c1c0fcc383a099c27ce0ebfe7901548911f3d3de91fc628b135a6862ca742c572db5cad8c8fae38dda' WHERE user_name = 'user1';
UPDATE users SET password = 'scrypt:32768:8:1$pZbQur0NFnAHY8bv$03a037c02f5e19384a5b0bedd72ebab5d8f33807ef1cccfccd7d46d1c3d201eb24efab9df90b358ccb8b9a93034142a9c41bd331e0f0710bf221330b9d0be262' WHERE user_name = 'user2';
UPDATE users SET password = 'scrypt:32768:8:1$FEOjOC8SXz8ZTChX$21d982dbc724b69141194fb88515b75e4357a0becc2025b97713f0d4c4a6715241e6d45c8d4ab1f55f2aaf79a875364fc816c774f62c95775e16e2583ae6d495' WHERE user_name = 'user3';
