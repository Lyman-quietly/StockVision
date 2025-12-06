"use client"

import { NewsItem } from "@/services/api"
import { ExternalLink } from "lucide-react"

interface NewsFeedProps {
    news: NewsItem[]
}

export function NewsFeed({ news }: NewsFeedProps) {
    if (!news || news.length === 0) {
        return <div className="text-muted-foreground">No news available</div>
    }

    return (
        <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
            {news.map((item) => (
                <div key={item.uuid} className="p-4 rounded-lg bg-card/40 border border-border/50 hover:bg-card/60 transition-colors">
                    <div className="flex justify-between items-start mb-2">
                        <span className="text-xs text-muted-foreground">{item.publisher}</span>
                        <SentimentBadge score={item.sentiment} />
                    </div>
                    <a href={item.link} target="_blank" rel="noopener noreferrer" className="group">
                        <h4 className="font-medium text-sm text-foreground mb-1 group-hover:text-blue-400 transition-colors">
                            {item.title}
                        </h4>
                        <ExternalLink className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity absolute right-4 top-4" />
                    </a>
                </div>
            ))}
        </div>
    )
}

function SentimentBadge({ score }: { score: number }) {
    let color = "bg-gray-500/20 text-gray-400"
    let label = "Neutral"

    if (score > 0.1) {
        color = "bg-emerald-500/20 text-emerald-400"
        label = "Positive"
    } else if (score < -0.1) {
        color = "bg-rose-500/20 text-rose-400"
        label = "Negative"
    }

    return (
        <span className={`text-[10px] uppercase tracking-wider font-bold px-2 py-0.5 rounded-full ${color}`}>
            {label}
        </span>
    )
}
