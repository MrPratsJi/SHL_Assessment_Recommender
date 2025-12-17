from fastapi import FastAPI
from api_layer.health_probe import router as health_router
from api_layer.recommend_router import router as recommend_router

def create_app():
    app = FastAPI(title="SHL Assessment Recommender")
    app.include_router(health_router)
    app.include_router(recommend_router)
    return app

app = create_app()
