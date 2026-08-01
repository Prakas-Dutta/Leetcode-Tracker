import {loginUser} from '../services/problemService';
import { Link, useNavigate } from 'react-router-dom';
import '../Styles/LoginForm.css';
import {authenticateUser} from '../services/problemService';

function LoginForm() {
    const navigate = useNavigate();
    const handleSubmit = async(e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        try {
                if (authenticateUser(username, password)) {
                const status = await loginUser(username, password);
                console.log(status);
                if(status.detail === "Login successful") {
                navigate("/home");
                } else {
                    alert("Login failed: Invalid username or password");
                }
            }
        } catch (error) {
            alert(error.message);
        }
    };
  return (
    <div className="login-container">
        <h2>Login</h2>
        <form className="login-form" onSubmit={(e) => handleSubmit(e)}>
            <div className="form-group">
                <input type="text" id="username" name="username" placeholder="Username" />
            </div>
            <div className="form-group">
                <input type="password" id="password" name="password" placeholder="Password" />
            </div>
            <button type="submit" className="login-button">Login</button>
        </form>
        <Link to="/signup" className="signup-link">Don't have an account? Sign up</Link>
    </div>
  );
}
export default LoginForm;