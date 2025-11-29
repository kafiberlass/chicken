export const clientApi = {
    async getAll() {
        // Заглушка - в реальности будет запрос к бэкенду
        return [
            {
                id: 'CL-001',
                name: 'Иван Петров',
                age: 35,
                occupation: 'IT-специалист',
                city: 'Москва',
                segment: 'premium',
                currentIncome: 120000
            },
            {
                id: 'CL-002',
                name: 'Мария Сидорова',
                age: 42,
                occupation: 'Бизнес-аналитик',
                city: 'Москва',
                segment: 'corporate',
                currentIncome: 150000
            },
            {
                id: 'CL-003',
                name: 'Алексей Козлов',
                age: 28,
                occupation: 'Разработчик',
                city: 'Санкт-Петербург',
                segment: 'standard',
                currentIncome: 80000
            },
            {
                id: 'CL-004',
                name: 'Елена Васнецова',
                age: 51,
                occupation: 'Финансовый директор',
                city: 'Москва',
                segment: 'vip',
                currentIncome: 300000
            },
            {
                id: 'CL-005',
                name: 'Дмитрий Соколов',
                age: 45,
                occupation: 'Предприниматель',
                city: 'Казань',
                segment: 'corporate',
                currentIncome: 250000
            }
        ];
    },

    async getStats() {
        return {
            totalClients: 1247,
            predictionsToday: 89,
            averageConfidence: 82.3,
            modelWMAE: 0.124,
            conversionRate: 76.5
        };
    }
};