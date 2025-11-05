# TrebolSoft Frontend - Plan de implementación

## 🎯 Objetivo
Crear una PWA (Progressive Web App) instalable para gestión de créditos y cobranza con captura de geolocalización y fotos.

## 🏗️ Stack tecnológico

### Core
- **React 18** - Framework UI
- **Vite** - Build tool rápido
- **React Router 6** - Navegación
- **TypeScript** - Type safety (opcional, empezar con JS)

### UI/Styling
- **TailwindCSS** - Utility-first CSS
- **Headless UI** - Componentes accesibles
- **Heroicons** - Iconos

### Estado y datos
- **Axios** - HTTP client con interceptors
- **React Query** - Cache y sincronización de datos del API
- **Zustand** - Estado global ligero (auth, user)

### PWA
- **vite-plugin-pwa** - Service worker y manifest
- **Workbox** - Cache strategies

## 📱 Características principales

### 1. Autenticación
- Login con username/password
- JWT almacenado en localStorage
- Auto-logout en 401
- Refresh automático de token

### 2. Roles y permisos
- **Admin**: CRUD completo de usuarios, clientes, créditos, transacciones
- **Supervisor**: Ver y editar datos de sus cobradores asignados
- **Cobrador**: Ver sus clientes asignados, registrar pagos, capturar ubicación y fotos

### 3. Gestión de clientes
- Lista de clientes asignados
- Crear/editar cliente
- **Captura de geolocalización** (navigator.geolocation)
- **Captura de foto de vivienda** (input capture="environment")
- Ver ubicación en Google Maps
- Ver foto de la casa

### 4. Gestión de créditos
- Lista de créditos por cliente
- Crear crédito con monto, interés, plazo, seguro
- Ver detalle: monto total, pago diario, saldo pendiente
- Estado: pendiente/completado

### 5. Registro de pagos
- Registrar pago diario
- Actualizar saldo pendiente
- Historial de pagos

### 6. PWA (instalable)
- Manifest.json con nombre, iconos, colores
- Service worker para cache offline
- Funciona sin conexión (lee datos cacheados)
- Instalable en Android/iOS/Desktop
- Splash screen personalizada

## 📂 Estructura del proyecto

```
trebolsoft-frontend/
├── public/
│   ├── icons/              # Iconos PWA (192x192, 512x512)
│   └── manifest.json       # PWA manifest
├── src/
│   ├── api/                # Axios config e interceptors
│   │   ├── axios.js
│   │   └── endpoints/
│   │       ├── auth.js
│   │       ├── clients.js
│   │       ├── credits.js
│   │       └── transactions.js
│   ├── components/         # Componentes reutilizables
│   │   ├── Layout.jsx
│   │   ├── Navbar.jsx
│   │   ├── ClientCard.jsx
│   │   ├── CreditCard.jsx
│   │   └── PhotoCapture.jsx
│   ├── pages/              # Páginas/rutas
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Clients/
│   │   │   ├── ClientList.jsx
│   │   │   ├── ClientForm.jsx
│   │   │   └── ClientDetail.jsx
│   │   ├── Credits/
│   │   │   ├── CreditList.jsx
│   │   │   ├── CreditForm.jsx
│   │   │   └── CreditDetail.jsx
│   │   └── Transactions/
│   │       ├── TransactionList.jsx
│   │       └── PaymentForm.jsx
│   ├── store/              # Zustand store
│   │   └── authStore.js
│   ├── hooks/              # Custom hooks
│   │   ├── useAuth.js
│   │   ├── useGeolocation.js
│   │   └── usePhotoCapture.js
│   ├── utils/              # Utilidades
│   │   └── helpers.js
│   ├── App.jsx             # Rutas principales
│   ├── main.jsx            # Entry point
│   └── index.css           # Tailwind imports
├── .env.example            # Variables de entorno
├── package.json
├── vite.config.js          # Config de Vite + PWA
└── tailwind.config.js
```

## 🚀 Comandos de inicio

### 1. Crear proyecto
```bash
npm create vite@latest trebolsoft-frontend -- --template react
cd trebolsoft-frontend
```

### 2. Instalar dependencias
```bash
npm install

# Router
npm install react-router-dom

# HTTP y estado
npm install axios @tanstack/react-query zustand

# UI
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @headlessui/react @heroicons/react

# PWA
npm install -D vite-plugin-pwa
```

