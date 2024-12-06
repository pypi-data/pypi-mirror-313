import tkinter as tk
from tkinter import filedialog, simpledialog

class FormFactory:
    def __init__(self, fields):
        self.fields = fields
        self.form_data = {}
        self.entries = {}

    def create_form(self):
        self.root = tk.Tk()
        self.root.title("Form Factory")

        for field_name, field_type in self.fields.items():
            frame = tk.Frame(self.root)
            frame.pack(fill='x', pady=5)

            label = tk.Label(frame, text=field_name, width=20, anchor='w')
            label.pack(side='left')

            if field_type == 'string':
                entry = tk.Entry(frame, width=30)
                entry.pack(side='left')
                self.entries[field_name] = entry
            elif field_type == 'password':
                entry = tk.Entry(frame, width=30, show='*')
                entry.pack(side='left')
                show_var = tk.IntVar()
                show_check = tk.Checkbutton(frame, text="Show", variable=show_var,
                                            command=lambda e=entry, sv=show_var: self.toggle_password(e, sv))
                show_check.pack(side='left')
                self.entries[field_name] = entry
            elif field_type == 'file':
                entry = tk.Entry(frame, width=30)
                entry.pack(side='left')
                button = tk.Button(frame, text="Browse", command=lambda e=entry: self.browse_file(e))
                button.pack(side='left')
                self.entries[field_name] = entry

        button_frame = tk.Frame(self.root)
        button_frame.pack(fill='x', pady=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side='left', padx=5)
        
        save_button = tk.Button(button_frame, text="Save", command=self.save)
        save_button.pack(side='right', padx=5)

        self.root.mainloop()
        return self.form_data

    def toggle_password(self, entry, show_var):
        if show_var.get():
            entry.config(show='')
        else:
            entry.config(show='*')

    def browse_file(self, entry):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def cancel(self):
        self.form_data = {"action": "cancel"}
        self.root.destroy()

    def save(self):
        self.form_data = {field: entry.get() for field, entry in self.entries.items()}
        self.form_data["action"] = "save"
        self.root.destroy()

def create_user_form(fields):
    factory = FormFactory(fields)
    return factory.create_form()