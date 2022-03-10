import { useState } from "react";
import { Card, Form } from "react-bootstrap";

function Todo(props) {
  const [todoDesc, setTodoDesc] = useState(props.desc)
  const [editMode, setEditMode] = useState(false);

  return (
    <Card bg="dark">
      <Card.Body>
        {editMode ? (
          <Form>
              <Form.Group>
                  <Form.Control plaintext value={todoDesc} onChange={setTodoDesc} />
              </Form.Group>
          </Form>
        ) : (
          <Card.Text
            style={
              props.is_completed
                ? { textDecoration: "line-through", color: "#AAA" }
                : {}
            }
            onClick={() => setEditMode(!editMode)}
          >
            {props.desc}
          </Card.Text>
        )}
      </Card.Body>
    </Card>
  );
}
