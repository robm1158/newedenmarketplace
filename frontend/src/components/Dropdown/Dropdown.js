import React from 'react';
import './Dropdown.css';

const Dropdown = ({ options, onChange }) => {
  return (
    <select className="dropdown" onChange={(e) => onChange(e.target.value)}>
      {options.map((option, index) => (
        <option key={index} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
};

export default Dropdown;