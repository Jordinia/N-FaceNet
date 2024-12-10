import React from 'react';
import axios from 'axios';

export const TokenCard = ({ token, onAction }) => {
    const handleActionClick = async () => {
        try {
            await axios.put(`http://localhost:5000/token/${token.token_id}`);
            onAction(); // Trigger a refetch
        } catch (error) {
            console.error('Error performing token action:', error);
        }
    };

    return (
        <div className="p-4 bg-white rounded-lg shadow-md flex justify-between items-center">
            <span className="font-medium">{token.name}</span>
            <button
                onClick={handleActionClick}
                className="px-3 py-1 bg-blue-500 text-white text-sm rounded-lg hover:bg-blue-600"
            >
                Action
            </button>
        </div>
    );
};
