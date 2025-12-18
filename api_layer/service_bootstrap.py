from fastapi import FastAPI
from api_layer.health_probe import router as health_router
from api_layer.recommend_router import router as recommend_router
from semantic_index.vector_forge import load_index
from semantic_index.embedding_gateway import get_model

def create_app():
    app = FastAPI(title="SHL Assessment Recommender")

    # preload heavy resources
    load_index()
    get_model()

    app.include_router(health_router)
    app.include_router(recommend_router)
    return app

app = create_app()
