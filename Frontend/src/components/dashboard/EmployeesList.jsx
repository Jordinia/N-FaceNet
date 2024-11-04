import React from 'react';
import { Search, Plus } from 'lucide-react';
import { EmployeeCard } from './EmployeeCard';

export const EmployeesList = ({ employees }) => {
  return (
    <div className="bg-white rounded-xl p-6">
      <h2 className="text-xl font-bold mb-4">Employees</h2>
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
        <input
          type="text"
          placeholder="Find your employee"
          className="w-full pl-10 pr-4 py-2 bg-gray-100 rounded-lg"
        />
      </div>
      <div className="space-y-3">
        {employees.map(employee => (
          <EmployeeCard key={employee.id} employee={employee} />
        ))}
        <button className="w-full py-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors flex items-center justify-center gap-2">
          <Plus className="w-5 h-5" />
          <span className="font-medium">Add Employee</span>
        </button>
      </div>
    </div>
  );
};

export default EmployeesList;
