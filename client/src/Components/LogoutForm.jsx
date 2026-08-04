import { logoutUser } from '../services/problemService';
import { useNavigate } from 'react-router-dom';
import '../Styles/LogoutForm.css';

function LogoutForm() {
  const navigate = useNavigate();
  const handleLogout = () => {
    logoutUser();
    navigate('/');
  };

  return (
    <div className="card">
      <span className="eyebrow">Session</span>
      <h2 className="heading">Want to logout?</h2>
      <button className="logoutBtn" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}

export default LogoutForm;