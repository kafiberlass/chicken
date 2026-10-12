import { useMemo, useState } from 'react';
import { Client } from '../../types';
import { ClientCard } from './ClientCard';

interface ClientListProps {
    clients: Client[];
    onClientSelect: (client: Client) => void;
}

export function ClientList({ clients, onClientSelect }: ClientListProps) {
    const [searchTerm, setSearchTerm] = useState('');
    // Отфильтрованный список вычисляется из пропсов, а не хранится в отдельном state:
    // так он не устаревает, когда список клиентов обновится с сервера.
    const filteredClients = useMemo(() => {
        const term = searchTerm.trim().toLowerCase();
        if (!term) return clients;
        return clients.filter(
            (client) =>
                client.name.toLowerCase().includes(term) ||
                client.id.toLowerCase().includes(term),
        );
    }, [clients, searchTerm]);

    return (
        <div className="client-list">
            <div className="client-list-header">
                <h2>База клиентов</h2>
                <span className="client-count">{filteredClients.length} клиентов</span>
            </div>

            <div className="client-search">
                <input
                    type="text"
                    placeholder="🔍 Поиск по имени или ID клиента..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="search-input"
                />
            </div>

            <div className="clients-grid">
                {filteredClients.map(client => (
                    <ClientCard
                        key={client.id}
                        client={client}
                        onSelect={onClientSelect}
                    />
                ))}
            </div>
        </div>
    );
}