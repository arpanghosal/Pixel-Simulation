# src/simulated_detector.py

import numpy as np
import time
from src.simulated_display import SimulatedLEDDisplay # Import our base display

class SimulatedParticleDetector(SimulatedLEDDisplay):
    """
    A simulated particle detector based on the LED display.
    Pixels represent detector cells that register energy.
    """
    def __init__(self, width, height, initial_background=(0, 0, 0), max_energy_per_pixel=255):
        """
        Initializes the simulated detector.
        :param width: Width of the detector grid.
        :param height: Height of the detector grid.
        :param initial_background: Initial color (e.g., background noise level).
        :param max_energy_per_pixel: Maximum 'energy' a single pixel can register.
                                     Corresponds to 255 for brightness.
        """
        super().__init__(width, height, initial_background)
        self.max_energy_per_pixel = max_energy_per_pixel
        print(f"SimulatedParticleDetector initialized: {width}x{height} cells.")

    def simulate_particle_hit(self, impact_x, impact_y, energy_deposited, spread_radius=1.0):
        """
        Simulates a particle hitting the detector.
        Energy is distributed radially from the impact point.
        :param impact_x: X-coordinate of the particle impact.
        :param impact_y: Y-coordinate of the particle impact.
        :param energy_deposited: Total 'energy' deposited by the particle.
        :param spread_radius: How far the energy spreads from the impact point (in pixels).
        """
        print(f"Simulating particle hit at ({impact_x:.1f},{impact_y:.1f}) with energy {energy_deposited:.2f}, radius {spread_radius:.1f}")

        # Determine the affected region (bounding box around the impact)
        x_min = max(0, int(impact_x - spread_radius))
        x_max = min(self.width, int(impact_x + spread_radius + 1))
        y_min = max(0, int(impact_y - spread_radius))
        y_max = min(self.height, int(impact_y + spread_radius + 1))

        # Simple radial energy distribution
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                distance = np.sqrt((x - impact_x)**2 + (y - impact_y)**2)
                
                if distance <= spread_radius:
                    # Energy falls off with distance from center
                    # We'll use a simple linear falloff, but a Gaussian could be more realistic
                    intensity_factor = (spread_radius - distance) / spread_radius
                    # Scale deposited energy to fit into RGB (0-255)
                    # Distribute total energy over affected pixels roughly,
                    # capping individual pixel energy at max_energy_per_pixel
                    
                    # For simplicity, distribute energy such that pixels closest to center get more
                    # Sum of intensity_factors might be used to normalize total_energy_deposited
                    # But for now, let's just make each affected pixel light up based on factor
                    
                    # Distribute energy such that the total sum roughly equals energy_deposited
                    # This simplified approach gives brighter pixels near the center
                    energy_at_pixel = energy_deposited * intensity_factor * 0.1 # Scaling factor to prevent overflow
                    
                    # Add to all R, G, B channels equally for a "white/grayscale" energy deposition
                    energy_val = int(min(self.max_energy_per_pixel, energy_at_pixel))
                    self.add_pixel_value(x, y, energy_val, energy_val, energy_val)
        
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