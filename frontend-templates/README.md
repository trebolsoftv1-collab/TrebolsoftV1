# Frontend Templates - TrebolSoft

## 📁 Contenido

Esta carpeta contiene los templates listos para usar en el proyecto frontend React + Vite + PWA.

### Archivos incluidos:

#### API Layer (`src/api/`)
- **axios.js**: Configuración de axios con interceptors para autenticación
- **endpoints/auth.js**: Funciones para login y obtener usuario actual
- **endpoints/clients.js**: CRUD completo de clientes + upload de fotos

#### Hooks personalizados (`src/hooks/`)
- **useGeolocation.js**: Hook para capturar ubicación GPS del dispositivo
- **usePhotoCapture.js**: Hook para capturar fotos con la cámara

#### Componentes (`src/components/`)
- **ClientLocationPhoto.jsx**: Componente completo para captura de ubicación y foto

## 🚀 Cómo usar

### 1. Instala Node.js
Descarga desde: https://nodejs.org/

### 2. Crea el proyecto Vite
```powershell
cd C:\Users\jpancha\trebolsoft-frontend
npm create vite@latest . -- --template react
npm install
```

### 3. Copia los templates
Copia el contenido de `frontend-templates/src/` al `src/` de tu proyecto Vite.

### 4. Instala dependencias
```powershell
npm install react-router-dom axios @tanstack/react-query zustand
npm install @headlessui/react @heroicons/react
npm install -D tailwindcss postcss autoprefixer vite-plugin-pwa
npx tailwindcss init -p
```

### 5. Configura TailwindCSS
Edita `tailwind.config.js`:
```js
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: '#10b981',
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

### 6. Crea `.env`
```
VITE_API_URL=https://trebolsoft.onrender.com
```

### 7. Ejecuta
```powershell
npm run dev
```

## 📱 Componentes destacados

### ClientLocationPhoto
Componente todo-en-uno para capturar ubicación y foto:

```jsx
import { ClientLocationPhoto } from './components/ClientLocationPhoto';

function ClientForm() {
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [photoFile, setPhotoFile] = useState(null);

  return (
    <form>
      {/* Otros campos del formulario */}
      
      <ClientLocationPhoto
        latitude={latitude}
        longitude={longitude}
        photoUrl={existingPhotoUrl}
        onLocationChange={(lat, lng) => {
          setLatitude(lat);
          setLongitude(lng);
        }}
        onPhotoChange={(file) => {
          setPhotoFile(file);
        }}
      />
      
      {/* Submit, etc. */}
    </form>
  );
}
```

### useGeolocation Hook
```jsx
import { useGeolocation } from '../hooks/useGeolocation';

function MyComponent() {
  const { location, error, loading, captureLocation } = useGeolocation();

  const handleCapture = async () => {
    const coords = await captureLocation();
    console.log(coords.latitude, coords.longitude);
  };

  return (
    <button onClick={handleCapture} disabled={loading}>
      {loading ? 'Obteniendo...' : 'Capturar ubicación'}
    </button>
  );
}
```

### usePhotoCapture Hook
```jsx
import { usePhotoCapture } from '../hooks/usePhotoCapture';

function MyComponent() {
  const { 
    photo, 
    preview, 
    inputRef, 
    handleFileSelect, 
    triggerCapture 
  } = usePhotoCapture();

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleFileSelect}
        className="hidden"
      />
      
      {preview ? (
        <img src={preview} alt="Preview" />
      ) : (
        <button onClick={triggerCapture}>
          📷 Capturar foto
        </button>
      )}
    </>
  );
}
```

### Clients API
```jsx
import { clientsAPI } from '../api/endpoints/clients';

// Crear cliente con ubicación
const newClient = await clientsAPI.createClient({
  dni: "12345678",
  full_name: "Juan Pérez",
  address: "Calle 123",
  phone: "555-1234",
  latitude: 4.7110,
  longitude: -74.0721,
});

// Subir foto
const result = await clientsAPI.uploadPhoto(clientId, photoFile);
console.log(result.photo_url); // URL de Cloudinary
```

## 🎨 Personalización

### Colores
Edita `tailwind.config.js` para cambiar los colores del tema.

### Iconos
Usa heroicons: https://heroicons.com/

### Componentes UI
Usa Headless UI: https://headlessui.com/

## 📖 Documentación completa

Ver `FRONTEND_SETUP_GUIDE.md` para instrucciones detalladas de setup y deploy.

## 🆘 Soporte

Si tienes problemas:
1. Verifica que Node.js esté instalado: `node --version`
2. Verifica que las variables de entorno estén configuradas (`.env`)
3. Revisa la consola del navegador para errores
4. Verifica que el backend esté corriendo en Render
