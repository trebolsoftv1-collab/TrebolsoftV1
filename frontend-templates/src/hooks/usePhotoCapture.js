import { useState, useRef } from 'react';

/**
 * Hook para capturar fotos usando la cámara del dispositivo
 */
export const usePhotoCapture = () => {
  const [photo, setPhoto] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    
    if (!file) {
      return;
    }

    // Validar tipo de archivo
    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      setError('Only JPG, PNG and WEBP images are allowed');
      return;
    }

    // Validar tamaño (5MB max)
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    if (file.size > maxSize) {
      setError('File size must be less than 5MB');
      return;
    }

    // Crear preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target.result);
      setPhoto(file);
      setError(null);
    };
    reader.onerror = () => {
      setError('Failed to read file');
    };
    reader.readAsDataURL(file);
  };

  const triggerCapture = () => {
    inputRef.current?.click();
  };

  const clearPhoto = () => {
    setPhoto(null);
    setPreview(null);
    setError(null);
    if (inputRef.current) {
      inputRef.current.value = '';
    }
  };

  return {
    photo,
    preview,
    error,
    inputRef,
    handleFileSelect,
    triggerCapture,
    clearPhoto,
  };
};
