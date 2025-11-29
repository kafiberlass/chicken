import React, { useState, useEffect } from 'react';
import { ClientList } from '../components/client/ClientList';
import { Client } from "../types";
import { Dashboard } from "../components/dashboard/Dashboard";
import '../styles/global.css';
import { clientApi } from '../services/clientApi';

interface MainDashboardProps {
    onClientSelect: (client: Client) => void;
}

interface Stats {
    totalClients?: number;
    averageIncome?: number;
}

export function MainDashboard({ onClientSelect }: MainDashboardProps) {
    const [view, setView] = useState<'overview' | 'clients'>('overview');
    const [clients, setClients] = useState<Client[]>([]);
    const [stats, setStats] = useState<Stats>({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const [clientsData, statsData] = await Promise.all([
                clientApi.getAll(),
                clientApi.getStats()
            ]);
            setClients(clientsData);
            setStats(statsData);
        } catch (error) {
            console.error('Error loading data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div>Загрузка...</div>;
    }

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