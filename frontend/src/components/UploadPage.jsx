import React, { useState } from "react";

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const uploadDocument = async () => {
    if (!file) return alert("Select a file first!");

    setUploading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/api/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await res.json();
      alert("Upload success!");
    } catch (err) {
      alert("Upload failed");
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  const resetDocuments = async () => {
    if (!confirm("Are you sure? This will delete all uploaded documents.")) return;

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/api/reset`,
        { method: "POST" }
      );

      const data = await res.json();
      alert(data.message);

      // Clear UI
      setFile(null);
    } catch (err) {
      alert("Reset failed");
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Upload Document (PDF / DOCX / TXT)</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadDocument} disabled={uploading}>
        {uploading ? "Uploading..." : "Upload"}
      </button>

      <button style={{ marginLeft: "20px", background: "red", color: "white" }}
        onClick={resetDocuments}
      >
        Reset All Documents
      </button>
    </div>
  );
};

export default UploadPage;
