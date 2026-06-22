param(
    [string]$RepositoryRoot = (Get-Location).Path,
    [string]$Config = "deucarian-package.json",
    [switch]$All,
    [string]$AuditRoot,
    [switch]$Json,
    [switch]$Ci,
    [switch]$CheckRemoteUrls
)

$ErrorActionPreference = "Stop"

$registryRoot = Split-Path -Parent $PSScriptRoot
$validator = Join-Path $PSScriptRoot "deucarian_package_validator.py"

$arguments = @(
    $validator,
    "--registry-root", $registryRoot
)

if ($All) {
    $arguments += "--all"
    if (-not $AuditRoot) {
        throw "AuditRoot is required when -All is specified."
    }
    $arguments += @("--audit-root", $AuditRoot)
} else {
    $arguments += @(
        "--repository-root", $RepositoryRoot,
        "--config", (Join-Path $RepositoryRoot $Config)
    )
}

if ($Json) {
    $arguments += "--json"
}

if ($Ci) {
    $arguments += "--ci"
}

if ($CheckRemoteUrls) {
    $arguments += "--check-remote-urls"
}

python @arguments
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
