import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import AuthContext from '../AuthContext/AuthContext';

export const PrivateRoute = ({ children, ...rest }) => {
  const { auth } = useContext(AuthContext);

  return auth ? children : <Navigate to="/" />;
};