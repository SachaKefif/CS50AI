[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string] $Project
)

$ErrorActionPreference = "Stop"

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]] $Command)

    & git @Command
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed: git $($Command -join ' ')"
    }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or is not available on PATH."
}

$repositoryRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$manifestPath = Join-Path $repositoryRoot "cs50-submissions.json"
$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
$projectProperty = $manifest.projects.PSObject.Properties[$Project]

if ($null -eq $projectProperty) {
    $available = ($manifest.projects.PSObject.Properties.Name | Sort-Object) -join ", "
    throw "Unknown project '$Project'. Available projects: $available"
}

$settings = $projectProperty.Value
$projectDirectory = [IO.Path]::GetFullPath((Join-Path $repositoryRoot $settings.path))

if (-not (Test-Path -LiteralPath $projectDirectory -PathType Container)) {
    throw "Project directory does not exist: $projectDirectory"
}

$temporaryBase = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
$temporaryName = "cs50-submit-$([guid]::NewGuid().ToString('N'))"
$temporaryDirectory = Join-Path $temporaryBase $temporaryName
New-Item -ItemType Directory -Path $temporaryDirectory | Out-Null

try {
    Invoke-Git -Command @("-C", $temporaryDirectory, "init", "--quiet", "--initial-branch=main")
    Invoke-Git -Command @("-C", $temporaryDirectory, "remote", "add", "origin", $manifest.repository)

    $remoteBranch = & git ls-remote --heads $manifest.repository $settings.branch
    if ($LASTEXITCODE -ne 0) {
        throw "Could not access $($manifest.repository). Run 'gh auth login' and 'gh auth setup-git' first."
    }

    if ($remoteBranch) {
        Invoke-Git -Command @("-C", $temporaryDirectory, "fetch", "--quiet", "--depth=1", "origin", $settings.branch)
        Invoke-Git -Command @("-C", $temporaryDirectory, "switch", "--quiet", "--create", $settings.branch, "FETCH_HEAD")
        Invoke-Git -Command @("-C", $temporaryDirectory, "rm", "-r", "--quiet", "--ignore-unmatch", "--", ".")
    }
    else {
        Invoke-Git -Command @("-C", $temporaryDirectory, "switch", "--quiet", "--orphan", $settings.branch)
    }

    foreach ($relativeFile in $settings.files) {
        $source = [IO.Path]::GetFullPath((Join-Path $projectDirectory $relativeFile))
        $projectPrefix = $projectDirectory.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar

        if (-not $source.StartsWith($projectPrefix, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Submission path escapes the project directory: $relativeFile"
        }
        if (-not (Test-Path -LiteralPath $source)) {
            throw "Required submission file does not exist: $source"
        }

        $destination = Join-Path $temporaryDirectory $relativeFile
        $destinationParent = Split-Path -Parent $destination
        if (-not (Test-Path -LiteralPath $destinationParent)) {
            New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
        }
        Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force
    }

    Invoke-Git -Command @("-C", $temporaryDirectory, "add", "--all")
    & git -C $temporaryDirectory diff --cached --quiet

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Nothing to submit: '$Project' is unchanged."
        return
    }
    if ($LASTEXITCODE -ne 1) {
        throw "Could not inspect the staged submission."
    }

    Invoke-Git -Command @("-C", $temporaryDirectory, "commit", "--quiet", "-m", "Submit $Project")
    Invoke-Git -Command @("-C", $temporaryDirectory, "push", "origin", "HEAD:refs/heads/$($settings.branch)")

    Write-Host "Submitted '$Project' successfully."
    Write-Host "Branch: $($settings.branch)"
    Write-Host "Progress: https://cs50.me/cs50ai"
}
finally {
    $resolvedTemporaryDirectory = [IO.Path]::GetFullPath($temporaryDirectory)
    $isSafeTemporaryPath =
        $resolvedTemporaryDirectory.StartsWith($temporaryBase, [StringComparison]::OrdinalIgnoreCase) -and
        (Split-Path -Leaf $resolvedTemporaryDirectory) -like "cs50-submit-*"

    if ($isSafeTemporaryPath -and (Test-Path -LiteralPath $resolvedTemporaryDirectory)) {
        Remove-Item -LiteralPath $resolvedTemporaryDirectory -Recurse -Force
    }
}
