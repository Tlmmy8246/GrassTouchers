import { useLogin } from "api/auth";

import { useEffect, useState } from "react";
import { useUserStore } from "store/useUserStore";

const Login = () => {
    const { mutate: login } = useLogin();
    const [userName, setUserName] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const user = useUserStore(state => state.user);

    useEffect(() => {
        if (user?.username && user?.password) {
            setUserName(user.username);
            setPassword(user.password);
        }
    }, [user])

    const updateUserText = (e: any) => {
        setUserName(e.target.value);
    }

    const updatePasswordText = (e: any) => {
        setPassword(e.target.value);
    }

    const submitBtnClicked = (e: any) => {
        e.preventDefault();
        login({ username: userName, password: password });
    }

    return (
        <div>
            Please enter your login information:
            <form>
                <label>User:</label> <br></br>
                <input type="text" id="username" name="Username" value={userName} onChange={updateUserText}></input><br></br>
                <label>Password:</label><br></br>
                <input type="text" id="password" name="Password" value={password} onChange={updatePasswordText}></input><br></br>
                <button onClick={submitBtnClicked}>Login</button>
            </form>
        </div>
    )
}

export default Login;
