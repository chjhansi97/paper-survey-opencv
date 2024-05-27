from cv2 import cv2
import numpy as np
import json
import os
import csv
import datetime
import sys
import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox

import time

start = time.time()


color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
              'white': [[180, 18, 255], [0, 0, 231]],
              'red1': [[180, 255, 255], [159, 50, 70]],
              'red2': [[9, 255, 255], [0, 50, 70]],
              'green': [[89, 255, 255], [36, 50, 70]],
              'blue': [[128, 255, 255], [90, 50, 70]],
              'yellow': [[35, 255, 255], [25, 50, 70]],
              'purple': [[158, 255, 255], [129, 50, 70]],
              'orange': [[24, 255, 255], [10, 50, 70]],
              'gray': [[180, 18, 230], [0, 0, 40]]}

def detect_box(image, line_min_width=25): #18
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lwr = np.array([0, 0, 0])
    upr = np.array([179, 255, 146])
    #
    #lwr = np.array([80, 85, 70])
    upr = np.array([179, 255, 146])
    mask = cv2.inRange(hsv, lwr, upr)
    image_invert = cv2.bitwise_not(mask)
    #

    imS = cv2.resize(image_invert, (550,600))
    cv2.imshow("image", imS)
    cv2.waitKey(10)

    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    th1, img_bin = cv2.threshold(gray_scale , 220, 225, cv2.THRESH_BINARY)
    kernal_h = np.ones((3, line_min_width), np.uint8)
    kernal_v = np.ones((line_min_width, 3), np.uint8)
    img_bin_h = cv2.morphologyEx(~img_bin, cv2.MORPH_OPEN, kernal_h)
    img_bin_v = cv2.morphologyEx(~img_bin, cv2.MORPH_OPEN, kernal_v)
    img_bin_final = img_bin_h | img_bin_v
    final_kernel = np.ones((3, 3), np.uint8)
    img_bin_final = cv2.dilate(img_bin_final, final_kernel, iterations=3)

    imS = cv2.resize(img_bin_final, (550,600))
    #cv2.imshow("image", imS)
    #cv2.waitKey()

    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)
    return ret, stats, labels, centroids


