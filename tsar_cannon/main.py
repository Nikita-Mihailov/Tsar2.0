from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests import Request
from back.tests import views



app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Received request: {request.method} {request.url}")
    print(f"Headers: {request.headers}")
    print(f"Body: {await request.body()}")
    response = await call_next(request)
    return response


# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# from .back.tests import views
app.include_router(views.router)


@app.get("/")
def read_root():
    return {"message": "Warehouse Management System API"}