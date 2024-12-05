import time
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets._footer import Footer
from textual_pyfiglet import FigletWidget


class TimeDisplay(FigletWidget):
    INIT_TIME: float = 0.0
    MAX_TIME: float = 35_999.9
    DECIMAL_PLACES: int = 1

    time: reactive[float] = reactive(INIT_TIME)

    def on_mount(self) -> None:
        self.start_time: float = 0.0
        self.total_time: float = 0.0

        self.update_timer = self.set_interval(
            1 / (10**self.DECIMAL_PLACES + 10), self.update_time, pause=True
        )

    def update_time(self) -> None:
        self.time = self.total_time + (time.perf_counter() - self.start_time)

    def _get_h_m_s(self, time: float) -> tuple[float, float, float]:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)

        return hours, minutes, seconds

    def format_time(self, time: float) -> str:
        hours, minutes, seconds = self._get_h_m_s(time)

        return f"{hours:.0f}:{minutes:02.0f}:{seconds:0{self.DECIMAL_PLACES + 3}.{self.DECIMAL_PLACES}f}"

    def watch_time(self, time: float) -> None:
        if time > self.MAX_TIME:
            self.stop()
        else:
            self.update(self.format_time(time))

    def start(self) -> None:
        if self.time < self.MAX_TIME:
            self.start_time = time.perf_counter()
            self.update_timer.resume()

    def stop(self) -> None:
        if self.time < self.MAX_TIME:
            self.update_timer.pause()
            self.total_time += time.perf_counter() - self.start_time
            self.time = self.total_time

    def reset(self) -> None:
        self.update_timer.pause()
        self.time = self.INIT_TIME
        self.total_time = self.INIT_TIME


class StopwatchScreen(Screen[None]):
    BINDINGS = [
        Binding("escape", "reset_time", "Reset"),
        Binding("space", "operate_timer", "Start / Stop"),
    ]

    def __init__(self) -> None:
        self.is_running_: bool = False
        super().__init__()

    def compose(self) -> ComposeResult:
        # uv build をすると src/segmock 内のディレクトリやファイルがビルドされて whl にまとめられるみたい。
        # font を src/segmock に移動して、 pathlib で動的に相対パスを指定すると正常に動作するようになった。
        font = Path(__file__).parent / "font" / "7segment"
        yield TimeDisplay(font=str(font))
        yield Footer()

    def action_operate_timer(self) -> None:
        time_display: TimeDisplay = self.query_one(TimeDisplay)

        if self.is_running_:
            time_display.stop()
            self.is_running_ = False
        else:
            time_display.start()
            self.is_running_ = True

    def action_reset_time(self) -> None:
        time_display: TimeDisplay = self.query_one(TimeDisplay)
        time_display.reset()
        self.is_running_ = False
