export interface Client {
    id: string;
    name: string;
    age: number;
    occupation: string;
    currentIncome: number;
    city: string;
    segment: string;
}

export interface Prediction {
    predictedIncome: number;
    currentIncome: number;
    confidence: number;
    shapValues: Array<{
        name: string;
        impact: number;
    }>;
}