# Setup del Frontend TrebolSoft

## Prerequisitos

### 1. Instalar Node.js (si no lo tienes)

Descarga e instala desde: https://nodejs.org/

**Recomendado**: Versión LTS (Long Term Support)

Verifica la instalación:
```powershell
node --version
npm --version
```

---

## Crear proyecto desde cero

### 1. Crear el directorio y proyecto Vite

```powershell
# Desde C:\Users\jpancha
cd trebolsoft-frontend

# Inicializar proyecto Vite con React
npm create vite@latest . -- --template react

# Instalar dependencias base
npm install
```

### 2. Instalar TailwindCSS

```powershell
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Edita `tailwind.config.js`:
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#10b981',    // verde trebol
        secondary: '#3b82f6',
        danger: '#ef4444',
      }
    },
  },
  plugins: [],
}
```

Edita `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 3. Instalar dependencias principales

```powershell
# Router
npm install react-router-dom

# HTTP y estado
npm install axios @tanstack/react-query zustand

# UI Components
npm install @headlessui/react @heroicons/react
```

### 4. Configurar PWA

```powershell
npm install -D vite-plugin-pwa
```

Edita `vite.config.js`:
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'robots.txt'],
      manifest: {
        name: 'TrebolSoft',
        short_name: 'TrebolSoft',
        description: 'Sistema de gestión de créditos y cobranza',
        theme_color: '#10b981',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: '/',
        icons: [
          {
            src: '/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      },
      workbox: {
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/trebolsoft\.onrender\.com\/api\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24 // 24 horas
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          }
        ]
      }
    })
  ],
  server: {
    port: 3000
  }
})
```

### 5. Crear archivo de variables de entorno

Crea `.env`:
```bash
VITE_API_URL=https://trebolsoft.onrender.com
```

Crea `.env.local` (para desarrollo local):
```bash
VITE_API_URL=http://localhost:10000
```

### 6. Estructura de carpetas

Crea la siguiente estructura:
```
src/
├── api/                 # Configuración de Axios
│   ├── axios.js
│   └── endpoints/
│       ├── auth.js
│       ├── clients.js
│       ├── credits.js
│       └── transactions.js
├── components/          # Componentes reutilizables
│   ├── Layout.jsx
│   ├── Navbar.jsx
│   ├── ProtectedRoute.jsx
│   ├── ClientCard.jsx
│   ├── CreditCard.jsx
│   └── PhotoCapture.jsx
├── pages/              # Páginas/rutas
│   ├── Login.jsx
│   ├── Dashboard.jsx
│   └── clients/
│       ├── ClientList.jsx
│       ├── ClientForm.jsx
│       └── ClientDetail.jsx
├── store/              # Zustand store
│   └── authStore.js
├── hooks/              # Custom hooks
│   ├── useAuth.js
│   ├── useGeolocation.js
│   └── usePhotoCapture.js
├── utils/              # Utilidades
│   └── helpers.js
├── App.jsx
├── main.jsx
└── index.css
```

---

## Comandos de desarrollo

```powershell
# Modo desarrollo (con hot reload)
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview
```

---

## Deploy en Vercel

### Opción 1: Desde GitHub

1. Sube el código a GitHub:
```powershell
git init
git add .
git commit -m "Initial frontend setup"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/trebolsoft-frontend.git
git push -u origin main
```

2. Ve a https://vercel.com
3. "Add New Project"
4. Importa desde GitHub
5. Configura:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment Variables:
     - `VITE_API_URL` = `https://trebolsoft.onrender.com`

### Opción 2: Deploy directo con Vercel CLI

```powershell
# Instalar Vercel CLI
npm install -g vercel

# Deploy
vercel

# Deploy a producción
vercel --prod
```

---

## Probar la PWA localmente

1. Build del proyecto:
```powershell
npm run build
npm run preview
```

2. Abre en Chrome: `http://localhost:4173`

3. DevTools → Application → Service Workers

4. En móvil (Android):
   - Conecta el móvil por USB
   - Habilita depuración USB
   - Chrome → chrome://inspect
   - Abre la URL local
   - Verás opción "Agregar a pantalla de inicio"

---

## Testing

### Test de autenticación
1. Abre `/login`
2. Ingresa credenciales
3. Verifica que redirija a `/dashboard`
4. Token debe estar en localStorage

### Test de geolocalización
1. Crea un cliente
2. Click en "Capturar ubicación"
3. Acepta permisos
4. Verifica que lat/lng se muestren
5. Click en "Ver en Google Maps"

### Test de foto
1. En móvil, edita un cliente
2. Click en "Capturar foto"
3. Toma una foto
4. Verifica que se suba a Cloudinary
5. La foto debe mostrarse en el detalle del cliente

---

## Troubleshooting

### Error: CORS al llamar la API
- Verifica que `CORS_ALLOWED_ORIGINS` en el backend incluya tu dominio de frontend
- En producción: `https://tu-app.vercel.app`
- En local: `http://localhost:3000`

### La PWA no se instala
- Debes usar HTTPS (en producción, Vercel lo provee automáticamente)
- Verifica que manifest.json tenga los iconos correctos
- Chrome DevTools → Lighthouse → PWA audit

### Geolocalización no funciona
- Requiere HTTPS (excepto localhost)
- Usuario debe dar permisos
- En iOS Safari, el permiso se pide cada vez

### Las fotos no se suben
- Verifica que Cloudinary esté configurado en Render
- Max 5MB por foto
- Solo JPG, PNG, WEBP

---

## Recursos adicionales

- Documentación Vite: https://vitejs.dev
- Documentación TailwindCSS: https://tailwindcss.com
- Documentación PWA: https://vite-pwa-org.netlify.app
- Geolocation API: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API
- File API: https://developer.mozilla.org/en-US/docs/Web/API/File_API

---

## Siguiente paso

Una vez tengas Node.js instalado y el proyecto creado, ejecuta:
```powershell
cd C:\Users\jpancha\trebolsoft-frontend
npm install
npm run dev
```

Y abre http://localhost:3000 para ver la aplicación.
