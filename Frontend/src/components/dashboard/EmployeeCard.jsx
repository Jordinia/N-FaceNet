import React from 'react';

export const EmployeeCard = ({ employee }) => {
  return (
    <div className="flex items-center justify-between p-3 bg-gray-100 rounded-lg">
      <div className="flex items-center gap-3">
        <img
          src={employee.avatar}
          alt={employee.name}
          className="w-10 h-10 rounded-full"
        />
        <div>
          <div className="font-semibold">{employee.name}</div>
        </div>
      </div>
      <div className="text-sm text-gray-500">
        at {employee.location}
      </div>
    </div>
  );
};

export default EmployeeCard;
