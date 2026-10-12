import { useState, useEffect } from 'react';
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
    // Тему читаем из localStorage сразу при создании state (ленивая инициализация),
    // чтобы не было мигания светлой темы при перезагрузке
    const [theme, setTheme] = useState<'light' | 'dark'>(() => {
        try {
            return localStorage.getItem('theme') === 'dark' ? 'dark' : 'light';
        } catch {
            return 'light';
        }
    });

    // Сохраняем тему в localStorage и применяем к документу
    useEffect(() => {
        try {
            localStorage.setItem('theme', theme);
        } catch {
            // localStorage может быть недоступен (приватный режим) — тема просто не сохранится
        }
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