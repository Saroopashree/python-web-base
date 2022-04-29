import { useState, useEffect } from "react";
import { useNavigate } from "react-router";
import axios from "axios";

import styles from "./todo.module.css";
import Todo from "./todo";
import { Button, Form, ListGroup } from "react-bootstrap";

const TodoScreen = (props) => {
  const navigate = useNavigate();

  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState("");

  const fetchAllTodos = () => {
    axios
      .get(`/api/todo/${props.userId}`)
      .then((response) => {
        console.log(response.data);
        setTodos(response.data);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const handleAddNewTodo = () => {
    axios
      .post(`/api/todo/${props.userId}`, { desc: newTodo })
      .then((response) => {
        let _todos = [...todos];
        _todos.push(response.data);
        setTodos(_todos);
        setNewTodo("");
      });
  };

  const handleTodoEdit = (id, desc, callback) => {
    axios
      .put(`/api/todo/${props.userId}/change-desc/${id}`, { desc })
      .then((response) => {
        let _todos = [...todos];
        _todos = _todos.map((t) => (t.id === id ? response.data : t));
        setTodos(_todos);
      })
      .finally(callback);
  };

  const handleTodoToggle = (id) => {
    axios
      .put(`/api/todo/${props.userId}/toggle-complete/${id}`)
      .then((response) => {
        let _todos = [...todos];
        _todos = _todos.map((t) => (t.id === id ? response.data : t));
        setTodos(_todos);
      });
  };

  const handleTodoDelete = (id) => {
    axios.delete(`/api/todo/${props.userId}/${id}`).then(fetchAllTodos);
  };

  useEffect(() => {
    if (!props.userId) {
      navigate("/signin");
    } else {
      fetchAllTodos();
    }
  }, [props.userId]);

  return (
    <>
      <h2 className={styles.appHeader}>Todo Application</h2>
      <div className={styles.todos}>
        <ListGroup className={styles.listGroup}>
          {todos.map((todo) => (
            <Todo
              todo={todo}
              handleTodoEdit={handleTodoEdit}
              handleTodoToggle={handleTodoToggle}
              handleTodoDelete={handleTodoDelete}
            />
          ))}
        </ListGroup>
        <Form.Group
          className={styles.newTodoFormGrp}
          onSubmit={handleAddNewTodo}
        >
          <Form.Control
            className={styles.addTodoInput}
            plaintext
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
          />
          <Button
            className={styles.addTodoBtn}
            variant="success"
            onClick={handleAddNewTodo}
          >
            Add Todo #{todos.length + 1}
          </Button>
        </Form.Group>
      </div>
    </>
  );
};

export default TodoScreen;
