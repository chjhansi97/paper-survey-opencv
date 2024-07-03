import os
import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
from PIL import Image, ImageTk

class ImageFormApp:
    labels_texts = ["116", "117", "118", "119", "120", "121"]

    def __init__(self, folder_path):
        self.folder_path = folder_path
        #self.image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg'))]
        self.current_index = self.load_last_index()
        self.root = tk.Tk()
        self.root.title("Image Viewer")

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        self.button_form = ttk.Button(self.root, text="Open Survey Form", command=self.open_form)
        self.button_form.pack(pady=10)

        self.root.bind("<Left>", self.previous_image)
        self.root.bind("<Right>", self.next_image)

        self.display_image_form()

    def display_image_form(self):
        image_path = os.path.join(self.folder_path, self.current_index)
        
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)

        # Resize the image to fit within the canvas dimensions while maintaining aspect ratio
        canvas_width, canvas_height = 800, 600
        image_pil.thumbnail((canvas_width, canvas_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image_pil)
        print(photo)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def next_image(self, event=None):
        processed_images = self.load_processed_images()
        while self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            if self.image_files[self.current_index] in processed_images:
                continue
            else:
                break

        self.display_image_form()
        self.save_last_index(self.current_index)

    def save_last_index(self, last_index):
        with open("last_index.txt", "w") as file:
            file.write(str(last_index))

    def previous_image(self, event=None):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_image_form()

    def load_last_index(self):
        try:
            with open("processed_manual_entries.txt", "r") as file:
                last_file = file.read().strip()
                print("Loaded last index:", last_file)
                return last_file
        except FileNotFoundError:
            print("Last index file not found. Starting from the first image.")
            return 0
              
    def load_processed_images(self):
        processed_images = []
        try:
            with open("processed_manual_entries.txt", "r") as file:
                for line in file:
                    processed_images.append(line.strip())
            
        except FileNotFoundError:
            print("Processed images file not found.")
        return processed_images

    def open_form(self):
        form_window = tk.Toplevel(self.root)
        form_window.title("Survey Form")

        form_frame = ttk.Frame(form_window)
        form_frame.pack(pady=15)

        self.entries = {}
        self.additional_options_frame = None

        for i, text in enumerate(self.labels_texts):
            label = ttk.Label(form_frame, text=text)
            label.grid(row=i, column=0, padx=10, pady=10)
            
            if text == "116":
                entry_frame = ttk.Frame(form_frame)
                entry_frame.grid(row=i, column=1, padx=5, pady=5)
                gender_var = tk.StringVar(value="kvinna")
                for option in ["kvinna", "man", "andra"]:
                    radio = ttk.Radiobutton(entry_frame, text=option, value=option, variable=gender_var)
                    radio.pack(side=tk.LEFT)
                self.entries[text] = gender_var

            elif text == "120":
                entry_frame = ttk.Frame(form_frame)
                entry_frame.grid(row=i, column=1, padx=5, pady=5)
                self.role_vars = {option: tk.BooleanVar() for option in ["Montör/Operatör", "Lagledare/teamleader", "Annat"]}
                for j, (option, var) in enumerate(self.role_vars.items()):
                    checkbox = ttk.Checkbutton(entry_frame, text=option, variable=var, command=lambda var=var, option=option: self.toggle_annat_entry(var, option, entry_frame))
                    checkbox.grid(row=j, column=0, padx=5, pady=5, sticky="w")
                self.entries[text] = self.role_vars

                # Create an entry field for "Annat" but don't pack it yet
                
                self.annat_entry = ttk.Entry(entry_frame)
                self.annat_entry.grid(row=len(self.role_vars), column=0, padx=5, pady=5)
                self.annat_entry.grid_remove()
                
            elif text == "121":
                entry_frame = ttk.Frame(form_frame)
                entry_frame.grid(row=i, column=1, padx=5, pady=5)
                self.option_var = tk.StringVar(value="no")
                for j, option in enumerate(["yes", "no"]):
                    radio = ttk.Radiobutton(entry_frame, text=option, value=option, variable=self.option_var, command=lambda option=option, row_num=i: self.toggle_additional_options(option, row_num))
                    radio.grid(row=0, column=j, padx=5, pady=5, sticky="w")
                self.entries[text] = self.option_var

                self.additional_options_frame = ttk.Frame(form_frame)
                self.additional_options_frame.grid(row=i+1, column=1, padx=5, pady=5)
                self.additional_options_frame.grid_remove()

                self.additional_annat_entry = ttk.Entry(self.additional_options_frame)
                self.additional_annat_entry.grid(row=4, column=1, padx=5, pady=5)
                self.additional_annat_entry.grid_remove()
            else:
                entry = ttk.Entry(form_frame)
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries[text] = entry

        def save_form():
            data = {}
            for text in self.labels_texts:
                if text == "120":
                    selected_roles = [option if option != "Annat" else f"Annat({self.annat_entry.get()})" for option, var in self.entries[text].items() if var.get()]
                    data[text] = ", ".join(selected_roles)
                elif text == "121":
                    if self.entries[text].get() == "yes":
                        additional_options = [widget.cget("text") if widget.cget("text") != "Annat" else f"Annat({self.additional_annat_entry.get()})" for widget in self.additional_option_widgets if widget.instate(['selected'])]
                        data[text] = f"Yes({', '.join(additional_options)})"
                    else:
                        data[text] = "No"
                else:
                    data[text] = self.entries[text].get()

            # Save form data to a CSV file
            csv_filename = os.path.join(self.folder_path, "form_data.csv")
            print("Saving data to:", csv_filename) 
            with open(csv_filename, "a", newline="") as csvfile:
                fieldnames = ["Image File"] + self.labels_texts
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if os.stat(csv_filename).st_size == 0:
                    writer.writeheader()

                row = {"Image File": self.image_files[self.current_index]}
                row.update(data)
                writer.writerow(row)
                print("Data saved successfully.")  
            with open("processed_manual_entries.txt", "a") as file:
                file.write(self.image_files[self.current_index] + "\n")
                print("Image filename saved:", self.image_files[self.current_index])

            form_window.destroy()            

        button_save = ttk.Button(form_frame, text="Save", command=save_form)
        button_save.grid(row=len(self.labels_texts) + 1, columnspan=2, padx=5, pady=10)

    def toggle_annat_entry(self, var, option, parent_frame):
        if option == "Annat" and var.get():
            self.annat_entry.grid()
        else:
            self.annat_entry.grid_remove()

        self.check_conditions()

    def toggle_additional_options(self, option, row_num):
        if option == "yes":
            if not hasattr(self, 'additional_option_widgets'):
                self.additional_option_widgets = []
                self.additional_option_vars = []
                for i, additional_option in enumerate(["Säkerhet/Arbetsmiljö", "Kvalitet", "Underhåll", "Annat"]):
                    checkbox_var = tk.BooleanVar()
                    checkbox = ttk.Checkbutton(self.additional_options_frame, text=additional_option, variable=checkbox_var, command=lambda additional_option=additional_option, option=option: self.toggle_annat_entry(additional_option, option, self.additional_options_frame))
                    checkbox.grid(row=i, column=0, padx=5, pady=5, sticky="w")
                    self.additional_option_widgets.append(checkbox)
                    self.additional_option_vars.append(checkbox_var) 

            self.additional_options_frame.grid(row=row_num + 1, column=1, padx=5, pady=5)

        else:
            
            self.additional_options_frame.grid_forget()
            if hasattr(self, 'additional_option_widgets'):
                for widget in self.additional_option_widgets:
                    widget.destroy()
                del self.additional_option_widgets
                for var in self.additional_option_vars:
                    var.set(False)
                del self.additional_option_vars
        self.check_conditions()

    def check_conditions(self):
        # Check if 'yes' is selected in the radiobuttons for 121 and 'Annat' is checked in the additional options
        if self.option_var.get() == "yes":
            for var, checkbox in zip(self.additional_option_vars, self.additional_option_widgets):
                if checkbox.cget("text") == "Annat" and var.get():
                    self.additional_annat_entry.grid()
                    break
            else:
                self.additional_annat_entry.grid_remove()
        else:
            self.additional_annat_entry.grid_remove()
            

if __name__ == "__main__":
    import sys
    from PIL import Image, ImageTk

    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        if not os.path.isdir(folder_path):
            print("Invalid folder path.")
        else:
            app = ImageFormApp(folder_path)
            app.root.mainloop()

    # else:
    #     folder_path = sys.argv[1]
        
    #     if not os.path.isdir(folder_path):
    #         print("Invalid folder path.")
    #     else:
    #         processed_images = set()
    #         if os.path.exists('processed_manual_entries.txt'):
    #             with open('processed_manual_entries.txt', 'r') as dir_log:
    #                 processed_images = set(dir_log.read().splitlines())

    #         for image in os.listdir(folder_path):
    #             if image in processed_images:
    #                 continue
    #             full_path = os.path.join(folder_path, image)
    #             print("fullpath", full_path)
    #             app = ImageFormApp(full_path)
                
            
