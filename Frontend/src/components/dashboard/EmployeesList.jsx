import React, { useState, useEffect } from 'react';
import { Search, Plus } from 'lucide-react';
import { EmployeeCard } from './EmployeeCard';
import { Modal, message } from 'antd';
import axios from 'axios';

export const EmployeesList = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [nik, setNik] = useState('');
  const [gender, setGender] = useState('');
  const [employeeList, setEmployeeList] = useState([]);

  // Fetch employees from API
  const fetchEmployees = async (query = '') => {
    try {
      const response = await axios.get(`http://localhost:5000/employee?name=${query}`);
      const employees = response.data.data.map((employee) => ({
        ...employee,
        location: employee.room || 'Away',
        avatar: `https://picsum.photos/seed/${employee.employee_id}/200`, // Generate avatar from employee ID
      }));
      setEmployeeList(employees);
    } catch (error) {
      console.error('Error fetching employees:', error);
      message.error('Failed to fetch employees');
    }
  };

  useEffect(() => {
    fetchEmployees(); // Initial load
  }, []);

  const showModal = () => setIsModalOpen(true);

  const handleOk = async () => {
    if (!name || !age || !nik || gender === '') {
      message.warning('Please fill out all fields');
      return;
    }

    try {
      const newEmployee = { nik, name, gender: gender === '1', age: parseInt(age, 10) };
      const response = await axios.post('http://localhost:5000/employee', newEmployee);

      if (response.data.status === 'success') {
        message.success('Employee added successfully');
        fetchEmployees(); // Refetch employees
        resetFields();
        setIsModalOpen(false);
      } else {
        message.error('Failed to add employee');
      }
    } catch (error) {
      console.error('Error adding employee:', error);
      message.error('Failed to add employee');
    }
  };

  const resetFields = () => {
    setName('');
    setAge('');
    setNik('');
    setGender('');
  };

  const handleCancel = () => {
    resetFields();
    setIsModalOpen(false);
  };

  const handleSearch = (e) => {
    const query = e.target.value;
    fetchEmployees(query);
  };

  return (
    <div className="bg-white rounded-xl p-6">
      <h2 className="text-xl font-bold mb-4">Employees</h2>
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
        <input
          onChange={handleSearch}
          type="text"
          placeholder="Find your employee"
          className="w-full pl-10 pr-4 py-2 bg-gray-100 rounded-lg"
        />
      </div>
      <div className="space-y-3">
        {employeeList.length === 0 && <p className="text-gray-500 text-center">No employees found.</p>}
        {employeeList.map((employee) => (
          <EmployeeCard key={employee.employee_id} employee={employee} />
        ))}
        <button
          onClick={showModal}
          className="w-full py-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors flex items-center justify-center gap-2"
        >
          <Plus className="w-5 h-5" />
          <span className="font-medium">Add Employee</span>
        </button>
      </div>

      {/* Modal */}
      <Modal title="Add Employee" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
        <div className="flex flex-col gap-4">
          <div>
            <label htmlFor="name">Employee Name</label>
            <input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              type="text"
              className="w-full px-4 py-2 rounded-lg"
            />
          </div>
          <div>
            <label htmlFor="age">Employee Age</label>
            <input
              id="age"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              type="number"
              className="w-full px-4 py-2 rounded-lg"
            />
          </div>
          <div>
            <label htmlFor="nik">Employee NIK</label>
            <input
              id="nik"
              value={nik}
              onChange={(e) => setNik(e.target.value)}
              type="text"
              className="w-full px-4 py-2 rounded-lg"
            />
          </div>
          <div>
            <label htmlFor="gender">Employee Gender</label>
            <select
              id="gender"
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              className="w-full px-4 py-2 rounded-lg"
            >
              <option value="">Select Gender</option>
              <option value="0">Male</option>
              <option value="1">Female</option>
            </select>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default EmployeesList;
