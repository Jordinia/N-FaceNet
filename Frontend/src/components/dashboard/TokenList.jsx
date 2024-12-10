import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TokenCard } from './TokenCard';

export const TokenList = () => {
    const [tokens, setTokens] = useState([]);

    const fetchTokens = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/token');
            if (response.data.status === 'success') {
                setTokens(response.data.data);
            }
        } catch (error) {
            console.error('Error fetching tokens:', error);
        }
    };

    useEffect(() => {
        fetchTokens();
    }, []);

    return (
        <div className="bg-white rounded-xl p-6 mt-8">
            <h2 className="text-xl font-bold mb-4">Tokens</h2>
            <div className="space-y-3">
                {tokens.length === 0 && <p className="text-gray-500 text-center">All tokens have been approved.</p>}
                {tokens.map((token) => (
                    <TokenCard key={token.token_id} token={token} onAction={fetchTokens} />
                ))}
            </div>
        </div>
    );
};
