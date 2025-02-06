from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, FishRecord, User, Tag, FishRecordTag
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import date
import pytz
import re

# 記録のメモからタグを抽出
def extract_tags(memo):
    pattern = r'(?<!\S)#([^\s#]+)(?=\s|$)'
    return re.findall(pattern, memo)

# 記録のメモからタグを強調表示
def highlight_tags(memo):
    pattern = r'(?<!\S)#([^\s#]+)(?=\s|$)'
    return re.sub(pattern, r'<span class="tag">#\1</span>', memo)

# 未使用のタグを削除
def remove_unused_tags():
    unused_tags = Tag.query.outerjoin(FishRecordTag, Tag.tag_id == FishRecordTag.tag_id).filter(FishRecordTag.tag_id == None).all()
    for tag in unused_tags:
        db.session.delete(tag)
    db.session.commit()

# 日本のタイムゾーンを設定
JST = pytz.timezone('Asia/Tokyo')

# タイムゾーンを考慮して日付をフォーマットする
def format_datetime_jst(dt):
    return dt.astimezone(JST).strftime('%Y年 %m月 %d日 %H:%M')

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

upload_folder = './static/uploads'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

default_photo_path = 'default.jpg'

db.init_app(app)

# テーブルが存在しない場合にテーブルを作成
@app.before_request
def create_tables():
    db.create_all()

# 記録一覧を表示
@app.route('/home')
def index():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    user = User.query.get(session['user_id'])
    records = FishRecord.query.filter_by(user_id=user_id).order_by(
        FishRecord.created_at.desc(),
        FishRecord.record_id.desc()
    ).all()
    tags = Tag.query.all()

    for record in records:
        record.created_at_jst = format_datetime_jst(record.created_at)
    
    return render_template('index.html', user=user,records=records, tags=tags)

# 記録を絞り込み・並べ替え
@app.route('/update_record_list', methods=['GET'])
def update_record_list():
    if 'user_id' not in session:
        return jsonify(records=[])

    user_id = session['user_id']
    tag_id = request.args.get('tag_id', type=int)
    sort_id = request.args.get('sort_id', type=int)
    sort_order = request.args.get('sort_order', type=int)

    query = FishRecord.query.filter_by(user_id=user_id)

    if tag_id != 0:
        query = query.join(FishRecordTag).filter(FishRecordTag.tag_id == tag_id)

    if sort_id == 0:
        if sort_order == 0:
            query = query.order_by(
                FishRecord.record_id.desc(),
            )
        else:
            query = query.order_by(
                FishRecord.record_id.asc()
            )
    elif sort_id == 1:
        if sort_order == 0:
            query = query.order_by(
                FishRecord.date.desc(),
                FishRecord.record_id.desc()
            )
        else:
            query = query.order_by(
                FishRecord.date.asc(),
                FishRecord.record_id.asc()
            )
    elif sort_id == 2:
        if sort_order == 0:
            query = query.order_by(
                FishRecord.fish_name.desc(),
                FishRecord.record_id.desc()
            )
        else:
            query = query.order_by(
                FishRecord.fish_name.asc(),
                FishRecord.record_id.asc()
            )
    elif sort_id == 3:
        if sort_order == 0:
            query = query.order_by(
                FishRecord.length.desc(),
                FishRecord.record_id.desc()
            )
        else:
            query = query.order_by(
                FishRecord.length.asc(),
                FishRecord.record_id.asc()
            )
    elif sort_id == 4:
        if sort_order == 0:
            query = query.order_by(
                FishRecord.location.desc(),
                FishRecord.record_id.desc()
            )
        else:
            query = query.order_by(
                FishRecord.location.asc(),
                FishRecord.record_id.asc()
            )

    records = query.all()
    total_records = FishRecord.query.filter_by(user_id=user_id).count()

    records_data = [{
        'record_id': record.record_id,
        'fish_name': record.fish_name,
        'photo_path': record.photo_path,
        'created_at': format_datetime_jst(record.created_at)
    } for record in records]

    response = {
        'total_records': total_records,
        'records': records_data
    }

    return jsonify(response)

# 記録を並べ替え
@app.route('/sort_records', methods=['GET'])
def sort_records():
    if 'user_id' not in session:
        return jsonify(records=[])

    user_id = session['user_id']
    sort_id = request.args.get('tag_id', type=int)

    if sort_id == 0:
        records = FishRecord.query.filter_by(user_id=user_id).order_by(
            FishRecord.created_at.desc(),
            FishRecord.record_id.desc()
        ).all()

    

