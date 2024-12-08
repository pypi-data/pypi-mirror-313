# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import multiprocessing
import os
from pathlib import Path

import datalayer_iam
import uvicorn
from uvicorn.config import LOGGING_CONFIG

ROOT_FOLDER = (
    Path(os.curdir).joinpath("data").resolve()
    # Trick to know if the package was processed by Nuitka or not.
    if hasattr(datalayer_iam, "__compiled__")
    else Path(__file__).resolve().parent
)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    logging_config = ROOT_FOLDER / "logging_config.json"

    uvicorn.run(
        "datalayer_iam.main:app",
        host="0.0.0.0",
        port=9700,
        workers=1,
        reload=False,
        log_level="info",
        log_config=str(logging_config) if logging_config.exists() else LOGGING_CONFIG,
    )
