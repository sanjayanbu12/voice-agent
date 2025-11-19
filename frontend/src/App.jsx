import React, { useState } from "react";
import LandingPage from "./components/LandingPage";
import UploadPage from "./components/UploadPage";
import ChatInterface from "./components/ChatInterface";

export default function App() {
  const [page, setPage] = useState("landing");
  const [docUploaded, setDocUploaded] = useState(false);

  return (
    <>
      <header className="header">
        <div style={{fontWeight:700}}>Sanjay Bot — RAG</div>
        <div>
          <button className="btn" onClick={() => setPage("chat")}>Chat</button>
          <button className="btn" style={{marginLeft:12}} onClick={() => setPage("upload")}>Upload</button>
        </div>
      </header>

      <div className="container">
        {page === "landing" && <LandingPage onStart={() => setPage("chat")} />}
        {page === "upload" && <UploadPage onUploaded={() => { setDocUploaded(true); setPage("chat"); }} />}
        {page === "chat" && <ChatInterface docUploaded={docUploaded} onBack={() => setPage("landing")} />}
      </div>
    </>
  );
}
