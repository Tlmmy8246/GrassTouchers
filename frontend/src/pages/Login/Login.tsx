import { useLogin } from "api/auth";

import { useState } from "react";

const Login = () => {
    const {mutate, isError, isSuccess, isLoading} = useLogin();
    const [userName, setUserName] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const updateUserText = (e) => {
        setUserName(e.target.value);
    }
    const updatePasswordText = (e) => {
        setPassword(e.target.value);
    }
    const submitBtnClicked = () => {
        mutate({
            username: userName,
            password: password
        })
    }

    console.log("% USER", userName);
    console.log("% PASSWORD", password);

    if(isError) return console.error("% SOMETHING WENT WRONG NOOO")

    return <div>ඞPlease enter your login information:ඞ<form>
        <label>User:</label> <br></br>
        <input type="text" id="username" name="Username" value={userName} onChange={updateUserText}></input><br></br>
        <label>Password:</label><br></br>
        <input type="text" id="password" name="Password" value={password} onChange={updatePasswordText}></input><br></br>
        <input value="Login" onClick={submitBtnClicked}></input>
        </form></div>

}

export default Login;
