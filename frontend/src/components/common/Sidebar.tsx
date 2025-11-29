import { Client } from '../../types';
import '../../styles/sidebar.css';

interface SidebarProps {
    currentView: string;
    onViewChange: (view: string) => void;
    selectedClient: Client | null;
    theme: 'light' | 'dark'; // Добавляем theme
    onThemeToggle: () => void; // Добавляем onThemeToggle
}

export function Sidebar({ currentView, onViewChange, selectedClient, theme, onThemeToggle }: SidebarProps) {
    const menuItems = [
        { id: 'dashboard', label: 'Панель управления', icon: '📊', badge: null },
        { id: 'analysis', label: 'Анализ клиента', icon: '👤', badge: selectedClient ? '✓' : null },
        { id: 'insights', label: 'Аналитика модели', icon: '🤖', badge: null },
        { id: 'clients', label: 'База клиентов', icon: '👥', badge: null },
        { id: 'settings', label: 'Настройки', icon: '⚙️', badge: null },
    ];

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <div className="sidebar-logo">
                    <div className="logo-icon">🏦</div>
                    <div className="logo-text">
                        <div className="logo-title">Альфа доходы</div>
                        <div className="logo-subtitle">Прогноз доходов</div>
                    </div>
                </div>
            </div>

            <nav className="sidebar-nav">
                {menuItems.map((item) => (
                    <button
                        key={item.id}
                        className={`sidebar-item ${currentView === item.id ? 'active' : ''}`}
                        onClick={() => onViewChange(item.id)}
                    >
                        <span className="sidebar-icon">{item.icon}</span>
                        <span className="sidebar-label">{item.label}</span>
                        {item.badge && <span className="sidebar-badge">{item.badge}</span>}
                    </button>
                ))}
            </nav>

            <div className="sidebar-footer">
                <div className="theme-toggle-sidebar">
                    <button
                        onClick={onThemeToggle}
                        className="theme-toggle-btn"
                        title={theme === 'light' ? 'Переключить на тёмную тему' : 'Переключить на светлую тему'}
                    >
                        {theme === 'light' ? '🌙' : '☀️'}
                    </button>
                </div>

                <div className="user-info">
                    <div className="user-avatar">👨‍💼</div>
                    <div className="user-details">
                        <div className="user-name">Сотрудник банка</div>
                        <div className="user-role">Менеджер</div>
                    </div>
                </div>
            </div>
        </div>
    );
}