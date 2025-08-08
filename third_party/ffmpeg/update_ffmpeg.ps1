param(
  [ValidateSet("gpl","lgpl")]
  [string]$License = "gpl"   # gpl / lgpl を選択
)

$ErrorActionPreference = "Stop"
try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch {}

# ---- Paths -----------------------------------------------------------
$Here    = Split-Path -Parent $PSCommandPath
$ArchDir = Join-Path $Here "win-x64"
$Current = Join-Path $ArchDir "current"
$Tmp     = Join-Path $ArchDir "_tmp"

# ダウンロードする “latest” 資産名を明示（チェックサム照合のためファイル名一致で保存）
$AssetName = "ffmpeg-master-latest-win64-$License-shared.zip"
$ZipPath   = Join-Path $ArchDir $AssetName
$ShaPath   = Join-Path $ArchDir "checksums.sha256"

# ---- Ensure folders --------------------------------------------------
New-Item -ItemType Directory -Force -Path $ArchDir | Out-Null
Import-Module BitsTransfer

# ---- Clean workspace every run (no history) -------------------------
Remove-Item $ZipPath -Force -ErrorAction SilentlyContinue
Remove-Item $ShaPath -Force -ErrorAction SilentlyContinue
Remove-Item $Tmp -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $Tmp | Out-Null

# ---- URLs for BtbN "latest" -----------------------------------------
# 固定URL: .../releases/latest/download/<asset>
$BaseLatest = "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download"
$ZipUrl = "$BaseLatest/$AssetName"
$ShaUrl = "$BaseLatest/checksums.sha256"   # 同じリリースのチェックサム一覧

try {
  # ---- Download (BITS: stable for large files) ----------------------
  Start-BitsTransfer -Source $ZipUrl -Destination $ZipPath
  Start-BitsTransfer -Source $ShaUrl -Destination $ShaPath

  # ---- Verify checksum (by exact asset name) ------------------------
  $actual   = (Get-FileHash $ZipPath -Algorithm SHA256).Hash.ToLower()
  $lines    = Get-Content -LiteralPath $ShaPath
  $pattern  = '^(?<hash>[0-9a-fA-F]{64})\s+(\*|\s)?' + [regex]::Escape($AssetName) + '$'
  $match    = $lines | ForEach-Object { [regex]::Match($_, $pattern) } | Where-Object { $_.Success } | Select-Object -First 1
  if ($match) {
    $expected = $match.Groups['hash'].Value.ToLower()
    if ($actual -ne $expected) { throw "SHA256 mismatch. expected=$expected actual=$actual" }
  } else {
    Write-Warning ("checksums.sha256 has no entry for {0}; skipping verification." -f $AssetName)
  }

  # ---- Extract & place into current (no version directories) --------
  Expand-Archive -LiteralPath $ZipPath -DestinationPath $Tmp -Force

  # 展開フォルダ（1つ）を検出
  $Extracted = Get-ChildItem -LiteralPath $Tmp -Directory | Select-Object -First 1
  if (-not $Extracted) { throw ("Extracted folder not found under {0}" -f $Tmp) }

  # 使いやすさのため ffmpeg.exe / ffprobe.exe をルートにも複製（任意）
  $Bin = Join-Path $Extracted.FullName "bin"
  if (Test-Path $Bin) {
    Copy-Item (Join-Path $Bin "ffmpeg.exe")  $Extracted.FullName -Force
    Copy-Item (Join-Path $Bin "ffprobe.exe") $Extracted.FullName -Force
  }

  # current を完全入れ替え（過去バージョンは保持しない）
  if (Test-Path $Current) { Remove-Item $Current -Recurse -Force }
  Move-Item -LiteralPath $Extracted.FullName -Destination $Current

  Write-Host ("FFmpeg current updated to BtbN latest ({0}-shared, win64)" -f $License)
}
finally {
  # ---- Cleanup -------------------------------------------------------
  Remove-Item $ZipPath -Force -ErrorAction SilentlyContinue
  Remove-Item $ShaPath -Force -ErrorAction SilentlyContinue
  Remove-Item $Tmp -Recurse -Force -ErrorAction SilentlyContinue
}
