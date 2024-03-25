import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import drugs, substancesAndNames, updates
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get('/')
async def root():
    return {"message": "Verr Med - Official API"}
#
#
# def startup():
#     print(f"Connected to verrmed")
#
#
# def shutdown():
#     print("Closed")
#
#
# app.add_event_handler("startup", func=startup)
# app.add_event_handler("shutdown", func=shutdown)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(substancesAndNames.router, prefix="/api/substAtivas", tags=["substAtivas"])

app.include_router(substancesAndNames.router, prefix="/api/substInativas", tags=["substInativas"])

app.include_router(substancesAndNames.router, prefix="/api/nomesComerciais", tags=["nomesComerciais"])

app.include_router(drugs.router, prefix="/api/medicamentos", tags=["medicamentos"])

app.include_router(updates.router, prefix="/api/updates", tags=["updates"])


if __name__ == "__main__":
    uvicorn.run(app)
