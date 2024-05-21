import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Container, Typography, Box, Switch, FormControlLabel } from '@mui/material';

function AuthForm({ setLoggedIn }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [username, setUsername] = useState('');
    const [isLogin, setIsLogin] = useState(true);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const url = isLogin ? 'http://localhost:5000/login' : 'http://localhost:5000/register';
        const payload = isLogin ? { email, password } : { username, email, password };

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();
            if (response.ok) {
                if (isLogin) {
                    setLoggedIn(true);
                    navigate('/');
                } else {
                    alert(data.message);
                    setIsLogin(true);
                }
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <Container maxWidth="xs">
            <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                minHeight="100vh"
            >
                <Typography variant="h4" component="h1" gutterBottom>
                    {isLogin ? 'Login' : 'Register'}
                </Typography>
                <form onSubmit={handleSubmit} style={{ width: '100%' }}>
                    {!isLogin && (
                        <TextField
                            label="Username"
                            variant="outlined"
                            margin="normal"
                            fullWidth
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    )}
                    <TextField
                        label="Email"
                        type="email"
                        variant="outlined"
                        margin="normal"
                        fullWidth
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <TextField
                        label="Password"
                        type="password"
                        variant="outlined"
                        margin="normal"
                        fullWidth
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        style={{ margin: '20px 0' }}
                    >
                        {isLogin ? 'Login' : 'Register'}
                    </Button>
                </form>
                <FormControlLabel
                    control={
                        <Switch
                            checked={!isLogin}
                            onChange={() => setIsLogin(!isLogin)}
                            name="mode"
                            color="primary"
                        />
                    }
                    label={isLogin ? 'Switch to Register' : 'Switch to Login'}
                />
            </Box>
        </Container>
    );
}

export default AuthForm;
