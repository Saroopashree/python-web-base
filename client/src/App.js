import { useState, useEffect } from "react";
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom";
import axios from "axios";

import "./App.css";
import Todo from "./components/todoScreen/todo";
import { Button, Form, ListGroup } from "react-bootstrap";
import AuthScreen from "./components/authScreen";
import TodoScreen from "./components/todoScreen";

function App() {
  const [userId, setUserId] = useState(null);

  return (
    <div id="app-start">
      <BrowserRouter>
        <Routes>
          <Route
            path="/signin"
            element={<AuthScreen setUserId={setUserId} />}
          />
          <Route path="/app" element={<TodoScreen userId={userId} />} />
          <Route path="/" element={<Redirect to="/signin" />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

const Redirect = ({ to }) => {
  const navigate = useNavigate();
  useEffect(() => {
    navigate(to, { replace: true });
  }, []);

  return null;
};

export default App;
