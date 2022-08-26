from tcod import console

class BlankSimulation:
    def __init__(self) -> None:
        self.width = 128
        self.height = 72

    def on_update(self, dt) -> None:
        raise NotImplementedError()

    def on_render(self, console: console) -> None:
        console.clear()
        return
