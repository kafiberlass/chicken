import { useState } from 'react';
import { ClientList } from '../components/client/ClientList';
import { Dashboard } from '../components/dashboard/Dashboard';
import { Loader, ErrorState } from '../components/common/Status';
import { clientApi } from '../services/clientApi';
import { useApi } from '../hooks/useApi';
import type { Client } from '../types';
import '../styles/global.css';

interface MainDashboardProps {
    onClientSelect: (client: Client) => void;
}

export function MainDashboard({ onClientSelect }: MainDashboardProps) {
    const [view, setView] = useState<'overview' | 'clients'>('overview');

    // Клиенты и статистика грузятся параллельно одним запросом-обёрткой
    const { data, error, loading, reload } = useApi(
        (signal) => Promise.all([clientApi.getAll(signal), clientApi.getStats(signal)]),
        [],
    );

    if (loading) return <Loader text="Загружаем данные клиентов..." />;
    if (error || !data) return <ErrorState error={error ?? new Error('Нет данных')} onRetry={reload} />;

    const [clients, stats] = data;

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
