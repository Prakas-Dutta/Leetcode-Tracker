import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { isTokenExpired } from "../services/problemService";

function ProtectedRoute({ children }) {
  const navigate = useNavigate();
  const token = sessionStorage.getItem("access_token");
  const expired = isTokenExpired(token);

  useEffect(() => {
    if (expired) {
      sessionStorage.removeItem("access_token");
      alert("You have to login to access this page. Please login.");
      navigate("/", { replace: true });
    }
  }, [expired, navigate]);

  if (expired) return null;
  return children;
}

export default ProtectedRoute;