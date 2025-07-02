# src/simulated_display.py

import numpy as np
import time

class SimulatedLEDDisplay:
    """
    A simulated LED display module.
    Acts like a simple hardware component with memory for pixels.
    """
    
    def __init__(self, width, height, initial_color=(0, 0, 0)):
        """
        Initializes the simulated display.
        :param width: Width of the display in pixels.
        :param height: Height of the display in pixels.
        :param initial_color: RGB tuple (0-255) for the background color.
        """
        if not all(0 <= c <= 255 for c in initial_color):
            raise ValueError("RGB values must be between 0 and 255.")

        self.width = width
        self.height = height
        # Internal memory for the display, represented as a 3D NumPy array (height, width, RGB)
        self._display_memory = np.full((height, width, 3), initial_color, dtype=np.uint8)
        self.initialized_time = time.time()
        print(f"SimulatedLEDDisplay initialized: {width}x{height} pixels.")
        self._simulate_boot_time() # Simulate a small boot delay

    def _simulate_boot_time(self):
        """Simulates a short boot-up time for the 'hardware'."""
        time.sleep(0.01) # A tiny delay
        # In a real firmware, this might involve self-tests, register setup, etc.
        print("Hardware boot sequence complete.")

    def set_pixel(self, x, y, color):
        """
        Sets the color of a specific pixel on the display.
        :param x: X-coordinate of the pixel (0 to width-1).
        :param y: Y-coordinate of the pixel (0 to height-1).
        :param color: RGB tuple (0-255) for the pixel color.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            print(f"Warning: Pixel coordinates ({x},{y}) out of bounds for {self.width}x{self.height} display.")
            return

        if not all(0 <= c <= 255 for c in color):
            raise ValueError("RGB values must be between 0 and 255.")

        self._display_memory[y, x] = color
        # Simulate a small processing delay for setting a pixel
        time.sleep(0.00001)
        
    
    # For pixel deposition
    def add_pixel_value(self, x, y, r_val=0, g_val=0, b_val=0):  
        """
        Increments the RGB values of a specific pixel, clamping at 255.
        Useful for simulating energy deposition.
        :param x, y: Coordinates of the pixel.
        :param r_val, g_val, b_val: Values to add to R, G, B channels.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            # print(f"Warning: Pixel coordinates ({x},{y}) out of bounds for {self.width}x{self.height} display.")
            return # Silently ignore out-of-bounds for "hits"

        current_color = self._display_memory[y, x]
        new_r = min(255, current_color[0] + r_val)
        new_g = min(255, current_color[1] + g_val)
        new_b = min(255, current_color[2] + b_val)
        
        self._display_memory[y, x] = [new_r, new_g, new_b]
        # Minimal delay for adding value, if needed
        # time.sleep(0.000001)    

    def fill_display(self, color):
        """
        Fills the entire display with a single color.
        :param color: RGB tuple (0-255).
        """
        if not all(0 <= c <= 255 for c in color):
            raise ValueError("RGB values must be between 0 and 255.")
        self._display_memory[:] = color
        print(f"Display filled with color: {color}")
        time.sleep(0.001) # Simulate a longer refresh time

    def clear_display(self):
        """Clears the display to black."""
        self.fill_display((0, 0, 0))
        print("Display cleared.")

    def get_display_data(self):
        """
        Retrieves the current pixel data from the display memory.
        This is like reading from a frame buffer register.
        :return: A NumPy array representing the current display content.
        """
        print("Retrieving display data...")
        time.sleep(0.0001) # Simulate reading time
        return self._display_memory.copy() # Return a copy to prevent external modification

    def get_firmware_version(self):
        """Simulates reading a firmware version register."""
        return "v1.0.0-alpha"

    def reset_hardware(self):
        """Simulates a hardware reset."""
        print("Performing hardware reset...")
        self._display_memory = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.initialized_time = time.time()
        time.sleep(0.05)
        print("Hardware reset complete.")


