/**
 * Document upload page.
 */
import { useState } from "react";
import DocumentUploader from "../components/DocumentUploader";
import "../pages/upload.css";

const Upload = () => {
  const [uploadedDocuments, setUploadedDocuments] = useState([]);

  const handleUploadComplete = (data) => {
    console.log("Upload complete:", data);
    // Add to uploaded documents list
    setUploadedDocuments((prev) => [
      ...prev,
      {
        id: Date.now(),
        ...data,
        uploadedAt: new Date().toISOString(),
      },
    ]);
  };

  return (
    <div className="upload-page">
      <div className="page-header">
        <h1>Upload Documents</h1>
        <p>Upload policy documents and other files for analysis</p>
      </div>

      <div className="upload-content">
        <div className="upload-section">
          <DocumentUploader onUploadComplete={handleUploadComplete} />
        </div>

        {uploadedDocuments.length > 0 && (
          <div className="uploaded-documents">
            <h2>Uploaded Documents</h2>
            <div className="documents-list">
              {uploadedDocuments.map((doc) => (
                <div key={doc.id} className="document-item">
                  <div className="document-icon">📄</div>
                  <div className="document-info">
                    <p className="document-name">{doc.filename || "Document"}</p>
                    <p className="document-date">
                      Uploaded: {new Date(doc.uploadedAt).toLocaleString()}
                    </p>
                  </div>
                  <div className="document-status">
                    <span className="status-badge status-success">Ready</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Upload;

