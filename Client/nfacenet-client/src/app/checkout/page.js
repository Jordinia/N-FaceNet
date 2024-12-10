'use client'

import React, { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Checkout() {
    const [nik, setNik] = useState("");
    const [employeeData, setEmployeeData] = useState(null);
    const inputRef = useRef(null);

    const router = useRouter();

    const handleGoToCheckin = () => {
        router.push('/'); // Navigate to /register page
    };

    useEffect(() => {
        // Autofocus the input field when the component mounts
        if (inputRef.current) {
            inputRef.current.focus();
        }
    }, []);

    const handleNikSubmit = async () => {
        if (!nik) {
            alert("Please enter a valid NIK.");
            return;
        }

        try {
            const response = await fetch(`http://localhost:5000/employee?nik=${nik}`);
            if (!response.ok) {
                throw new Error(`Error fetching employee data: ${response.status}`);
            }

            const result = await response.json();
            if (result.status === "success" && result.data.length > 0) {
                const employee = result.data[0];
                setEmployeeData(employee);

                // Send employee_id to the checkout API
                await handleCheckout(employee.employee_id);
            } else {
                alert("Employee not found.");
                setEmployeeData(null);
            }
        } catch (error) {
            console.error("Error fetching employee data:", error);
            alert("Failed to retrieve employee data. Please try again.");
        }
    };

    const handleCheckout = async (employeeId) => {
        try {
            const response = await fetch(`http://localhost:5000/entry/checkout/${employeeId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error(`Error during checkout: ${response.status}`);
            }

            alert("Checkout successful.");
        } catch (error) {
            console.error("Error during checkout:", error);
            alert("Checkout failed. Please try again.");
        }
    };

    const handleInputKeyDown = (event) => {
        if (event.key === "Enter") {
            handleNikSubmit();
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-2xl font-bold mb-4">Employee Checkout</h1>

            <input
                ref={inputRef}
                type="text"
                placeholder="Enter NIK"
                value={nik}
                onChange={(e) => setNik(e.target.value)}
                onKeyDown={handleInputKeyDown}
                className="px-4 py-2 w-64 text-center bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
            />

            {employeeData && (
                <div className="mt-8 p-4 bg-white rounded-lg shadow-md">
                    <h2 className="text-lg font-semibold">Employee Details</h2>
                    <p><strong>Name:</strong> {employeeData.name}</p>
                    <p><strong>NIK:</strong> {employeeData.nik}</p>
                    <p><strong>Current Room:</strong> {employeeData.room}</p>
                </div>
            )}
            
            <button
                onClick={handleGoToCheckin}
                className="mt-6 p-2 bg-green-500 text-white rounded-full shadow-md hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2"
            >
                Check In
            </button>
        </div>
    );
}
