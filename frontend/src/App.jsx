import React, { useState } from 'react';
import MainDashboard from './pages/MainDashboard';
import ClientAnalysis from './pages/ClientAnalysis';
import ModelInsights from './pages/ModelInsights';
import './styles/global.css';

function App() {
    const [currentView, setCurrentView] = useState('dashboard');
    const [selectedClient, setSelectedClient] = useState(null);

    // Функция для выбора клиента с автоматическим переходом
    const handleClientSelect = (client) => {
        setSelectedClient(client);
        setCurrentView('analysis'); // Автоматически переходим к анализу
    };

    const renderView = () => {
        switch (currentView) {
            case 'dashboard':
                return <MainDashboard onClientSelect={handleClientSelect} />;
            case 'analysis':
                return <ClientAnalysis client={selectedClient} />;
            case 'insights':
                return <ModelInsights />;
            default:
                return <MainDashboard onClientSelect={handleClientSelect} />;
        }
    };

    return (
        <div className="app">
            <header className="app-header">
                <div className="header-brand">
                    <div className="logo">🏦</div>
                    <h1>Прогноз доходов</h1>
                </div>
                <nav className="header-nav">
                    <button
                        className={currentView === 'dashboard' ? 'nav-btn active' : 'nav-btn'}
                        onClick={() => setCurrentView('dashboard')}
                    >
                        📊 Дашборд
                    </button>
                    <button
                        className={currentView === 'analysis' ? 'nav-btn active' : 'nav-btn'}
                        onClick={() => setCurrentView('analysis')}
                        // УБРАЛИ disabled - кнопка всегда доступна
                    >
                        👤 Анализ клиента
                    </button>
                    <button
                        className={currentView === 'insights' ? 'nav-btn active' : 'nav-btn'}
                        onClick={() => setCurrentView('insights')}
                    >
                        🤖 Модель
                    </button>
                </nav>
            </header>
            <main className="main-content">
                {renderView()}
            </main>
        </div>
    );
}

export default App;