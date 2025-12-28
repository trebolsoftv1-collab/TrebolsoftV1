# Script para verificar si el deploy del cambio de seguridad ya está activo

Write-Host "🔍 VERIFICANDO ESTADO DEL DEPLOY EN RENDER" -ForegroundColor Cyan
Write-Host "=" * 60

# Test 1: Health check
Write-Host "`n1️⃣ Health Check..."
try {
    $health = Invoke-WebRequest -Uri "https://api.trebolsoft.com/health" -UseBasicParsing
    Write-Host "   ✅ API respondiendo OK" -ForegroundColor Green
} catch {
    Write-Host "   ❌ API no responde" -ForegroundColor Red
    exit
}

# Test 2: Root endpoint (debería devolver JSON con info de docs)
Write-Host "`n2️⃣ Verificando endpoint raíz..."
try {
    $root = Invoke-WebRequest -Uri "https://api.trebolsoft.com/" -UseBasicParsing
    $json = $root.Content | ConvertFrom-Json
    Write-Host "   Mensaje: $($json.message)" -ForegroundColor Yellow
    Write-Host "   Docs status: $($json.docs)" -ForegroundColor Yellow
    
    if ($json.docs -eq "disabled in production") {
        Write-Host "   ✅ Cambio aplicado correctamente" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Aún no se aplicó el cambio" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ⚠️  Root devuelve HTML (versión anterior)" -ForegroundColor Yellow
}

# Test 3: Docs endpoint (debe fallar con 404)
Write-Host "`n3️⃣ Verificando /docs (DEBE estar bloqueado)..."
try {
    $docs = Invoke-WebRequest -Uri "https://api.trebolsoft.com/docs" -UseBasicParsing -ErrorAction Stop
    Write-Host "   ❌ DOCS AÚN DISPONIBLE - Deploy pendiente" -ForegroundColor Red
    Write-Host "   ⏳ Espera 2-3 minutos y vuelve a ejecutar este script" -ForegroundColor Yellow
} catch {
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Host "   ✅ DOCS BLOQUEADO CORRECTAMENTE (404)" -ForegroundColor Green
        Write-Host "`n🎉 DEPLOY COMPLETADO CON ÉXITO" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Error inesperado: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# Test 4: Login (debe seguir funcionando)
Write-Host "`n4️⃣ Verificando que login siga funcionando..."
# ⚠️ IMPORTANTE: Cambia "TU_CONTRASENA_AQUI" por la contraseña real de tu usuario 'trebolsoft'
$adminPassword = "TU_CONTRASENA_AQUI"
$body = "username=trebolsoft&password=$adminPassword"
try {
    $response = Invoke-WebRequest -Uri "https://api.trebolsoft.com/api/v1/auth/token" -Method POST -ContentType "application/x-www-form-urlencoded" -Body $body -UseBasicParsing
    Write-Host "   ✅ Login funcionando correctamente" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Login falló: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n" + ("=" * 60)
Write-Host "Ejecuta este script cada 2-3 minutos hasta que todo esté ✅" -ForegroundColor Cyan
