import { login } from "api/auth";

import { useState } from "react";

const Login = () => {
    // const { mutate, isError, isSuccess, isLoading } = useLogin();
    const [userName, setUserName] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const updateUserText = (e: any) => {
        setUserName(e.target.value);
    }

    const updatePasswordText = (e: any) => {
        setPassword(e.target.value);
    }

    const submitBtnClicked = async () => {
        const res = await login({ username: userName, password: password });
        console.log("% LOGIN RES", res);
        if (res.error) {
            console.error("% LOGIN ERROR", res.error);
        }
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
