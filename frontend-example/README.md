# 📦 Ejemplos de Código Frontend

Este directorio contiene ejemplos de código listos para usar en Lovable o en un proyecto React local.

## 📁 Archivos

- `api-service.ts` - Servicio completo para llamadas al API
- `useKPIs.ts` - Hook de React para obtener KPIs

## 🚀 Uso Rápido

### En Lovable

1. Copia el contenido de `api-service.ts`
2. Pégalo en un archivo nuevo en Lovable: `src/services/api-service.ts`
3. Copia el contenido de `useKPIs.ts`
4. Pégalo en: `src/hooks/useKPIs.ts`
5. Usa el hook en tus componentes:

```tsx
import { useKPIs } from './hooks/useKPIs';

function Dashboard() {
  const { data, loading, error } = useKPIs(2025);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1>Ingresos: ${data?.financial.revenue.toLocaleString()}</h1>
    </div>
  );
}
```

### En Proyecto React Local

1. Instala dependencias:
```bash
npm install
```

2. Crea `.env.local`:
```env
VITE_API_URL=http://localhost:8000/api
```

3. Copia los archivos a tu proyecto:
```bash
cp api-service.ts src/services/
cp useKPIs.ts src/hooks/
```

4. Usa en tus componentes como se muestra arriba.

## 🔗 Endpoints Disponibles

Todos los métodos están disponibles en `apiService`:

```typescript
import apiService from './services/api-service';

// KPIs
const kpis = await apiService.getKPIs(2025);

// Ingresos por cliente
const customers = await apiService.getRevenueByCustomer(2025, 10);

// Capital de trabajo
const workingCapital = await apiService.getWorkingCapitalSummary(2025);

// Alertas
const alerts = await apiService.getAlerts(2025);
```

## ⚙️ Configuración

La URL base del API se configura automáticamente:
- Si existe `VITE_API_URL` en variables de entorno, la usa
- Si no, usa `http://localhost:8000/api` por defecto

Para cambiar la URL, agrega en `.env`:
```env
VITE_API_URL=https://tu-backend.com/api
```

