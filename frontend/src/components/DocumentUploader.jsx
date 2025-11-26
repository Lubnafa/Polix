/**
 * DocumentUploader component for uploading PDFs and documents.
 */
import { useState } from "react";
import "./DocumentUploader.css";

const DocumentUploader = ({ onUploadComplete }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (selectedFile) => {
    // Check file type
    const allowedTypes = [
      "application/pdf",
      "text/plain",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      setUploadStatus({
        type: "error",
        message: "Please upload a PDF, TXT, or DOC file.",
      });
      return;
    }

    // Check file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (selectedFile.size > maxSize) {
      setUploadStatus({
        type: "error",
        message: "File size must be less than 10MB.",
      });
      return;
    }

    setFile(selectedFile);
    setUploadStatus(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setUploadStatus(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      // Upload to backend
      const response = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      setUploadStatus({
        type: "success",
        message: "Document uploaded successfully!",
      });

      // Call callback if provided
      if (onUploadComplete) {
        onUploadComplete(data);
      }

      // Reset file after successful upload
      setTimeout(() => {
        setFile(null);
        setUploadStatus(null);
      }, 2000);
    } catch (error) {
      console.error("Upload error:", error);
      setUploadStatus({
        type: "error",
        message: "Failed to upload document. Please try again.",
      });
    } finally {
      setUploading(false);
    }
  };

  const handleRemove = () => {
    setFile(null);
    setUploadStatus(null);
  };

  return (
    <div className="document-uploader">
      <div className="uploader-header">
        <h2>Upload Document</h2>
        <p>Upload PDF, TXT, or DOC files for analysis</p>
      </div>

      <div
        className={`upload-area ${dragActive ? "drag-active" : ""} ${
          file ? "has-file" : ""
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {file ? (
          <div className="file-preview">
            <div className="file-icon">📄</div>
            <div className="file-info">
              <p className="file-name">{file.name}</p>
              <p className="file-size">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
            <button className="remove-button" onClick={handleRemove}>
              ✕
            </button>
          </div>
        ) : (
          <>
            <div className="upload-icon">📤</div>
            <p className="upload-text">
              Drag and drop your file here, or click to browse
            </p>
            <input
              type="file"
              id="file-input"
              className="file-input"
              onChange={handleFileChange}
              accept=".pdf,.txt,.doc,.docx"
            />
            <label htmlFor="file-input" className="browse-button">
              Browse Files
            </label>
          </>
        )}
      </div>

      {uploadStatus && (
        <div
          className={`upload-status upload-status-${uploadStatus.type}`}
        >
          {uploadStatus.message}
        </div>
      )}

      {file && (
        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={uploading}
        >
          {uploading ? "Uploading..." : "Upload Document"}
        </button>
      )}
    </div>
  );
};

export default DocumentUploader;