def main(basepath, step=True, save_audit_img=True):
    with open('loop_digi_profile.json', 'r', encoding='utf-8') as file:
        profile = json.loads(file.read())

    data = {}
    audit_log = []
    

    for dir in os.listdir(basepath):
        print(dir)
        for key, value in profile.items():
            data_values = []
            error = False
            if value['total'] == 0:
                continue

            image_path = os.path.join(basepath,dir,f'{key}.jpg')  # 'data/output/202030/8.jpg'
            image = cv2.imread(image_path)
            cropped_image = image[80:2100, 100:1550]
            image = cropped_image
            ret, stats, labels, _ = detect_box(image)


            if len(stats[2:]) != int(value['total']):

                audit_log.append([dir,
                                  key,
                                  f'Identified number of questions no match ({len(stats[2:])}) ({int(value["total"])})'])
                print(([dir,
                        key,
                        f'Identified number of questions no match ({len(stats[2:])}) ({int(value["total"])})']))
                error = True
                data_values.append('Identified number of questions no match')
                

            for k, v in value['q'].items():

                question_values = []

                for x,y,w,h,area in np.sort(stats[v[0]:v[1]], axis=0):
                    box = image[y:y+h, x:x+w]

                    gray_scale = cv2.cvtColor(box, cv2.COLOR_BGR2GRAY)
                    th1, img_bin = cv2.threshold(gray_scale, 210, 225, cv2.THRESH_BINARY)


                    if np.mean(img_bin) < 190:

                        question_values.append(np.mean(img_bin))
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    else:


                        question_values.append(0)
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    if step == 'verbose':
                        imS = cv2.resize(image, (550,600))
                        cv2.imshow("image", imS)
                        cv2.waitKey(10)

                dup = [n for n in question_values if n > 0]
                #print(question_values)
                if len(dup) > 1:
                    audit_log.append([dir, k, 'Multiple answers'])
                    print([dir, k, 'Multiple answers'])
                    error = True
                    data_values.append('Multiple answers')

                if max(question_values) == 0:
                    data_value = 'NULL'
                    audit_log.append([dir, k, 'Empty answer'])
                    print([dir, k, 'Empty answer'])
                    data_values.append('Empty answer')
                    # error = True
                    
                else:
                    data_value = question_values.index(max(question_values)) + 1

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, str(data_value), (x +40, y +20), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(image, str(k), (x - 1200, y + 20), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                data[k] = data_value

            # if error:
            #     imS = cv2.resize(image, (550,600))
            #     cv2.imshow("image", imS)
            #     create_form(dir)
            #     cv2.waitKey()

            if 'Empty answer' in data_values:
                imS = cv2.resize(image, (550,600))
                cv2.imshow("image", imS)
                result = yes_no_dialog()
                #if yes direct to update dialog box else continue
                if result == True:
                    create_form(dir)
                else:
                    continue
            elif error:
                imS = cv2.resize(image, (550,600))
                cv2.imshow("image", imS)
                create_form(dir)
                cv2.waitKey()

            if save_audit_img:
                if not os.path.exists(os.path.join(os.path.join(basepath,dir,'audit'))):
                    os.makedirs(os.path.join(os.path.join(basepath,dir,'audit')))

                cv2.imwrite(os.path.join(basepath,dir,'audit',f'{key}_audit.jpg'), image)

        # if data_value == 'NULL':
        #         #dialog box for asking to update the answers or not
        #         imS = cv2.resize(image, (550,600))
        #         cv2.imshow("image", imS)
        #         result = yes_no_dialog()
        #         cv2.waitKey()

        #         #if yes direct to update dialog box else continue
        #         if result == True:
        #             create_form(dir)
        #         else:
        #             continue

        


        with open(os.path.join(basepath,dir,f'{dir}.json'), 'w') as json_output:
            json_output.write(json.dumps(data, indent=4))

        with open(os.path.join(basepath, f'log.txt'), 'w') as log_output:
            for l in audit_log:
               log_output.write(f'{l[0]},{l[1]},{l[2]}\n')
            #json_output.write(json.dumps(data, indent=4))
        #print(data)
    #cv2.imshow("image", imS)
    #cv2.waitKey()
    #print(audit_log)
    print(data_values)

def yes_no_dialog():
    result = messagebox.askyesno("Confirmation", "Do you want to update the answers?")
    return result

def create_form(dir):
    title='details'
    fields = ['Survey Number', 'Q.No', 'Answer']

    
    def save_details():
        data = [entry_widgets[field].get() for field in fields]
        
        with open('details.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
        
            # Check if the file is empty
            file_empty = file.tell() == 0
            
            # Write column names if the file is empty
            if file_empty:
                writer.writerow(fields)
                writer.writerow(data)
            else:
                writer.writerow(data)

                
            # # Check if an entry with the same survey number and question number exists
            # else:
            #     file.seek(0)
            #     reader = csv.reader(file, delimiter=',')
            #     found = False
            #     for row in reader:
            #         print(row[1],data[1])
            #         if row[0] == data[0] and row[1] == data[1]:
            #             # Update the existing row with the latest data
            #             row[:] = data
            #             found = True
            #             break
                
            #     # If no existing entry found, append the new data
            #     if not found:
            #         writer.writerow(data)

            # Close the window
            root.destroy()
           
            print("updated")
        create_form(dir)

    # Create the main window
    root = tk.Tk()
    root.title(title)

    # Create a frame for the form
    frame = ttk.Frame(root, padding="25")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Create form fields
    row = 0
    entry_widgets = {}
    for field, value in zip(fields, [dir] + [''] * (len(fields) - 1)):
        label = ttk.Label(frame, text=f"{field}:")
        label.grid(row=row, column=0, sticky=tk.W)
        entry_widgets[field] = ttk.Entry(frame)
        entry_widgets[field].grid(row=row, column=1, sticky=tk.W)
        entry_widgets[field].insert(tk.END, value)
        row += 1

    # Save button
    save_button = ttk.Button(frame, text="Save", command=save_details)
    save_button.grid(row=row, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == '__main__':
   main(sys.argv[1])


