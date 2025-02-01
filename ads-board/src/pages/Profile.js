import React, { useState, useEffect } from "react";
import API from "../api"; // Adjust the import path as necessary

const Profile = () => {
    const [user, setUser] = useState({ username: '', email: '', avatar: '' });
    const [message, setMessage] = useState('');

    useEffect(() => {
        // Fetch user data on component mount
        const fetchUserData = async () => {
            try {
                const response = await API.get('/auth/user/');
                setUser(response.data);
            } catch (error) {
                console.error("Error fetching user data:", error);
            }
        };
        fetchUserData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUser({ ...user, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await API.patch('/auth/user/update/', user); // Ensure this is the correct endpoint
            setMessage("Profile updated successfully!");
            setUser(response.data);
        } catch (error) {
            setMessage("Error updating profile.");
            console.error("Error updating profile:", error);
        }
    };

    return (
        <div>
            <h1>Profile Page</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input type="text" name="username" value={user.username} onChange={handleChange} />
                </div>
                <div>
                    <label>Email:</label>
                    <input type="email" name="email" value={user.email} onChange={handleChange} />
                </div>
                <div>
                    <label>Avatar URL:</label>
                    <input type="text" name="avatar" value={user.avatar} onChange={handleChange} />
                </div>
                <button type="submit">Update Profile</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Profile;
