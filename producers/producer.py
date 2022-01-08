import argparse
import datetime
import random
import uuid
from concurrent import futures
from dataclasses import dataclass
from time import sleep

SENSOR_IDS = (
    "e970d2fb-d92e-488e-a9bf-8442abd51c9e",
    "e6f9687e-2926-463b-9886-8f990ab369d0",
    "7fb0f204-7e36-4047-b328-b24b8f9addb5",
    "2c400e84-8b68-4ad4-bd23-49304d9b8bd5",
)


@dataclass
class Measurement:
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
            epoch=int(datetime.datetime.now().timestamp()),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "temperature": self.temperature,
            "epoch": self.epoch,
        }


def produce_random_event(max_delay: int) -> None:
    while True:
        event = Measurement.create_random_measurement()
        print(f"Sending {event} event.")
        sleep(random.randint(1, max_delay))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n-workers",
        type=int,
        default=1,
        help=("Amount of workers that will be spawn to produce random events."),
    )
    parser.add_argument(
        "-max-delay",
        type=int,
        default=5,
        help=(
            "Maximum wait time (in seconds) before new event is produced by worker. "
            "Randomly picked from range 1 to -max-delay arg value."
        ),
    )

    args = parser.parse_args()

    fn_args = (args.max_delay for _ in range(args.n_workers))

    print(
        f"Starting {args.n_workers} worker(s) with {args.max_delay} seconds of max delay between producing new event."
    )

    with futures.ThreadPoolExecutor(max_workers=args.n_workers) as executor:
        executor.map(produce_random_event, fn_args)
