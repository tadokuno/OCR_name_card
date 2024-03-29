from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

@app.route("/callback", methods=['POST'])
def callback():
    # X-Line-Signatureヘッダーから署名を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    print("Request body: " + body)

    # 署名を検証し、ハンドラを呼び出す
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーからのメッセージテキストを取得
    user_message = event.message.text

    # 返信メッセージを送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'受け取ったメッセージ: {user_message}')
    )

if __name__ == "__main__":
    app.run()
