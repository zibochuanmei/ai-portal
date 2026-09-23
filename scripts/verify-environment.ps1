param(
    [switch]$SkipDocker
)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\")).Path
Set-Location $projectRoot

function Require-Command([string]$name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "未找到命令 $name，请先按 docs/推荐开发环境配置方案.md 安装统一开发工具。"
    }
}

function Get-VersionNumbers([string]$versionText) {
    $match = [regex]::Match($versionText, "(\d+)\.(\d+)\.(\d+)")
    if (-not $match.Success) {
        throw "无法解析版本号：$versionText"
    }
    return @([int]$match.Groups[1].Value, [int]$match.Groups[2].Value, [int]$match.Groups[3].Value)
}

Require-Command "python"
Require-Command "node"

$pythonVersion = (& python --version 2>&1).ToString()
$pythonNumbers = Get-VersionNumbers $pythonVersion
if ($pythonNumbers[0] -ne 3 -or $pythonNumbers[1] -ne 13 -or $pythonNumbers[2] -ne 15) {
    throw "Python 版本必须是 3.13.15，当前为：$pythonVersion"
}
Write-Host "[通过] $pythonVersion"

$nodeVersion = (& node --version 2>&1).ToString()
$nodeNumbers = Get-VersionNumbers $nodeVersion
if ($nodeNumbers[0] -ne 24 -or $nodeNumbers[1] -ne 21 -or $nodeNumbers[2] -ne 0) {
    throw "Node.js 版本必须是 24.21.0，当前为：$nodeVersion"
}
Write-Host "[通过] Node.js $nodeVersion"

Require-Command "git"
$gitVersion = (& git --version 2>&1).ToString()
$gitNumbers = Get-VersionNumbers $gitVersion
$gitAtLeastRequired = ($gitNumbers[0] -gt 2) -or
    ($gitNumbers[0] -eq 2 -and $gitNumbers[1] -gt 55) -or
    ($gitNumbers[0] -eq 2 -and $gitNumbers[1] -eq 55 -and $gitNumbers[2] -ge 0)
if (-not $gitAtLeastRequired) {
    throw "Git 版本必须是 2.55.0 或更高版本（Windows 安装包的构建号可不同），当前为：$gitVersion"
}
Write-Host "[通过] $gitVersion"

$envExample = Join-Path $projectRoot "infra\.env.example"
$envText = Get-Content -Raw $envExample
if ($envText -notmatch "(?m)^COMPOSE_PROJECT_NAME=ai-portal\s*$") {
    throw "infra/.env.example 必须统一使用 COMPOSE_PROJECT_NAME=ai-portal"
}
Write-Host "[通过] Compose 项目名为 ai-portal"

if (-not $SkipDocker) {
    Require-Command "docker"
    & docker compose version | Out-Host
    & docker compose --env-file infra/.env.example -f infra/docker-compose.yml config --quiet
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose 配置校验失败。"
    }
    Write-Host "[通过] Docker Compose 配置"
}

Write-Host "团队统一环境检查通过。"
