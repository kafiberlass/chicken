import type { Client, Prediction, Stats } from '../types';

// Мок-бэкенд для демо без сервера. Отвечает настоящими объектами Response,
// поэтому код выше (request, хуки, компоненты) не знает, что данные ненастоящие.

const clients: Client[] = [
    { id: 'CL-001', name: 'Иван Петров', age: 35, occupation: 'IT-специалист', city: 'Москва', segment: 'premium', currentIncome: 120000 },
    { id: 'CL-002', name: 'Мария Сидорова', age: 42, occupation: 'Бизнес-аналитик', city: 'Москва', segment: 'corporate', currentIncome: 150000 },
    { id: 'CL-003', name: 'Алексей Козлов', age: 28, occupation: 'Разработчик', city: 'Санкт-Петербург', segment: 'standard', currentIncome: 80000 },
    { id: 'CL-004', name: 'Елена Васнецова', age: 51, occupation: 'Финансовый директор', city: 'Москва', segment: 'vip', currentIncome: 300000 },
    { id: 'CL-005', name: 'Дмитрий Соколов', age: 45, occupation: 'Предприниматель', city: 'Казань', segment: 'corporate', currentIncome: 250000 },
];

const stats: Stats = {
    totalClients: 1247,
    predictionsToday: 89,
    averageConfidence: 82.3,
    modelWMAE: 0.124,
    conversionRate: 76.5,
};

// Детерминированный «прогноз»: для одного клиента всегда одинаковый результат
function hash(str: string): number {
    let h = 0;
    for (const ch of str) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
    return h;
}

function predict(client: Client): Prediction {
    const h = hash(client.id);
    const growth = ((h % 40) - 10) / 100; // от -10% до +29%
    return {
        clientId: client.id,
        currentIncome: client.currentIncome,
        predictedIncome: Math.round(client.currentIncome * (1 + growth)),
        confidence: 70 + (h % 25),
        shapValues: [
            { name: 'Опыт работы', impact: 0.15 },
            { name: 'Образование', impact: 0.12 },
            { name: 'Отрасль', impact: 0.08 },
            { name: 'Регион', impact: client.city === 'Москва' ? 0.07 : -0.02 },
            { name: 'Возраст', impact: client.age > 45 ? -0.04 : 0.03 },
        ],
    };
}

function json(body: unknown, status = 200): Response {
    return new Response(JSON.stringify(body), {
        status,
        headers: { 'Content-Type': 'application/json' },
    });
}

// Задержка сети, которую можно прервать через AbortSignal — как настоящий fetch
function delay(ms: number, signal?: AbortSignal | null): Promise<void> {
    return new Promise((resolve, reject) => {
        if (signal?.aborted) return reject(new DOMException('Aborted', 'AbortError'));
        const timer = setTimeout(resolve, ms);
        signal?.addEventListener('abort', () => {
            clearTimeout(timer);
            reject(new DOMException('Aborted', 'AbortError'));
        });
    });
}

export async function mockFetch(path: string, init: RequestInit = {}): Promise<Response> {
    await delay(400 + Math.random() * 400, init.signal);

    // Для демонстрации экрана ошибки: откройте сайт с ?fail в адресе
    if (new URLSearchParams(window.location.search).has('fail')) {
        return json({ detail: 'Сервис прогнозов временно недоступен' }, 503);
    }

    if (path === '/clients') return json(clients);
    if (path === '/stats') return json(stats);

    const match = path.match(/^\/clients\/([^/]+)\/prediction$/);
    if (match) {
        const client = clients.find((c) => c.id === decodeURIComponent(match[1]));
        return client ? json(predict(client)) : json({ detail: 'Клиент не найден' }, 404);
    }

    return json({ detail: `Неизвестный адрес: ${path}` }, 404);
}
