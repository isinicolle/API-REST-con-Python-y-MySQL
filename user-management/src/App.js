import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [users, setUsers] = useState([]);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [editUserId, setEditUserId] = useState(null);

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        const response = await axios.get('http://127.0.0.1:5000/users');
        setUsers(response.data);
    };

    const createUser = async () => {
        const response = await axios.post('http://127.0.0.1:5000/users', {
            name,
            email
        });
        setUsers([...users, { id: response.data.id, name, email }]);
        setName('');
        setEmail('');
    };

    const updateUser = async () => {
        await axios.put(`http://127.0.0.1:5000/users/${editUserId}`, {
            name,
            email
        });
        setUsers(users.map(user => (user.id === editUserId ? { ...user, name, email } : user)));
        setName('');
        setEmail('');
        setEditUserId(null);
    };

    const deleteUser = async (id) => {
        await axios.delete(`http://127.0.0.1:5000/users/${id}`);
        setUsers(users.filter(user => user.id !== id));
    };

    return (
        <div>
            <h1>Gestión de Usuarios</h1>
            <input 
                type="text" 
                placeholder="Nombre" 
                value={name} 
                onChange={e => setName(e.target.value)} 
            />
            <input 
                type="email" 
                placeholder="Email" 
                value={email} 
                onChange={e => setEmail(e.target.value)} 
            />
            <button onClick={editUserId ? updateUser : createUser}>
                {editUserId ? 'Actualizar Usuario' : 'Crear Usuario'}
            </button>

            <h2>Usuarios</h2>
            <ul>
                {users.map(user => (
                    <li key={user.id}>
                        {user.name} - {user.email}
                        <button onClick={() => {
                            setEditUserId(user.id);
                            setName(user.name);
                            setEmail(user.email);
                        }}>Editar</button>
                        <button onClick={() => deleteUser(user.id)}>Eliminar</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
