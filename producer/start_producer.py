import argparse
import queue
import random
from concurrent import futures
from time import sleep

import config
import requests
from colorama import Fore
from models import TemperatureMeasurement


def produce_random_event(args) -> None:
    counter_queue, error_queue, max_delay = args
    event = TemperatureMeasurement.create_random_measurement()
    response = requests.post(
        config.API_URL,
        event.to_json_string(),
        headers={"x-api-key": config.API_KEY},
    )

    if response.status_code != 200:
        error_queue.put(1)

    counter_queue.put(1)
    sleep(random.randint(1, max_delay))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n-events", type=int, default=200, help="Amount of events to be produced."
    )
    parser.add_argument(
        "-n-workers",
        type=int,
        default=1,
        help="Amount of workers that will be spawn to produce random events.",
    )
    parser.add_argument(
        "-max-delay",
        type=int,
        default=5,
        help=(
            "Maximum interval (in seconds) before worker produces new event. "
            "Randomly picked from range 1 to -max-delay input argument value."
        ),
    )

    app_args = parser.parse_args()
    q = queue.Queue()
    err_q = queue.Queue()

    fn_args = ((q, err_q, app_args.max_delay) for _ in range(app_args.n_events))

    print("*" * 20)
    print(
        f"{Fore.YELLOW}Starting {app_args.n_workers} worker(s) with {app_args.max_delay} "
        "seconds of max delay between producing new event."
    )
    print("")

    with futures.ThreadPoolExecutor(max_workers=app_args.n_workers) as executor:
        executor.map(produce_random_event, fn_args)

        while q.qsize() < app_args.n_events:
            print(
                f"{Fore.CYAN}Produced events count: {Fore.GREEN}{q.qsize()} {Fore.CYAN}| "
                f"{Fore.CYAN}Errors: {Fore.RED}{err_q.qsize()}",
            )
            sleep(1)

    print()
    print(f"{Fore.YELLOW}Finished producing {app_args.n_events} events. Quitting!")
    print()
