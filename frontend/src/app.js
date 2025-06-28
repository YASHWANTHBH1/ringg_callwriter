import React, { useState } from "react";
import "./app.css";
import { useNavigate } from "react-router-dom";

function App() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    url: "",
    mode: "",
    intentCount: 3,
    domain: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.url || !formData.mode || !formData.domain) {
      setError("Please fill all fields before generating.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Failed to generate scripts.");
        return;
      }

      navigate("/results", { state: { scripts: data.scripts } });
    } catch (err) {
      setError("API Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* 🔊 Announcement */}
      <div className="announcement-bar">
        Language Barrier? Solved. Now Let Me Join the Team That’s Breaking Calling Limits.
      </div>

      {/* 🔗 Navbar */}
      <header className="navbar">
        <img src="/assets/ringg_logo.png" alt="Ringg Logo" className="logo" />

        {/* Desktop Links */}
        <nav className="nav-links desktop-only">
          <a href="https://github.com/YASHWANTHBH1/ringg_callwriter" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="https://drive.google.com/file/d/1n0qKidtfdrJya3v9v9Ppd2XzrcW4UKJ3/view?usp=sharing" target="_blank" rel="noopener noreferrer">Resume</a>
          <a href="https://yashwanthbh.netlify.app/" target="_blank" rel="noopener noreferrer">Portfolio</a>
        </nav>

        {/* Desktop Contact Button */}
        <a href="mailto:yashwanthbh382@gmail.com" className="contact-btn desktop-only">Contact</a>

        {/* Mobile Button */}
        <button className="know-more-btn mobile-only" onClick={() => setShowMobileMenu(!showMobileMenu)}>
          {showMobileMenu ? "Close" : "Know More"}
        </button>
      </header>

      {/* Mobile Nav Dropdown */}
      {showMobileMenu && (
        <nav className="mobile-nav mobile-only">
          <a href="https://github.com/YASHWANTHBH1/ringg_callwriter" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="https://drive.google.com/file/d/1n0qKidtfdrJya3v9v9Ppd2XzrcW4UKJ3/view?usp=sharing" target="_blank" rel="noopener noreferrer">Resume</a>
          <a href="https://yashwanthbh.netlify.app/" target="_blank" rel="noopener noreferrer">Portfolio</a>
          <a href="mailto:yashwanthbh382@gmail.com">Contact</a>
        </nav>
      )}

      {/* 📢 Hero Section */}
      <section className="hero-section">
        <h1 className="main-heading">AI That Writes for Your AI</h1>
        <h2 className="sub-heading">Auto Script Generation</h2>
        <p className="hero-description">
          Meet the custom AI tool I built for <a href="https://ringg.ai">Ringg.ai</a>.
        </p>
      </section>

      {/* 📱 Phone Frame Form */}
      <div className="page">
        <div className="phone-wrapper">
          <div className="phone-frame">
            <div className="notch" />
            <div className="screen">
              <div className="form-card">
                <div className="card-header">
                  <div className="header-text">
                    <h2>Ringg AI Call Writer</h2>
                    <div className="online-status">
                      <center><span className="dot" /> Online</center>
                    </div>
                  </div>
                </div>

                <form onSubmit={handleSubmit} className="card-form">
                  <input type="text" name="url" placeholder="Company URL / FAQs" value={formData.url} onChange={handleChange} />
                  <select name="mode" value={formData.mode} onChange={handleChange}>
                    <option value="">Select Mode</option>
                    <option value="friendly">Friendly</option>
                    <option value="professional">Professional</option>
                    <option value="casual">Casual</option>
                  </select>
                  <input type="number" name="intentCount" min="1" max="6" value={formData.intentCount} onChange={handleChange} />
                  <select name="domain" value={formData.domain} onChange={handleChange}>
                    <option value="">Select Domain</option>
                    <option value="sales">Sales</option>
                    <option value="support">Support</option>
                    <option value="healthcare">Healthcare</option>
                    <option value="finance">Finance</option>
                    <option value="travel">Travel</option>
                    <option value="food">Food Delivery</option>
                  </select>

                  {error && <div className="error">{error}</div>}
                  <button type="submit" className="generate-btn">
                    {loading ? "Generating..." : "Generate"}
                  </button>
                </form>
              </div>
            </div>
          </div>
          <img src="/assets/cut-overlay.png" alt="Overlay Design" className="phone-bottom-overlay" />
        </div>
      </div>
    </div>
  );
}

export default App;














