# src/simulated_detector.py

import numpy as np
import time
from src.simulated_display import SimulatedLEDDisplay

class SimulatedParticleDetector(SimulatedLEDDisplay):
    """
    A simulated particle detector based on the LED display.
    Pixels represent detector cells that register energy.
    """
    def __init__(self, width, height, initial_background=(0, 0, 0), max_energy_per_pixel=255):
        super().__init__(width, height, initial_background)
        self.max_energy_per_pixel = max_energy_per_pixel
        print(f"SimulatedParticleDetector initialized: {width}x{height} cells.")

    def simulate_particle_hit(self, impact_x, impact_y, peak_brightness_contribution, spread_radius=1.0):
        """
        Simulates a particle hitting the detector with a Gaussian energy spread.
        'peak_brightness_contribution' directly controls the maximum pixel brightness at the center.
        :param impact_x: X-coordinate of the particle impact.
        :param impact_y: Y-coordinate of the particle impact.
        :param peak_brightness_contribution: The desired brightness (0-255) for the pixel at the impact center.
        :param spread_radius: A measure of how far the energy spreads (roughly 2.5 sigma of the Gaussian).
        """
        print(f"Simulating particle hit at ({impact_x:.1f},{impact_y:.1f}) with peak brightness {peak_brightness_contribution:.0f}, radius {spread_radius:.1f}")

        # Ensure peak_brightness_contribution is within valid range (0-255)
        peak_brightness_contribution = min(max(0, peak_brightness_contribution), self.max_energy_per_pixel)

        # Define the standard deviation (sigma) for the Gaussian spread
        sigma = spread_radius / 2.5 # Let's say radius covers about 2.5 sigma

        # Determine the affected region (bounding box around the impact)
        # Extend bounds slightly to capture the tails of the Gaussian
        buffer_pixels = int(spread_radius * 2) # Ensures full spread is captured
        x_min = max(0, int(impact_x - buffer_pixels))
        x_max = min(self.width, int(impact_x + buffer_pixels + 1))
        y_min = max(0, int(impact_y - buffer_pixels))
        y_max = min(self.height, int(impact_y + buffer_pixels + 1))

        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                distance_sq = (x - impact_x)**2 + (y - impact_y)**2
                
                # Gaussian value for this pixel (between 0 and 1, peaking at 1 at center)
                gaussian_intensity = np.exp(-distance_sq / (2 * sigma**2))
                
                # Scale by the desired peak_brightness_contribution
                pixel_value_to_add = int(peak_brightness_contribution * gaussian_intensity)
                
                # Add to all R, G, B channels equally for a "white/grayscale" energy deposition
                self.add_pixel_value(x, y, pixel_value_to_add, pixel_value_to_add, pixel_value_to_add)
        
        time.sleep(0.005) # Simulate processing time for a hit


    def add_background_noise(self, noise_level, seed=None):
        """
        Adds random noise to the detector pixels.
        :param noise_level: Max intensity of noise for each pixel (0-255).
        :param seed: Optional seed for reproducibility.
        """
        print(f"Adding background noise with max level: {noise_level}")
        rng = np.random.default_rng(seed)
        noise_matrix = rng.integers(0, noise_level + 1, size=(self.height, self.width, 3), dtype=np.uint8)
        
        # Add noise to existing display memory, clamping at 255
        self._display_memory = np.minimum(self._display_memory + noise_matrix, 255).astype(np.uint8)
        time.sleep(0.002)

    def get_total_deposited_energy(self):
        """
        Calculates the total 'energy' deposited across all pixels.
        Assumes R, G, B channels represent similar energy contributions.
        :return: Sum of all pixel values (summed across R,G,B channels).
        """
        # Sum all channel values for all pixels
        total_energy = np.sum(self._display_memory)
        print(f"Total deposited energy read: {total_energy}")
        return total_energy

    def get_max_pixel_value(self):
        """Returns the highest single pixel channel value on the display."""
        return np.max(self._display_memory)






###########

