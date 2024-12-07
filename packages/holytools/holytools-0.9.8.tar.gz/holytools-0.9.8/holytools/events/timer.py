from datetime import datetime


class Timer:
    def __init__(self):
        self.start_time : datetime = datetime.now()

    def restart(self):
        self.start_time = datetime.now()

    def capture(self, verbose : bool = True) -> float:
        now = datetime.now()
        delta = now-self.start_time
        delta_sec = delta.total_seconds()
        if verbose:
            print(f'Time has been running for {delta_sec} seconds')
        return delta_sec

