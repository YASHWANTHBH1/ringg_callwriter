import React from "react";
import { useLocation, Link } from "react-router-dom";
import "./result.css";
import "./app.css"; // for announcement-bar, navbar, etc.

function Results() {
  const location = useLocation();
  const { scripts } = location.state || { scripts: [] };

  const downloadJSON = () => {
    const json = JSON.stringify(scripts, null, 2);
    const blob = new Blob([json], { type: "application/json" });
    const href = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = href;
    link.download = "callwriter_output.json";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="app-container">
      <div className="announcement-bar">
        Language Barrier? Solved. Now Let Me Join the Team That’s Breaking Calling Limits.
      </div>

      <header className="navbar">
        <img src="/assets/ringg_logo.png" alt="Ringg Logo" className="logo" />
        <nav className="nav-links">
          <a href="https://github.com/YASHWANTHBH1/ringg_callwriter" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="https://drive.google.com/file/d/1n0qKidtfdrJya3v9v9Ppd2XzrcW4UKJ3/view?usp=sharing" target="_blank" rel="noopener noreferrer">Resume</a>
          <a href="https://yashwanthbh.netlify.app/" target="_blank" rel="noopener noreferrer">Portfolio</a>
        </nav>
        <Link to="/">
          <a href="mailto:yashwanthbh382@gmail.com" className="contact-btn">Contact</a>
        </Link>
      </header>

      <div className="results-container">
        <h1 className="results-heading">Generated Intents</h1>

        <div className="results-grid">
          {scripts.map((intent, idx) => (
            <div key={idx} className="intent-card">
              <h3>{intent.intent}</h3>
              {intent.script.map((line, i) => (
                <div key={i}>
                  {line.user && (
                    <div className="chat-bubble user-message">
                      <strong>👤 User:</strong> {line.user}
                    </div>
                  )}
                  {line.ai && (
                    <div className="chat-bubble ai-message">
                      <strong>🤖 AI:</strong> {line.ai}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>

        <button onClick={downloadJSON} className="download-btn">
          ⬇ Download JSON
        </button>
      </div>
    </div>
  );
}

export default Results;


