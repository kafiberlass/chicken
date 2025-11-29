import { Client } from "../components/client/ClientCard";

interface PredictionData {
    predictedIncome: number;
    currentIncome: number;
    confidence: number;
}

interface PredictionResultProps {
    prediction: PredictionData | null;
    client: Client | null;
}

export function PredictionResult({ prediction, client }: PredictionResultProps) {
    if (!prediction || !client) {
        return (
            <div className="prediction-result empty">
                <h3>Прогноз дохода клиента</h3>
                <p>Выберите клиента для получения прогноза</p>
            </div>
        );
    }

    const incomeChange = prediction.predictedIncome - prediction.currentIncome;
    const changePercent = ((incomeChange / prediction.currentIncome) * 100).toFixed(1);

    return (
        <div className="prediction-result">
            <h3>Прогноз дохода: {client.name}</h3>

            <div className="income-comparison">
                <div className="income-card">
                    <div className="income-label">Текущий доход</div>
                    <div className="income-value current">
                        {prediction.currentIncome.toLocaleString('ru-RU')} ₽
                    </div>
                </div>

                <div className="trend-arrow">
                    {incomeChange > 0 ? '↗' : '↘'}
                </div>

                <div className="income-card">
                    <div className="income-label">Прогнозируемый доход</div>
                    <div className="income-value predicted">
                        {prediction.predictedIncome.toLocaleString('ru-RU')} ₽
                    </div>
                    <div className={`change ${incomeChange >= 0 ? 'positive' : 'negative'}`}>
                        {incomeChange >= 0 ? '+' : ''}{changePercent}%
                    </div>
                </div>
            </div>

            <div className="confidence">
                <span>Достоверность прогноза: </span>
                <strong>{prediction.confidence}%</strong>
            </div>
        </div>
    );
}