from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, fish_records, User
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
import uuid

# .envファイルを読み込む
load_dotenv()

# 環境変数からデータベース接続情報を取得
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
@app.route('/home')
def index():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    records = fish_records.query.filter_by(user_id=user_id).order_by(fish_records.created_at.desc()).all()
    return render_template('index.html', records=records)

# メモ一覧を絞り込み
@app.route('/get_details', methods=['POST'])
def get_details():
    if 'user_id' not in session:
        return redirect('/')
    data = request.json
    detail = data.get("option", "")
    if detail in details:
        return jsonify({"details": details[detail]})
    return jsonify({"details": []})

# メモの詳細を表示
@app.route('/record/<record_id>')
def view_record(record_id):
    if 'user_id' not in session:
        return redirect('/')
    record = fish_records.query.get_or_404(str(record_id))
    return render_template('view_record.html', record=record)

# 新しいメモの作成フォームを表示
@app.route('/create', methods=['GET'])
def show_create_record():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create_record.html')

# 新しいメモを作成
@app.route('/create', methods=['POST'])
def create_record():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    photo = request.files['photo']
    if photo:
        filename = secure_filename(photo.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        upload_folder = './static/uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        photo_path = unique_filename
        photo.save(upload_folder + '/' + photo_path)
    else:
        photo_path = None
    
    fish_name = request.form['fish_name']
    length = request.form['length']
    location = request.form['location']
    date = request.form['date']
    memo = request.form['memo']
    new_record = fish_records(fish_name=fish_name, user_id=user_id, length=length, location=location, date=date, memo=memo, photo_path=photo_path)
    db.session.add(new_record)
    db.session.commit()
    return redirect(url_for('index'))

# メモを削除
@app.route('/record/<record_id>/delete', methods=['POST'])
def delete_record(record_id):
    if 'user_id' not in session:
        return redirect('/')
    record = fish_records.query.get_or_404(str(record_id))
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/account', methods=['GET'])
def account():
    if 'user_id' not in session:
        return redirect('/')
    user = User.query.get(session['user_id'])
    return render_template('account.html', user=user)

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect('/')
    user = User.query.get(session['user_id'])
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    if not check_password_hash(user.password, current_password):
        flash("現在のパスワードが違います。", "error")
        return redirect('/account')
    user.password = generate_password_hash(new_password)
    db.session.commit()
    flash("パスワードを変更しました。", "success")
    return redirect('/account')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    fish_records.query.filter_by(user_id=user_id).delete()
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    session.pop('user_id', None)
    return redirect('/')

# ログイン画面を表示
@app.route('/', methods=['GET'])
def authentication():
    return render_template('authentication.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(user_name=username).first()
        if existing_user:
            flash("このユーザ名は既に使用されています。", ("register", "error"))
            return redirect('/')
        hashed_password = generate_password_hash(password)
        new_user = User(user_name=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.user_id
        flash("会員登録されました。", "success")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(user_name=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            flash("ログインしました", "success")
            return redirect(url_for('index'))
        if user:
            flash("パスワードが違います。", ("login", "error"))
            return redirect('/')
        else:
            flash("このユーザ名は存在しません。", ("login", "error"))
            return redirect('/')
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
