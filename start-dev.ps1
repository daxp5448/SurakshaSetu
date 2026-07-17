$root = $PSScriptRoot
$python = "C:\Users\daksh\AppData\Local\Programs\Python\Python314\python.exe"

if (-not (Test-Path $python)) {
  throw "Python runtime not found at $python"
}

Start-Process -FilePath $python -ArgumentList "-m","uvicorn","app.main:app","--app-dir","backend","--host","127.0.0.1","--port","8000","--reload" -WorkingDirectory $root
Start-Process -FilePath "npm.cmd" -ArgumentList "run","dev" -WorkingDirectory "$root\frontend"

Write-Host "Backend:  http://127.0.0.1:8000"
Write-Host "Frontend: http://127.0.0.1:5174"
