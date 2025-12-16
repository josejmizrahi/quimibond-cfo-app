import { useState, useEffect } from "react"
import { apiService, KPIDashboard } from "@/services/api"
import { KPICard } from "@/components/KPICard"
import { AlertBadge } from "@/components/AlertBadge"
import { LoadingState, LoadingKPICards } from "@/components/LoadingState"
import { ErrorState } from "@/components/ErrorState"
import { ChartCard } from "@/components/ChartCard"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select } from "@/components/ui/select"
import { RefreshCw } from "lucide-react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts"

export function Dashboard() {
  const [kpis, setKpis] = useState<KPIDashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [year, setYear] = useState(new Date().getFullYear())

  const fetchKPIs = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await apiService.getKPIs(year)
      setKpis(response.data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al cargar datos")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchKPIs()
  }, [year])

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  if (loading) {
    return <LoadingState message="Cargando datos de Odoo..." />
  }

  if (error) {
    return <ErrorState error={error} onRetry={fetchKPIs} />
  }

  if (!kpis) return null

  const marginsData = [
    {
      name: "Bruto",
      value: kpis.financial.gross_margin,
    },
    {
      name: "Operativo",
      value: kpis.financial.operating_margin,
    },
    {
      name: "Neto",
      value: kpis.financial.net_margin,
    },
  ]

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Dashboard CFO - Quimibond</h1>
            <p className="text-muted-foreground">
              Última actualización: {new Date(kpis.last_updated).toLocaleString("es-MX")}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <Select
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
            >
              {[2022, 2023, 2024, 2025, 2026].map((y) => (
                <option key={y} value={y}>
                  {y}
                </option>
              ))}
            </Select>
            <Button onClick={fetchKPIs} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              Actualizar
            </Button>
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <KPICard
            title="Ingresos"
            value={formatCurrency(kpis.financial.revenue)}
            status={kpis.financial.revenue > 0 ? "good" : "critical"}
          />
          <KPICard
            title="Margen Bruto"
            value={`${kpis.financial.gross_margin.toFixed(1)}%`}
            status={
              kpis.financial.gross_margin > 30
                ? "good"
                : kpis.financial.gross_margin > 25
                ? "warning"
                : "critical"
            }
          />
          <KPICard
            title="Utilidad Neta"
            value={formatCurrency(kpis.financial.net_income)}
            status={kpis.financial.net_income > 0 ? "good" : "critical"}
          />
          <KPICard
            title="Ciclo de Caja"
            value={`${kpis.working_capital.cash_conversion_cycle.toFixed(0)} días`}
            status={
              kpis.working_capital.cash_conversion_cycle < 45
                ? "good"
                : kpis.working_capital.cash_conversion_cycle < 60
                ? "warning"
                : "critical"
            }
          />
        </div>

        {/* Charts Row */}
        <div className="grid gap-4 md:grid-cols-2">
          <ChartCard title="Márgenes">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={marginsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value) => `${value}%`} />
                <Bar dataKey="value" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

          <Card>
            <CardHeader>
              <CardTitle>Capital de Trabajo</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Cuentas por Cobrar</span>
                    <span className="font-semibold">
                      {formatCurrency(kpis.working_capital.ar_total)}
                    </span>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {kpis.working_capital.ar_days.toFixed(0)} días
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Inventario</span>
                    <span className="font-semibold">
                      {formatCurrency(kpis.working_capital.inventory_value)}
                    </span>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {kpis.working_capital.inventory_days.toFixed(0)} días
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Cuentas por Pagar</span>
                    <span className="font-semibold">
                      {formatCurrency(kpis.working_capital.ap_total)}
                    </span>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {kpis.working_capital.ap_days.toFixed(0)} días
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Alerts */}
        {kpis.alerts.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Alertas ({kpis.alerts.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {kpis.alerts.map((alert, index) => (
                  <AlertBadge key={index} {...alert} />
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Concentration */}
        <Card>
          <CardHeader>
            <CardTitle>Concentración de Clientes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Top Cliente</span>
                <span className="font-semibold">
                  {kpis.concentration.top_customer_pct.toFixed(1)}%
                </span>
              </div>
              <div className="flex justify-between">
                <span>Top 3 Clientes</span>
                <span className="font-semibold">
                  {kpis.concentration.top3_pct.toFixed(1)}%
                </span>
              </div>
              <div className="flex justify-between">
                <span>Índice HHI</span>
                <span
                  className={`font-semibold ${
                    kpis.concentration.hhi_index > 2500
                      ? "text-red-500"
                      : kpis.concentration.hhi_index > 1500
                      ? "text-yellow-500"
                      : "text-green-500"
                  }`}
                >
                  {kpis.concentration.hhi_index.toFixed(0)}
                </span>
              </div>
              <div className="text-sm text-muted-foreground mt-2">
                Riesgo: {kpis.concentration.concentration_risk}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
