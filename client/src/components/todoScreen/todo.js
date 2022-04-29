import { useState } from "react";
import { PropTypes } from "prop-types";
import { Button, Form, ListGroup } from "react-bootstrap";

import styles from "./todo.module.css";

const Todo = (props) => {
  const [todoDesc, setTodoDesc] = useState(props.todo.desc);
  const [editMode, setEditMode] = useState(false);

  return (
    <ListGroup.Item bg="dark">
      <div>
        {editMode ? (
          <Form>
            <Form.Group
              onSubmit={() =>
                props.handleTodoEdit(props.todo.id, todoDesc, () =>
                  setEditMode(false)
                )
              }
            >
              <Form.Control
                className={styles.todoEditInput}
                plaintext
                value={todoDesc}
                onChange={(e) => setTodoDesc(e.target.value)}
              />
              <Button
                className={styles.todoEditButton}
                variant="success"
                onClick={() =>
                  props.handleTodoEdit(props.todo.id, todoDesc, () =>
                    setEditMode(false)
                  )
                }
              >
                Save
              </Button>
              <Button
                variant="danger"
                onClick={() => {
                  setTodoDesc(props.todo.desc);
                  setEditMode(false);
                }}
              >
                X
              </Button>
            </Form.Group>
          </Form>
        ) : (
          <div className={styles.todoItem}>
            <div className={styles.checkboxDescWrapper}>
              <input
                type="checkbox"
                checked={props.todo.is_completed}
                onClick={() => props.handleTodoToggle(props.todo.id)}
              />
              <div
                className={styles.todoDesc}
                style={
                  props.todo.is_completed
                    ? { textDecoration: "line-through", color: "#AAA" }
                    : {}
                }
                onClick={() => setEditMode(!editMode)}
              >
                {props.todo.desc}
              </div>
            </div>
            <Button
              variant="danger"
              onClick={() => props.handleTodoDelete(props.todo.id)}
            >
              X
            </Button>
          </div>
        )}
      </div>
    </ListGroup.Item>
  );
};

Todo.propTypes = {
  todo: PropTypes.shape({
    id: PropTypes.number.isRequired,
    desc: PropTypes.string.isRequired,
    is_completed: PropTypes.bool.isRequired,
  }),
  handleTodoEdit: PropTypes.func.isRequired,
  handleTodoToggle: PropTypes.func.isRequired,
  handleTodoDelete: PropTypes.func.isRequired,
};

export default Todo;
