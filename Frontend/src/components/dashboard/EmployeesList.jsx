import React, { useState } from 'react';
import { Search, Plus } from 'lucide-react';
import { EmployeeCard } from './EmployeeCard';
import { Modal } from 'antd';
import { employees } from '../../utils/dummy/employeeData';

export const EmployeesList = () => {

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [name, setName] = useState('');
  const [role, setRole] = useState('');
  const [age, setAge] = useState(0);
  const [nik, setNik] = useState('');
  const [gender, setGender] = useState();
  const [employeeList, setEmployeeList] = useState(employees);

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    if ([name, role, age, nik, gender].includes('')) return;
    setIsModalOpen(false);
    const newEmployee = {
      id: Date.now(),
      current_room_id: -1,
      gender,
      age,
      top_color_id: 16,
      bottom_color_id: 17,
      // role_id: 17,
      nik,
      face_path: 'Employees/32',

      name,
      role,
      location: '',
      avatar: 'http://fakeimg.pl/40x40'
    }

    setEmployeeList([newEmployee, ...employeeList])
    resetField()
  };

  const resetField = () => {
    setName('');
    setRole('');
    setAge(0);
    setNik('');
    setGender();
  }

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const filterEmployee = (value) => {
    const filteredEmployees = employees.filter(employee => employee.name.toLowerCase().includes(value.toLowerCase()));
    setEmployeeList(filteredEmployees);
  }

  return (
    <div className="bg-white rounded-xl p-6">
      <h2 className="text-xl font-bold mb-4">Employees</h2>
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
        <input
          onChange={(e) => filterEmployee(e.target.value)}
          type="text"
          placeholder="Find your employee"
          className="w-full pl-10 pr-4 py-2 bg-gray-100 rounded-lg"
        />
      </div>
      <div className="space-y-3">
        {employeeList.length === 0 && <p className="text-gray-500 text-center">No employees found.</p>}
        {employeeList.map(employee => (
          <EmployeeCard key={employee.id} employee={employee} />
        ))}
        <button onClick={showModal} className="w-full py-3 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors flex items-center justify-center gap-2">
          <Plus className="w-5 h-5" />
          <span className="font-medium">Add Employee</span>
        </button>
      </div>


      {/* Modal */}
      <Modal title="Add employee" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
        <div className='flex gap-2 w-full items-center justify-center mb-4'>
          <div className='flex flex-col w-full'>
            <label htmlFor="name">Employee Name</label>
            <input onChange={(e) => setName(e.target.value)} id='name' type="text" className='w-full px-4 py-2 rounded-lg' />
          </div>
          <div className='flex flex-col w-full'>
            <label htmlFor="role">Employee Role</label>
            <input onChange={(e) => setRole(e.target.value)} id='role' type="text" className='w-full px-4 py-2 rounded-lg' />
          </div>
        </div>
        <div className='flex gap-2 w-full items-center justify-center mb-4'>
          <div className='flex flex-col w-full'>
            <label htmlFor="age">Employee Age</label>
            <input onChange={(e) => setAge(e.target.value)} id='age' type="number" className='w-full px-4 py-2 rounded-lg' />
          </div>
          <div className='flex flex-col w-full'>
            <label htmlFor="nik">Employee NIk</label>
            <input onChange={(e) => setNik(e.target.value)} id='nik' type="number" className='w-full px-4 py-2 rounded-lg' />
          </div>
        </div>
        <div className='flex gap-2 w-full items-center justify-center mb-4'>
          <div className='flex flex-col w-full'>
            <label htmlFor="gender">Employee Gender</label>
            <select onChange={(e) => setGender(e.target.value)} name="gender" id="gender" className='w-full px-4 py-2 rounded-lg'>
              <option selected value="">Select Gender</option>
              <option value="1">Male</option>
              <option value="0">Female</option>
            </select>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default EmployeesList;
