// src/components/client/ClientCard.jsx
import React from 'react';

export default function ClientCard({ client, onSelect }) {
    return (
        <div
            className="client-card"
            onClick={() => onSelect(client)}
            style={{
                margin: "10px",
                background: 'white',
                padding: '1rem',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                cursor: 'pointer',
                border: '2px solid transparent',
                transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = '#3b82f6';
                e.currentTarget.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'transparent';
                e.currentTarget.style.transform = 'translateY(0)';
            }}
        >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                <h3 style={{ margin: 0, color: '#1e293b' }}>{client.name}</h3>
                <span style={{
                    background: client.segment === 'vip' ? '#f59e0b' : '#3b82f6',
                    color: 'white',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '12px',
                    fontSize: '0.8rem',
                    fontWeight: 'bold'
                }}>
          {client.segment}
        </span>
            </div>

            <div style={{ color: '#64748b', fontSize: '0.9rem' }}>
                <div>ID: {client.id}</div>
                <div>Возраст: {client.age} лет</div>
                <div>Профессия: {client.occupation}</div>
                <div>Город: {client.city}</div>
                <div style={{ marginTop: '0.5rem', fontWeight: 'bold', color: '#059669' }}>
                    Доход: {client.currentIncome?.toLocaleString('ru-RU')} ₽
                </div>
            </div>

            <button
                style={{
                    marginTop: '1rem',
                    width: '100%',
                    background: '#3b82f6',
                    color: 'white',
                    border: 'none',
                    padding: '0.5rem',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontWeight: 'bold'
                }}
            >
                Анализировать ›
            </button>
        </div>
    );
}