"use client"

import * as React from "react"
import { useState } from "react"
import { Search, TrendingUp, Activity, Newspaper } from "lucide-react"
import { StockChart } from "@/components/StockChart"
import { Predictions } from "@/components/Predictions"
import { NewsFeed } from "@/components/NewsFeed"
import { stockService } from "@/services/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useCallback } from "react"
import { StockHistory, NewsItem, PredictionResponse } from "@/services/api"

export default function Dashboard() {
  const [ticker, setTicker] = useState("AAPL")
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState<StockHistory[]>([])
  const [news, setNews] = useState<NewsItem[]>([])
  const [predictions, setPredictions] = useState<PredictionResponse | null>(null)
  const [error, setError] = useState("")

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError("")
    try {
      const [histData, newsData, predData] = await Promise.all([
        stockService.getHistory(ticker),
        stockService.getNews(ticker),
        stockService.getPredictions(ticker),
      ])
      setHistory(histData)
      setNews(newsData)
      setPredictions(predData)
    } catch (err) {
      console.error(err)
      setError("Failed to fetch data. Please check the ticker or backend connection.")
    } finally {
      setLoading(false)
    }
  }, [ticker]) // Dependency on ticker

  // Initial fetch
  React.useEffect(() => {
    fetchData()
  }, [fetchData])


  return (
    <div className="min-h-screen bg-background p-6 space-y-8">
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            StockVision
          </h1>
          <p className="text-muted-foreground">AI-Powered Stock Analysis & Prediction</p>
        </div>

        <div className="flex w-full md:w-auto items-center space-x-2">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search Ticker (e.g. NVDA)"
              className="w-full rounded-md border bg-card px-9 py-2 text-sm outline-none focus:ring-1 focus:ring-ring"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              onKeyDown={(e) => e.key === "Enter" && fetchData()}
            />
          </div>
          <Button onClick={fetchData} disabled={loading}>
            {loading ? <Activity className="mr-2 h-4 w-4 animate-spin" /> : "Analyze"}
          </Button>
        </div>
      </header>

      {error && (
        <div className="p-4 rounded-md bg-destructive/10 text-destructive text-sm font-medium">
          {error}
        </div>
      )}

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Left Col: Chart & Stats */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="border-none bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-emerald-500" />
                Price History
              </CardTitle>
            </CardHeader>
            <CardContent>
              <StockChart data={history} />
            </CardContent>
          </Card>

          <Predictions data={predictions} />
        </div>

        {/* Right Col: News & Sentiment */}
        <div className="space-y-6">
          <Card className="h-full border-none bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Newspaper className="h-5 w-5 text-blue-500" />
                Market News & Sentiment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <NewsFeed news={news} />
            </CardContent>
          </Card>
        </div>

      </div>
    </div>
  )
}
