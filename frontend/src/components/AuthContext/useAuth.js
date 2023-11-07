import { useContext } from 'react';
import AuthContext from './AuthContext';

// A custom hook to quickly access the auth context
const useAuth = () => {
    return useContext(AuthContext);
};

export default useAuth;
