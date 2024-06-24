# 4lph4bet Processor

This scripty processes a grid image generated with the 4lph4bet family of LoRAs for Stable Diffusion 1.5 for font creation using [Calligraphr](https://www.calligraphr.com/). The script `process_4lph4bet_grid_image.py` performs the following tasks:

1. Resizes the input grid image if necessary.
2. Converts the image to grayscale and applies Canny edge detection.
3. Finds and merges contours.
4. Extracts individual images from the grid, inverts colors, and saves them with a transparent background.
5. Places the extracted images onto a template for [Calligraphr](https://www.calligraphr.com/) and saves all processed glyphs individually.

## Files

- `process_4lph4bet_grid_image.py`: The main script for processing the grid image.
- `4lph4bet_calligraphr_template.png`: The template image onto which the extracted images are placed.
- `requirements.txt`: A list of dependencies required to run the script.
- `README.md`: Information on how to use the script.
- `LICENSE`: License inforamtion.

## Setup Instructions

### Prerequisites

- Python 3.6 or higher

### Download and Extract the Package

Download the `4lph4bet_processor` folder or clone the repository.

### Setting Up the Environment

1. Open a terminal or command prompt and navigate to the extracted directory (`4lph4bet_processor`).
  
2. Set up a virtual environment (optional but recommended):
  
  ```bash
  python -m venv env
  ```
  
3. Activate the virtual environment:
  
  - On Windows:
    
    ```bash
    .\env\Scripts\activate
    ```
    
  - On macOS and Linux:
    
    ```bash
    source env/bin/activate
    ```
    
4. Install the required packages:
  
  ```bash
  pip install -r requirements.txt
  ```
  

### Running the Script

Use the following command to run the script:

```bash
python process_4lph4bet_grid_image.py
```

The script will ask for the absolute path to your grid image. Provide the path and press Enter.

### Recommended Image Size

It is recommended (but not necessary) to upscale the grid image to 4096 by 4096 pixels for better processing results.

## Output

The script will save the processed images in an `[input_filename]_intermediate_outputs` directory. This folder as well as the final processed image with a timestamp will be saved in the same directory as the input grid image. The isolated glyphs will be saved in the folder for further processing if needed.

## Notes

- Ensure that the `4lph4bet_preset.png` file is in the same directory as the script.
- If you encounter any issues, please ensure you have the correct versions of the required packages as listed in `requirements.txt`.
- Further post processing like kerning or baseline offset might be required in Calligraphr.
- The free version of Calligraphy only allows 75 characters to be exported as a font so in this case the character set needs to be reduced before export.

## License

`CC BY-SA 4.0`
