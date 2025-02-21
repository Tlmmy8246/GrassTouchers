// TODO: Add your API endpoints from fastapi here
export const endpoints = {
	auth: {
		login: '/login',
		postLogin: '/post-login/'
	},
	chat: {
		duel: {
			messages: 'duel/messages'
		},
		global: {
			messages: 'global/messages'
		}
	}
}
