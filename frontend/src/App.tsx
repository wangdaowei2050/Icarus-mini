import { useState, useEffect, useRef } from "react";

const API_BASE = "http://127.0.0.1:8000";

type Role = "user" | "assistant";

interface Message {
  role: Role;
  content: string;
}

interface Conversation {
  id: number;
  title: string;
  created_at: string;
}

export default function App() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeId, setActiveId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [model, setModel] = useState("qwen3.7-max");
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function fetchConversations() {
    const res = await fetch(`${API_BASE}/api/conversations`);
    const data: Conversation[] = await res.json();
    setConversations(data.reverse());
  }

  async function createConversation(): Promise<Conversation> {
    const res = await fetch(`${API_BASE}/api/conversations`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: "新会话" }),
    });
    const data: Conversation = await res.json();
    setConversations((prev) => [data, ...prev]);
    setActiveId(data.id);
    setMessages([]);
    return data;
  }

  async function deleteConversation(id: number, e: React.MouseEvent) {
    e.stopPropagation();
    await fetch(`${API_BASE}/api/conversations/${id}`, { method: "DELETE" });
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeId === id) {
      setActiveId(null);
      setMessages([]);
    }
  }

  async function loadConversation(id: number) {
    setActiveId(id);
    setError(null);
    const res = await fetch(`${API_BASE}/api/conversations/${id}`);
    const data = await res.json();
    setMessages(data.messages ?? []);
  }

  async function sendMessage() {
    if (!input.trim() || streaming) return;

    let conversationId = activeId;
    if (conversationId === null) {
      const conv = await createConversation();
      conversationId = conv.id;
    }

    const userMsg: Message = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg, { role: "assistant", content: "" }]);
    setInput("");
    setStreaming(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_id: conversationId, message: userMsg.content, model }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();
      let reply = "";

      if (reader) {
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          reply += decoder.decode(value, { stream: true });
          setMessages((prev) => [...prev.slice(0, -1), { role: "assistant", content: reply }]);
        }
      }
    } catch {
      setMessages((prev) => prev.slice(0, -1));
      setError("请求失败，请检查后端服务或 API Key。");
    } finally {
      setStreaming(false);
      fetchConversations();
    }
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="layout">
      {/* ── Sidebar ── */}
      <aside className="sidebar">
        <div className="sidebar-header">Icarus Mini</div>

        <button className="btn-new" onClick={createConversation}>
          + 新会话
        </button>

        <nav className="conv-list">
          {conversations.map((c) => (
            <div
              key={c.id}
              className={`conv-item${activeId === c.id ? " active" : ""}`}
              onClick={() => loadConversation(c.id)}
            >
              <span className="conv-title">{c.title}</span>
              <button
                className="btn-delete"
                onClick={(e) => deleteConversation(c.id, e)}
                title="删除会话"
              >
                ×
              </button>
            </div>
          ))}
        </nav>
      </aside>

      {/* ── Main ── */}
      <main className="chat-main">
        {/* Messages */}
        <div className="messages">
          {messages.length === 0 ? (
            <div className="empty-hint">
              <span className="empty-icon">✦</span>
              <span>开始一段对话</span>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`msg-row ${msg.role}`}>
                <div className={`bubble ${msg.role}`}>
                  {msg.content ||
                    (streaming && i === messages.length - 1 ? "▋" : "")}
                </div>
              </div>
            ))
          )}
          <div ref={bottomRef} />
        </div>

        {/* Error banner */}
        {error && (
          <div className="error-banner">
            <span>{error}</span>
            <button className="error-close" onClick={() => setError(null)}>×</button>
          </div>
        )}

        {/* Input */}
        <div className="input-area">
          <div className="input-row">
            <textarea
              className="textarea"
              rows={3}
              placeholder="输入消息，Enter 发送，Shift+Enter 换行…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKeyDown}
            />
            <button
              className="btn-send"
              onClick={sendMessage}
              disabled={streaming || !input.trim()}
            >
              发送
            </button>
          </div>

          <div className="toolbar">
            <span className="label">模型</span>
            <select
              className="model-select"
              value={model}
              onChange={(e) => setModel(e.target.value)}
            >
              <option value="qwen3.7-max">Qwen 3.7 Max</option>
              <option value="deepseek-v4-flash">DeepSeek V4 Flash</option>
            </select>
          </div>
        </div>
      </main>

      <style>{`
        .layout {
          display: flex;
          height: 100svh;
          overflow: hidden;
        }

        /* ── Sidebar ── */
        .sidebar {
          width: 220px;
          flex-shrink: 0;
          border-right: 1px solid var(--border);
          display: flex;
          flex-direction: column;
          padding: 16px 12px;
          gap: 8px;
        }
        .sidebar-header {
          font-size: 15px;
          font-weight: 600;
          color: var(--text-h);
          padding: 4px 8px 12px;
          letter-spacing: -0.3px;
        }
        .btn-new {
          background: var(--accent);
          color: #fff;
          border: none;
          border-radius: 8px;
          padding: 9px 12px;
          font-size: 13px;
          cursor: pointer;
          text-align: left;
          transition: opacity 0.15s;
        }
        .btn-new:hover { opacity: 0.88; }

        .conv-list {
          flex: 1;
          overflow-y: auto;
          display: flex;
          flex-direction: column;
          gap: 2px;
        }
        .conv-item {
          display: flex;
          align-items: center;
          gap: 4px;
          border: 1px solid transparent;
          border-radius: 8px;
          padding: 8px 6px 8px 10px;
          font-size: 13px;
          color: var(--text);
          cursor: pointer;
          transition: background 0.12s, border-color 0.12s;
        }
        .conv-item:hover {
          background: var(--accent-bg);
        }
        .conv-item.active {
          background: var(--accent-bg);
          border-color: var(--accent-border);
          color: var(--text-h);
        }
        .conv-title {
          flex: 1;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .btn-delete {
          flex-shrink: 0;
          background: none;
          border: none;
          color: var(--text);
          font-size: 15px;
          line-height: 1;
          padding: 2px 4px;
          border-radius: 4px;
          cursor: pointer;
          opacity: 0;
          transition: opacity 0.12s, background 0.12s;
        }
        .conv-item:hover .btn-delete { opacity: 0.6; }
        .btn-delete:hover { opacity: 1 !important; background: var(--accent-bg); }

        /* ── Chat main ── */
        .chat-main {
          flex: 1;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }
        .messages {
          flex: 1;
          overflow-y: auto;
          padding: 28px 32px;
          display: flex;
          flex-direction: column;
          gap: 14px;
        }

        .empty-hint {
          margin: auto;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 10px;
          color: var(--text);
          opacity: 0.45;
          font-size: 15px;
        }
        .empty-icon { font-size: 28px; }

        .msg-row { display: flex; }
        .msg-row.user      { justify-content: flex-end; }
        .msg-row.assistant { justify-content: flex-start; }

        .bubble {
          max-width: 68%;
          padding: 11px 16px;
          font-size: 15px;
          line-height: 1.65;
          white-space: pre-wrap;
          word-break: break-word;
          border-radius: 16px;
        }
        .bubble.user {
          background: var(--accent);
          color: #fff;
          border-bottom-right-radius: 4px;
        }
        .bubble.assistant {
          background: var(--code-bg);
          color: var(--text-h);
          border-bottom-left-radius: 4px;
        }

        /* ── Error banner ── */
        .error-banner {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
          margin: 0 24px 4px;
          padding: 10px 14px;
          background: rgba(239, 68, 68, 0.1);
          border: 1px solid rgba(239, 68, 68, 0.35);
          border-radius: 10px;
          font-size: 13px;
          color: #ef4444;
        }
        .error-close {
          background: none;
          border: none;
          color: #ef4444;
          font-size: 16px;
          cursor: pointer;
          padding: 0 2px;
          line-height: 1;
          opacity: 0.7;
        }
        .error-close:hover { opacity: 1; }

        /* ── Input area ── */
        .input-area {
          border-top: 1px solid var(--border);
          padding: 16px 24px;
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .input-row {
          display: flex;
          gap: 10px;
          align-items: flex-end;
        }
        .textarea {
          flex: 1;
          resize: none;
          border: 1px solid var(--border);
          border-radius: 12px;
          padding: 11px 14px;
          font-size: 15px;
          font-family: var(--sans);
          background: var(--bg);
          color: var(--text-h);
          outline: none;
          line-height: 1.5;
          transition: border-color 0.15s;
        }
        .textarea:focus { border-color: var(--accent-border); }
        .textarea::placeholder { color: var(--text); opacity: 0.5; }

        .btn-send {
          background: var(--accent);
          color: #fff;
          border: none;
          border-radius: 12px;
          padding: 11px 22px;
          font-size: 15px;
          cursor: pointer;
          transition: opacity 0.15s;
          white-space: nowrap;
        }
        .btn-send:disabled { opacity: 0.4; cursor: not-allowed; }
        .btn-send:not(:disabled):hover { opacity: 0.88; }

        .toolbar {
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .label {
          font-size: 13px;
          color: var(--text);
        }
        .model-select {
          border: 1px solid var(--border);
          border-radius: 6px;
          padding: 4px 8px;
          font-size: 13px;
          background: var(--bg);
          color: var(--text);
          cursor: pointer;
          outline: none;
        }
        .model-select:focus { border-color: var(--accent-border); }
      `}</style>
    </div>
  );
}
