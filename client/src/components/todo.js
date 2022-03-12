import { useState } from "react";
import { PropTypes } from "prop-types";
import { Button, Form, ListGroup } from "react-bootstrap";

import "./todo.module.css";

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
              <Form.Control plaintext value={todoDesc} onChange={setTodoDesc} />
            </Form.Group>
          </Form>
        ) : (
          <div className="todo-item">
            <div className="checkbox-desc-wrapper">
              <input
                type="checkbox"
                onClick={() => props.handleTodoToggle(props.todo.id)}
              />
              <div
                style={
                  props.is_completed
                    ? { textDecoration: "line-through", color: "#AAA" }
                    : {}
                }
                onClick={() => setEditMode(!editMode)}
              >
                {props.desc}
              </div>
            </div>
            <Button variant="danger" onClick={() => props.handleTodoDelete(props.todo.id)}>
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
