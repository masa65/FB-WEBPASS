from flask import Flask, request, render_template, redirect, session, url_for
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage

app = Flask(__name__)
app.secret_key = 'your_secret_key'

LINE_CHANNEL_ACCESS_TOKEN = 'iXGTnYok1lvGMfgrSvcvd2PleaTdeLjAAiQVT9bBAGG2/bPEnmvB8tB6/VJI9Dbz/SuH+lBcNDIvI+Jr/oN+vAcwhOC7ca8PpXVLTL8hLnYqPPud46zp9pUV+3yxZRnDaq212DbVRgLBz4Y3k5l7TwdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

USERS = {
    "まぁさん": "590223",
    "Macnair": "aaa111",
    "seingrent": "abcd007",
    "Maron": "good4278",
    "金槌の人魚": "bdo777",
    "亡霊河童": "bdo478",
    "チョコサンドクッキー": "ramuramu",
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

@app.route('/send', methods=['POST'])
def send():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    selected_bosses = request.form.getlist('boss')
    message_text = f'{user_id} からの通知: WBボス名 - ' + ', '.join(selected_bosses)
    try:
        line_bot_api.broadcast(TextSendMessage(text=message_text))
    except LineBotApiError as e:
        print(e)
        return 'メッセージ送信失敗', 500
    return redirect(url_for('message_sent'))

@app.route('/send_custom_message', methods=['POST'])
def send_custom_message():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user_id = session['user_id']
    custom_message = request.form['custom_message']
    message_text = f'{user_id} からのカスタムメッセージ: {custom_message}'
    try:
        line_bot_api.broadcast(TextSendMessage(text=message_text))
    except LineBotApiError as e:
        print(e)
        return 'メッセージ送信失敗', 500
    return redirect(url_for('message_sent'))

@app.route('/message_sent')
def message_sent():
    return render_template('message_sent.html')

if __name__ == "__main__":
    app.run(debug=True)