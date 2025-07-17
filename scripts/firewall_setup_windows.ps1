# Script de Configuração de Firewall para Windows
# Trabalho Prático 02 - Segurança Computacional

Write-Host "🔥 Configurando Windows Firewall para SQL Injection Demo" -ForegroundColor Yellow
Write-Host "=========================================================" -ForegroundColor Yellow

function Check-Command {
    param($description)
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $description" -ForegroundColor Green
    } else {
        Write-Host "❌ Erro: $description" -ForegroundColor Red
        exit 1
    }
}

$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Este script precisa ser executado como Administrador!" -ForegroundColor Red
    Write-Host "💡 Clique com botão direito no PowerShell e selecione 'Executar como administrador'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Executando como Administrador" -ForegroundColor Green

Write-Host "📝 Configurando logging do Windows Firewall..." -ForegroundColor Cyan
try {
    netsh advfirewall set allprofiles logging allowedconnections enable
    netsh advfirewall set allprofiles logging droppedconnections enable
    netsh advfirewall set allprofiles logging filename "%systemroot%\system32\logfiles\firewall\pfirewall.log"
    netsh advfirewall set allprofiles logging maxfilesize 4096
    Write-Host "✅ Logging configurado" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao configurar logging: $_" -ForegroundColor Red
}

Write-Host "🧹 Removendo regras existentes do projeto..." -ForegroundColor Cyan
try {
    netsh advfirewall firewall delete rule name="SQL Injection Demo - HTTP" >$null 2>&1
    netsh advfirewall firewall delete rule name="SQL Injection Demo - App" >$null 2>&1
    netsh advfirewall firewall delete rule name="SQL Injection Demo - MySQL" >$null 2>&1
    Write-Host "✅ Regras antigas removidas" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Nenhuma regra anterior encontrada" -ForegroundColor Yellow
}

Write-Host "🎯 Configurando regra para aplicação vulnerável (porta 5000)..." -ForegroundColor Cyan
try {
    netsh advfirewall firewall add rule name="SQL Injection Demo - App" dir=in action=allow protocol=TCP localport=5000
    Write-Host "✅ Porta 5000 liberada para aplicação" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao configurar porta 5000: $_" -ForegroundColor Red
}

Write-Host "🌐 Configurando regra para HTTP (porta 80)..." -ForegroundColor Cyan
try {
    netsh advfirewall firewall add rule name="SQL Injection Demo - HTTP" dir=in action=allow protocol=TCP localport=80
    Write-Host "✅ Porta 80 liberada para HTTP" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao configurar porta 80: $_" -ForegroundColor Red
}

Write-Host "🗄️ Configurando regra para MySQL local (porta 3306)..." -ForegroundColor Cyan
try {
    netsh advfirewall firewall add rule name="SQL Injection Demo - MySQL" dir=in action=allow protocol=TCP localport=3306 remoteip=127.0.0.1,172.16.0.0/12
    Write-Host "✅ Porta 3306 liberada apenas para acesso local" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro ao configurar porta 3306: $_" -ForegroundColor Red
}

Write-Host "📊 Configurando auditoria de eventos..." -ForegroundColor Cyan
try {
    auditpol /set /category:"Logon/Logoff" /success:enable /failure:enable
    
    auditpol /set /category:"Object Access" /success:enable /failure:enable
    
    Write-Host "✅ Auditoria configurada" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Erro ao configurar auditoria: $_" -ForegroundColor Yellow
}

Write-Host "" -ForegroundColor White
Write-Host "📋 Regras configuradas:" -ForegroundColor Yellow
Write-Host "=======================" -ForegroundColor Yellow
try {
    netsh advfirewall firewall show rule name="SQL Injection Demo - App"
    netsh advfirewall firewall show rule name="SQL Injection Demo - HTTP"
    netsh advfirewall firewall show rule name="SQL Injection Demo - MySQL"
} catch {
    Write-Host "❌ Erro ao exibir regras" -ForegroundColor Red
}

Write-Host "" -ForegroundColor White
Write-Host "🔍 Para monitorar logs do Windows Firewall:" -ForegroundColor Cyan
Write-Host "Get-Content C:\Windows\System32\LogFiles\Firewall\pfirewall.log -Tail 20 -Wait" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "📝 Para ver eventos de segurança:" -ForegroundColor Cyan
Write-Host "Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625,4624} -MaxEvents 10" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "🛠️ Para remover as regras depois:" -ForegroundColor Cyan
Write-Host "netsh advfirewall firewall delete rule name=`"SQL Injection Demo - App`"" -ForegroundColor White
Write-Host "netsh advfirewall firewall delete rule name=`"SQL Injection Demo - HTTP`"" -ForegroundColor White
Write-Host "netsh advfirewall firewall delete rule name=`"SQL Injection Demo - MySQL`"" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "✅ Windows Firewall configurado com sucesso!" -ForegroundColor Green
Write-Host "⚠️  ATENÇÃO: Este é um ambiente de teste. Revise as regras antes de usar em produção!" -ForegroundColor Yellow 