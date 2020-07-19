from typing import NamedTuple
from queue import PriorityQueue
from random import randint


class Event(NamedTuple):
    time: int
    proc: int
    action: str


def taxi_process(id_, trips, start_time=0):
    time = yield Event(start_time, id_, 'leave garage')
    for _ in range(trips):
        time = yield Event(time, id_, 'pick up passenger')
        time = yield Event(time, id_, 'drop off passenger')

    yield Event(time, id_, 'going home')


DEFAULT_INTERVAL = 5
TAXI_NUM = 3


class Simulator:
    def __init__(self, procs_map) -> None:
        self.events = PriorityQueue()
        self.procs = dict(procs_map)

    def run(self, end_time: int):
        for _, proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)

        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print('=== end of events ===')
                break

            current_event = self.events.get()
            sim_time, proc_id, _ = current_event
            print(f'taxt:{proc_id} {"    " * proc_id}{current_event}')
            active_proc = self.procs[proc_id]
            next_time = sim_time + randint(1, 11)
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            print(self.events.qsize())


def main():
    taxis = {i: taxi_process(i, (i + 1) * 2, i * DEFAULT_INTERVAL)
             for i in range(TAXI_NUM)}

    sim = Simulator(taxis)
    sim.run(50)


if __name__ == "__main__":
    main()
