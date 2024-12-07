# Instruction

If you start for the first time:
```powershell
pip install uv
```

Run:  
```powershell
python hello.py
```

Enable running script:  
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Start env:  
```powershell
.\.venv\Scripts\activate.ps1
```

Start jupyter lab:  
[uv-jupyter-reference]
```powershell
uv run --with jupyter jupyter lab
```

[uv-jupyter-reference]: https://docs.astral.sh/uv/guides/integration/jupyter/#using-jupyter-within-a-project