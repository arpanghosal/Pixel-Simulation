# Simulated Firmware Project: From Display to Detector to Deep Learning

This project explores the development of simulated firmware for a modular display system, evolving into a particle detector simulation, and culminating in the application of deep learning for event classification. It's designed to showcase a progression from low-level hardware simulation to high-level machine learning applications within a structured Python project.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [How to Run](#how-to-run)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Author](#author)

## Project Overview

Initially conceived as a simple LED display simulator, this project has expanded to demonstrate several key concepts:

1.  **Simulated LED Display:** A Python class mimicking the behavior of a basic LED matrix, allowing pixel-level control and display.
2.  **Simulated Particle Detector:** An extension of the display, transforming it into a conceptual 2D particle detector grid where "particle hits" are simulated with realistic Gaussian energy deposition. Background noise can also be applied.
3.  **Event Data Generation:** A robust system to generate a dataset of these simulated detector events, including single hits, double hits, and noise-only scenarios, all tagged with "ground truth" labels.
4.  **Machine Learning for Event Classification:** A Convolutional Neural Network (CNN) is trained to classify the generated detector events into categories (single hit, double hit, or noise).

This project serves as a comprehensive example of bridging physics simulation with modern deep learning techniques using Python and Jupyter Notebooks.

## Features

* **`SimulatedLEDDisplay`:**
    * Configurable width, height, and initial background color.
    * Pixel-level control (`set_pixel`, `add_pixel_value`).
    * Full display fill (`fill_display`).
    * Display data retrieval as a NumPy array (suitable for visualization).
    * Basic hardware reset.
* **`SimulatedParticleDetector`:**
    * Inherits all functionalities from `SimulatedLEDDisplay`.
    * `simulate_particle_hit()`: Models energy deposition with a Gaussian spatial distribution, controllable by impact point, peak brightness, and spread radius.
    * `add_background_noise()`: Adds random noise to the detector.
    * `get_total_deposited_energy()`: Sums pixel values to mimic a total energy readout.
* **Event Data Generation (in Jupyter Notebook):**
    * Automated generation of a customizable number of simulated detector events.
    * Randomized parameters for particle hits (position, brightness, radius) and noise levels.
    * Categorical event types: 'single_hit', 'double_hit', 'noise_only' with configurable probabilities.
    * Events saved as compressed NumPy archives (`.npz`) containing both the image data and comprehensive ground truth labels.
* **Machine Learning Model (in Jupyter Notebook):**
    * Data loading and preprocessing pipeline for the generated `.npz` dataset.
    * Normalization of image data.
    * One-hot encoding of categorical labels.
    * Training/validation data splitting.
    * Definition of a simple yet effective Convolutional Neural Network (CNN) using TensorFlow/Keras.
    * Model training, evaluation, and visualization of training history (accuracy and loss curves).
    * Demonstration of predictions on unseen validation data.

## Project Structure
.
|-- notebooks
|   `-- simulated_events
`-- src
    `-- __pycache__

5 directories



## Setup and Installation

To get this project up and running on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
    cd simulated_firmware_project
    ```
    (Remember to replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub details.)

2.  **Create a Virtual Environment (Recommended):**
    Virtual environments help manage project dependencies without conflicts.
    ```bash
    python -m venv .venv
    ```

3.  **Activate the Virtual Environment:**
    * **On macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    * **On Windows (Command Prompt):**
        ```bash
        .venv\Scripts\activate.bat
        ```
    * **On Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```

4.  **Install Dependencies:**
    Once the virtual environment is activated, install all required packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

After setting up the environment:

1.  **Launch Jupyter Notebook:**
    From the root of your project directory (where `README.md` is located), run:
    ```bash
    jupyter notebook
    ```
    This will open a browser window displaying the Jupyter file browser.

2.  **Open the Main Notebook:**
    Navigate to `notebooks/detector_events.ipynb` and open it.

3.  **Run Cells Sequentially:**
    Execute the cells in the notebook from top to bottom.
    * The initial cells will set up the simulated display and detector.
    * Subsequent cells will demonstrate particle hit simulations and basic visualizations.
    * The "Event Data Generation" section will create the dataset (this might take a few minutes depending on `NUM_EVENTS`).
    * The "Machine Learning" section will then load this generated data, define the CNN, train it, and evaluate its performance.

## Future Enhancements

This project is designed to be extensible. Potential future enhancements include:

* **More Complex Physics Simulations:**
    * Precise Gaussian normalization for total energy.
    * Energy thresholds and non-linear detector responses.
    * Simulation of different particle types (e.g., muon tracks, electron showers) with distinct patterns.
    * Detector non-uniformities (dead/hot pixels, varying sensitivity).
* **Advanced Machine Learning Tasks:**
    * **Regression:** Training the CNN to predict particle impact coordinates (`x`, `y`) or total deposited energy from the image.
    * **Anomaly Detection:** Identifying unusual particle events.
    * **Denoising:** Training models to remove background noise from detector images.
    * **Deployment:** Integrating the trained ML model into a simulated "firmware" pipeline for real-time inference.
* **GUI/Visualization:** Develop a simple graphical interface to interact with the detector and visualize events dynamically.

