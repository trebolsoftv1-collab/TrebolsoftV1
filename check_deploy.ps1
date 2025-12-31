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
# ⚠️ Asegúrate de que esta sea la contraseña actual de tu usuario 'trebolsoft'
# Si la cambiaste en la BD, actualízala aquí.
$adminPassword = "Porquesi2025" 
$body = "username=trebolsoft&password=$adminPassword"
try {
    $response = Invoke-WebRequest -Uri "https://api.trebolsoft.com/api/v1/auth/token" -Method POST -ContentType "application/x-www-form-urlencoded" -Body $body -UseBasicParsing
    Write-Host "   ✅ Login funcionando correctamente" -ForegroundColor Green
    
    # Guardar token para pruebas de módulos
    $token = ($response.Content | ConvertFrom-Json).access_token
} catch {
    Write-Host "   ❌ Login falló: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# Test 5: Verificar Módulos
Write-Host "`n5️⃣ Verificando Módulos Principales..."
$headers = @{ "Authorization" = "Bearer $token" }
$modules = @{
    "Clientes" = "api/v1/clients/"
    "Créditos" = "api/v1/credits/"
    "Transacciones" = "api/v1/transactions/"
    "Cajas (Ruta English)" = "api/v1/boxes/"
    "Cajas (Ruta Español)" = "api/v1/cajas/"
}

foreach ($name in $modules.Keys) {
    try {
        # Usamos ErrorAction Stop para capturar 404s o 500s
        $res = Invoke-WebRequest -Uri "https://api.trebolsoft.com/$($modules[$name])" -Headers $headers -UseBasicParsing -ErrorAction Stop
        
        # Si responde 200 o 405 (Method Not Allowed, significa que la ruta existe pero pide POST/GET específico), es éxito
        Write-Host "   ✅ $name: DISPONIBLE" -ForegroundColor Green
    } catch {
        $statusCode = $_.Exception.Response.StatusCode
        if ($statusCode -eq 404) {
             if ($name -like "*Cajas*") {
                Write-Host "   🔸 $name: No encontrado (Probablemente usaste la otra ruta)" -ForegroundColor DarkGray
             } else {
                Write-Host "   ❌ $name: NO ENCONTRADO (404) - ¿El archivo está en TrebolsoftV1?" -ForegroundColor Red
             }
        } else {
             Write-Host "   ❌ $name: FALLÓ ($statusCode)" -ForegroundColor Red
        }
    }
}

Write-Host "`n" + ("=" * 60)
Write-Host "Ejecuta este script cada 2-3 minutos hasta que todo esté ✅" -ForegroundColor Cyan
