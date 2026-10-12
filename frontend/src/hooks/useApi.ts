import { useCallback, useEffect, useState } from 'react';

interface ApiState<T> {
    data: T | null;
    error: Error | null;
    loading: boolean;
    reload: () => void;
}

/**
 * Загружает данные и следит за состоянием запроса.
 * При смене зависимостей или размонтировании компонента
 * предыдущий запрос отменяется через AbortController,
 * поэтому устаревший ответ не перезапишет свежие данные.
 */
export function useApi<T>(
    fetcher: (signal: AbortSignal) => Promise<T>,
    deps: unknown[],
): ApiState<T> {
    const [data, setData] = useState<T | null>(null);
    const [error, setError] = useState<Error | null>(null);
    const [loading, setLoading] = useState(true);
    const [attempt, setAttempt] = useState(0);

    useEffect(() => {
        const controller = new AbortController();
        setLoading(true);
        setError(null);

        fetcher(controller.signal)
            .then((result) => setData(result))
            .catch((err: unknown) => {
                // Отмена — не ошибка: компонент ушёл со страницы или пришли новые параметры
                if (err instanceof DOMException && err.name === 'AbortError') return;
                setError(err instanceof Error ? err : new Error(String(err)));
            })
            .finally(() => {
                if (!controller.signal.aborted) setLoading(false);
            });

        return () => controller.abort();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [...deps, attempt]);

    const reload = useCallback(() => setAttempt((n) => n + 1), []);

    return { data, error, loading, reload };
}
