param(
    [string]$ToolchainPrefix = "arm-none-eabi",
    [string]$Configuration = "Release"
)

$ErrorActionPreference = "Stop"

$target = "c8t6_minimal"
$buildDir = Join-Path $PSScriptRoot "build"
$firmwareRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$cc = "$ToolchainPrefix-gcc"
$objcopy = "$ToolchainPrefix-objcopy"
$size = "$ToolchainPrefix-size"

foreach ($tool in @($cc, $objcopy, $size)) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "$tool not found. Install GNU Arm Embedded Toolchain or STM32CubeCLT and add it to PATH."
    }
}

New-Item -ItemType Directory -Force -Path $buildDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $buildDir "src") | Out-Null

$cpuFlags = @("-mcpu=cortex-m3", "-mthumb")
$cFlags = @()
$cFlags += $cpuFlags
$cFlags += @(
    "-std=c11",
    "-Os",
    "-Wall",
    "-Wextra",
    "-ffunction-sections",
    "-fdata-sections",
    "-fno-builtin",
    "-fno-unwind-tables",
    "-fno-asynchronous-unwind-tables",
    "-I$firmwareRoot"
)

$sources = @(
    "src/startup_stm32f103c8t6.c",
    "src/main.c"
)

$objects = @()
foreach ($source in $sources) {
    $sourcePath = Join-Path $PSScriptRoot $source
    $objectPath = Join-Path $buildDir ($source -replace "\.c$", ".o")
    New-Item -ItemType Directory -Force -Path (Split-Path $objectPath) | Out-Null
    & $cc @cFlags -c $sourcePath -o $objectPath
    $objects += $objectPath
}

$elf = Join-Path $buildDir "$target.elf"
$bin = Join-Path $buildDir "$target.bin"
$map = Join-Path $buildDir "$target.map"
$linker = Join-Path $PSScriptRoot "linker\stm32f103c8t6.ld"
$ldFlags = @()
$ldFlags += $cpuFlags
$ldFlags += @(
    "-nostdlib",
    "-Wl,--gc-sections",
    "-Wl,-Map=$map",
    "-T",
    $linker
)

& $cc @objects @ldFlags -o $elf
& $objcopy -O binary $elf $bin
& $size $elf

Write-Host "Built $elf"
Write-Host "Built $bin"
