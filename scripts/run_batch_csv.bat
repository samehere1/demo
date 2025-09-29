@echo off
setlocal
REM Run from repo root no matter where this .bat is called
cd /d %~dp0
cd ..

REM Ensure data folder exists
if not exist data mkdir data

echo [1/1] Calling batch prediction endpoint and saving CSV...
curl --fail -o data\future_unseen_examples_scores.csv ^
  -X POST "http://localhost:8080/v1/predict_batch?output=csv" ^
  -H "accept: text/csv" ^
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

echo.
echo ✅ Done!
echo    CSV predictions saved: data\future_unseen_examples_scores.csv
echo.
echo Press any key to close...
pause >nul
endlocal
