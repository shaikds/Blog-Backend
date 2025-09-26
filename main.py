import time
from fastapi import FastAPI, Request
from app.routers import posts # Import the router module

app = FastAPI(
    title="Modular Blog API",
    description="A professional, modular API using FastAPI and Pydantic.",
    version="1.0.0"
)

# Middleware for process time logging
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    total_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(total_time)
    print(f"Request to {request.url.path} took {total_time:.4f} seconds")
    return response

# Include the posts router
app.include_router(posts.router)

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to the Modular Blog API! Check out /docs for endpoints."}
