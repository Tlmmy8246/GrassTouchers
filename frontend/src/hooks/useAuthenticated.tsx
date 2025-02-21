import { useUserStore } from "store/useUserStore"

const useAuthenticated = () => {
  const user = useUserStore(state => state.user); // TODO: LATER CHECK FOR ACCESS_TOKEN AND SENDING AN API REQUEST TO CHECK IF THE TOKEN IS VALID

  const isAuthenticated = !!user;

  return { isAuthenticated };
}

export default useAuthenticated;
