import os
import pygame as pg
from apple import APPLE_NORMAL, APPLE_GOLD, APPLE_SPOILED


class AppleSpriteManager:
    """
    Loads and provides sprite surfaces for different apple types.
    """

    def __init__(self, cell_size: int):
        self.cell_size = cell_size
        self.surfaces = {}
        self._load_sprites()

    def _load_sprites(self):
        """
        Look for PNG files in
        """
        base_dir = os.path.dirname(__file__)
        sprites_dir = os.path.join(base_dir, "assets", "sprites", "apples")

        # Map apple kind -> filename
        filenames = {
            APPLE_NORMAL: "apple_normal.png",
            APPLE_GOLD: "apple_gold.png",
            APPLE_SPOILED: "apple_spoiled.png",
        }

        for kind, name in filenames.items():
            path = os.path.join(sprites_dir, name)
            try:
                image = pg.image.load(path).convert_alpha()
            except Exception:
                # If anything goes wrong, fall back to rectangles for this kind
                self.surfaces[kind] = None
                continue

            # Scale
            size = int(self.cell_size * 1.1)
            image = pg.transform.smoothscale(image, (size, size))

            self.surfaces[kind] = image

    def get_surface(self, kind: str):
        """Return the loaded surface for the apple kind, or None if unavailable."""
        return self.surfaces.get(kind)
