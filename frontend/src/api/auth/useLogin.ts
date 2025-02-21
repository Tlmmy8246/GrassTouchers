import http from "utils/https";
import { endpoints } from "global/endpoints";
import { useUserStore } from "store/useUserStore";
import { useMutation } from "react-query";
import token from "utils/token";
import { useNavigate } from "react-router";
import { routePaths } from "global/routePaths";

interface ILoginPostData {
	username: string;
	password: string;
}

export const login = (postData: ILoginPostData) => {
	return http().post(endpoints.auth.postLogin, postData);
}

export const useLogin = () => {
	const addUserDetails = useUserStore((state) => state.addUserDetails);
	const navigate = useNavigate();

	return useMutation(login, {
		onSuccess: ({ payload }) => {
			const { apiToken, userUniqueToken, ...userData } = payload;
			token.setToken({ accessToken: apiToken, userUniqueToken: userUniqueToken });
			addUserDetails(userData);
			navigate(routePaths.home);
		},
		onError: ({ error }) => {
			console.log("% LOGIN ERROR", error);
			// TODO: Add a toaster to show an error occured
		}
	})
};
