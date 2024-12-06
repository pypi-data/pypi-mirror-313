import datetime
import pathlib

from fastapi import FastAPI

from ambient_client_common.utils import logger
from ambient_edge_server import config
from ambient_edge_server.routers import (
    auth,
    crud,
    daemon,
    health,
    ping,
    plugins,
    ports,
    software,
)
from ambient_edge_server.services.service_manager import svc_manager

app = FastAPI()
logger.debug("Initialized FastAPI app")


async def startup():
    logger.info("Starting up ...")
    # initialize services
    try:
        await svc_manager.init()
        logger.info("Services initialized.")

    except Exception as e:
        logger.warning("Failed to initialize services: {}", e)

    # ensure asset availabilitry
    try:
        package_location = pathlib.Path(__file__).parent
        logger.debug("app.startup() - __file__: {}", __file__)
        logger.debug("app.startup() - package location: {}", package_location)
        jinja_template_location = (
            package_location / config.settings.service_template_location
        )
        if not jinja_template_location.exists():
            logger.warning("Jinja template file not found: {}", jinja_template_location)
        word_art_path = package_location / config.settings.word_art_path
        if not word_art_path.exists():
            logger.warning("Word art file not found: {}", word_art_path)
            return
        logger.debug("Word Art path: {}", word_art_path)
        logger.info("\n{}\n", open(word_art_path.absolute()).read())
        logger.info(
            "Started at: {}\t\t\tVersion:{}",
            datetime.datetime.now(),
            config.settings.version,
        )
    except Exception as e:
        logger.error("Failed to load assets: {}", e)


app.add_event_handler("startup", startup)

routers = [ping, ports, auth, daemon, crud, health, plugins, software]

for router in routers:
    app.include_router(router.router)
