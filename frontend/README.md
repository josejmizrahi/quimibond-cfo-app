# 📊 Quimibond CFO Dashboard - Frontend

Frontend del Dashboard CFO construido con React, TypeScript, Tailwind CSS y componentes shadcn/ui.

## 🚀 Inicio Rápido

### Instalación

```bash
cd frontend
npm install
```

### Desarrollo

```bash
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

### Build para Producción

```bash
npm run build
```

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── ui/             # Componentes base de shadcn
│   │   ├── KPICard.tsx     # Tarjeta de KPI
│   │   ├── AlertBadge.tsx  # Badge de alerta
│   │   ├── LoadingState.tsx # Estados de carga
│   │   ├── ErrorState.tsx   # Estados de error
│   │   ├── StatCard.tsx     # Tarjeta de estadística
│   │   └── ChartCard.tsx    # Contenedor de gráficas
│   ├── pages/              # Páginas
│   │   └── Dashboard.tsx    # Dashboard principal
│   ├── services/            # Servicios
│   │   └── api.ts          # Cliente API
│   └── lib/                 # Utilidades
│       └── utils.ts        # Funciones helper
```

## 🎨 Componentes Disponibles

### Componentes UI (shadcn)

- `Card` - Tarjeta contenedora
- `Button` - Botón con variantes
- `Select` - Selector dropdown
- `Skeleton` - Placeholder de carga

### Componentes de Negocio

- `KPICard` - Muestra un KPI con variación y estado
- `AlertBadge` - Muestra alertas con iconos y colores
- `LoadingState` - Estado de carga reutilizable
- `ErrorState` - Estado de error con retry
- `StatCard` - Tarjeta de estadística simple
- `ChartCard` - Contenedor para gráficas

## 🔌 Configuración del API

El frontend se conecta al backend en `http://localhost:8000/api` por defecto.

Para cambiar la URL, crea un archivo `.env`:

```env
VITE_API_URL=http://localhost:8000/api
```

## 📦 Dependencias Principales

- **React 19** - Framework UI
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Estilos utility-first
- **Recharts** - Gráficas y visualizaciones
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos
- **shadcn/ui** - Componentes UI

## 🎯 Características

- ✅ Dashboard con KPIs en tiempo real
- ✅ Gráficas interactivas con Recharts
- ✅ Sistema de alertas visual
- ✅ Componentes reutilizables
- ✅ Estados de carga y error
- ✅ Diseño responsive
- ✅ Tema claro/oscuro (preparado)

## 🔧 Desarrollo

### Agregar un Nuevo Componente

1. Crea el componente en `src/components/`
2. Usa los componentes base de `ui/` cuando sea posible
3. Exporta desde el componente
4. Importa donde lo necesites

### Agregar una Nueva Página

1. Crea la página en `src/pages/`
2. Usa los componentes reutilizables
3. Conecta con el API usando `apiService`
4. Maneja estados de carga y error

## 📝 Notas

- Todos los componentes son reutilizables
- Los estilos usan Tailwind CSS con el sistema de diseño de shadcn
- El código está completamente tipado con TypeScript
- Los componentes siguen las mejores prácticas de React
