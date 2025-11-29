interface SidebarProps {
    currentView: string;
    onViewChange: (view: string) => void;
    selectedClient: any;
}

export function Sidebar({ currentView, onViewChange, selectedClient }: SidebarProps) {
    const menuItems = [
        { id: 'dashboard', label: 'Дашборд', icon: '📊', badge: null },
        { id: 'analysis', label: 'Анализ клиента', icon: '👤', badge: selectedClient ? '✓' : null },
        { id: 'insights', label: 'Аналитика модели', icon: '🤖', badge: null },
        { id: 'clients', label: 'База клиентов', icon: '👥', badge: null },
        { id: 'reports', label: 'Отчеты', icon: '📈', badge: null },
        { id: 'settings', label: 'Настройки', icon: '⚙️', badge: null },
    ];

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <div className="sidebar-logo">
                    <div className="logo-icon">🏦</div>
                    <div className="logo-text">
                        <div className="logo-title">Bank AI</div>
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