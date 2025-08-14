<#
  Fast tree generator controlled ONLY by .dirignore
  - FS mode: custom traversal with pruning (no AllDirectories), very fast on large repos
  - Git mode: same behavior as before (git ls-files) ※未追跡は出ません
  - Excludes:
      * Prefix lines like "apps/" or "services/backups" => exclude that subtree
      * Basename lines like "__pycache__"               => exclude any path whose segment equals the name
  - No wildcard support in .dirignore (* ? ignored)
  - Outputs (default to tools/ where this script lives):
      * dir-tree.txt (box-drawing tree)
      * dir-path.txt (path list; first line "<root>/", others are FULL paths prefixed with "<root>/";
                      root-level files are moved to the BOTTOM of dir-path)
#>

[CmdletBinding()]
param(
  # box-drawing tree filename (under OutDir)
  [string]$Out = "dir-tree.txt",

  # path list filename (under OutDir)
  [string]$OutPathName = "dir-path.txt",

  # output directory; default = this script's directory (tools/)
  [string]$OutDir = $null,

  # tree root; default = this script's directory (override with -Root . from repo root)
  [string]$Root = $null,

  [ValidateSet('FS','Git')]
  [string]$Source = 'FS',

  # use only .dirignore located at $Root
  [string]$TreeIgnoreFile = ".dirignore",

  [switch]$StdOut,
  [switch]$DebugEx
)

# ------------ resolve script location & defaults ------------
$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptDir  = if ($ScriptPath) { Split-Path -Parent $ScriptPath } else { (Get-Location).Path }

if ([string]::IsNullOrWhiteSpace($OutDir)) { $OutDir = $ScriptDir }
if (-not [System.IO.Path]::IsPathRooted($OutDir)) { $OutDir = Join-Path $ScriptDir $OutDir }

if ([string]::IsNullOrWhiteSpace($Root)) { $Root = $ScriptDir }

# ------------ helpers ------------
function Resolve-Root([string]$p) {
  try { (Resolve-Path -LiteralPath $p).Path } catch { Write-Error "Invalid Root: $p"; exit 1 }
}
$Root = Resolve-Root $Root
$rootUri = [Uri]((Join-Path $Root ".") + [IO.Path]::DirectorySeparatorChar)

function To-Rel([string]$absPath) {
  $u = [Uri]$absPath
  ($rootUri.MakeRelativeUri($u).ToString() -replace '\\','/').Trim('/')
}

# normalize helpers
function NormRel([string]$rel) { (($rel -replace '\\','/').Trim('/')) }
function Lower([string]$s) { if ($null -eq $s) { "" } else { $s.ToLowerInvariant() } }

# .dirignore loader (prefixes & basenames, lower-cased)
function Load-TreeIgnore([string]$root,[string]$fileName) {
  $f = Join-Path $root $fileName
  $prefixes = New-Object 'System.Collections.Generic.List[string]'
  $basenames = New-Object 'System.Collections.Generic.List[string]'
  if (Test-Path $f -PathType Leaf) {
    $lines = Get-Content -LiteralPath $f -Encoding UTF8
    foreach ($line in $lines) {
      $t = $line.Trim()
      if ($t -eq "" -or $t.StartsWith("#")) { continue }
      if ($t.Contains("*") -or $t.Contains("?")) { continue }  # no globs
      $t = NormRel $t
      if ($t -eq "." -or $t -eq "") { continue }
      if ($t.Contains("/")) { $prefixes.Add((Lower $t)) } else { $basenames.Add((Lower $t)) }
    }
  }
  # NOTE: No auto-hide for .git or node_modules (show them unless listed in .dirignore)

  # unique & sort (case-insensitive)
  $cmp = [System.StringComparer]::OrdinalIgnoreCase
  $pArr = $prefixes.ToArray()
  [Array]::Sort($pArr, $cmp)
  $pArr = $pArr | Select-Object -Unique
  $bArr = $basenames.ToArray()
  [Array]::Sort($bArr, $cmp)
  $bArr = $bArr | Select-Object -Unique

  if ($DebugEx) {
    Write-Host "[.dirignore] prefixes  =" ($pArr -join ", ")
    Write-Host "[.dirignore] basenames =" ($bArr -join ", ")
    Write-Host "[CFG] Root     =" $Root
    Write-Host "[CFG] OutDir   =" $OutDir
  }
  [PSCustomObject]@{ Prefixes=$pArr; Basenames=$bArr }
}

