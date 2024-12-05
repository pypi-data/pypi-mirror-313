from aiokafka import ConsumerRebalanceListener
import asyncio

from buz.kafka.infrastructure.kafka_python.rebalance_ready import RebalanceReady


class SimpleKafkaLockRebalancer(ConsumerRebalanceListener):
    __REBALANCING_INTERVAL_CHECK = 0.3

    def __init__(self, kafka_python_multithreaded_consumer: RebalanceReady):
        self.kafka_python_multithreaded_consumer = kafka_python_multithreaded_consumer

    async def on_partitions_revoked(self, revoked):
        while not self.kafka_python_multithreaded_consumer.is_ready_for_rebalancing():
            await asyncio.sleep(self.__REBALANCING_INTERVAL_CHECK)

    async def on_partitions_assigned(self, assigned):
        pass
