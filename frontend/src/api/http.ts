import { mockFetch } from './mock';

// Адрес бэкенда берётся из переменной окружения (файл .env: VITE_API_URL=http://localhost:8000).
// Если адрес не задан — например, в задеплоенном демо, — запросы обрабатывает мок.
const API_URL: string | undefined = import.meta.env.VITE_API_URL;

export const isMockMode = !API_URL;

export class ApiError extends Error {
    constructor(public status: number, message: string) {
        super(message);
        this.name = 'ApiError';
    }
}

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const headers = { 'Content-Type': 'application/json', ...init.headers };

    const response = API_URL
        ? await fetch(`${API_URL}${path}`, { ...init, headers })
        : await mockFetch(path, init);

    if (!response.ok) {
        // Пытаемся достать понятное сообщение из тела ответа, иначе — статус
        let message = `Ошибка сервера (${response.status})`;
        try {
            const body = await response.json();
            if (body?.detail) message = body.detail;
        } catch {
            // тело не JSON — оставляем сообщение по умолчанию
        }
        throw new ApiError(response.status, message);
    }

    return response.json() as Promise<T>;
}
