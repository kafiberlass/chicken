export const predictionApi = {
    async predictIncome(client) {
        // Заглушка - в реальности запрос к ML модели
        return {
            predictedIncome: Math.round(client.currentIncome * (1 + (Math.random() * 0.4 - 0.1))),
            currentIncome: client.currentIncome,
            confidence: Math.round(70 + Math.random() * 25),
            shapValues: [
                { name: 'Опыт работы', impact: 0.15 },
                { name: 'Образование', impact: 0.12 },
                { name: 'Отрасль', impact: 0.08 },
                { name: 'Регион', impact: 0.05 },
                { name: 'Возраст', impact: -0.03 }
            ]
        };
    }
};