from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.conversation import router as conversation_router
from app.db.session import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Icarus Mini")

app.include_router(chat_router)
app.include_router(health_router)
app.include_router(conversation_router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Icarus Mini</title>
    </head>
    <body>
        <h1>Icarus Mini</h1>

        <select id="model">
            <option value="qwen3.7-max">
                Qwen3.7-Max
            </option>

            <option value="deepseek-v4-flash">
                DeepSeek-V4-Flash
            </option>
        </select>

        <br><br>

        <textarea
            id="message"
            rows="4"
            cols="50"
            placeholder="输入你的问题">
        </textarea>

        <br>

        <button onclick="sendMessage()">
            发送
        </button>

        <h3>AI 回复：</h3>
        <div id="reply"></div>

       <script>
            const messages = [];

            async function sendMessage() {
                const messageInput = document.getElementById("message");
                const modelSelect = document.getElementById("model");
                const replyDiv = document.getElementById("reply");

                const message = messageInput.value;
                const model = modelSelect.value;

                messages.push({
                    role: "user",
                    content: message
                });

                replyDiv.innerText = "";

                const response = await fetch("/api/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        messages: messages,
                        model: model
                    })
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");

                let assistantReply = "";

                while (true) {
                    const { done, value } = await reader.read();

                    if (done) {
                        break;
                    }

                    const chunk = decoder.decode(value, { stream: true });
                    assistantReply += chunk;
                    replyDiv.innerText = assistantReply;
                }

                messages.push({
                    role: "assistant",
                    content: assistantReply
                });

                messageInput.value = "";
            }
</script>
    </body>
    </html>
    """