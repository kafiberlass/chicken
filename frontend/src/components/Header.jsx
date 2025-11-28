import React from 'react';

export default function Header() {
    return (
        <header style={{
            background: '#1a73e8',
            color: 'white',
            padding: '1rem 2rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
        }}>
            <h1 style={{ margin: 0 }}>🏦 Bank Online</h1>
            <nav>
                <button style={{
                    background: 'rgba(255,255,255,0.2)',
                    border: 'none',
                    color: 'white',
                    padding: '0.5rem 1rem',
                    borderRadius: '4px',
                    cursor: 'pointer'
                }}>
                    Выйти
                </button>
            </nav>
        </header>
    );
}