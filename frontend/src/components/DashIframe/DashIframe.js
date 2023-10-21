import React from 'react';

function DashIframe() {
  return (
    <iframe 
      src="http://127.0.0.1:5000/dashboard/" 
      title="Dash App" 
      width="100%" 
      height="600px" 
      style={{border: 'none'}}
    ></iframe>
  );
}

export default DashIframe;