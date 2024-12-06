import os
import sys

import uvicorn


def run():
    print(f"sys.path: {sys.path}    os.getcwd(): {os.getcwd()}")
    try:
        print("attempting imports ...")
        from ambient_edge_server.app import app

        print(f"app: {app}")
        from ambient_client_common.utils import logger

        print(f"logger: {logger}")

        logger.debug("running server ...")
        logger.debug("running app: {} ...", app)
        uvicorn.run(app, host="0.0.0.0", port=7417)
    except Exception as e:
        print("error running server: ", e)


if __name__ == "__main__":
    run()
