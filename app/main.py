from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, fish_records, User
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
app.secret_key = 'your_secret_key'  # セッション管理のためのキー

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
    if 'user_id' not in session:
        return redirect('/login')  # ログインしていない場合はログインページへ
    
    user_id = session['user_id']
    records = fish_records.query.filter_by(user_id=user_id).order_by(fish_records.created_at.desc()).all()
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

# アカウントページを表示
@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html')

# ログイン画面を表示（最初の画面にするべき）
@app.route('/log_in', methods=['GET'])
def log_in():
    return render_template('log_in.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 既にユーザー名が存在するか確認
        existing_user = User.query.filter_by(user_name=username).first()
        if existing_user:
            return render_template('log_in.html', register_error_message="このユーザ名は既に使用されています。")

        # パスワードをハッシュ化してDBに保存
        hashed_password = generate_password_hash(password)
        new_user = User(user_name=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.user_id  # ユーザーIDをセッションに保存
        return render_template('index.html', welcome_message="会員登録されました。")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ユーザー検索
        user = User.query.filter_by(user_name=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id  # ユーザーIDをセッションに保存
            return redirect('/')  # ログイン成功後、トップページへリダイレクト
        if user:
            return render_template('log_in.html', login_error_message="パスワードが違います。")
        else:
            return render_template('log_in.html', login_error_message="このユーザ名は存在しません。")

    return render_template('log_in.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
