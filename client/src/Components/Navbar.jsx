import { Link } from "react-router-dom";

function Navbar() {
    return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary">
    <div className="container-fluid">
      <Link className="navbar-brand" to="/home">LeetiBuddy</Link>
      <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div className="navbar-nav">
          <Link className="nav-link active" aria-current="page" to="/home">Home</Link>
          <Link className="nav-link" to="/add">Add Problem</Link>
          <Link className="nav-link" to="/delete">Delete Problem</Link>
          <Link className="nav-link" to="/update">Update Problem</Link>
          <Link className="nav-link" to="/performance">Performance</Link>
          <Link className="nav-link" to="/suggestions">Suggestions</Link>
          {!sessionStorage.getItem("access_token") ? (
              <Link className="nav-link" to="/login">Login</Link>
          ) : (
              <Link className="nav-link" to="/logout">Logout</Link>
          )}
        </div>
      </div>
    </div>
  </nav>
    )
}
export default Navbar;