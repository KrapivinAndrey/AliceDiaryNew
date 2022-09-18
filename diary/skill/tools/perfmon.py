from dataclasses import dataclass
from typing import Dict


class PerfMonitor:
    def __init__(self) -> None:
        self.measures: Dict[str, list] = {}
        self.measure_start: float = 0
        self.measure_stop: float = 0

    def save_measure(self, method: str, start: float, stop: float):
        delta = stop - start
        if self.measures.get(method) is None:
            if len(self.measures) == 0:
                self.measure_start = start
            self.measures[method] = []
        self.measures[method].append(
            Measure(method=method, start=start, stop=stop, delta=delta)
        )
        self.measure_stop = stop

    def print_report(self):
        report = []
        report_total = self.measure_stop - self.measure_start
        for method, measures in self.measures.items():
            method_total = 0
            for m in measures:
                method_total += m.delta
            report.append(f"method={method}; total={method_total}")
        report.insert(0, f"REPORT; total={report_total}")
        for r in report:
            print(r)


@dataclass(frozen=True)
class Measure:
    method: str
    start: float
    stop: float
    delta: float
