from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="API Gateway")

SERVICES = {
    "student": "http://localhost:8001"
}

async def forward(service, path, method, body=None):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = SERVICES[service] + path

    async with httpx.AsyncClient() as client:
        if method == "GET":
            res = await client.get(url)
        elif method == "POST":
            res = await client.post(url, json=body)
        elif method == "PUT":
            res = await client.put(url, json=body)
        elif method == "DELETE":
            res = await client.delete(url)
        else:
            raise HTTPException(status_code=405)

    return JSONResponse(content=res.json() if res.text else None, status_code=res.status_code)

@app.get("/")
def root():
    return {"message": "Gateway running"}

@app.get("/gateway/students")
async def get_students():
    return await forward("student", "/api/students", "GET")

@app.get("/gateway/students/{id}")
async def get_student(id: int):
    return await forward("student", f"/api/students/{id}", "GET")

@app.post("/gateway/students")
async def create_student(req: Request):
    body = await req.json()
    return await forward("student", "/api/students", "POST", body)

@app.put("/gateway/students/{id}")
async def update_student(id: int, req: Request):
    body = await req.json()
    return await forward("student", f"/api/students/{id}", "PUT", body)

@app.delete("/gateway/students/{id}")
async def delete_student(id: int):
    return await forward("student", f"/api/students/{id}", "DELETE")