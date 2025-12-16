/**
 * Hook de React para obtener KPIs del dashboard
 * Ejemplo de uso en componentes React
 */

import { useState, useEffect } from 'react';
import { apiService, KPIDashboard } from './api-service';

export function useKPIs(year?: number) {
  const [data, setData] = useState<KPIDashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchKPIs() {
      try {
        setLoading(true);
        setError(null);
        const kpis = await apiService.getKPIs(year);
        
        if (!cancelled) {
          setData(kpis);
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err : new Error('Error desconocido'));
          setLoading(false);
        }
      }
    }

    fetchKPIs();

    return () => {
      cancelled = true;
    };
  }, [year]);

  return { data, loading, error };
}

// Ejemplo de uso en un componente:
/*
import { useKPIs } from './hooks/useKPIs';

function Dashboard() {
  const { data, loading, error } = useKPIs(2025);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return null;

  return (
    <div>
      <h1>Ingresos: ${data.financial.revenue.toLocaleString()}</h1>
      <p>Margen Bruto: {data.financial.gross_margin}%</p>
      <p>Alertas: {data.alerts.length}</p>
    </div>
  );
}
*/