# prefix exclusion: relLower == p or relLower startswith "p/"
function ExByPrefix([string]$relLower, [string[]]$pArr) {
  foreach ($p in $pArr) {
    if ($relLower.Length -eq $p.Length) {
      if ($relLower.Equals($p, [StringComparison]::OrdinalIgnoreCase)) { return $true }
    } elseif ($relLower.Length -gt $p.Length) {
      if ($relLower.StartsWith($p, [StringComparison]::OrdinalIgnoreCase) -and $relLower[$p.Length] -eq '/') { return $true }
    }
  }
  return $false
}

# basename exclusion (segment equality anywhere) — directory-name or file-name
function ExByBasename([string]$relLower, [string]$nameLower, [string[]]$bArr) {
  foreach ($b in $bArr) { if ($nameLower.Equals($b, [StringComparison]::OrdinalIgnoreCase)) { return $true } }
  return $false
}

$ig = Load-TreeIgnore -root $Root -fileName $TreeIgnoreFile

# ------------ FS traversal with pruning (FAST) ------------
$rootName = (Split-Path -Leaf $Root)

# outputs
$treeLines = New-Object 'System.Collections.Generic.List[string]'
$treeLines.Add($rootName)
$pathLines = New-Object 'System.Collections.Generic.List[string]'
$pathLines.Add("$rootName/")

# collect root-level files to move them to the bottom of dir-path
$rootFilesFull = New-Object 'System.Collections.Generic.List[string]'

# case-insensitive .NET sort (fast)
$cmp = [System.StringComparer]::OrdinalIgnoreCase

# children fetcher with pruning
function Get-Children {
  param(
    [string]$absDir,         # absolute path of current directory
    [string]$relLower        # current directory's relative path (lowercase; "" at root)
  )
  $dirs = New-Object 'System.Collections.Generic.List[string]'
  $files = New-Object 'System.Collections.Generic.List[string]'

  try {
    foreach ($dAbs in [System.IO.Directory]::EnumerateDirectories($absDir)) {
      $name = Split-Path -Leaf $dAbs
      $nameLower = Lower $name
      $childRelLower = if ($relLower) { "$relLower/$nameLower" } else { $nameLower }
      if (ExByBasename $childRelLower $nameLower $ig.Basenames) { continue }
      if (ExByPrefix   $childRelLower $ig.Prefixes)             { continue }
      $dirs.Add($name)
    }
    foreach ($fAbs in [System.IO.Directory]::EnumerateFiles($absDir)) {
      $name = Split-Path -Leaf $fAbs
      $nameLower = Lower $name
      if (ExByBasename $nameLower $nameLower $ig.Basenames) { continue }
      $files.Add($name)
    }
  } catch {
    # access denied etc.: skip
  }

  $dArr = $dirs.ToArray();  [Array]::Sort($dArr, $cmp)
  $fArr = $files.ToArray(); [Array]::Sort($fArr, $cmp)
  return [PSCustomObject]@{ Dirs=$dArr; Files=$fArr }
}

