from multiprocessing.connection import wait
from re import I
import tcod
import doomfire, fireworks, render3d, gameoflife
from datetime import datetime
import numpy as np

WIDTH, HEIGHT = 1280, 720

FLAGS = tcod.context.SDL_WINDOW_RESIZABLE 

def main() -> None:
    """Main gameplay loop"""
    tileset = tcod.tileset.load_tilesheet(
        "16x16-sb-ascii.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    current_sim = fireworks.FireWorks() 
    
    current_time = datetime.now()
    last_frame_time = current_time
    delta_time = current_time - last_frame_time

    with tcod.context.new(
        width = WIDTH,
        height = HEIGHT,
        tileset = tileset,
        title = "Simulation",
        vsync = True,
        sdl_window_flags = FLAGS,
    ) as context:
        root_console = tcod.Console(current_sim.width, current_sim.height, order = "F")
        while True:
            # Calculate Delta Time
            last_frame_time = current_time
            current_time = datetime.now()
            delta_time = current_time - last_frame_time
            
            # Update sim and render
            current_sim.on_update(float(delta_time.microseconds / 1000000))
            current_sim.on_render(root_console)
            context.present(root_console)

            # Handle Events
            for event in tcod.event.get():
                context.convert_event(event)  # Sets tile coordinates for mouse events.
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()

    

if __name__ == "__main__":
    main()