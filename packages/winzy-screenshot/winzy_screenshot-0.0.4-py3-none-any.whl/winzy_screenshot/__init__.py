import winzy
import datetime
import logging
from pynput import keyboard
from PIL import Image, ImageGrab
from typing import Tuple
import tempfile
import os


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


class ScreenshotManager:
    def __init__(self, bboxes: list[Tuple[float, float, float, float]]):
        """
        Initialize the ScreenshotManager with a list of bounding boxes for cropping.

        Args:
            bboxes (list[Tuple[float, float, float, float]]): List of bounding boxes as (left, top, width, height) in percentages.
        """
        self.bboxes = bboxes
        self.esc_pressed_count = 0

    def take_screenshot(self) -> Image:
        """
        Takes a screenshot and returns it as a PIL Image.
        """
        return ImageGrab.grab()

    def save_image(self, image: Image, filename: str) -> None:
        """
        Saves the provided image to a file.

        Args:
            image (Image): The image to save.
            filename (str): The filename to save the image as.
        """
        try:
            image.save(filename)
            logging.info(f"Image saved: {filename}")
        except Exception as e:
            logging.error(f"Failed to save image: {e}")

    def crop_image(
        self, image: Image, bbox: Tuple[float, float, float, float]
    ) -> Image:
        """
        Crops the image using the provided bounding box percentages.

        Args:
            image (Image): The image to crop.
            bbox (Tuple[float, float, float, float]): Bounding box as (left, top, width, height) in percentages.

        Returns:
            Image: The cropped image.
        """
        left_percent, top_percent, width_percent, height_percent = bbox
        image_width, image_height = image.size

        # Convert percentages to pixel values
        left = int(image_width * (left_percent / 100))
        top = int(image_height * (top_percent / 100))
        right = int(image_width * ((left_percent + width_percent) / 100))
        bottom = int(image_height * ((top_percent + height_percent) / 100))

        return image.crop((left, top, right, bottom))

    def on_press(self, key):
        """
        Handles key press events. Takes and saves both original and cropped screenshots.

        Args:
            key: The key pressed.
        """
        if key == keyboard.Key.esc:
            self.esc_pressed_count += 1
            if self.esc_pressed_count >= 2:
                logging.info("Exiting on double ESC press.")
                return False
        elif key == keyboard.Key.shift_r:
            # Capture and save original screenshot
            screenshot = self.take_screenshot()
            print("\a", flush=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            original_filename = f"screenshot_{timestamp}.png"
            self.save_image(screenshot, original_filename)

            # Crop and save cropped screenshots for each bounding box
            for i, bbox in enumerate(self.bboxes):
                cropped_screenshot = self.crop_image(screenshot, bbox)
                cropped_filename = f"cropped_screenshot_{i}_{timestamp}.png"
                self.save_image(cropped_screenshot, cropped_filename)

    def on_release(self, key):
        """
        Handles key release events (currently not used).
        """
        pass

    def start_listener(self):
        """
        Starts the keyboard listener.
        """
        with keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        ) as listener:
            listener.join()


def create_parser(subparser):
    parser = subparser.add_parser("screenshot", description="Screenshot using python ")
    # Add subprser arguments here.
    parser.add_argument(
        "-b",
        "--bbox",
        nargs=4,
        type=float,
        action="append",
        help="Bounding box as left,top,width,height in percentages (can be specified multiple times)",
    )

    parser.add_argument(
        "-ut",
        "--use-tempdir",
        action="store_true",
        help="Use tempdir to save the screenshots",
    )

    parser.add_argument(
        "-t",
        "--title",
        type=str,
        default=None,
        help="Create BBOX for the windows whose title is given.",
    )

    return parser


class HelloWorld:
    """Screenshot using python"""

    __name__ = "screenshot"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.main)

    def main(self, args):
        bboxes = args.bbox if args.bbox else []

        cwd = os.getcwd()
        if args.use_tempdir:
            tempdir = tempfile.gettempdir()
            print(f"Saving screenshots: {tempdir}")
            os.chdir(tempdir)

        if args.title:
            from winzy_win_geometry import get_window_geometry_percentage

            win = get_window_geometry_percentage(args.title)
            if win:
                bboxes.append([win["x"], win["y"], win["width"], win["height"]])

        print("Press `Right shift` to take a screenshot. Esc twice to end.")
        manager = ScreenshotManager(bboxes)
        manager.start_listener()

        if args.use_tempdir:
            os.chdir(cwd)

    def hello(self, args):
        # this routine will be called when "winzy screenshot is called."
        print("Hello! This is an example ``winzy`` plugin.")


screenshot_plugin = HelloWorld()
