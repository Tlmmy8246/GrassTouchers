import { useState } from 'react'
import { useRegister } from 'api/auth';
import { useUserStore } from 'store/useUserStore';

const Register = () => {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');

	const addUserDetails = useUserStore(state => state.addUserDetails);

	const { mutate: register } = useRegister();

	const updateUsername = (e: any) => {
		setUsername(e.target.value);
	}

	const updatePassword = (e: any) => {
		setPassword(e.target.value);
	}

	const submitBtnClicked = (e: any) => {
		e.preventDefault();
		addUserDetails({ username, password });
		register({ username, password });
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
