import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function ProtectedRoute({ children }) {
  const navigate = useNavigate();
  const token = sessionStorage.getItem("access_token");
  console.log(token);
  useEffect(() => {
    if (!token) {
      navigate("/", { replace: true });
    }
  }, [token, navigate]);

  if (!token) {
    return null;
  }

  return children;
}

export default ProtectedRoute;