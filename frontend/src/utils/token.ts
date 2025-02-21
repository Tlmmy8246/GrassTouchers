import * as localStorage from './storage';

type TTokenObj = {
	accessToken: string;
	userUniqueToken: string;
	expiryDate?: string;
};

const ACCESS_TOKEN = 'access_token';
const USER_UNIQUE_TOKEN = 'user_unique_token';
const EXPIRY_DATE = 'expiry_date';

type TReturnTypes = {
	setToken: (tokenObj: TTokenObj) => void;
	getAccessToken: () => string | null;
	getUserUniqueToken: () => string | null;
	getTokenExpiryDate: () => string | null;
	clearToken: () => void;
};

const token = (): TReturnTypes => {
	function _setToken(tokenObj: TTokenObj) {
		localStorage.set(ACCESS_TOKEN, tokenObj.accessToken);
		localStorage.set(USER_UNIQUE_TOKEN, tokenObj.userUniqueToken);
		if (tokenObj.expiryDate) {
			localStorage.set(EXPIRY_DATE, tokenObj.expiryDate);
		}
	}

	function _getAccessToken() {
		return localStorage.get(ACCESS_TOKEN) === 'undefined' ? undefined : localStorage.get(ACCESS_TOKEN);
	}

	function _getUserUniqueToken() {
		return localStorage.get(USER_UNIQUE_TOKEN) === 'undefined' ? undefined : localStorage.get(USER_UNIQUE_TOKEN);
	}

	function _getTokenExpiryDate() {
		return localStorage.get(EXPIRY_DATE) === 'undefined' ? undefined : localStorage.get(EXPIRY_DATE);
	}

	function _clearToken() {
		localStorage.remove(ACCESS_TOKEN);
		localStorage.remove(USER_UNIQUE_TOKEN);
	}

	return {
		setToken: _setToken,
		getAccessToken: _getAccessToken,
		getUserUniqueToken: _getUserUniqueToken,
		getTokenExpiryDate: _getTokenExpiryDate,
		clearToken: _clearToken,
	};
};

export default token();
