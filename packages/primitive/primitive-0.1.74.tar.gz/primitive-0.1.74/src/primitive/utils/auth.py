import sys

from loguru import logger

from ..graphql.sdk import create_session


def create_new_session(primitive):
    token = primitive.host_config.get("token")
    transport = primitive.host_config.get("transport")
    fingerprint = primitive.host_config.get("fingerprint")

    if not token or not transport:
        logger.enable("primitive")
        logger.error(
            "CLI is not configured. Run `primitive config` to add an auth token."
        )
        sys.exit(1)

    return create_session(
        host=primitive.host,
        token=token,
        transport=transport,
        fingerprint=fingerprint,
    )


def guard(func):
    def wrapper(self, *args, **kwargs):
        if self.primitive.session is None:
            self.primitive.session = create_new_session(self.primitive)

        return func(self, *args, **kwargs)

    return wrapper
