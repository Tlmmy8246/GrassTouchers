import { useState } from 'react'
import { register } from 'api/auth/useRegister';

const Register = () => {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');

	const updateUsername = (e: any) => {
		setUsername(e.target.value);
	}

	const updatePassword = (e: any) => {
		setPassword(e.target.value);
	}

	const submitBtnClicked = async (e: any) => {
		e.preventDefault();
		const res = await register({ username, password });
		console.log('% REGISTER RES', res);
		if (res.error) {
			console.error('% REGISTER ERROR', res.error);
		}
	}

	return (
		<div>
			<h1>Register</h1>
			<form>
				<label>User:</label>
				<input type="text" id="username" name="Username" onChange={updateUsername}></input>
				<label>Password:</label>
				<input type="text" id="password" name="Password" onChange={updatePassword}></input>
				<button onClick={submitBtnClicked}>Register</button>
			</form>
		</div>
	)
}

export default Register
