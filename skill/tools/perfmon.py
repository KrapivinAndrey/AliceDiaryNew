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
        report = []
        report_total = 0
        for method, measures in self.measures.items():
            method_total = 0
            for m in measures:
                method_total += m.delta
            report_total += method_total
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
