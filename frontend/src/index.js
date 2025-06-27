import React from "react";
import ReactDOM from "react-dom/client";
import App from "./app";
import Results from "./results"; // ✅ Import Results page
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./app.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  </React.StrictMode>
);


