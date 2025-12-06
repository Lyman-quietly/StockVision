"use client"

import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts"
import { StockHistory } from "@/services/api"

interface StockChartProps {
    data: StockHistory[]
}

export function StockChart({ data }: StockChartProps) {
    if (!data || data.length === 0) {
        return (
            <div className="h-[400px] flex items-center justify-center text-muted-foreground">
                No Data Available
            </div>
        )
    }

    // Format date for display
    const formattedData = data.map(item => ({
        ...item,
        dateStr: new Date(item.Date).toLocaleDateString()
    }))

    return (
        <div className="h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={formattedData}>
                    <defs>
                        <linearGradient id="colorClose" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                    <XAxis
                        dataKey="dateStr"
                        stroke="#666"
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                        minTickGap={30}
                    />
                    <YAxis
                        stroke="#666"
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                        domain={['auto', 'auto']}
                        tickFormatter={(value) => `$${value.toFixed(0)}`}
                    />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff' }}
                        itemStyle={{ color: '#fff' }}
                    />
                    <Area
                        type="monotone"
                        dataKey="Close"
                        stroke="#3b82f6"
                        strokeWidth={2}
                        fillOpacity={1}
                        fill="url(#colorClose)"
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    )
}
