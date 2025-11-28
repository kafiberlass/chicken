import React, { useState, useEffect } from 'react';
import ClientList from '../components/client/ClientList';
import Dashboard from '../components/dashboard/Dashboard.jsx';
import '../styles/global.css';
import { clientApi } from '../services/clientApi';

export default function MainDashboard({ onClientSelect }) {
    const [view, setView] = useState('overview');
    const [clients, setClients] = useState([]);
    const [stats, setStats] = useState({});

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        const clientsData = await clientApi.getAll();
        const statsData = await clientApi.getStats();
        setClients(clientsData);
        setStats(statsData);
    };

    return (
        <div className="main-dashboard">
            <div className="dashboard-header">
                <h1>Панель управления прогнозами доходов</h1>
                <p>Точный прогноз — уверенные решения для Банка</p>
            </div>

            <div className="view-switcher">
                <button
                    className={view === 'overview' ? 'active' : ''}
                    onClick={() => setView('overview')}
                >
                    📊 Обзор системы
                </button>
                <button
                    className={view === 'clients' ? 'active' : ''}
                    onClick={() => setView('clients')}
                >
                    👥 База клиентов
                </button>
            </div>

            {view === 'overview' ? (
                <Dashboard stats={stats} clients={clients} onClientSelect={onClientSelect} />
            ) : (
                <ClientList clients={clients} onClientSelect={onClientSelect} />
            )}
        </div>
    );
}