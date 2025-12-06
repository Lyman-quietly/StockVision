"use client"

import { PredictionResponse } from "@/services/api"
import { Card } from "@/components/ui/card"
import { Brain, Calculator, ChevronRight } from "lucide-react"

interface PredictionsProps {
    data: PredictionResponse | null
}

export function Predictions({ data }: PredictionsProps) {
    if (!data) return null

    return (
        <div className="space-y-4">
            <h2 className="text-xl font-semibold tracking-tight">AI Predictions</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {/* Statistical Models */}
                <PredictionCard
                    title="Moving Average"
                    icon={<Calculator className="h-4 w-4 text-orange-400" />}
                    prediction={data.statistical.moving_average.prediction_next_day}
                    type="Statistical"
                />
                <PredictionCard
                    title="Linear Trend"
                    icon={<Calculator className="h-4 w-4 text-orange-400" />}
                    // Linear trend returns an array of predictions, take the first one
                    prediction={data.statistical.linear_trend.predictions?.[0]}
                    type="Statistical"
                />
                <PredictionCard
                    title="ARIMA"
                    icon={<Calculator className="h-4 w-4 text-orange-400" />}
                    // ARIMA returns a forecast array, take the first one
                    prediction={data.statistical.arima.predictions?.[0]}
                    type="Statistical"
                />

                {/* ML Models */}
                <PredictionCard
                    title="Random Forest"
                    icon={<Brain className="h-4 w-4 text-purple-400" />}
                    prediction={data.ml.random_forest.prediction}
                    type="Machine Learning"
                />
                <PredictionCard
                    title="XGBoost"
                    icon={<Brain className="h-4 w-4 text-purple-400" />}
                    prediction={data.ml.xgboost.prediction}
                    type="Machine Learning"
                />
                <PredictionCard
                    title="Support Vector"
                    icon={<Brain className="h-4 w-4 text-purple-400" />}
                    prediction={data.ml.svr.prediction}
                    type="Machine Learning"
                />
            </div>
        </div>
    )
}

function PredictionCard({ title, icon, prediction, type }: { title: string, icon: React.ReactNode, prediction?: number, type: string }) {
    return (
        <Card className="bg-card/40 border p-4 flex flex-col justify-between hover:bg-card/60 transition-colors">
            <div className="flex justify-between items-start">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    {icon}
                    <span>{title}</span>
                </div>
                <span className="text-[10px] text-muted-foreground/50 uppercase">{type}</span>
            </div>

            <div className="mt-4">
                <div className="text-2xl font-bold">
                    {prediction ? `$${prediction.toFixed(2)}` : "N/A"}
                </div>
                <div className="text-xs text-muted-foreground mt-1 flex items-center">
                    Projected Close <ChevronRight className="h-3 w-3" />
                </div>
            </div>
        </Card>
    )
}
