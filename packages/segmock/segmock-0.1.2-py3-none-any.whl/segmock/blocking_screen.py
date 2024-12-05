from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center
from textual.events import Resize
from textual.screen import ModalScreen
from textual.widgets import Footer, Label

MIN_WIDTH: int = 158
MIN_HEIGHT: int = 17


class BlockingScreen(ModalScreen[None]):
    BINDINGS = [Binding("q", "app.quit", "Exit")]

    def compose(self) -> ComposeResult:
        width: int = self.app.size.width
        height: int = self.app.size.height

        with Center():
            yield Label(
                f"The app screen size must be at least {MIN_WIDTH}x{MIN_HEIGHT}\n"
            )
        with Center():
            yield Label(f"Current app screen size: {width}x{height}")
        yield Footer()

    async def on_resize(self, event: Resize) -> None:
        if (
            event.size.width >= MIN_WIDTH
            and event.size.height >= MIN_HEIGHT
            and self.is_current
        ):
            self.app.pop_screen()