# 記録の詳細を表示
@app.route('/record/<record_id>')
def view_record(record_id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.query.get(session['user_id'])
    record = FishRecord.query.get_or_404(str(record_id))
    record.memo = highlight_tags(record.memo)
    record.created_at_jst = format_datetime_jst(record.created_at)
    record.updated_at_jst = format_datetime_jst(record.updated_at)
    return render_template('view_record.html', user=user, record=record)

# 新しい記録の作成フォームを表示
@app.route('/create', methods=['GET'])
def show_create_record():
    if 'user_id' not in session:
        return redirect('/')
    user = User.query.get(session['user_id'])
    return render_template('create_record.html', user=user)

# 新しい記録を作成
@app.route('/create', methods=['POST'])
def create_record():
    if 'user_id' not in session:
        return redirect('/')
    new_user_id = session['user_id']

    new_photo = request.files['photo']
    if new_photo:
        filename = secure_filename(new_photo.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        new_photo_path = unique_filename
        new_photo.save(upload_folder + '/' + new_photo_path)
    else:
        new_photo_path = default_photo_path
    
    new_fish_name = request.form['fish_name'] or '無銘の魚'
    new_length = request.form['length'] or 999999
    new_location = request.form['location'] or 'NoData'
    new_date = request.form['date'] or date(1, 1, 1)
    new_memo = request.form['memo'] or 'NoData'

    new_record = FishRecord(
        user_id=new_user_id,
        photo_path=new_photo_path,
        fish_name=new_fish_name,
        length=new_length,
        location=new_location,
        date=new_date,
        memo=new_memo
    )

    db.session.add(new_record)
    db.session.commit()

    tags = extract_tags(new_memo)
    for tag_name in tags:
        tag = Tag.query.filter_by(tag_name=tag_name).first()
        if not tag:
            tag = Tag(tag_name=tag_name)
            db.session.add(tag)
            db.session.commit()
        existing_record_tag = FishRecordTag.query.filter_by(record_id=new_record.record_id, tag_id=tag.tag_id).first()
        if not existing_record_tag:
            new_record_tag = FishRecordTag(record_id=new_record.record_id, tag_id=tag.tag_id)
            db.session.add(new_record_tag)

    db.session.commit()
    return redirect(url_for('index'))

# 記録の編集フォームを表示
@app.route('/edit/<record_id>', methods=['GET'])
def show_edit_record(record_id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.query.get(session['user_id'])
    record = FishRecord.query.get_or_404(str(record_id))
    return render_template('edit_record.html', user=user, record=record)

# 記録を編集
@app.route('/edit/<record_id>', methods=['POST'])
def edit_record(record_id):
    if 'user_id' not in session:
        return redirect('/')
    record = FishRecord.query.get_or_404(str(record_id))

    new_photo = request.files['photo']
    if new_photo:
        filename = secure_filename(new_photo.filename)
        new_photo_path = filename
        new_photo.save(upload_folder + '/' + new_photo_path)
        record.photo_path = new_photo_path
    
    record.fish_name = request.form['fish_name'] or '無銘の魚'
    record.length = request.form['length'] or 999999
    record.location = request.form['location'] or 'NoData'
    record.date = request.form['date'] or date(1, 1, 1)
    record.memo = request.form['memo'] or 'NoData'
    record.updated_at = db.func.now()

    db.session.commit()

    FishRecordTag.query.filter_by(record_id=record.record_id).delete()

    tags = extract_tags(record.memo)
    for tag_name in tags:
        tag = Tag.query.filter_by(tag_name=tag_name).first()
        if not tag:
            tag = Tag(tag_name=tag_name)
            db.session.add(tag)
            db.session.commit()
        existing_record_tag = FishRecordTag.query.filter_by(record_id=record.record_id, tag_id=tag.tag_id).first()
        if not existing_record_tag:
            new_record_tag = FishRecordTag(record_id=record.record_id, tag_id=tag.tag_id)
            db.session.add(new_record_tag)

    db.session.commit()

    remove_unused_tags()

    return redirect(url_for('index'))

# 記録を削除
@app.route('/record/<record_id>/delete', methods=['POST'])
def delete_record(record_id):
    if 'user_id' not in session:
        return redirect('/')
    record = FishRecord.query.get_or_404(str(record_id))

    db.session.delete(record)
    db.session.commit()

    remove_unused_tags()

    return redirect(url_for('index'))

# アカウント情報を表示
@app.route('/account', methods=['GET'])
def account():
    if 'user_id' not in session:
        return redirect('/')
    user = User.query.get(session['user_id'])
    return render_template('account.html', user=user)

# パスワードを変更
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

# ログアウト
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

# アカウントを削除
@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']

    FishRecord.query.filter_by(user_id=user_id).delete()

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    remove_unused_tags()

    session.pop('user_id', None)
    return redirect('/')

# 認証画面を表示
@app.route('/', methods=['GET'])
def authentication():
    return render_template('authentication.html')

# 新規アカウント登録
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

# ログイン
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
