import React, { useState, useEffect } from 'react';
import { predictionApi } from '../services/predictionApi';
import { Client } from "../components/client/ClientCard";

interface ClientAnalysisProps {
    client: Client | null;
}

interface Prediction {
    predictedIncome: number;
    currentIncome: number;
    confidence: number;
    shapValues: Array<{
        name: string;
        impact: number;
    }>;
}

export function ClientAnalysis({ client }: ClientAnalysisProps) {
    const [prediction, setPrediction] = useState<Prediction | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (client) {
            loadPrediction();
        }
    }, [client]);

    const loadPrediction = async () => {
        // ДОБАВЛЯЕМ ПРОВЕРКУ - если client null, выходим из функции
        if (!client) return;

        setLoading(true);
        try {
            const predictionData = await predictionApi.predictIncome(client);
            setPrediction(predictionData);
        } catch (error) {
            console.error('Ошибка прогнозирования:', error);
        } finally {
            setLoading(false);
        }
    };

    if (!client) {
        return (
            <div style={{
                background: 'white',
                padding: '3rem',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                textAlign: 'center'
            }}>
                <h2>Анализ клиента</h2>
                <p style={{ color: '#64748b', marginTop: '1rem' }}>
                    Выберите клиента из списка для анализа
                </p>
            </div>
        );
    }

    if (loading) {
        return (
            <div style={{
                background: 'white',
                padding: '2rem',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                textAlign: 'center'
            }}>
                <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⏳</div>
                <p>Анализируем данные клиента...</p>
            </div>
        );
    }

    const incomeChange = prediction ? prediction.predictedIncome - prediction.currentIncome : 0;
    const changePercent = prediction ? ((incomeChange / prediction.currentIncome) * 100).toFixed(1) : 0;

    return (
        <div className="client-analysis">
            <div style={{
                background: 'white',
                padding: '2rem',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                marginBottom: '2rem'
            }}>
                <h2>Анализ клиента: {client.name}</h2>
                <div style={{
                    display: 'flex',
                    gap: '2rem',
                    marginTop: '1rem',
                    color: '#64748b',
                    fontSize: '0.9rem'
                }}>
                    <span>ID: {client.id}</span>
                    <span>Сегмент: {client.segment}</span>
                    <span>Город: {client.city}</span>
                </div>
            </div>

            {prediction && (
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: '2rem'
                }}>
                    <div style={{
                        background: 'white',
                        padding: '2rem',
                        borderRadius: '8px',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                    }}>
                        <h3>Прогноз дохода</h3>

                        <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            marginTop: '1.5rem'
                        }}>
                            <div style={{ textAlign: 'center' }}>
                                <div style={{ color: '#64748b', fontSize: '0.9rem' }}>Текущий</div>
                                <div style={{
                                    fontSize: '1.5rem',
                                    fontWeight: 'bold',
                                    color: '#1e293b',
                                    marginTop: '0.5rem'
                                }}>
                                    {prediction.currentIncome?.toLocaleString('ru-RU')} ₽
                                </div>
                            </div>

                            <div style={{ fontSize: '2rem', color: '#3b82f6' }}>
                                {incomeChange > 0 ? '↗' : '↘'}
                            </div>

                            <div style={{ textAlign: 'center' }}>
                                <div style={{ color: '#64748b', fontSize: '0.9rem' }}>Прогноз</div>
                                <div style={{
                                    fontSize: '1.5rem',
                                    fontWeight: 'bold',
                                    color: incomeChange > 0 ? '#059669' : '#dc2626',
                                    marginTop: '0.5rem'
                                }}>
                                    {prediction.predictedIncome?.toLocaleString('ru-RU')} ₽
                                </div>
                                <div style={{
                                    color: incomeChange > 0 ? '#059669' : '#dc2626',
                                    fontSize: '0.9rem',
                                    marginTop: '0.25rem'
                                }}>
                                    {incomeChange > 0 ? '+' : ''}{changePercent}%
                                </div>
                            </div>
                        </div>

                        <div style={{
                            marginTop: '1.5rem',
                            padding: '1rem',
                            background: '#f8fafc',
                            borderRadius: '6px'
                        }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                <span>Достоверность:</span>
                                <strong>{prediction.confidence}%</strong>
                            </div>
                        </div>
                    </div>

                    <div style={{
                        background: 'white',
                        padding: '2rem',
                        borderRadius: '8px',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                    }}>
                        <h3>Факторы влияния</h3>
                        <div style={{ marginTop: '1rem' }}>
                            {prediction.shapValues?.map((feature, index) => (
                                <div key={index} style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center',
                                    padding: '0.75rem 0',
                                    borderBottom: '1px solid #f1f5f9'
                                }}>
                                    <span style={{ color: '#64748b' }}>{feature.name}</span>
                                    <span style={{
                                        color: feature.impact > 0 ? '#059669' : '#dc2626',
                                        fontWeight: 'bold'
                                    }}>
                                        {feature.impact > 0 ? '+' : ''}{feature.impact.toFixed(3)}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}