"use client"

import { Search, Activity } from "lucide-react"
import { Button } from "@/components/ui/button"

interface HeaderProps {
    ticker: string
    setTicker: (value: string) => void
    loading: boolean
    fetchData: () => void
}

export function Header({ ticker, setTicker, loading, fetchData }: HeaderProps) {
    return (
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
    )
}
