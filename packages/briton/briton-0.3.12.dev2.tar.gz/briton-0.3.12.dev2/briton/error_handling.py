import logging
from contextlib import contextmanager

import grpc
from fastapi import HTTPException

logger = logging.getLogger(__name__)


@contextmanager
def grpc_error_handling():
    try:
        yield
    except grpc.RpcError as rpc_error:
        # Handle gRPC errors here
        status_code = rpc_error.code()
        details = rpc_error.details()
        logger.warning(f"gRPC error: {status_code}, {details}")
        if (
            status_code == grpc.StatusCode.INVALID_ARGUMENT
            or status_code == grpc.StatusCode.UNIMPLEMENTED
        ):
            raise HTTPException(status_code=400, detail=details)

        # If the error is another type of gRPC error, we should return a 500
        if status_code == grpc.StatusCode.UNAVAILABLE:
            logger.warning("Server is unavailable, please try again later.")
        elif status_code == grpc.StatusCode.INTERNAL:
            logger.warning("Internal server error occurred.")
        else:
            logger.warning(f"An unexpected error occurred: {status_code}")
        raise HTTPException(status_code=500, detail="Briton error during inference")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"An error has occurred: {ex}")
