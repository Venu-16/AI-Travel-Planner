import { useState } from "react";
import { login, register } from "../services/api";

function Auth({ onAuth }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const fn = mode === "login" ? login : register;
      const res = await fn({ email, password });
      if (res.error) return setError(res.error);
      onAuth && onAuth(true);
    } catch (err) {
      setError("Auth failed");
    }
  };

  return (
    <div style={{ maxWidth: 360 }}>
      <h2>{mode === "login" ? "Login" : "Register"}</h2>
      <form onSubmit={submit}>
        <input
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">{mode === "login" ? "Log in" : "Create account"}</button>
      </form>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <div style={{ marginTop: 8 }}>
        <button onClick={() => setMode(mode === "login" ? "register" : "login")}> 
          {mode === "login" ? "Need an account?" : "Have an account?"}
        </button>
      </div>
    </div>
  );
}

export default Auth;
