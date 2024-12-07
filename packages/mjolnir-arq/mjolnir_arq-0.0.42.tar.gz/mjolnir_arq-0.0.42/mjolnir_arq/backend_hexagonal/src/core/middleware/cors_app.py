# middleware.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

class CorsAppConfigurator:
    @staticmethod
    def setup_cors(app: FastAPI):
        origins = ['*']
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
