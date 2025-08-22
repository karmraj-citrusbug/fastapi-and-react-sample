import asyncio
import json
import logging
from typing import Any, Dict, Optional

from redis.asyncio import Redis as AsyncRedis

from config.settings import app_settings
from src.infrastructure.websockets.connection_manager import ConnectionManager
from src.schema.utils import WebsocketMessageTypesEnum

logger = logging.getLogger(__name__)


async def get_redis_connection():
    """Get a Redis connection for the current event loop."""
    return AsyncRedis(host=app_settings.REDIS_HOST, decode_responses=True)


async def redis_listener():
    redis_conn = await get_redis_connection()
    pubsub = redis_conn.pubsub()
    await pubsub.psubscribe("user_channel_*", "public_channel")

    connection_manager = ConnectionManager()

    try:
        while True:
            try:
                # Use a timeout to prevent blocking indefinitely
                message = await asyncio.wait_for(
                    pubsub.get_message(ignore_subscribe_messages=True), timeout=1.0
                )

                if not message:
                    await asyncio.sleep(0.1)  # Prevent CPU spinning
                    continue

                if message["type"] != "pmessage":
                    continue

                channel = message["channel"]
                try:
                    data = json.loads(message["data"])
                except json.JSONDecodeError as e:
                    logger.error("Invalid JSON on channel %s: %s", channel, str(e))
                    continue

                # Handle user-specific channels
                if channel.startswith("user_channel_"):
                    user_id = channel.rsplit("_", 1)[-1]
                    logger.debug("Sending to user_channel: user_id=%s", user_id)
                    await connection_manager.send_personal_message(
                        user_id=user_id, data=data
                    )

                # Handle public broadcast
                elif channel == "public_channel":
                    logger.debug("Broadcasting on public_channel")
                    await connection_manager.broadcast(data)

                else:
                    logger.warning("Unhandled Redis channel: %s", channel)

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.exception("Error processing Redis message: %s", str(e))
                await asyncio.sleep(1)  # Wait before retrying on error

    except Exception as e:
        logger.exception("Redis listener error: %s", str(e))
    finally:
        await pubsub.punsubscribe()
        await pubsub.close()
        await redis_conn.close()


async def publish_updates(
    data_type: WebsocketMessageTypesEnum,
    data: Dict[str, Any],
    user_id: Optional[str] = None,
):
    redis_conn = None
    try:
        redis_conn = await get_redis_connection()
        if user_id:
            await redis_conn.publish(
                f"user_channel_{user_id}", json.dumps({data_type: data})
            )
        else:
            await redis_conn.publish("public_channel", json.dumps({data_type: data}))
    except Exception as e:
        logger.exception("Error publishing Redis message: %s", str(e))
    finally:
        if redis_conn:
            await redis_conn.close()
