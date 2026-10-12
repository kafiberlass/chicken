export function ModelInsights() {
    return (
        <div style={{
            background: 'var(--card-bg)',
            padding: '2rem',
            borderRadius: '8px',
            boxShadow: 'var(--shadow)'
        }}>
            <h2>Анализ ML модели</h2>
            <p style={{ color: 'var(--text-secondary)', marginTop: '1rem' }}>
                Здесь будет отображаться информация о производительности модели,
                метрики качества и другие аналитические данные.
            </p>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1rem',
                marginTop: '2rem'
            }}>
                <div style={{
                    background: 'var(--surface-muted)',
                    padding: '1.5rem',
                    borderRadius: '6px',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🤖</div>
                    <div style={{ fontWeight: 'bold', color: 'var(--text-primary)' }}>Gradient Boosting</div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Алгоритм</div>
                </div>

                <div style={{
                    background: 'var(--surface-muted)',
                    padding: '1.5rem',
                    borderRadius: '6px',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📊</div>
                    <div style={{ fontWeight: 'bold', color: 'var(--text-primary)' }}>0.124</div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>WMAE</div>
                </div>


            </div>
        </div>
    );
}