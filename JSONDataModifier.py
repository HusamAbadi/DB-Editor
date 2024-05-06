import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class JSONFileModifier:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON File Modifier")
        self.root.configure(bg="#2E2E2E")
        self.root.geometry("800x500")

        # Calculate horizontal and vertical margins
        self.horizontal_margin = 20
        self.vertical_margin = 20

        # Load File Button
        self.load_button = tk.Button(self.root, text="Load File", command=self.load_file, font=("Arial", 12))
        self.load_button.place(x=self.horizontal_margin, y=self.vertical_margin)

        # Identifier Section
        self.identifier_label = tk.Label(self.root, text="Identifier:", bg="#2E2E2E", fg="white")
        self.identifier_label.place(x=self.horizontal_margin, y=self.vertical_margin + 40)

        self.identifier_text = tk.Label(self.root, text="", bg="#2E2E2E", fg="white")
        self.identifier_text.place(x=self.horizontal_margin + 140, y=self.vertical_margin + 40)

        self.identifier_entry_label = tk.Label(self.root, text="Confirmed Identifier:", bg="#2E2E2E", fg="white")
        self.identifier_entry_label.place(x=self.horizontal_margin, y=self.vertical_margin + 70)

        self.identifier_entry = tk.Entry(self.root)
        self.identifier_entry.place(x=self.horizontal_margin + 140, y=self.vertical_margin + 70)

        self.file_path = ""
        self.data = []
        self.current_record_index = 0

        # Identifier Image
        self.identifier_image_label = tk.Label(self.root, bg="#2E2E2E")
        self.identifier_image_label.place(x=360 - self.horizontal_margin, y=self.vertical_margin)

        # Results Section
        self.results_label = tk.Label(self.root, text="Results:", bg="#2E2E2E", fg="white")
        self.results_label.place(x=self.horizontal_margin, y=self.vertical_margin + 110)

        self.results_text = tk.Label(self.root, text="", bg="#2E2E2E", fg="white")
        self.results_text.place(x=self.horizontal_margin + 140, y=self.vertical_margin + 110)

        self.results_entry_label = tk.Label(self.root, text="Confirmed Results:", bg="#2E2E2E", fg="white")
        self.results_entry_label.place(x=self.horizontal_margin, y=self.vertical_margin + 140)

        self.results_entry = tk.Entry(self.root)
        self.results_entry.place(x=self.horizontal_margin + 140, y=self.vertical_margin + 140)

        # Results Image
        self.results_image_label = tk.Label(self.root, bg="#2E2E2E")
        self.results_image_label.place(x=360 - self.horizontal_margin, y=self.vertical_margin + 120)

        # Previous and Next Buttons
        self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_record)
        self.previous_button.place(x=self.horizontal_margin, y=self.vertical_margin + 200)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_record)
        self.next_button.place(x=self.horizontal_margin + 90, y=self.vertical_margin + 200)

        # Search Section
        self.search_entry_label = tk.Label(self.root, text="Search Confirmed Identifier:", bg="#2E2E2E", fg="white")
        self.search_entry_label.place(x=self.horizontal_margin, y=self.vertical_margin + 240)

        # Search Entry
        self.search_entry = tk.Entry(self.root)
        self.search_entry.place(x=self.horizontal_margin + 240, y=self.vertical_margin + 240)

        # Search Button
        self.search_button = tk.Button(self.root, text="Search", command=self.search_record)
        self.search_button.place(x=self.horizontal_margin + 400, y=self.vertical_margin + 240)

        # Save Changes Button
        self.save_button = tk.Button(self.root, text="Save Changes", command=self.save_changes)
        self.save_button.place(x=self.horizontal_margin, y=500 - self.vertical_margin - 40)

        # Listbox to display all records
        self.records_listbox = tk.Listbox(self.root, width=50)
        self.records_listbox.place(x=500, y=self.vertical_margin + 60)

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if self.file_path:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
                if isinstance(self.data, list) and self.data:
                    self.show_all_records()

    def show_record(self, index):
        if self.data:
            entry = self.data[index]
            self.identifier_text.config(text=entry.get("identifier", ""))
            self.results_text.config(text=str(entry.get("results", "")))
            self.identifier_entry.delete(0, tk.END)
            self.results_entry.delete(0, tk.END)
            self.identifier_image_label.config(image=None)
            self.results_image_label.config(image=None)

            # Display confirmed data if available
            confirmed_identifier = entry.get("confirmed_identifier", "")
            confirmed_results = entry.get("confirmed_results", "")
            if confirmed_identifier:
                self.identifier_entry.insert(0, confirmed_identifier)
            if confirmed_results:
                self.results_entry.insert(0, confirmed_results)

            # Display identifier image
            identifier_image_name = entry.get("identifier_image", "")
            if identifier_image_name:
                identifier_image = Image.open(identifier_image_name)
                identifier_image = identifier_image.resize((100, 100), Image.ANTIALIAS) if hasattr(Image, 'ANTIALIAS') else identifier_image.resize(
                    (100, 100))
                self.identifier_image = ImageTk.PhotoImage(identifier_image)
                self.identifier_image_label.config(image=self.identifier_image)
                self.identifier_image_label.image = self.identifier_image

            # Display results image
            results_image_name = entry.get("result_image", "")
            if results_image_name:
                results_image = Image.open(results_image_name)
                results_image = results_image.resize((100, 100), Image.ANTIALIAS) if hasattr(Image, 'ANTIALIAS') else results_image.resize(
                    (100, 100))
                self.results_image = ImageTk.PhotoImage(results_image)
                self.results_image_label.config(image=self.results_image)
                self.results_image_label.image = self.results_image

    def previous_record(self):
        if self.current_record_index > 0:
            self.current_record_index -= 1
            self.show_record(self.current_record_index)

    def next_record(self):
        if self.current_record_index < len(self.data) - 1:
            self.current_record_index += 1
            self.show_record(self.current_record_index)

    def search_record(self):
        search_query = self.search_entry.get()
        if search_query:
            for index, entry in enumerate(self.data):
                confirmed_identifier = entry.get("confirmed_identifier", "")
                identifier = entry.get("identifier", "")
                if confirmed_identifier == search_query or identifier == search_query:
                    self.current_record_index = index
                    self.show_record(self.current_record_index)
                    return
            else:
                messagebox.showinfo("Search Result", "Record not found.")

    def save_changes(self):
        if self.data:
            confirmed_identifier = self.identifier_entry.get()
            confirmed_results = self.results_entry.get()
            entry = self.data[self.current_record_index]
            if confirmed_identifier:
                entry["confirmed_identifier"] = confirmed_identifier
            if confirmed_results:
                entry["confirmed_results"] = confirmed_results

            # Save changes to the same file
            with open(self.file_path, 'w') as file:
                json.dump(self.data, file, indent=4)

            messagebox.showinfo("Save Changes", "Changes have been successfully saved.")

    def show_all_records(self):
        if self.data:
            self.records_listbox.delete(0, tk.END)
            for index, entry in enumerate(self.data):
                identifier = entry.get("identifier", "")
                self.records_listbox.insert(tk.END, f"Record {index + 1}: {identifier}")

            self.records_listbox.bind("<<ListboxSelect>>", self.on_record_select)

    def on_record_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = int(selection[0])
            self.current_record_index = index
            self.show_record(index)


def main():
    root = tk.Tk()
    app = JSONFileModifier(root)
    root.mainloop()


if __name__ == "__main__":
    main()
