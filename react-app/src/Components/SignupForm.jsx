import {signupUser} from '../services/problemService';
import { useNavigate, Link } from 'react-router-dom';
import '../Styles/LoginForm.css';
import {authenticateUser} from '../services/problemService';


function SignupForm() {
    const navigate = useNavigate();
    const handleSubmit = async(e) => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        try {
            if (authenticateUser(username, password)) {
                    const status = await signupUser(username, password);
                    if(status.detail === "User created successfully") {
                    navigate("/login");
                    } else {
                        alert(status.detail);
                    }
            }
        } catch (error) {
            alert(error.message);
        }
    };
  return (
    <div className="login-container">
        <h2>Signup</h2>
        <form className="login-form" onSubmit={(e) => handleSubmit(e)}>
            <div className="form-group">
                <input type="text" id="username" name="username" placeholder="Username" />
            </div>
            <div className="form-group">
                <input type="password" id="password" name="password" placeholder="Password" />
            </div>
            <button type="submit" className="login-button">Signup</button>
        </form>
        <Link to="/login" className="signup-link">Already have an account? Login</Link>
    </div>
  );
}
export default SignupForm;