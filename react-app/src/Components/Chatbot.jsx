// src/components/Chatbot.jsx
import { chatbotSuggestions } from "../services/problemService";
import { useEffect, useState } from "react";
import "../Styles/Chatbot.css";

function Chatbot() {
  const [suggestions, setSuggestions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    chatbotSuggestions()
      .then((data) => setSuggestions(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="chatbot-card chatbot-status">
        <div className="spinner-border" role="status" />
        <p>Analyzing your performance...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="chatbot-card chatbot-status chatbot-error">
        <p>⚠️ Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="chatbot-card">
      <h1 className="chatbot-title">Suggestions Based on Your Performance</h1>

      <section className="chatbot-section">
        <h3 className="chatbot-section-heading">Reasoning</h3>
        <p className="chatbot-text">{suggestions.reasoning}</p>
      </section>

      <section className="chatbot-section">
        <h3 className="chatbot-section-heading">Focus On</h3>
        <span className="chatbot-focus-badge">{suggestions.suggested_focus}</span>
      </section>

      <section className="chatbot-section">
        <h3 className="chatbot-section-heading">Weak Patterns</h3>
        <div className="chatbot-tags">
          {suggestions.weak_patterns.map((pattern, i) => (
            <span key={i} className="chatbot-tag">{pattern}</span>
          ))}
        </div>
      </section>

      <section className="chatbot-section">
        <h3 className="chatbot-section-heading">Recommended Problems</h3>
        <ul className="chatbot-problem-list">
          {suggestions.suggested_problems.map((problem, index) => (
            <li key={index} className="chatbot-problem-item">
              <a
                href={problem.url}
                target="_blank"
                rel="noopener noreferrer"
                className="chatbot-problem-link"
              >
                {problem.name}
                <span className="chatbot-link-arrow">→</span>
              </a>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default Chatbot;