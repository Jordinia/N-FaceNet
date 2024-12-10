'use client';

import React, { useState } from "react";
import { useRouter } from 'next/navigation'; // Import the useRouter hook

export default function RegisterForm() {
  const router = useRouter(); // Initialize the useRouter hook

  const handleGoToRegister = () => {
    router.push('/register'); // Navigate to /register page
  };

  const [formData, setFormData] = useState({
    nik: "",
    name: "",
    gender: "Male", // Default value
    age: "",
  });
  const [token, setToken] = useState(""); // State untuk menyimpan token

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://100.71.234.28:5000/employee", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nik: formData.nik,
          name: formData.name,
          gender: formData.gender === "Male",
          age: parseInt(formData.age, 10),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create employee");
      }

      const result = await response.json();

      // Simpan token di state
      setToken(result.authentication.token);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(token);
    alert("Token copied to clipboard!"); // Pemberitahuan bahwa token berhasil disalin
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-6 text-gray-900">Register Employee</h1>
      
      {/* Form hanya ditampilkan jika token belum diterima */}
      {!token ? (
        <form
          onSubmit={handleSubmit}
          className="bg-white p-6 rounded-lg shadow-md w-full max-w-md"
        >
          {/* NIK Field */}
          <div className="mb-4">
            <label htmlFor="nik" className="block text-sm font-medium text-gray-700">
              NIK
            </label>
            <input
              type="text"
              id="nik"
              name="nik"
              value={formData.nik}
              onChange={handleInputChange}
              className="mt-1 p-2 block w-full border rounded-md text-gray-900"
              required
            />
          </div>

          {/* Name Field */}
          <div className="mb-4">
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">
              Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className="mt-1 p-2 block w-full border rounded-md text-gray-900"
              required
            />
          </div>

          {/* Gender Field */}
          <div className="mb-4">
            <label htmlFor="gender" className="block text-sm font-medium text-gray-700">
              Gender
            </label>
            <select
              id="gender"
              name="gender"
              value={formData.gender}
              onChange={handleInputChange}
              className="mt-1 p-2 block w-full border rounded-md text-gray-900"
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>

          {/* Age Field */}
          <div className="mb-4">
            <label htmlFor="age" className="block text-sm font-medium text-gray-700">
              Age
            </label>
            <input
              type="number"
              id="age"
              name="age"
              value={formData.age}
              onChange={handleInputChange}
              className="mt-1 p-2 block w-full border rounded-md text-gray-900"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
          >
            Submit
          </button>
        </form>
      ) : (
        // Tampilkan token dan tombol salin jika token sudah diterima
        <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md text-center">
          <p className="text-lg font-medium">Token:</p>
          <p className="bg-gray-100 p-2 rounded-md my-4">{token}</p>
          <button
            onClick={handleCopyToClipboard}
            className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700"
          >
            Copy to Clipboard
          </button>

          {/* New Button to Go to Register Page */}
          <button
            onClick={handleGoToRegister}
            className="mt-6 p-2 bg-green-500 text-white rounded-full shadow-md hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2"
          >
            Register
          </button>
        </div>
      )}
    </div>
  );
}
