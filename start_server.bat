@echo off
echo ========================================
echo Fairfax County Property Search API
echo ========================================
echo.
echo Starting server on http://localhost:8001
echo Interactive docs: http://localhost:8001/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m uvicorn api:app --reload --port 8001

pause
