import './settings.css';

interface SettingsProps {
    theme: 'light' | 'dark';
    onThemeToggle: () => void;
}

export function Settings({ theme, onThemeToggle }: SettingsProps) {
    return (
        <div className="settings-page">
            <div className="content-container">
                <div className="settings-header">
                    <h1>Настройки системы</h1>
                    <p>Управление внешним видом и параметрами приложения</p>
                </div>

                <div className="settings-sections">
                    {/* Секция темы */}
                    <div className="settings-section">
                        <h2>🎨 Внешний вид</h2>
                        <div className="setting-item">
                            <div className="setting-info">
                                <h3>Цветовая тема</h3>
                                <p>Выберите preferred цветовую схему приложения</p>
                            </div>
                            <div className="setting-control">
                                <div className="theme-selector">
                                    <button
                                        className={`theme-option ${theme === 'light' ? 'active' : ''}`}
                                        onClick={() => theme !== 'light' && onThemeToggle()}
                                    >
                                        <div className="theme-preview light">
                                            <div className="preview-header"></div>
                                            <div className="preview-content">
                                                <div className="preview-card"></div>
                                                <div className="preview-card"></div>
                                            </div>
                                        </div>
                                        <span>Светлая</span>
                                    </button>

                                    <button
                                        className={`theme-option ${theme === 'dark' ? 'active' : ''}`}
                                        onClick={() => theme !== 'dark' && onThemeToggle()}
                                    >
                                        <div className="theme-preview dark">
                                            <div className="preview-header"></div>
                                            <div className="preview-content">
                                                <div className="preview-card"></div>
                                                <div className="preview-card"></div>
                                            </div>
                                        </div>
                                        <span>Тёмная</span>
                                    </button>
                                </div>

                                <div className="theme-toggle-compact">
                                    <label className="toggle-label">
                                        <input
                                            type="checkbox"
                                            checked={theme === 'dark'}
                                            onChange={onThemeToggle}
                                            className="toggle-input"
                                        />
                                        <span className="toggle-slider">
                      <span className="toggle-icon">{theme === 'light' ? '☀️' : '🌙'}</span>
                    </span>
                                        <span className="toggle-text">
                      {theme === 'light' ? 'Светлая тема' : 'Тёмная тема'}
                    </span>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>


                    {/* Секция модели */}
                    <div className="settings-section">
                        <h2>🤖 Настройки модели</h2>
                        <div className="setting-item">
                            <div className="setting-info">
                                <h3>Автообновление модели</h3>
                                <p>Автоматически переобучать модель при новых данных</p>
                            </div>
                            <div className="setting-control">
                                <label className="switch">
                                    <input type="checkbox" defaultChecked />
                                    <span className="slider"></span>
                                </label>
                            </div>
                        </div>

                        <div className="setting-item">
                            <div className="setting-info">
                                <h3>Порог достоверности</h3>
                                <p>Минимальная достоверность для показа прогноза</p>
                            </div>
                            <div className="setting-control">
                                <select className="select-input" defaultValue="75">
                                    <option value="60">60%</option>
                                    <option value="75">75%</option>
                                    <option value="85">85%</option>
                                    <option value="90">90%</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Секция данных */}
                    <div className="settings-section">
                        <h2>📊 Управление данными</h2>
                        <div className="setting-item">
                            <div className="setting-info">
                                <h3>Экспорт данных</h3>
                                <p>Скачать все данные в CSV формате</p>
                            </div>
                            <div className="setting-control">
                                <button className="btn-secondary">📥 Экспорт</button>
                            </div>
                        </div>

                        <div className="setting-item">
                            <div className="setting-info">
                                <h3>Очистка кэша</h3>
                                <p>Удалить временные данные приложения</p>
                            </div>
                            <div className="setting-control">
                                <button className="btn-warning">🗑️ Очистить</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}