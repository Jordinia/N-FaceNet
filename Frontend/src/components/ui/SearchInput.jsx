import React from 'react';
import { Search } from 'lucide-react';

const SearchInput = ({ 
  placeholder = 'Search...', 
  value, 
  onChange,
  className = '',
  ...props 
}) => {
  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
      <input
        type="text"
        className={`w-full pl-10 pr-4 py-2 bg-gray-100 rounded-lg border-transparent focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-200 ${className}`}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        {...props}
      />
    </div>
  );
};

export default SearchInput;