import React, { useState } from 'react';
import {MainDashboard} from './pages/MainDashboard';
import { ClientAnalysis } from './pages/ClientAnalysis';
import {ModelInsights} from './pages/ModelInsights';
import { Sidebar } from './components/common/Sidebar';
import { Client } from './types';
import './styles/global.css';

function App() {
    const [currentView, setCurrentView] = useState<string>('dashboard');
    const [selectedClient, setSelectedClient] = useState<Client | null>(null);

    const renderView = () => {
        switch (currentView) {
            case 'dashboard':
                return <MainDashboard onClientSelect={setSelectedClient} />;
            case 'analysis':
                return <ClientAnalysis client={selectedClient} />;
            case 'insights':
                return <ModelInsights />;
            case 'clients':
                return (
                    <div style={{ padding: '2rem' }}>
                        <h2>База клиентов</h2>
                        <p>Здесь будет полная база клиентов...</p>
                    </div>
                );
            case 'reports':
                return (
                    <div style={{ padding: '2rem' }}>
                        <h2>Отчеты</h2>
                        <p>Здесь будут отчеты по эффективности модели...</p>
                    </div>
                );
            case 'settings':
                return (
                    <div style={{ padding: '2rem' }}>
                        <h2>Настройки</h2>
                        <p>Настройки модели и системы...</p>
                    </div>
                );
            default:
                return <MainDashboard onClientSelect={setSelectedClient} />;
        }
    };

    return (
        <div className="app-with-sidebar">
            <Sidebar
                currentView={currentView}
                onViewChange={setCurrentView}
                selectedClient={selectedClient}
            />
            <main className="main-content-with-sidebar">
                {renderView()}
            </main>
        </div>
    );
}

export default App;