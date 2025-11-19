import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function ChatInterface({ docUploaded, onBack }) {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const messagesRef = useRef();

  useEffect(() => {
    messagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendQuery = async (q) => {
    if (!q.trim()) return;
    setMessages(prev => [...prev, { sender: "user", text: q }]);
    setText("");
    setIsThinking(true);
    try {
      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/chat`, { query: q });
      const bot = res.data.response;
      setMessages(prev => [...prev, { sender: "bot", text: bot }]);
      const u = new SpeechSynthesisUtterance(bot);
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
    } catch (e) {
      console.error(e);
      setMessages(prev => [...prev, { sender: "bot", text: "Error contacting server." }]);
    } finally {
      setIsThinking(false);
    }
  };

  const onSend = () => sendQuery(text);

  const onVoice = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return alert("No speech recognition in this browser");
    const rec = new SpeechRecognition();
    rec.lang = "en-US";
    rec.onresult = (ev) => {
      const t = ev.results[0][0].transcript;
      sendQuery(t);
    };
    rec.start();
  };

  return (
    <div>
      <div style={{ marginBottom: 12 }}>
        <button className="btn" onClick={onBack}>Back</button>
      </div>
      <div className="chat-window">
        <div className="messages">
          {!docUploaded && <div style={{ color: "#555" }}>No document uploaded — the bot can still respond but will say "I don't have enough information..." unless you upload a doc first.</div>}
          {messages.map((m, i) => (
            <div key={i} className={`message ${m.sender === "user" ? "user" : "bot"}`}>
              {m.text}
            </div>
          ))}
          {isThinking && <div className="message bot">Thinking...</div>}
          <div ref={messagesRef}></div>
        </div>

        <div className="input-row">
          <input className="input" value={text} onChange={(e) => setText(e.target.value)} placeholder="Type or use voice" />
          <button className="btn" onClick={onSend} disabled={!text.trim()}>Send</button>
          <button className="btn" onClick={onVoice} style={{marginLeft:8}}>Voice</button>
        </div>
      </div>
    </div>
  );
}
