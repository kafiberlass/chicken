import { request } from '../api/http';
import type { Client, Stats } from '../types';

export const clientApi = {
    getAll(signal?: AbortSignal) {
        return request<Client[]>('/clients', { signal });
    },

    getStats(signal?: AbortSignal) {
        return request<Stats>('/stats', { signal });
    },
};
