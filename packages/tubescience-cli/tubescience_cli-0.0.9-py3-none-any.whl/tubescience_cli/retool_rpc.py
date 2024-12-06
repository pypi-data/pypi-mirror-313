import asyncio
from retoolrpc import RetoolRPC, RetoolRPCConfig

from ._settings import settings


rpc_config = RetoolRPCConfig(
        api_token=settings.retool_rpc.token.get_secret_value(),
        host=settings.retool_rpc.host,
        resource_id=settings.retool_rpc.resource_id,
        environment_name=settings.retool_rpc.environment_name,
        polling_interval_ms=settings.retool_rpc.polling_interval_ms,  # optional version number for functions schemas
        log_level=settings.retool_rpc.log_level,  # use 'debug' for more verbose logging
    )

ts_retool_rpc = RetoolRPC(rpc_config)


def helloWorld(args, context):
    return f"Hello {args['name']}"


ts_retool_rpc.register(
    {
        "name": "helloWorld",
        "arguments": {
            "name": {
                "type": "string",
                "description": "Your name",
                "required": True,
                "array": False,
            },
        },
        "implementation": helloWorld,
        "permissions": None,
    }
)

async def start_rpc():
    await ts_retool_rpc.listen()
