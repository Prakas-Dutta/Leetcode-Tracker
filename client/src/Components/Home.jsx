// src/components/Home.jsx
import { Link } from "react-router-dom";
import "../Styles/Home.css";

function Home() {
  return (
    <div className="home-hero">
      <div className="home-badge">📊 LeetCode Tracker</div>
      <h1 className="home-title">
        Track Your <span className="home-title-accent">Problem-Solving</span> Journey
      </h1>
      <p className="home-subtitle">
        Log the problems you solve, tag them by pattern, and see where you're
        strong — and where you need more reps.
      </p>

      <div className="home-actions">
        <Link to="/add" className="home-btn home-btn-primary">
          Add a Problem
        </Link>
        <Link to="/performance" className="home-btn home-btn-secondary">
          View Performance
        </Link>
      </div>

      <div className="home-features">
        <div className="home-feature-card">
          <span className="home-feature-icon">➕</span>
          <h3>Log Problems</h3>
          <p>Record each problem along with the pattern or approach you used.</p>
        </div>
        <div className="home-feature-card">
          <span className="home-feature-icon">📈</span>
          <h3>See Patterns</h3>
          <p>Visualize which patterns you've mastered and which need more work.</p>
        </div>
        <div className="home-feature-card">
          <span className="home-feature-icon">🤖</span>
          <h3>Get Suggestions</h3>
          <p>Get tailored problem recommendations based on your weak spots.</p>
        </div>
      </div>
    </div>
  );
}

export default Home;