import { useState } from "react";
import AddProblemForm from "./Components/AddProblemForm";
import ProblemCount from "./Components/ProblemCount";

function App() {
  const handleProblemAdded = (newProblem) => {
    setProblems((prev) => [...prev, newProblem]);
  };

  return (
    <>
      <div className="d-flex justify-content-end">
        <ProblemCount />
      </div>
      <div className="d-flex justify-content-center">
        <AddProblemForm onProblemAdded={handleProblemAdded} />
      </div>
    </>
  );
}

export default App;
