#!/usr/bin/env python3
import argparse
from pathlib import Path
import uuid
from PIL import Image, ImageDraw

class RoundedCorner(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description='Add rounded corners to images')
        self.add_argument('path', type=str, help='Input image path')
        self.add_argument('-e', '--export', type=str,
                         help='Export path (default: random UUID.png)',
                         default=None)
        self.add_argument('-r', '--radius', type=int,
                         help='Corner radius (default: auto-calculated)',
                         default=-1)

    def process_image(self):
        args = self.parse_args()

        # Validate input path
        if not Path(args.path).exists():
            print(f"Error: Input file '{args.path}' does not exist")
            return False

        # Generate export path if not provided
        export_path = args.export or f'{uuid.uuid4()}.png'

        try:
            # Open and process image
            im = Image.open(args.path)
            im = im.convert('RGBA')
            w, h = im.size

            # Calculate radius if not specified
            rad = args.radius
            if rad < 0:
                hmean = 2 * w * h / (w + h)
                rad = int(hmean * 0.05)

            # Create corner mask
            circle = Image.new('L', (rad * 2, rad * 2), 0)
            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)

            # Apply corners
            alpha = Image.new('L', im.size, "white")
            alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
            alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
            alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
            alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))

            im.putalpha(alpha)
            print(f'Exporting to {export_path}')
            im.save(export_path)
            return True

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return False

    @staticmethod
    def entrypoint():
        return RoundedCorner().process_image()
