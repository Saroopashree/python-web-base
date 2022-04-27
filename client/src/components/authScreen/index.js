import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Form, Tab, Tabs, Button, Alert } from "react-bootstrap";
import styles from "./auth.module.css";

const AuthScreen = (props) => {
  const navigate = useNavigate();
  const [error, setError] = useState({ login: "", register: "" });
  const [tabKey, setTabKey] = useState("login");

  const login = (username, password) => {
    axios.post("/api/users/login", { username, password }).then((response) => {
      if (!response.data.id) {
        setError({ login: response.data.message, register: "" });
      } else {
        setError({ login: "", register: "" });
        props.setUserId(response.data.id);
        navigate("/app");
      }
    });
  };

  const register = (username, password) => {
    axios
      .post("/api/users/register", { username, password })
      .then((response) => {
        if (!response.data.id) {
          setError({ login: "", register: response.data.message });
        } else {
          setError({ login: "", register: "" });
          props.setUserId(response.data.id);
          navigate("/app");
        }
      });
  };

  return (
    <>
      <div className={styles.appHeader}>
        <Tabs
          activeKey={tabKey}
          onSelect={(k) => setTabKey(k)}
          classname="mb-3"
        >
          <Tab eventKey="login" title="Sign In">
            <AuthForm title="Log-in" onSubmit={login} error={error.login} />
          </Tab>
          <Tab eventKey="register" title="Sign Up">
            <AuthForm
              title="Register"
              onSubmit={register}
              error={error.register}
            />
          </Tab>
        </Tabs>
      </div>
    </>
  );
};

export default AuthScreen;

const AuthForm = (props) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <Form className={styles.form}>
      <Form.Group
        className={styles.formGroup}
        onSubmit={() => props.onSubmit(username, password)}
      >
        <Form.Label>Username</Form.Label>
        <Form.Control
          className={styles.formInput}
          value={username}
          placeholder="john_doe"
          onChange={(e) => setUsername(e.target.value)}
        />
      </Form.Group>
      <Form.Group className={styles.formGroup}>
        <Form.Label>Password</Form.Label>
        <Form.Control
          className={styles.formInput}
          type="password"
          value={password}
          placeholder="password"
          onChange={(e) => setPassword(e.target.value)}
        />
      </Form.Group>
      {Boolean(props.error) && <Alert variant="danger">{props.error}</Alert>}
      <Button
        className={styles.submitBtn}
        variant="success"
        onClick={() => props.onSubmit(username, password)}
      >
        {props.title}
      </Button>
    </Form>
  );
};
