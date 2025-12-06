import axios from "axios"

const API_BASE_URL = "http://localhost:8000"

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
})

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

export const stockService = {
    getHistory: async (ticker: string) => {
        const response = await api.get<StockHistory[]>(`/stock/${ticker}/history`)
        return response.data
    },

    getNews: async (ticker: string) => {
        const response = await api.get<NewsItem[]>(`/stock/${ticker}/news`)
        return response.data
    },

    getPredictions: async (ticker: string) => {
        const response = await api.get<PredictionResponse>(`/predict/${ticker}`)
        return response.data
    }
}
