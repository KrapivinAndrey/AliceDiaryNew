from dataclasses import dataclass


class PerfMonitor:
    def __init__(self) -> None:
        self.measures = {}

    def save_measure(self, method: str, start: float, stop: float):
        delta = stop - start
        if self.measures.get(method) is None:
            self.measures[method] = []
        self.measures[method].append(
            Measure(method=method, start=start, stop=stop, delta=delta)
        )

    def print_report(self):
        print(f"===PERF=REPORT========")
        for method, measures in self.measures.items():
            total_delta = 0
            for m in measures:
                total_delta += m.delta
            print(f"method={method}; total={total_delta}")


@dataclass(frozen=True)
class Measure:
    method: str
    start: float
    stop: float
    delta: float
