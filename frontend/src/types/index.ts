export interface Client {
    id: string;
    name: string;
    age: number;
    occupation: string;
    city: string;
    segment: string;
    currentIncome: number;
}

export interface Prediction {
    predictedIncome: number;
    confidence: number;
    shapValues: Array<{
        name: string;
        impact: number;
    }>;
}