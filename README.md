# ESP-8266 display
Working with SSD1306 display through ESP-8266 using Micropython

## Using:
- ESP-8266 (can work with [NodeMCU](https://en.wikipedia.org/wiki/NodeMCU) dev platform or with [ESP-01](https://en.wikipedia.org/wiki/ESP8266#Pinout_of_ESP-01))
- SSD1306 128*64 LCD Display
- [Micropython](https://micropython.org/)

## Utilities
### Erasing and flashing ESP

- `esp_erase.sh` script can be used to easily erase and flash ESP from scratch. Usage:
    ```
    source esp_erase.sh [path_to_micropython_bin]
    ```

- Uploading of files to the board can be easily done using `esp_push.sh`. Usage:
    ```
    source esp_push.sh
    ```
    This deletes all the files from the board and then uploads everithing from the `esp/` dir.

### Converting images

- Use `img_to_bin.py` script to convert images to binary format. By default it gets all images from `raw_images/` folders and then stores converted files to the `esp/images/`. You can change it by changing static variables in the script. Converter accepts any file format supported by [Pillow](https://pillow.readthedocs.io/en/4.1.x/handbook/image-file-formats.html). Usage is simple, just run:
    ```
    python img_to_bin.py
    ```
    Images are stored in `.bin` files. Encoding is simple each pixel is converted to `0-255` using PIL and then from `0-255` to `0-1` where `0` is black and `1` is white. Thats done simply by checking is value more than `127` or less. File is simply a sequence of `0`s and `1`s.

## Display usage
Display is a subclass of [`SSD1306_I2C`](https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py) that implements some addictional methods.
- `hardware_scroll` - Allows you to use hardware scroll that supported by SSD1306
- `clear` - Fills display black and refreshes
- `draw_from_file` - Allows you to draw binary image from file (use `img_to_bin.py` to convert image to supported format). 
- `draw_from_sequence` - Allows you to draw image from sequence. I suggest to use generators for better memory optimization.