# unified walk that writes both tree (dirs->files) and paths (files->dirs)
function Walk {
  param(
    [string]$absDir,
    [string]$relLower,      # "" at root
    [string]$treePrefix,    # visual prefix for box drawing
    [string]$pathPrefix     # logical prefix relative to root (no leading slash, e.g., "services/")
  )

  $children = Get-Children -absDir $absDir -relLower $relLower
  $dirs  = $children.Dirs
  $files = $children.Files

  # ---- PATHS: files first (but root-level files are deferred to bottom) ----
  if ($pathPrefix -eq "") {
    foreach ($fn in $files) { $rootFilesFull.Add("$($rootName)/$fn") }
  } else {
    foreach ($fn in $files) { $pathLines.Add("$($rootName)/$pathPrefix$fn") }
  }

  # ---- TREE: dirs then files; recurse only into dirs ----
  $combined = New-Object 'System.Collections.Generic.List[object]'
  foreach ($dn in $dirs)  { $combined.Add([PSCustomObject]@{ Name=$dn; IsDir=$true  }) }
  foreach ($fn in $files) { $combined.Add([PSCustomObject]@{ Name=$fn; IsDir=$false }) }

  $count = $combined.Count
  for ($i=0; $i -lt $count; $i++) {
    $item = $combined[$i]; $isLast = ($i -eq $count-1)
    $connector = if ($isLast) { [string]([char]0x2517) + [char]0x2500 + ' ' } else { [string]([char]0x2523) + [char]0x2500 + ' ' } # ┗─ / ┣─
    if ($item.IsDir) {
      $treeLines.Add("$treePrefix$connector$($item.Name)/")
      # PATHS: directory line before its children
      $pathLines.Add("$($rootName)/$pathPrefix$($item.Name)/")

      $childAbs = Join-Path $absDir $item.Name
      $childRelLower = if ($relLower) { "$relLower/$(Lower $item.Name)" } else { (Lower $item.Name) }
      $nextTreePrefix = if ($isLast) { "$treePrefix   " } else { "$treePrefix" + [string]([char]0x2503) + '  ' } # '   ' or '┃  '
      $nextPathPrefix = "$pathPrefix$($item.Name)/"
      Walk -absDir $childAbs -relLower $childRelLower -treePrefix $nextTreePrefix -pathPrefix $nextPathPrefix
    } else {
      $treeLines.Add("$treePrefix$connector$($item.Name)")
    }
  }
}

