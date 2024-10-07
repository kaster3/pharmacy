import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fast_depends import inject, Depends
from fastapi.responses import ORJSONResponse

from core.settings import get_settings, Settings


@inject
@asynccontextmanager
async def lifespan(app: FastAPI, settings: Settings = Depends(get_settings)):
    logging.basicConfig(
        level=logging.INFO,
        format=settings.log.format,
    )
    logging.info("Application starts successfully!")
    yield


application = FastAPI(
    default_response_class=ORJSONResponse, 
    lifespan=lifespan
)


@inject
def main(settings: Settings = Depends(get_settings)) -> None:
    uvicorn.run(
        app=settings.conf.app,
        host=settings.conf.host,
        port=settings.conf.port,
        workers=settings.conf.workers,
        reload=settings.conf.reload,
    )


if __name__ == "__main__":
    main()



