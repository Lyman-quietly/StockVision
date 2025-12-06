import axios from "axios"

const API_BASE_URL = "http://127.0.0.1:8000"

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
})

// --- Interfaces ---

export interface StockHistory {
    Date: string
    Open: number
    High: number
    Low: number
    Close: number
    Volume: number
}

export interface NewsItem {
    uuid: string
    title: string
    publisher: string
    link: string
    sentiment: number
    providerPublishTime?: number // Optional fields based on usage
    type?: string
}

export interface PredictionStats {
    model: string
    current_sma?: number[]
    prediction_next_day?: number
    predictions?: number[]
    prediction?: number
}

export interface PredictionResponse {
    ticker: string
    statistical: {
        moving_average: PredictionStats
        linear_trend: PredictionStats
        arima: PredictionStats
    }
    ml: {
        random_forest: PredictionStats
        xgboost: PredictionStats
        svr: PredictionStats
    }
}

// --- Service ---

export const stockService = {
    getHistory: async (ticker: string): Promise<StockHistory[]> => {
        const response = await api.get<StockHistory[]>(`/stock/${ticker}/history`)
        return response.data
    },

    getNews: async (ticker: string): Promise<NewsItem[]> => {
        const response = await api.get<NewsItem[]>(`/stock/${ticker}/news`)
        return response.data
    },

    getPredictions: async (ticker: string): Promise<PredictionResponse> => {
        const response = await api.get<PredictionResponse>(`/predict/${ticker}`)
        return response.data
    }
}
