import { createContext } from 'react';

const AuthContext = createContext({
  auth: null,
  setAuth: () => {}
});

export default AuthContext;