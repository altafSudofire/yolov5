from glob import glob
import time
from collections import Counter
from aws_method import *

image_list = glob('runs/detect/exp43/crops/number-plate/*')
text_list = []

def on_file_created(event):
    if event.src_path.endswith('.jpg'):
        new_image = event.src_path
        image_list.append(new_image)
        print("New image added:", new_image)

def watch_images_folder(path):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_file_created

    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

def send_num(num):
    print("Sending number:", num)

def process_numbers(numbers):
    if len(numbers) == 1:
        send_num(numbers[0])
    elif len(numbers) < 10:
        counter = Counter(numbers)
        most_common = counter.most_common(1)[0][0]
        send_num(most_common)
    else:
        if numbers[-1] == numbers[-10]:
            pass
        else:
            counter = Counter(numbers)
            most_common = counter.most_common(1)[0][0]
            send_num(most_common)

def read_num():
    while True:
        if len(image_list) > 0:
            image = image_list.pop(0)
            # Process the image and extract the text
            # Save the extracted text to the text_list
            extracted_text = extract_text_from_image(image)
            text_list.append(extracted_text)
            print("Extracted text:", extracted_text)

            # if len(text_list) >= 10:
            #     numbers = text_list[-10:]
            #     process_numbers(numbers)
            #     del text_list[-10:]
            # elif len(text_list) < 10 and len(text_list) > 1:
            #     numbers = text_list[:]
            #     process_numbers(numbers)
            #     text_list.clear()
            # elif len(text_list) == 1:
            #     number = text_list[0]
            #     send_num(number)
            #     text_list.clear()

        time.sleep(1)  # Sleep for 1 second

def extract_text_from_image(image):
    # Your code to extract text from the image goes here
    # Replace this with your actual implementation
    extracted_text = read_num()
    return extracted_text

watch_images_folder('runs/detect/exp43/crops/number-plate')
read_num()
