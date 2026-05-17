from openai import OpenAI
from flask import Flask, render_template, request, session
import os

app = Flask(__name__)
app.secret_key = '123456'

# ✅ 从环境变量读取 API KEY（安全）
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.siliconflow.cn/v1"
)

@app.route('/', methods=['GET', 'POST'])
def home():
    # 初始化聊天记录
    if 'messages' not in session:
        session['messages'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']

        # 调用 AI
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": "system", "content": "你是一个简洁、自然、像真人聊天的助手，说话不要太官方。"},
                {"role": "user", "content": user_input}
            ]
        )

        ai_reply = response.choices[0].message.content

        # 存聊天记录
        session['messages'].append({"role": "user", "content": user_input})
        session['messages'].append({"role": "ai", "content": ai_reply})

        session.modified = True

    return render_template("index.html", messages=session['messages'])


if __name__ == '__main__':
    app.run(debug=True)