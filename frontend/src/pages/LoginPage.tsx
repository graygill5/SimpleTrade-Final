import { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export function LoginPage() {
  const nav = useNavigate();
  const { login, signup } = useAuth();
  const [isSignup, setIsSignup] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (isSignup) await signup(username, email, password);
    else await login(email, password);
    nav('/market');
  }

  return (
    <div className="centered-card">
      <h2>{isSignup ? 'Create account' : 'Login'}</h2>
      <form onSubmit={submit}>
        {isSignup && <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />}
        <input placeholder="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">{isSignup ? 'Sign up' : 'Login'}</button>
      </form>
      <button className="secondary" onClick={() => setIsSignup((x) => !x)}>
        {isSignup ? 'Have an account? Login' : 'Need an account? Sign up'}
      </button>
    </div>
  );
}
