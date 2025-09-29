# scripts/run_json_tiny.ps1
$ErrorActionPreference = "Stop"

# Always run from repo root
Set-Location -Path (Split-Path -Parent $PSScriptRoot)  # .. up from scripts/

# Ensure data/ exists
if (-not (Test-Path -Path "data")) { New-Item -ItemType Directory -Path "data" | Out-Null }

# Payload 1
$json1 = @'
{
  "bedrooms": 4, "bathrooms": 1, "sqft_living": 1680, "sqft_lot": 5043,
  "floors": 1.5, "waterfront": 0, "view": 0, "condition": 4, "grade": 6,
  "sqft_above": 1680, "sqft_basement": 0, "yr_built": 1911, "yr_renovated": 0,
  "zipcode": 98118, "lat": 47.5354, "long": -122.273,
  "sqft_living15": 1560, "sqft_lot15": 5765
}
'@
Set-Content -Encoding UTF8 -Path "data\tiny1.json" -Value $json1

# Payload 2
$json2 = @'
{
  "bedrooms": 3, "bathrooms": 2.5, "sqft_living": 2220, "sqft_lot": 6380,
  "floors": 1.5, "waterfront": 0, "view": 0, "condition": 4, "grade": 8,
  "sqft_above": 1660, "sqft_basement": 560, "yr_built": 1931, "yr_renovated": 0,
  "zipcode": 98115, "lat": 47.6974, "long": -122.313,
  "sqft_living15": 950, "sqft_lot15": 6380
}
'@
Set-Content -Encoding UTF8 -Path "data\tiny2.json" -Value $json2

# Call /v1/predict twice and aggregate responses
$o = @()
$o += Invoke-RestMethod -Uri "http://localhost:8080/v1/predict" -Method Post -ContentType "application/json" -Body (Get-Content -Raw "data\tiny1.json")
$o += Invoke-RestMethod -Uri "http://localhost:8080/v1/predict" -Method Post -ContentType "application/json" -Body (Get-Content -Raw "data\tiny2.json")

# Save one JSON array file
$outFile = "data\future_unseen_examples_scores_tiny.json"
$o | ConvertTo-Json | Set-Content -Encoding UTF8 $outFile

Write-Host "✅ Saved $outFile"
Get-Content $outFile
