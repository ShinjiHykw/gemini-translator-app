import os
import google.generativeai as genai
from flask import Flask, render_template, request

app = Flask(__name__)

# --- 変更点：環境変数からAPIキーを読み込む ---
# os.environ.get() を使って、Renderに設定したキーを安全に読み込みます。
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("APIキーが設定されていません。環境変数 GEMINI_API_KEY を設定してください。")
genai.configure(api_key=api_key)
# -----------------------------------------

model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""
    original_text = ""
    direction = request.form.get('direction', 'ja_to_zh')

    if request.method == 'POST':
        original_text = request.form.get('text_to_translate', '')

        if original_text:
            if direction == "ja_to_zh":
                prompt = f"以下の日本語の文章を、自然な台湾華語（繁体字）に翻訳してください。\n\n日本語：{original_text}\n\n台湾華語："
            else:
                prompt = f"以下の台湾華語（繁体字）の文章を、自然な日本語に翻訳してください。\n\n台湾華語：{original_text}\n\n日本語："

            response = model.generate_content(prompt)
            translated_text = response.text

    return render_template('index.html',
                           translated_text=translated_text,
                           original_text=original_text,
                           direction=direction)

# Gunicornから実行されるため、この部分はRenderでは使われません
if __name__ == '__main__':
    # ポート番号はRenderが自動で設定するため、hostとportの指定は削除します
    app.run(debug=True)
