interface SHAPFeature {
    name: string;
    impact: number;
}

interface SHAPChartProps {
    shapValues: SHAPFeature[] | null;
}

export function SHAPChart({ shapValues }: SHAPChartProps) {
    if (!shapValues) return null;

    return (
        <div className="shap-chart">
            <h3>Объяснение прогноза (SHAP)</h3>
            <div className="shap-features">
                {shapValues.map((feature, index) => (
                    <div key={index} className="shap-feature">
                        <div className="feature-name">{feature.name}</div>
                        <div className="feature-impact">
                            <div
                                className={`impact-bar ${feature.impact > 0 ? 'positive' : 'negative'}`}
                                style={{ width: `${Math.abs(feature.impact) * 100}%` }}
                            >
                                <span className="impact-value">
                                    {feature.impact > 0 ? '+' : ''}{feature.impact.toFixed(3)}
                                </span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}