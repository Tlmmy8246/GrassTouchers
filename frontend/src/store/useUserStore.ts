import { create } from 'zustand';
import { combine, persist } from 'zustand/middleware';

const userInitialState = {
	user: null
}

const userStore = combine(userInitialState, set => ({
	addUserDetails: (userDetails: any) => set(prev => ({ ...prev, user: userDetails })),
}));

export const useUserStore = create(persist(userStore, { name: 'user' }));
