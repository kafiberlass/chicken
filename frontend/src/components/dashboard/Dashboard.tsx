import { Client } from '../../types';

interface Stats {
    totalClients?: number;
    predictionsToday?: number;
    averageConfidence?: number;
    modelWMAE?: number | string;
    conversionRate?: number;
}

interface DashboardProps {
    stats: Stats;
    clients: Client[];
    onClientSelect: (client: Client) => void;
}

export function Dashboard({ stats, clients, onClientSelect }: DashboardProps) {
    const metrics = [
        { label: 'Всего клиентов', value: stats.totalClients || 0, icon: '👥', color: '#3b82f6' },
        { label: 'Прогнозов сегодня', value: stats.predictionsToday || 0, icon: '📈', color: '#10b981' },
        { label: 'Средняя достоверность', value: `${stats.averageConfidence || 0}%`, icon: '🎯', color: '#f59e0b' },
        { label: 'WMAE модели', value: stats.modelWMAE || '0.124', icon: '🤖', color: '#ef4444' }
    ];

    return (
        <div className="dashboard">
            <div style={{ marginBottom: '2rem' }}>
                <h2>Ключевые метрики</h2>
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                    gap: '1rem',
                    marginTop: '1rem'
                }}>
                    {metrics.map((metric, index) => (
                        <div key={index} style={{
                            background: 'white',
                            padding: '1.5rem',
                            borderRadius: '8px',
                            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                            borderLeft: `4px solid ${metric.color}`
                        }}>
                            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                                {metric.icon}
                            </div>
                            <div style={{
                                fontSize: '1.5rem',
                                fontWeight: 'bold',
                                color: '#1e293b',
                                marginBottom: '0.25rem'
                            }}>
                                {metric.value}
                            </div>
                            <div style={{ color: '#64748b' }}>
                                {metric.label}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div>
                <div style={{
                    background: 'white',
                    padding: '1.5rem',
                    borderRadius: '8px',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}>
                    <h3>Последние клиенты</h3>
                    <div style={{ marginTop: '1rem' }}>
                        {clients.slice(0, 3).map((client: Client) => (
                            <div
                                key={client.id}
                                style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center',
                                    padding: '0.75rem',
                                    borderBottom: '1px solid #e2e8f0',
                                    cursor: 'pointer'
                                }}
                                onClick={() => onClientSelect(client)}
                            >
                                <div>
                                    <div style={{ fontWeight: 'bold' }}>{client.name}</div>
                                    <div style={{ color: '#64748b', fontSize: '0.9rem' }}>
                                        {client.occupation} • {client.currentIncome?.toLocaleString('ru-RU')} ₽
                                    </div>
                                </div>
                                <button style={{
                                    background: '#3b82f6',
                                    color: 'white',
                                    border: 'none',
                                    padding: '0.25rem 0.75rem',
                                    borderRadius: '4px',
                                    cursor: 'pointer',
                                    fontSize: '0.8rem'
                                }}>
                                    Анализ
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}