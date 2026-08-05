function PageNotFound() {
  return (
    <div style={styles.container}>
      <h1 style={styles.code}>404</h1>
      <p style={styles.message}>Page not found.</p>
      <a href="/" style={styles.link}>Go back home</a>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#f9fafb",
    padding: "1rem",
    textAlign: "center",
  },
  code: {
    fontSize: "4rem",
    fontWeight: "bold",
    color: "#1f2937",
    margin: 0,
  },
  message: {
    fontSize: "1.25rem",
    color: "#6b7280",
    marginTop: "0.5rem",
    marginBottom: "1.5rem",
  },
  link: {
    padding: "0.5rem 1rem",
    borderRadius: "0.375rem",
    backgroundColor: "#2563eb",
    color: "#fff",
    fontSize: "0.875rem",
    fontWeight: 500,
    textDecoration: "none",
  },
};

export default PageNotFound;