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

CREATE TABLE IF NOT EXISTS tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fish_record_tags (
    record_id INTEGER NOT NULL REFERENCES fish_records(record_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (record_id, tag_id)
);

-- ダミーデータ挿入
INSERT INTO users (user_name, password) VALUES
('user1', 'password1'),
('user2', 'password2'),
('user3', 'password3');

INSERT INTO fish_records (user_id, photo_path, fish_name, length, location, date, memo, created_at, updated_at) VALUES
(1, 'samples/5_1.jpg', 'クロダイ', 45.0, '神奈川県 横浜港', '2021-01-01', '#海水魚 はじめての釣果！', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'samples/021.jpg', '長靴', 30.0, '東京都 多摩川', '2021-01-02', '#釣りの副産物', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'samples/306_1.jpg', 'キハダ', 150.0, '静岡県 焼津港', '2021-01-03', '#海水魚 大物ゲット', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'samples/550_1.jpg', 'ヒラメ', 70.0, '千葉県 館山港', '2021-01-04', '#海水魚 美味しい魚', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'samples/645_1.jpg', 'カタクチイワシ', 15.0, '神奈川県 江ノ島', '2021-01-05', '#海水魚 小さいけどたくさん釣れた', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'samples/790_1.jpg', 'マダコ', 50.0, '神奈川県 三浦半島', '2021-01-06', '#海水魚 タコ釣り初挑戦', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'samples/816_1.jpg', 'イトウ', 100.0, '北海道 釧路川', '2021-01-07', '#淡水魚 希少な魚', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'samples/931_1.jpg', 'サクラマス', 60.0, '北海道 石狩川', '2021-01-08', '#淡水魚 美しい魚', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, DEFAULT, 'マンボウ', 60.0, '北海道', '2021-01-03', 'メモ3', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, DEFAULT, 'サメ', 40.0, '北海道', '2021-01-04', 'メモ4', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, DEFAULT, 'ながぐつ', 70.0, '北海道', '2021-01-05', 'メモ5', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, DEFAULT, 'タイヤ', 50.0, '北海道', '2021-01-06', 'メモ6', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO tags (tag_name) VALUES
('海水魚'),
('淡水魚'),
('釣りの副産物');

INSERT INTO fish_record_tags (record_id, tag_id) VALUES
(1, 1),
(2, 3),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 2),
(8, 2);

UPDATE users SET password = 'scrypt:32768:8:1$TB4EdHmyhKDTEXDv$121dace93d5193d1e7ea38bd82e17ad2768a2a3240e0f0c1c0fcc383a099c27ce0ebfe7901548911f3d3de91fc628b135a6862ca742c572db5cad8c8fae38dda' WHERE user_name = 'user1';
UPDATE users SET password = 'scrypt:32768:8:1$pZbQur0NFnAHY8bv$03a037c02f5e19384a5b0bedd72ebab5d8f33807ef1cccfccd7d46d1c3d201eb24efab9df90b358ccb8b9a93034142a9c41bd331e0f0710bf221330b9d0be262' WHERE user_name = 'user2';
UPDATE users SET password = 'scrypt:32768:8:1$FEOjOC8SXz8ZTChX$21d982dbc724b69141194fb88515b75e4357a0becc2025b97713f0d4c4a6715241e6d45c8d4ab1f55f2aaf79a875364fc816c774f62c95775e16e2583ae6d495' WHERE user_name = 'user3';