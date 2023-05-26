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

# ***************************************************** #
# import time

# timer_started = False
# timer_start_time = 0
# timer_duration = 5
# pause_duration = 3

# for i, det in enumerate(pred):  # per image
#     seen += 1
#     if webcam:  # batch_size >= 1
#         p, im0, frame = path[i], im0s[i].copy(), dataset.count
#         s += f'{i}: '
#     else:
#         p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

#     p = Path(p)  # to Path
#     save_path = str(save_dir / p.name)  # im.jpg
#     txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
#     s += '%gx%g ' % im.shape[2:]  # print string
#     gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
#     imc = im0.copy() if save_crop else im0  # for save_crop
#     annotator = Annotator(im0, line_width=line_thickness, example=str(names))
    
#     if len(det):
#         # Rescale boxes from img_size to im0 size
#         det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

#         # Print results
#         for c in det[:, 5].unique():
#             n = (det[:, 5] == c).sum()  # detections per class
#             s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

#         # Write results
#         for *xyxy, conf, cls in reversed(det):
#             if save_txt:  # Write to file
#                 xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
#                 line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
#                 with open(f'{txt_path}.txt', 'a') as f:
#                     f.write(('%g ' * len(line)).rstrip() % line + '\n')

#             if save_img or save_crop or view_img:  # Add bbox to image
#                 c = int(cls)  # integer class
#                 label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
#                 annotator.box_label(xyxy, label, color=colors(c, True))
#             if save_crop:
#                 save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)
#             crop1 = imc[int(xyxy[1]):int(xyxy[3]), int(xyxy[0]):int(xyxy[2])]
            
#             if not timer_started:  # Start the timer when the first frame is detected
#                 timer_start_time = time.time()
#                 timer_started = True
            
#             if time.time() - timer_start_time >= timer_duration:  # Timer duration reached, read the number
#                 # Perform OCR using pytesseract on crop1
#                 text = pytesseract.image_to_string(crop1, config='-l eng --psm 9 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
#                 print(text)

#                 # Pause for the specified pause duration
#                 time.sleep(pause_duration)
                
#                 # Reset the timer and start again
#                 timer_start_time = time.time()
            
#             # print(crop1, type(crop1))
#             text = pytesseract.image_to_string(crop1, config='-l eng --psm 9 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
#             print(text)
# ********************************************* #