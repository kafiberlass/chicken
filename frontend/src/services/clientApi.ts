export const clientApi = {
    async getAll() {
        // Заглушка - в реальности будет запрос к бэкенду
        return [
            {
                id: 'CL-001',
                name: 'Иван Петров',
                age: 35,
                occupation: 'IT-специалист',
                currentIncome: 85000,
                city: 'Москва',
                segment: 'premium'
            },
            {
                id: 'CL-002',
                name: 'Мария Сидорова',
                age: 42,
                occupation: 'Бизнес-аналитик',
                currentIncome: 120000,
                city: 'Москва',
                segment: 'vip'
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