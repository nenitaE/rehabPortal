import React, { useState } from "react";
import { login } from "../../store/session";
import { useDispatch } from "react-redux";
import { useModal } from "../../context/Modal";
import { useHistory } from 'react-router-dom'
import "./LoginForm.css";

function LoginFormModal() {
  const dispatch = useDispatch();
  const history = useHistory();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState([]);
  const { closeModal } = useModal();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await dispatch(login(email, password));
    if (data) {
      setErrors(data);
    } else {
        closeModal()
    }
  };

  const handleDemoClinicianLogin = async (e) => {
    e.preventDefault();
    setEmail('demo@aa.io');
    setPassword('password');
  };
  const handleDemoPatientLogin = async (e) => {
    e.preventDefault();
    setEmail('marnie@aa.io');
    setPassword('password');
  };

  return (
    <>
      <h1>Log In</h1>
      <form onSubmit={handleSubmit}>
        <ul>
          {errors.map((error, idx) => (
            <li key={idx}>{error}</li>
          ))}
        </ul>
        <label>
          Email
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <button onClick={handleDemoClinicianLogin}>Click to Fill Demo Therapist-User Data</button>
        <button onClick={handleDemoPatientLogin}>Click to Fill Demo Patient-User Data</button>
        <button className="submit-modal-button" type="submit">Log In</button>
      </form>
    </>
  );
}

export default LoginFormModal;
