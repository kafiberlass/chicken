import React, { useState } from 'react';
import ClientCard from './ClientCard';

export default function ClientList({ clients, onClientSelect }) {
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredClients, setFilteredClients] = useState(clients);

    const handleSearch = (term) => {
        setSearchTerm(term);
        const filtered = clients.filter(client =>
            client.name.toLowerCase().includes(term.toLowerCase()) ||
            client.id.includes(term)
        );
        setFilteredClients(filtered);
    };

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
                    onChange={(e) => handleSearch(e.target.value)}
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