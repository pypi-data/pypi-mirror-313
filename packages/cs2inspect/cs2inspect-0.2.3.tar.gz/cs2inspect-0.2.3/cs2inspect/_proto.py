__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "20.07.2024"
__email__ = "m@hler.eu"
__status__ = "Development"


from dataclasses import dataclass, field

from cs2inspect._hex import float_to_bytes
from cs2inspect._rarity import parse_rarity
from cs2inspect.econ_pb2 import CEconItemPreviewDataBlock


@dataclass
class Builder:
    defindex: int
    paintindex: int
    paintseed: int
    paintwear: float
    rarity: str | int
    stickers: list[dict] = field(default_factory=list)

    def build(self) -> CEconItemPreviewDataBlock:
        return CEconItemPreviewDataBlock(
            defindex=self.defindex,
            paintindex=self.paintindex,
            paintseed=self.paintseed,
            paintwear=float_to_bytes(self.paintwear),
            rarity=parse_rarity(self.rarity),
            stickers=[
                CEconItemPreviewDataBlock.Sticker(
                    slot=sticker['slot'],
                    sticker_id=sticker['sticker_id'],
                    wear=sticker['wear']
                ) for sticker in self.stickers
            ]
        )


if __name__ == '__main__':
    exit(1)
