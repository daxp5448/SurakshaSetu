$python = "C:\Users\daksh\AppData\Local\Programs\Python\Python314\python.exe"
if (-not (Test-Path $python)) {
  throw "Python runtime not found at $python"
}

Set-Location "$PSScriptRoot"
& $python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
