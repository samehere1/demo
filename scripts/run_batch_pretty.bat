@echo off
setlocal
REM Run from repo root no matter where this .bat is called
cd /d %~dp0
cd ..

REM Ensure data folder exists
if not exist data mkdir data

echo [1/2] Calling batch prediction endpoint and saving RAW JSON...
curl --fail -o data\future_unseen_examples_scores.json ^
  -X POST "http://localhost:8080/v1/predict_batch?output=json" ^
  -H "accept: application/json" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@data\future_unseen_examples.csv;type=text/csv"

IF ERRORLEVEL 1 (
  echo.
  echo ❌ Batch prediction failed. Check that the API is running and the CSV exists at data\future_unseen_examples.csv
  echo.
  echo Press any key to close...
  pause >nul
  endlocal
  exit /b 1
)

echo [2/2] Creating PRETTY-PRINTED JSON copy...
powershell -NoLogo -NoProfile -Command "Get-Content data\future_unseen_examples_scores.json | ConvertFrom-Json | ConvertTo-Json -Depth 5 | Set-Content data\future_unseen_examples_scores_pretty.json"

IF ERRORLEVEL 1 (
  echo.
  echo ⚠️  Pretty-print step encountered an issue. RAW output is still available at:
  echo     data\future_unseen_examples_scores.json
  echo.
  echo Press any key to close...
  pause >nul
  endlocal
  exit /b 1
)

echo.
echo ✅ Done!
echo    RAW   : data\future_unseen_examples_scores.json
echo    PRETTY: data\future_unseen_examples_scores_pretty.json
echo.
echo (Tip) Open the pretty file in VS Code for a nice view:
echo       code data\future_unseen_examples_scores_pretty.json
echo.
echo Press any key to close...
pause >nul
endlocal
