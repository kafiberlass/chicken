import React, { useState, useEffect } from 'react';
import { MainDashboard } from './pages/MainDashboard';
import { ClientAnalysis } from './pages/ClientAnalysis';
import { ModelInsights } from './pages/ModelInsights';
import { Sidebar } from './components/common/Sidebar';
import { Settings } from './pages/Settings';
import { Client } from './types';
import './styles/global.css';

function App() {
    const [currentView, setCurrentView] = useState<string>('dashboard');
    const [selectedClient, setSelectedClient] = useState<Client | null>(null);
    const [theme, setTheme] = useState<'light' | 'dark'>('light');

    // Загружаем тему из localStorage при загрузке
    useEffect(() => {
        const savedTheme = localStorage.getItem('theme') as 'light' | 'dark';
        if (savedTheme) {
            setTheme(savedTheme);
        }
    }, []);

    // Сохраняем тему в localStorage и применяем к документу
    useEffect(() => {
        localStorage.setItem('theme', theme);
        document.documentElement.setAttribute('data-theme', theme);
    }, [theme]);

    // Функция переключения темы
    const toggleTheme = () => {
        setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
    };

    const renderView = () => {
        switch (currentView) {
            case 'dashboard':
                return <MainDashboard onClientSelect={setSelectedClient} />;
            case 'analysis':
                return <ClientAnalysis client={selectedClient} />;
            case 'insights':
                return <ModelInsights />;
            case 'settings':
                return <Settings theme={theme} onThemeToggle={toggleTheme} />; // Используем компонент Settings
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
                theme={theme}
                onThemeToggle={toggleTheme}
            />
            <main className="main-content-with-sidebar">
                {renderView()}
            </main>
        </div>
    );
}

export default App;