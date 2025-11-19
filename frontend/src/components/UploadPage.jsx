import React, { useState } from "react";
import axios from "axios";

export default function UploadPage({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) return alert("Choose a file first");
    setLoading(true);
    const fdata = new FormData();
    fdata.append("file", file);
    try {
      await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/upload`, fdata, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      alert("Uploaded successfully");
      onUploaded();
    } catch (e) {
      console.error(e);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-area">
      <h3>Upload document (pdf / docx / txt)</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <div style={{ marginTop: 12 }}>
        <button className="btn" onClick={upload} disabled={loading}>{loading ? "Uploading..." : "Upload"}</button>
      </div>
    </div>
  );
}
