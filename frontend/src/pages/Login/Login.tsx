import { useLogin } from "api/auth";

const Login = () => {
    const { mutate } = useLogin();

    const handleBtnClick = () => {
        mutate({
            username: "admin",
            password: "admin"
        })
    }

    return (
        <div>
            <button onClick={handleBtnClick}>Login</button>
        </div>
    )
}

export default Login;
