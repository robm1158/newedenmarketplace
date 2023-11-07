import React, { useContext, useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import AuthContext from '../AuthContext/AuthContext';
import { LoginPopup } from '../LoginPopup/LoginPopup'; // Adjust the import path as needed

export const PrivateRoute = ({ children }) => {
  const { auth } = useContext(AuthContext);
  const [popupOpen, setPopupOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    if (!auth && location.pathname === '/userprofile') {
      console.log('User is not authenticated, should show popup');
      setPopupOpen(true);
    }
  }, [auth, location]);

  const handleClose = () => {
    setPopupOpen(false);
    console.log('Popup closed');
  };

  // If the user is authenticated or the popup is not open, render the children.
  // Otherwise, render nothing, and the popup will handle the message to the user.
  return (
    <>
      {auth || !popupOpen ? children : null}
      <LoginPopup open={popupOpen} onClose={handleClose} />
    </>
  );
};
