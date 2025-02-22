import { useRegister } from 'api/auth';
import { useUserStore } from 'store/useUserStore';
import { useEffect } from "react";
import { Button, Input } from "components";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import tokenService from 'utils/token';
import { routePaths } from "global/routePaths";

interface RegisterFormData {
	username: string;
	password: string;
}

const Register = () => {
	const navigate = useNavigate();
	const { register, handleSubmit, formState: { errors } } = useForm<RegisterFormData>();

	const addUserDetails = useUserStore(state => state.addUserDetails);

	const { mutate: registerMutate } = useRegister();

	const onSubmit = (data: RegisterFormData) => {
		addUserDetails(data);
		registerMutate(data);
	}

	useEffect(() => {
		if (tokenService.getAccessToken()) {
			navigate(routePaths.globalChat);
		}
	}, [])

	return (
		<div className="register-container">
			<div className="bg-gray-800/80 text-xl p-6 rounded-lg w-[75%] text-gray-100">
				<h1 className="text-3xl mb-5">Register to avoid touching grass!</h1>
				<form className="flex flex-col justify-center text-2xl" onSubmit={handleSubmit(onSubmit)}>
					<div className="flex gap-15 mb-2">
						<label className="mr-3">User:</label>
						<div className="w-full">
							<Input className="font-bold" type="text" id="username" {...register("username", { required: true })} />
							{errors.username && <span className="ml-4 text-lg text-red-700">This field is required</span>}
						</div>
					</div>
					<div className="flex gap-3 mb-5">
						<label>Password:</label>
						<div className="w-full">
							<Input type="text" id="password" {...register("password", { required: true })} />
							{errors.password && <span className="ml-4 text-lg text-red-700">This field is required</span>}
						</div>
					</div>
					<div className="flex justify-center">
						<Button type="submit">Register</Button>
					</div>
				</form>
			</div>
		</div>
	)
}

export default Register