if ($Source -eq 'FS') {
  Walk -absDir $Root -relLower "" -treePrefix "" -pathPrefix ""
}
else {
  # ------------ Git mode (respects dir-path ordering) ------------
  $git = Get-Command git -ErrorAction SilentlyContinue
  if (-not $git) { Write-Error "Git not found."; exit 1 }
  $repoTop = (& git -C $Root rev-parse --show-toplevel 2>$null).Trim()
  if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($repoTop)) { Write-Error "Not a Git repo: $Root"; exit 1 }
  $uriRepo = [Uri]((Join-Path $repoTop ".") + [IO.Path]::DirectorySeparatorChar)
  $prefixRel = $uriRepo.MakeRelativeUri($rootUri).ToString().TrimEnd('/') -replace '\\','/'

  if ([string]::IsNullOrWhiteSpace($prefixRel)) { $raw = & git -C $repoTop ls-files -z -- . }
  else { $raw = & git -C $repoTop ls-files -z -- "$prefixRel" }
  if ($LASTEXITCODE -ne 0) { Write-Error "git ls-files failed."; exit 1 }

  $files = @()
  if ($null -ne $raw) { $files = ($raw -split "`0") | Where-Object { $_ } | ForEach-Object { $_ -replace '\\','/' } }

  # apply .dirignore to git file list (prefix/basename)
  $keep = New-Object 'System.Collections.Generic.List[string]'
  foreach ($f in $files) {
    $rel = NormRel $f
    $relLower = Lower $rel
    $nameLower = Lower ([IO.Path]::GetFileName($rel))
    if (ExByBasename $relLower $nameLower $ig.Basenames) { continue }
    if (ExByPrefix   $relLower $ig.Prefixes)             { continue }
    $keep.Add($rel)
  }

  # Build map dir -> files (sorted), and set of subdirs
  $treeLines.Clear(); $treeLines.Add($rootName)
  $pathLines.Clear(); $pathLines.Add("$rootName/")
  $rootFilesFull.Clear()

  $byDir = @{}
  foreach ($p in $keep) {
    $dir = if ($p.Contains('/')) { $p.Substring(0, $p.LastIndexOf('/')) } else { "" }
    $name = if ($dir -eq "") { $p } else { $p.Substring($dir.Length + 1) }
    if (-not $byDir.ContainsKey($dir)) { $byDir[$dir] = New-Object 'System.Collections.Generic.List[string]' }
    $byDir[$dir].Add($name)
  }

  function Write-Git {
    param([string]$dir, [string]$treePrefix, [string]$pathPrefix)

    # files in this dir (sorted)
    $filesHere = @()
    if ($byDir.ContainsKey($dir)) {
      $filesHere = $byDir[$dir].ToArray()
      [Array]::Sort($filesHere, [System.StringComparer]::OrdinalIgnoreCase)
    }

    # dirs here (derived from keys)
    $dirsHereSet = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($k in $byDir.Keys) {
      if ($dir -eq "") {
        if ($k -ne "" ) {
          if ($k.Contains('/')) { $dirsHereSet.Add($k.Substring(0, $k.IndexOf('/'))) } else { $dirsHereSet.Add($k) }
        }
      } else {
        if ($k.StartsWith("$dir/")) {
          $rest = $k.Substring($dir.Length + 1)
          if ($rest.Contains('/')) { $dirsHereSet.Add($rest.Substring(0, $rest.IndexOf('/'))) } else { $dirsHereSet.Add($rest) }
        }
      }
    }
    $dirsHere = $dirsHereSet.ToArray()
    [Array]::Sort($dirsHere, [System.StringComparer]::OrdinalIgnoreCase)

    # PATHS: files first (root-level files are deferred)
    if ($pathPrefix -eq "") {
      foreach ($f in $filesHere) { $rootFilesFull.Add("$($rootName)/$f") }
    } else {
      foreach ($f in $filesHere) { $pathLines.Add("$($rootName)/$pathPrefix$f") }
    }

    # TREE: dirs then files
    $combined = New-Object 'System.Collections.Generic.List[object]'
    foreach ($d in $dirsHere)  { $combined.Add([PSCustomObject]@{ Name=$d; IsDir=$true  }) }
    foreach ($f in $filesHere) { $combined.Add([PSCustomObject]@{ Name=$f; IsDir=$false }) }

    for ($i=0; $i -lt $combined.Count; $i++) {
      $item   = $combined[$i]; $isLast = ($i -eq $combined.Count-1)
      $conn   = if ($isLast) { [string]([char]0x2517) + [char]0x2500 + ' ' } else { [string]([char]0x2523) + [char]0x2500 + ' ' }
      if ($item.IsDir) {
        $treeLines.Add("$treePrefix$conn$($item.Name)/")
        $pathLines.Add("$($rootName)/$pathPrefix$($item.Name)/")
        $nextTree = if ($isLast) { "$treePrefix   " } else { "$treePrefix" + [string]([char]0x2503) + '  ' }
        $nextPath = "$pathPrefix$($item.Name)/"
        $nextDir  = if ($dir -eq "") { $item.Name } else { "$dir/$($item.Name)" }
        Write-Git -dir $nextDir -treePrefix $nextTree -pathPrefix $nextPath
      } else {
        $treeLines.Add("$treePrefix$conn$($item.Name)")
      }
    }
  }

  Write-Git -dir "" -treePrefix "" -pathPrefix ""
}

# ------------ write outputs (always log created/overwritten + size) ------------
if (-not (Test-Path -LiteralPath $OutDir -PathType Container)) {
  New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
}

# 1) box-drawing tree
$destTree   = Join-Path $OutDir $Out
$wasTree    = Test-Path -LiteralPath $destTree -PathType Leaf
$treeLines  | Out-File -FilePath $destTree -Encoding utf8 -Force
$treeBytes  = (Get-Item -LiteralPath $destTree).Length
Write-Host ("{0} Wrote tree (source={1}): {2} ({3} bytes)" -f ($(if($wasTree){'[Overwritten]'}else{'[Created]'}), $Source, $destTree, $treeBytes))
if ($StdOut) { $treeLines | ForEach-Object { $_ } }

# 2) path list
$destPaths  = Join-Path $OutDir $OutPathName
$wasPaths   = Test-Path -LiteralPath $destPaths -PathType Leaf
foreach ($rf in $rootFilesFull) { $pathLines.Add($rf) }
$pathLines  | Out-File -FilePath $destPaths -Encoding utf8 -Force
$pathsBytes = (Get-Item -LiteralPath $destPaths).Length
Write-Host ("{0} Wrote path list      : {1} ({2} bytes)" -f ($(if($wasPaths){'[Overwritten]'}else{'[Created]'}), $destPaths, $pathsBytes))
