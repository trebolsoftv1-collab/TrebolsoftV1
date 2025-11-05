import { MapPinIcon, CameraIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { useGeolocation } from '../hooks/useGeolocation';
import { usePhotoCapture } from '../hooks/usePhotoCapture';

/**
 * Componente para capturar ubicación y foto en el formulario de cliente
 */
export function ClientLocationPhoto({ 
  latitude, 
  longitude, 
  photoUrl, 
  onLocationChange, 
  onPhotoChange 
}) {
  const { location, loading: geoLoading, error: geoError, captureLocation } = useGeolocation();
  const { 
    photo, 
    preview, 
    error: photoError, 
    inputRef, 
    handleFileSelect, 
    triggerCapture, 
    clearPhoto 
  } = usePhotoCapture();

  const handleCaptureLocation = async () => {
    try {
      const coords = await captureLocation();
      onLocationChange(coords.latitude, coords.longitude);
    } catch (err) {
      console.error('Error capturing location:', err);
    }
  };

  const handlePhotoSelect = (e) => {
    handleFileSelect(e);
    if (e.target.files?.[0]) {
      onPhotoChange(e.target.files[0]);
    }
  };

  const currentPhotoUrl = preview || photoUrl;
  const currentLat = location?.latitude || latitude;
  const currentLng = location?.longitude || longitude;

  return (
    <div className="space-y-4">
      {/* Geolocalización */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          📍 Ubicación del cliente
        </label>
        
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleCaptureLocation}
            disabled={geoLoading}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            <MapPinIcon className="h-5 w-5" />
            {geoLoading ? 'Obteniendo...' : 'Capturar ubicación'}
          </button>

          {currentLat && currentLng && (
            <div className="flex-1 text-sm text-gray-600">
              <span className="font-mono">
                {currentLat.toFixed(6)}, {currentLng.toFixed(6)}
              </span>
              <a
                href={`https://maps.google.com/?q=${currentLat},${currentLng}`}
                target="_blank"
                rel="noopener noreferrer"
                className="ml-3 text-blue-600 hover:underline"
              >
                Ver en Google Maps →
              </a>
            </div>
          )}
        </div>

        {geoError && (
          <p className="mt-2 text-sm text-red-600">{geoError}</p>
        )}
      </div>

      {/* Foto de la casa */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          📷 Foto de la vivienda
        </label>

        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handlePhotoSelect}
          className="hidden"
        />

        {currentPhotoUrl ? (
          <div className="relative">
            <img
              src={currentPhotoUrl}
              alt="Vista previa"
              className="w-full h-64 object-cover rounded-lg"
            />
            <button
              type="button"
              onClick={() => {
                clearPhoto();
                onPhotoChange(null);
              }}
              className="absolute top-2 right-2 p-2 bg-red-600 text-white rounded-full hover:bg-red-700"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>
        ) : (
          <button
            type="button"
            onClick={triggerCapture}
            className="w-full flex items-center justify-center gap-2 px-4 py-8 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 hover:bg-gray-100"
          >
            <CameraIcon className="h-8 w-8 text-gray-400" />
            <span className="text-gray-600">Capturar foto de la casa</span>
          </button>
        )}

        {photoError && (
          <p className="mt-2 text-sm text-red-600">{photoError}</p>
        )}
        
        <p className="mt-2 text-xs text-gray-500">
          Máx. 5MB • Formatos: JPG, PNG, WEBP
        </p>
      </div>
    </div>
  );
}
