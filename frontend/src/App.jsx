import { useState } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

function App() {
  // User ka YouTube URL yahan store hoga.
  const [url, setUrl] = useState("");

  // User jo audio/video file select karega, woh yahan store hogi.
  const [file, setFile] = useState(null);

  // Whisper se milne wala complete transcript yahan store hoga.
  const [transcription, setTranscription] = useState("");

  // Mistral se generate hua summary yahan store hoga.
  const [summary, setSummary] = useState("");

  // Whisper audio process/transcribe kar raha ho to true hoga.
  const [loading, setLoading] = useState(false);

  // Mistral summary generate kar raha ho to true hoga.
  const [summaryLoading, setSummaryLoading] = useState(false);

  // Summary ko screen par show/hide karne ke liye.
  const [showSummary, setShowSummary] = useState(false);

  // Transcript ko screen par show/hide karne ke liye.
  const [showTranscript, setShowTranscript] = useState(false);

  // Agar koi error aaye to uska message yahan store hoga.
  const [error, setError] = useState("");

  // YouTube URL ko backend par bhejne ka function.
  const processUrl = async () => {
    // URL empty hai to request backend ko nahi bhejenge.
    if (!url.trim()) {
      setError("Please enter a YouTube URL.");
      return;
    }

    // Naya process start karne se pehle purana result clear kar rahe hain.
    setError("");
    setTranscription("");
    setSummary("");
    setShowSummary(false);
    setShowTranscript(false);

    // Processing indicator start.
    setLoading(true);

    try {
      // FormData ka use karke URL backend ko bhejenge.
      const formData = new FormData();

      formData.append("url", url);

      // Abhi translation off rakhi hai.
      formData.append("translate", "false");

      // FastAPI ke /process-url endpoint ko request bhej rahe hain.
      // /api Vite proxy ke through localhost:8000 par jayega.
      const response = await fetch("/api/process-url", {
        method: "POST",
        body: formData,
      });

      // Backend se JSON response read kar rahe hain.
      const data = await response.json();

      // Agar backend ne error response diya hai to error throw karenge.
      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to process YouTube URL."
        );
      }

      // Backend se mila transcript state mein save kar rahe hain.
      setTranscription(data.transcription || "");

    } catch (err) {
      // Koi error aata hai to console aur UI dono mein show karenge.
      console.error(err);
      setError(
        err.message || "Something went wrong while processing the URL."
      );
    } finally {
      // Request complete hone ke baad loading hata denge.
      setLoading(false);
    }
  };

  // Local audio/video file ko backend par upload karne ka function.
  const uploadFile = async () => {
    // Agar user ne file select nahi ki to request nahi bhejenge.
    if (!file) {
      setError("Please select an audio or video file.");
      return;
    }

    // Purane results clear kar rahe hain.
    setError("");
    setTranscription("");
    setSummary("");
    setShowSummary(false);
    setShowTranscript(false);

    // Upload + Whisper processing start.
    setLoading(true);

    try {
      // File ko FormData ke andar bhejenge.
      const formData = new FormData();

      formData.append("file", file);

      // Translation abhi off hai.
      formData.append("translate", "false");

      // FastAPI ke /upload endpoint ko request bhej rahe hain.
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      // Backend response ko JSON mein convert kar rahe hain.
      const data = await response.json();

      // Backend error handle kar rahe hain.
      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to upload file."
        );
      }

      // Backend se mila transcript React state mein save kar rahe hain.
      setTranscription(data.transcription || "");

    } catch (err) {
      // Upload/process mein error aaye to user ko show karenge.
      console.error(err);
      setError(
        err.message || "Something went wrong while uploading the file."
      );
    } finally {
      // Upload/process complete hone ke baad loading stop.
      setLoading(false);
    }
  };

  // Existing transcript ko Mistral AI ke paas bhejkar summary generate karega.
  const generateSummary = async () => {
    // Transcript nahi hai to summary generate nahi kar sakte.
    if (!transcription.trim()) {
      setError("Please process a meeting first.");
      return;
    }

    // Purana error aur summary clear kar rahe hain.
    setError("");
    setSummary("");
    setShowSummary(false);

    // Summary generation start.
    setSummaryLoading(true);

    try {
      // Transcript ko FormData mein convert karke backend ko bhejenge.
      const formData = new FormData();
      formData.append("transcript", transcription);

      // FastAPI ke /summarize endpoint ko request bhej rahe hain.
      const response = await fetch("/api/summarize", {
        method: "POST",
        body: formData,
      });

      // Backend ka response read kar rahe hain.
      const data = await response.json();

      // Agar summary API error deti hai to error show karenge.
      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to generate summary."
        );
      }

      // Mistral se mila summary state mein save kar rahe hain.
      setSummary(data.summary || "");

    } catch (err) {
      // Summary generation mein error aaye to UI par show karenge.
      console.error(err);
      setError(
        err.message || "Something went wrong while generating summary."
      );
    } finally {
      // Summary generation complete hone ke baad loading stop.
      setSummaryLoading(false);
    }
  };

  return (
    <div className="app">

      {/* App ka heading aur short description */}
      <header className="header">
        <h1>AI V Assistant</h1>

        <p>
          AI-powered Meeting Transcription & Summary
        </p>
      </header>

      <main className="container">

        {/* YouTube URL se meeting process karne wala section */}
        <section className="card">
          <h2>🎥 Process YouTube Meeting</h2>

          <p className="description">
            Paste a YouTube meeting or video URL.
          </p>

          {/* User yahan YouTube URL enter karega */}
          <input
            type="text"
            placeholder="https://www.youtube.com/watch?v=..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={loading || summaryLoading}
          />

          {/* URL backend ko bhejne ka button */}
          <button
            onClick={processUrl}
            disabled={loading || summaryLoading}
          >
            {loading ? "Processing..." : "Process URL"}
          </button>
        </section>

        {/* Local audio/video upload karne wala section */}
        <section className="card">
          <h2>📁 Upload Meeting</h2>

          <p className="description">
            Upload an audio or video meeting file.
          </p>

          {/* User yahan audio/video file select karega */}
          <input
            type="file"
            accept="audio/*,video/*"
            onChange={(e) => setFile(e.target.files[0])}
            disabled={loading || summaryLoading}
          />

          {/* Selected file backend ko bhejne ka button */}
          <button
            onClick={uploadFile}
            disabled={loading || summaryLoading}
          >
            {loading ? "Processing..." : "Upload & Process"}
          </button>
        </section>

        {/* Whisper transcript generate kar raha hai to ye section dikhega */}
        {loading && (
          <section className="card loading">
            <h2>⏳ Processing Meeting...</h2>

            <img
              src="/singer-justin-timberlake-well-were-waiting-knyndp2iij7uincb.gif"
              alt="Still waiting"
              className="waiting-gif"
            />

            <p>
              Whisper is transcribing your meeting.
            </p>
            <p>
              Please wait...
            </p>
          </section>
        )}

        {/* Backend se error aaye to ye message show hoga */}
        {error && (
          <section className="error">
            <strong>❌ Error:</strong>
            <p>{error}</p>
          </section>
        )}

        {/* Transcript successfully generate ho gaya ho to result section dikhega */}
        {transcription && !loading && (
          <section className="card result">

            <div className="success-message">
              <h2>Transcript Ready</h2>

              <p>
                Your meeting has been successfully transcribed.
              </p>
            </div>

            {/* Result ke main action buttons */}
            <div className="result-buttons">

              {/* Jab tak summary generate nahi hui, Generate Summary button dikhega */}
              {!summary && !summaryLoading && (
                <button
                  className="primary-button"
                  onClick={generateSummary}
                >
                 Generate Summary
                </button>
              )}

              {/* Summary generate hone ke baad View Summary button dikhega */}
              {summary && (
                <button
                  className="secondary-button"
                  onClick={() => {
                    // Summary show/hide kar rahe hain.
                    setShowSummary(!showSummary);

                    // Transcript ko hide kar rahe hain taaki ek time par
                    // ek hi content visible rahe.
                    setShowTranscript(false);
                  }}
                >
                  {showSummary ? "Hide Summary" : "View Summary"}
                </button>
              )}

              {/* Transcript ko show/hide karne ka button */}
              <button
                className="secondary-button"
                onClick={() => {
                  setShowTranscript(!showTranscript);

                  // Transcript open karte waqt summary hide.
                  setShowSummary(false);
                }}
              >
                {showTranscript
                  ? "Hide Transcript"
                  : "View Transcript"}
              </button>
            </div>

            {/* Mistral summary generate kar raha hai to loading screen */}
            {summaryLoading && (
              <div className="summary-loading">
                <h3>⏳ Generating Summary...</h3>

                <img
                  src="/singer-justin-timberlake-well-were-waiting-knyndp2iij7uincb.gif"
                  alt="Generating summary"
                  className="waiting-gif"

                />

                <p>
                  Mistral AI is analyzing your meeting.
                </p>

                <p>
                  Please wait...
                </p>
              </div>
            )}

            {/* Summary successfully generate ho gayi */}
            {summary && !summaryLoading && (
              <div className="summary-status">
                <h3>✅ Summary Ready</h3>

                {/* User View Summary click karega tab actual summary dikhegi */}
                {showSummary && (
                  <div className="content-box">
                    <h3>📋 Meeting Summary</h3>

                    <div className="text-content">
                     <ReactMarkdown>{summary}</ReactMarkdown>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* User View Transcript click karega tab transcript dikhega */}
            {showTranscript && (
              <div className="content-box">
                <h3>📝 Meeting Transcript</h3>

                <div className="text-content">
                  {transcription}
                </div>
              </div>
            )}

          </section>
        )}

      </main>
    </div>
  );
}

export default App;