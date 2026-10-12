import { request } from '../api/http';
import type { Prediction } from '../types';

export const predictionApi = {
    getForClient(clientId: string, signal?: AbortSignal) {
        return request<Prediction>(`/clients/${encodeURIComponent(clientId)}/prediction`, { signal });
    },
};
