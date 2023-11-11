import { createContext } from 'react';

// Initial value can be whatever you prefer
const PaidContext = createContext({
  isPaid: false,
  setPaid: () => {}
});

export default PaidContext;