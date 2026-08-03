// App.jsx
import { useState } from "react";
import AddProblemForm from "./Components/AddProblemForm";
import ProblemCount from "./Components/ProblemCount";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Performance from "./Components/Performance";
import DeleteProblemForm from "./Components/DeleteProblemForm";
import Home from "./Components/Home";
import Navbar from "./Components/Navbar";
import Chatbot from "./Components/Chatbot";
import UpdateProblemForm from "./Components/UpdateProblemForm";
import LoginForm from "./Components/LoginForm";
import SignupForm from "./Components/SignupForm";
import ProtectedRoute from "./Components/ProtectedRoute";

function App() {
  const [problems, setProblems] = useState([]);

  const handleProblemAdded = (newProblem) => {
    setProblems((prev) => [...prev, newProblem]);
  };

const router = createBrowserRouter([
    {path: "/", element: <LoginForm />},
    {path: "/signup", element: <SignupForm />},
    { path: "/home", element: <ProtectedRoute><><Navbar /><ProblemCount /><Home /></></ProtectedRoute> },
    { path: "/add", element: <ProtectedRoute><><Navbar /><AddProblemForm onProblemAdded={handleProblemAdded} /></></ProtectedRoute> },
    { path: "/delete", element: <ProtectedRoute><><Navbar /><DeleteProblemForm /></></ProtectedRoute> },
    { path: "/performance", element: <ProtectedRoute><><Navbar /><Performance /></></ProtectedRoute> },
    { path: "/suggestions", element: <ProtectedRoute><><Navbar /><Chatbot /></></ProtectedRoute> },
    { path: "/update", element: <ProtectedRoute><><Navbar /><UpdateProblemForm /></></ProtectedRoute> }
]);

  return <RouterProvider router={router} />;
}

export default App;