### 3. Configurar Tailwind
```js
// tailwind.config.js
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

### 4. Configurar PWA
```js
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'robots.txt', 'icons/*.png'],
      manifest: {
        name: 'TrebolSoft',
        short_name: 'TrebolSoft',
        description: 'Sistema de gestión de créditos y cobranza',
        theme_color: '#10b981',
        background_color: '#ffffff',
        display: 'standalone',
        icons: [
          {
            src: '/icons/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icons/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ]
})
```

### 5. Variables de entorno
```bash
# .env
VITE_API_URL=https://trebolsoft.onrender.com
```

## 🎨 Componentes clave

### Captura de geolocalización
```jsx
// hooks/useGeolocation.js
export const useGeolocation = () => {
  const [location, setLocation] = useState(null);
  const [error, setError] = useState(null);

  const capture = () => {
    if (!navigator.geolocation) {
      setError('Geolocation not supported');
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        });
      },
      (err) => setError(err.message)
    );
  };

  return { location, error, capture };
};
```

### Captura de foto
```jsx
// components/PhotoCapture.jsx
export const PhotoCapture = ({ onCapture }) => {
  const inputRef = useRef();

  const handleChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Preview
    const reader = new FileReader();
    reader.onload = (e) => {
      onCapture(file, e.target.result);
    };
    reader.readAsDataURL(file);
  };

  return (
    <div>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleChange}
        className="hidden"
      />
      <button onClick={() => inputRef.current.click()}>
        📷 Capturar foto
      </button>
    </div>
  );
};
```

## 📦 Deploy en Vercel

### 1. Conectar repositorio
1. Push del frontend a GitHub (repo separado o carpeta)
2. Ve a: https://vercel.com
3. Importar proyecto desde GitHub
4. Vercel detecta automáticamente Vite

### 2. Configurar variables
```
VITE_API_URL=https://trebolsoft.onrender.com
```

### 3. Build settings
- Framework Preset: Vite
- Build Command: `npm run build`
- Output Directory: `dist`

### 4. Deploy
- Click en "Deploy"
- Vercel te da una URL: `https://trebolsoft.vercel.app`
- Auto-deploy en cada push a main

## ✅ Checklist de implementación

### Fase 1: Setup (1 día)
- [ ] Crear proyecto Vite
- [ ] Instalar dependencias
- [ ] Configurar Tailwind
- [ ] Configurar PWA
- [ ] Configurar Axios con interceptors
- [ ] Configurar React Router

### Fase 2: Auth (1 día)
- [ ] Página de login
- [ ] Store de autenticación (Zustand)
- [ ] Interceptor para agregar token
- [ ] Manejo de 401 (auto-logout)
- [ ] Protected routes

### Fase 3: Dashboard y navegación (1 día)
- [ ] Layout con navbar
- [ ] Dashboard con resumen por rol
- [ ] Menú lateral responsive
- [ ] Navegación entre módulos

### Fase 4: Clientes (2 días)
- [ ] Lista de clientes
- [ ] Formulario crear/editar cliente
- [ ] Captura de geolocalización
- [ ] Captura de foto de casa
- [ ] Upload de foto a backend
- [ ] Ver ubicación en Google Maps
- [ ] Ver foto de la casa

### Fase 5: Créditos (1 día)
- [ ] Lista de créditos por cliente
- [ ] Formulario crear crédito
- [ ] Vista detalle crédito
- [ ] Cálculo automático de totales

### Fase 6: Transacciones (1 día)
- [ ] Formulario registrar pago
- [ ] Historial de pagos
- [ ] Actualización de saldo

### Fase 7: PWA y deploy (1 día)
- [ ] Iconos PWA
- [ ] Configurar manifest
- [ ] Service worker
- [ ] Probar instalación en móvil
- [ ] Deploy en Vercel
- [ ] Probar end-to-end

**Total: ~8 días de desarrollo**

## 📱 Instalación de la PWA

### Android
1. Abre la URL en Chrome
2. Click en menú (3 puntos)
3. "Agregar a pantalla de inicio"
4. Se instala como app nativa

### iOS
1. Abre la URL en Safari
2. Click en "Compartir"
3. "Agregar a inicio"
4. Se instala como app

### Desktop
1. Abre en Chrome/Edge
2. Icono de instalación en barra de direcciones
3. "Instalar TrebolSoft"

---

**Next steps**: Una vez tengas Cloudinary configurado, podemos empezar con el frontend.
