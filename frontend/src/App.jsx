import "./App.css";
import { useState } from "react";

function App() {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);

  const [result, setResult] = useState("Awaiting Verification...");
  const [loading, setLoading] = useState(false);

  const verifySignature = async () => {
    if (!image1 || !image2) {
      alert("Please upload both signatures");
      return;
    }

    const formData = new FormData();
    formData.append("image1", image1);
    formData.append("image2", image2);

    try {
      setLoading(true);
      setResult("Verifying...");

      const response = await fetch("http://127.0.0.1:5000/verify", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setResult(
        `${data.result} (${(data.prediction_score * 100).toFixed(2)}%)`
      );
    } catch (error) {
      console.error(error);
      setResult("Server Error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <div className="logo">
          ✍ Signature Verification System
        </div>

        <h1>
          Signature <span>Verification</span>
        </h1>

        <p className="subtitle">
          Upload two signature images and verify authenticity using
          AI-powered Siamese Neural Network
        </p>

        <div className="upload-section">
          <div className="upload-box">
            <h3>Signature Image 1</h3>

            <input
              type="file"
              accept="image/*"
              onChange={(e) => setImage1(e.target.files[0])}
            />
          </div>

          <div className="upload-box">
            <h3>Signature Image 2</h3>

            <input
              type="file"
              accept="image/*"
              onChange={(e) => setImage2(e.target.files[0])}
            />
          </div>
        </div>

        <button
          className="verify-btn"
          onClick={verifySignature}
        >
          {loading ? "Verifying..." : "Verify Signature"}
        </button>

        <div className="result-box">
          <h3>Verification Result</h3>

          <div className="result-status">
            {result}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;