import supabase from "utils/supabase";

interface IRegisterPostData {
	username: string;
	password: string;
}

export const register = async (postData: IRegisterPostData) => {
	const { data, error } = await supabase.auth.signUp({
		email: postData.username,
		password: postData.password
	});

	if (error) return { data: null, error, isError: true };

	// TODO: Redirect the user to the login page if the data is true

	return { data, error: null, isError: false };
}
