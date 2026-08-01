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

function App() {
  const [problems, setProblems] = useState([]);

  const handleProblemAdded = (newProblem) => {
    setProblems((prev) => [...prev, newProblem]);
  };

const router = createBrowserRouter([
    {path: "/", element: <LoginForm />},
    {path: "/signup", element: <SignupForm />},
    { path: "/home", element: <><Navbar /><ProblemCount /><Home /></> },
    { path: "/add", element: <><Navbar /><AddProblemForm onProblemAdded={handleProblemAdded} /></> },
    { path: "/delete", element: <><Navbar /><DeleteProblemForm /></> },
    { path: "/performance", element: <><Navbar /><Performance /></> },
    { path: "/suggestions", element: <><Navbar /><Chatbot /></> },
    { path: "/update", element: <><Navbar /><UpdateProblemForm /></> }
]);

  return <RouterProvider router={router} />;
}

export default App;