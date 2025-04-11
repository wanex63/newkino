import React from 'react';
import { useAuth } from '../../context/AuthContext';

const RegisterPage = () => {
    const { login } = useAuth();

    return (
        <div>
            <h2>Register</h2>
            <button onClick={() => login({ name: 'User' })}>Register</button>
        </div>
    );
};

export default RegisterPage;
