import json
from typing import Optional

from pydantic import BaseModel, Field
from pymediasoup.emitter import EnhancedEventEmitter
from pymediasoup.transport import DataConsumer, DataProducer

from .log import base_logger

logger = base_logger.getChild("Bot")


class BotOptions(BaseModel):
    dataConsumer: DataConsumer
    dataProducer: Optional[DataProducer]

    class Config:
        arbitrary_types_allowed = True


class VolatileDataMessage(BaseModel):
    from_peer_id: str = Field(
        description="Peer Id of the sender",
    )
    payload: str
    label: Optional[str]
    to: str


class Bot(EnhancedEventEmitter):
    def __init__(self, options: BotOptions):
        super().__init__()

        self.bot_data_consumer = options.dataConsumer
        self.bot_data_producer = options.dataProducer

        self.__register_bot_data_consumer_event(data_consumer=self.bot_data_consumer)

        if self.bot_data_producer:
            self.__register_bot_data_producer_event(
                data_producer=self.bot_data_producer
            )

    def __register_bot_data_consumer_event(self, data_consumer: DataConsumer):
        logger.info("Registering bot data consumer events")

        def on_message_callback(message: str):
            jsonParsed = json.loads(message)

            if jsonParsed.get("label") == "lastN":
                self.emit("active_speakers_change", jsonParsed.get("payload"))
                return

            logger.info(f"Received message: {message}")
            self.emit("received_volatile_data", jsonParsed)

        data_consumer.on("message", on_message_callback)

        data_consumer.on("close", lambda: logger.info("Data consumer closed"))

        data_consumer.on("error", lambda: logger.error("Data consumer error"))

        data_consumer.on("open", lambda: logger.info("Data consumer open"))

    def __register_bot_data_producer_event(self, data_producer: DataProducer):
        logger.info("Registering bot data producer events")

        data_producer.on("close", lambda: logger.info("Data producer closed"))

        data_producer.on("error", lambda: logger.error("Data producer error"))

        data_producer.on("open", lambda: logger.info("Data producer opened"))

        data_producer.on(
            "bufferedamountlow",
            lambda: logger.info("Data producer buffered amount low"),
        )

    async def send_data(self, message: VolatileDataMessage) -> bool:
        try:
            if self.bot_data_producer is None:
                logger.error("Data producer not available")
                return False

            if self.bot_data_producer.readyState != "open":
                logger.error("Data producer not open")
                return False

            payload = {
                "from": message.from_peer_id,
                "payload": message.payload,
                "label": message.label if message.label else None,
                "to": message.to,
            }

            json_payload = json.dumps(payload)

            logger.info(f"Sending message: {json_payload}")
            self.bot_data_producer.send(json_payload)

            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    async def close(self):
        try:
            await self.bot_data_consumer.close()
            if self.bot_data_producer:
                await self.bot_data_producer.close()
        except Exception as e:
            logger.error(f"Error closing bot: {e}")
