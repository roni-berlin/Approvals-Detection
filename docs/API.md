## API Run Command
```
uvicorn api.main:app --host 0.0.0.0 --port 8080 --env-file .env
```

## Usage Example
```
curl -X POST "http://localhost:8080/ERC20/get_approvals" -H "accept: application/json" -H "Content-Type: application/json" -d "[\"0x005e20fCf757B55D6E27dEA9BA4f90C0B03ef852\"]"
```