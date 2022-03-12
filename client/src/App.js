import { useState, useEffect } from "react";
import axios from "axios";

import "./App.css";
import Todo from "./components/todo";
import { Button, Form, ListGroup } from "react-bootstrap";

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState("second");

  const fetchAllTodos = () => {
    axios.get("server:8000/todo/").then((response) => {
      setTodos(response.data);
    });
  };

  const handleAddNewTodo = () => {
    axios.post("server:8000/todo/", { desc: newTodo }).then((response) => {
      let _todos = [...todos];
      _todos.push(response.data);
      setTodos(_todos);
      setNewTodo("");
    });
  };

  const handleTodoEdit = (id, desc, callback) => {
    axios
      .put(`server:8000/todo/change-desc/${id}`, { desc })
      .then((response) => {
        let _todos = [...todos];
        _todos = _todos.map((t) => (t.id === id ? response.data : t));
        setTodos(_todos);
      })
      .finally(callback);
  };

  const handleTodoToggle = (id) => {
    axios.put(`server:8000/todo/toggle-complete/${id}`).then((response) => {
      let _todos = [...todos];
      _todos = _todos.map((t) => (t.id === id ? response.data : t));
      setTodos(_todos);
    });
  };

  const handleTodoDelete = (id) => {
    axios.delete(`server:8000/todo/${id}`).then(fetchAllTodos);
  };

  useEffect(() => {
    fetchAllTodos();
  }, []);

  return (
    <div id="app-start">
      <h2 id="app-header">Todo App</h2>
      <ListGroup>
        {todos.map((todo) => (
          <Todo
            todo={todo}
            handleTodoEdit={handleTodoEdit}
            handleTodoToggle={handleTodoToggle}
            handleTodoDelete={handleTodoDelete}
          />
        ))}
      </ListGroup>
      <Form.Group onSubmit={handleAddNewTodo}>
        <Form.Control plaintext value={newTodo} onChange={setNewTodo} />
        <Button variant="success">Add Todo #{todos.length}</Button>
      </Form.Group>
    </div>
  );
}

export default App;
