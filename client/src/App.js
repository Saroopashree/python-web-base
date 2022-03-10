import { useState, useEffect } from "react";
import axios from "axios"

import logo from './logo.svg';
import './App.css';

function App() {
  const [todos, setTodos] = useState([])

  useEffect(() => {
    axios.get("server:8000/todo/").then(response => {
      setTodos(response.data);
    })
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
