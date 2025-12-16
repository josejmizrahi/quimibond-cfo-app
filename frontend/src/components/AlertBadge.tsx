import { AlertTriangle, Info, XCircle } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { cn } from "@/lib/utils"

interface AlertBadgeProps {
  type: "CRITICAL" | "WARNING" | "INFO"
  category: string
  message: string
  impact?: string
}

export function AlertBadge({ type, category, message, impact }: AlertBadgeProps) {
  const icons = {
    CRITICAL: XCircle,
    WARNING: AlertTriangle,
    INFO: Info,
  }

  const colors = {
    CRITICAL: "border-red-500 bg-red-50 dark:bg-red-950",
    WARNING: "border-yellow-500 bg-yellow-50 dark:bg-yellow-950",
    INFO: "border-blue-500 bg-blue-50 dark:bg-blue-950",
  }

  const Icon = icons[type]

  return (
    <Card className={cn("border-l-4", colors[type])}>
      <CardHeader className="pb-2">
        <div className="flex items-center gap-2">
          <Icon className={cn("h-4 w-4", {
            "text-red-500": type === "CRITICAL",
            "text-yellow-500": type === "WARNING",
            "text-blue-500": type === "INFO",
          })} />
          <CardTitle className="text-sm font-semibold">{category}</CardTitle>
          <span className={cn("text-xs px-2 py-0.5 rounded", {
            "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300": type === "CRITICAL",
            "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300": type === "WARNING",
            "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300": type === "INFO",
          })}>
            {type}
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm">{message}</p>
        {impact && (
          <p className="text-xs text-muted-foreground mt-1">Impacto: {impact}</p>
        )}
      </CardContent>
    </Card>
  )
}

