
function Navbar() {
    return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary">
    <div className="container-fluid">
      <a className="navbar-brand" href="/home">LeetiBuddy</a>
      <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div className="navbar-nav">
          <a className="nav-link active" aria-current="page" href="/home">Home</a>
          <a className="nav-link" href="/add">Add Problem</a>
          <a className="nav-link" href="/delete">Delete Problem</a>
          <a className="nav-link" href="/update">Update Problem</a>
          <a className="nav-link" href="/performance">Performance</a>
          <a className="nav-link" href="/suggestions">Suggestions</a>
        </div>
      </div>
    </div>
  </nav>
    )
}
export default Navbar;