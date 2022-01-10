import datetime
import json
import random
import uuid
from dataclasses import dataclass

SENSOR_IDS = (
    "e970d2fb-d92e-488e-a9bf-8442abd51c9e",
    "e6f9687e-2926-463b-9886-8f990ab369d0",
    "7fb0f204-7e36-4047-b328-b24b8f9addb5",
    "2c400e84-8b68-4ad4-bd23-49304d9b8bd5",
)


@dataclass
class TemperatureMeasurement:
    id: str
    sensor_id: str
    temperature: float
    epoch: int

    @classmethod
    def create_random_measurement(cls):
        return cls(
            id=str(uuid.uuid4()),
            sensor_id=random.choice(SENSOR_IDS),
            temperature=random.randint(10, 35) + round(random.random(), 2),
            epoch=int(datetime.datetime.utcnow().timestamp()),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "temperature": self.temperature,
            "epoch": self.epoch,
        }

    def to_json_string(self):
        return json.dumps(self.to_dict())
