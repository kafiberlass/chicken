// src/pages/ModelInsights.jsx
import React from 'react';

export default function ModelInsights() {
    return (
        <div style={{
            background: 'white',
            padding: '2rem',
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
            <h2>Анализ ML модели</h2>
            <p style={{ color: '#64748b', marginTop: '1rem' }}>
                Здесь будет отображаться информация о производительности модели,
                метрики качества и другие аналитические данные.
            </p>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1rem',
                marginTop: '2rem'
            }}>
                <div style={{
                    background: '#f8fafc',
                    padding: '1.5rem',
                    borderRadius: '6px',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🤖</div>
                    <div style={{ fontWeight: 'bold', color: '#1e293b' }}>Gradient Boosting</div>
                    <div style={{ color: '#64748b', fontSize: '0.9rem' }}>Алгоритм</div>
                </div>

                <div style={{
                    background: '#f8fafc',
                    padding: '1.5rem',
                    borderRadius: '6px',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📊</div>
                    <div style={{ fontWeight: 'bold', color: '#1e293b' }}>0.124</div>
                    <div style={{ color: '#64748b', fontSize: '0.9rem' }}>WMAE</div>
                </div>

                <div style={{
                    background: '#f8fafc',
                    padding: '1.5rem',
                    borderRadius: '6px',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🎯</div>
                    <div style={{ fontWeight: 'bold', color: '#1e293b' }}>82.3%</div>
                    <div style={{ color: '#64748b', fontSize: '0.9rem' }}>Точность</div>
                </div>
            </div>
        </div>
    );
}