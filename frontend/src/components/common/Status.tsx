interface LoaderProps {
    text?: string;
}

export function Loader({ text = 'Загрузка...' }: LoaderProps) {
    return (
        <div className="status-box" role="status">
            <div className="spinner" aria-hidden="true" />
            <p>{text}</p>
        </div>
    );
}

interface ErrorStateProps {
    error: Error;
    onRetry: () => void;
}

export function ErrorState({ error, onRetry }: ErrorStateProps) {
    return (
        <div className="status-box status-error" role="alert">
            <p className="status-title">Не удалось загрузить данные</p>
            <p className="status-detail">{error.message}</p>
            <button type="button" className="retry-button" onClick={onRetry}>
                Повторить
            </button>
        </div>
    );
}
