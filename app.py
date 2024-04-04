from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# messagesリストをグローバル変数として定義
messages = []


USERS = {
    "まぁさん": "590223",
    "Macnair": "aaa111",
    "seingrent": "abcd007",
    "shadeliver": "good4278",
    "金槌の人魚": "bdo777",
    "亡霊河童": "bdo478",
    "ベトコン": "ramuramu",
    "研修生": "1192",
    "研修生２": "8819",
    "user10": "password10"
}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in USERS and USERS[username] == password:
        session['user_id'] = username
        return redirect(url_for('main_page'))
    else:
        return 'ログイン失敗', 401

@app.route('/main')
def main_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('main_page.html', user_id=session['user_id'])

from datetime import datetime

from datetime import datetime

import requests  # requestsライブラリをインポート

@app.route('/send', methods=['POST'])
def send():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    selected_bosses = request.form.getlist('boss')
    message_text = f'{user_id} からの通知: FB - ' + ', '.join(selected_bosses)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'user_id': user_id,
        'message': message_text,
        'timestamp': timestamp
    }
    # 新しいアプリのエンドポイントにメッセージを送信
    response = requests.post('http://localhost:5001/receive_message', json=data)
    # 送信したメッセージをセッションに保存
    session['last_message'] = message_text
    return redirect(url_for('message_sent'))

@app.route('/send_custom_message', methods=['POST'])
def send_custom_message():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    custom_message = request.form['custom_message']
    message_text = f'{user_id} からのお知らせ: {custom_message}'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'user_id': user_id,
        'message': message_text,
        'timestamp': timestamp
    }
    # 新しいアプリのエンドポイントにメッセージを送信
    response = requests.post('http://localhost:5001/receive_message', json=data)
    # 送信したメッセージをセッションに保存
    session['last_message'] = message_text
    return redirect(url_for('message_sent'))

@app.route('/message_sent')
def message_sent():
    # セッションからメッセージを取得（セッションにメッセージがなければデフォルト値を設定）
    message = session.get('last_message', 'メッセージはありません。')
    # メッセージをテンプレートに渡す
    return render_template('message_sent.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)