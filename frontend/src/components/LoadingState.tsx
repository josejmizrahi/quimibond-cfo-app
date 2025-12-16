import { RefreshCw } from "lucide-react"
import { Card, CardContent } from "./ui/card"
import { Skeleton } from "./ui/skeleton"

export function LoadingState({ message = "Cargando datos..." }: { message?: string }) {
  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center">
        <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4" />
        <p className="text-muted-foreground">{message}</p>
      </div>
    </div>
  )
}

export function LoadingCard() {
  return (
    <Card>
      <div className="p-6 space-y-4">
        <Skeleton className="h-4 w-1/4" />
        <Skeleton className="h-8 w-1/2" />
        <Skeleton className="h-4 w-3/4" />
      </div>
    </Card>
  )
}

export function LoadingKPICards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {[1, 2, 3, 4].map((i) => (
        <LoadingCard key={i} />
      ))}
    </div>
  )
}

