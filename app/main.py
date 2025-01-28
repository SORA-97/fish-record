from flask import Flask, render_template, jsonify, request, redirect, url_for
from app.models import db, fish_records, user
from dotenv import load_dotenv
import os
from uuid import UUID

# .envファイルを読み込む
load_dotenv()

# 環境変数からデータベース接続情報を取得
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

app = Flask(__name__)

# SQLAlchemy設定
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

details = {
    "0": [],
    "1": ["サバ", "タイ", "アジ", "マンボウ", "その他"],
    "2": ["池", "川", "海", "その他"],
    "3": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
}

# メモ一覧を表示
@app.route('/')
def index():
    records = fish_records.query.order_by(fish_records.created_at.desc()).all()
    return render_template('index.html', records=records)

# メモ一覧を絞り込み
@app.route('/get_details', methods=['POST'])
def get_details():
    data = request.json
    detail = data.get("option", "")
    if detail in details:
        return jsonify({"details": details[detail]})
    return jsonify({"details": []})

# メモの詳細を表示
@app.route('/record/<record_id>')
def view_record(record_id):
    record = fish_records.query.get_or_404(str(record_id))
    return render_template('view_record.html', record=record)

# 新しいメモの作成フォームを表示
@app.route('/create', methods=['GET'])
def show_create_record():
    return render_template('create_record.html')

# 新しいメモを作成
@app.route('/create', methods=['POST'])
def create_record():
    user_id = 1
    fish_name = request.form['fish_name']
    length = request.form['length']
    location = request.form['location']
    date = request.form['date']
    memo = request.form['memo']
    new_record = fish_records(fish_name=fish_name, user_id=user_id, length=length, location=location, date=date, memo=memo)
    db.session.add(new_record)
    db.session.commit()
    return redirect(url_for('index'))

# メモを削除
@app.route('/record/<record_id>/delete', methods=['POST'])
def delete_record(record_id):
    record = fish_records.query.get_or_404(str(record_id))
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

# 新しいメモの作成フォームを表示
@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
