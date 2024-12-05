from pathlib import Path

from textual.app import App
from textual.binding import Binding
from textual.events import Resize
from textual.widgets import Footer

from segmock.blocking_screen import MIN_HEIGHT, MIN_WIDTH, BlockingScreen
from segmock.clock import ClockScreen
from segmock.stopwatch import StopwatchScreen


class Segmock(App[None]):
    CSS_PATH = Path(__file__).parent / "app.tcss"
    ENABLE_COMMAND_PALETTE = False
    MODES = {
        "clock": ClockScreen,
        "stopwatch": StopwatchScreen,
    }
    DEFAULT_MODE = "clock"
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("f", "toggle_footer_visibility", "Footer"),
        Binding("c", "app.switch_mode('clock')", "Clock"),
        Binding("s", "app.switch_mode('stopwatch')", "Stopwatch"),
    ]

    async def on_resize(self, event: Resize) -> None:
        if event.size.width < MIN_WIDTH or event.size.height < MIN_HEIGHT:
            self.push_screen(BlockingScreen())

    def action_toggle_footer_visibility(self) -> None:
        footer = self.query_one(Footer)
        footer.visible = not footer.visible
