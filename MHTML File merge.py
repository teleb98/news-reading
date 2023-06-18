# Webpage source code merge
# "C:\Source\WEB\" 폴더의 *.mhtml 파일 2개를 읽는다.
# 처음부터 끝부분까지 이미지 파일로 만든 후 좌측과 우측에 배치하여 하나의 파일로 만든다.
# 만들어진 파일을 "C:\Source\WEB\" 폴더에 저장한다.


import os
import glob
from io import BytesIO
from PIL import Image
from selenium import webdriver

source_folder = "C:\\Source\\WEB\\"


zoom_factor = 2  # Set the zoom factor for high-quality images

# Get the list of mhtml files in the source folder
mhtml_files = glob.glob(os.path.join(source_folder, "*.mhtml"))

# output_file 이름은 원본 이름과 동일하게 한다.
output_file = os.path.basename(mhtml_files[0])[:-6] + ".png"

# Check if there are 2 mhtml files
if len(mhtml_files) != 2:
    print("Error: There should be exactly 2 mhtml files in the folder.")
else:
    # Set up the webdriver
    chromedriver_path = "path/to/chromedriver.exe"  # Replace with the path to your ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(chromedriver_path, options=options)

    # Take screenshots of the web pages
    screenshots = []

    for file in mhtml_files:
        driver.get("file://" + file)
        
        # Get the full height of the web page
        full_height = driver.execute_script("return document.body.scrollHeight")
        
        # Set the browser window height to the full height of the web page
        driver.set_window_size(driver.execute_script("return document.body.clientWidth"), full_height)

        screenshot = driver.get_screenshot_as_png()
        screenshots.append(screenshot)

    # Close the webdriver
    driver.quit()

    # Combine the screenshots side by side
    images = [Image.open(BytesIO(screenshot)) for screenshot in screenshots]
    
    # Resize the images for high-quality
    resized_images = [image.resize((int(image.size[0] * zoom_factor), int(image.size[1] * zoom_factor)), Image.ANTIALIAS) for image in images]
    
    widths, heights = zip(*(image.size for image in resized_images))

    total_width = sum(widths)
    max_height = max(heights)

    merged_image = Image.new("RGB", (total_width, max_height))

    x_offset = 0
    for image in resized_images:
        merged_image.paste(image, (x_offset, 0))
        x_offset += image.size[0]

    # Save the merged image
    output_path = os.path.join(source_folder, output_file)
    merged_image.save(output_path)

    print(f"Merged image saved to {output_path}")