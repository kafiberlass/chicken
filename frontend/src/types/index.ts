export interface Client {
    id: string;
    name: string;
    age: number;
    occupation: string;
    city: string;
    segment: string;
    currentIncome: number;
}

export interface ShapValue {
    name: string;
    impact: number;
}

export interface Prediction {
    clientId: string;
    predictedIncome: number;
    currentIncome: number;
    confidence: number;
    shapValues: ShapValue[];
}

export interface Stats {
    totalClients: number;
    predictionsToday: number;
    averageConfidence: number;
    modelWMAE: number;
    conversionRate: number;
}
