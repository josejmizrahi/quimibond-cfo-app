import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { TrendingUp, TrendingDown } from "lucide-react"
import { cn } from "@/lib/utils"

interface KPICardProps {
  title: string
  value: string | number
  variation?: number
  variationType?: "positive_good" | "negative_good"
  subtitle?: string
  status?: "good" | "warning" | "critical"
}

export function KPICard({
  title,
  value,
  variation,
  variationType = "positive_good",
  subtitle,
  status,
}: KPICardProps) {
  const isPositive = variation !== undefined && variation > 0
  const isGood = variationType === "positive_good" ? isPositive : !isPositive

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {status && (
          <div
            className={cn("h-2 w-2 rounded-full", {
              "bg-green-500": status === "good",
              "bg-yellow-500": status === "warning",
              "bg-red-500": status === "critical",
            })}
          />
        )}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {subtitle && <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>}
        {variation !== undefined && (
          <div className="flex items-center text-xs mt-1">
            {isGood ? (
              <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
            ) : (
              <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
            )}
            <span className={cn(isGood ? "text-green-500" : "text-red-500")}>
              {Math.abs(variation).toFixed(1)}%
            </span>
            <span className="text-muted-foreground ml-1">vs año anterior</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

