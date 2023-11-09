import React from 'react';
import { useNavigate } from 'react-router-dom';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';

export const LoginPopup = ({ open, onClose }) => {
  const navigate = useNavigate();

  const handleClose = () => {
    onClose();  // Close the popup
    navigate('/');  // Redirect to the home page
  };

  return (
    <Dialog open={open} onClose={handleClose}>
      <DialogTitle>{"Access Denied"}</DialogTitle>
      <DialogContent dividers>
        You must log in to view this page.
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="primary">
          OK
        </Button>
      </DialogActions>
    </Dialog>
  );
};
