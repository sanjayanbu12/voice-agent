import React from "react";

export default function LandingPage({ onStart }) {
  return (
    <div className="upload-area">
      <h2>Welcome to RAG Voice Bot</h2>
      <p>Upload a document and ask questions — the bot will answer using only the uploaded document.</p>
      <div style={{marginTop:12}}>
        <button className="btn" onClick={onStart}>Start Chat</button>
      </div>
    </div>
  );
}
