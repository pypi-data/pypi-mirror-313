import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from fhir.resources.codesystem import CodeSystem

class CodeSystemEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FHIR CodeSystem Editor")
        self.geometry("800x600")
        
        self.codesystem = None
        self.selected_concept = None

        # Layout configuration
        self.left_panel = ttk.Frame(self, width=300)
        self.right_panel = ttk.Frame(self, width=500)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left Panel UI
        self.create_left_panel()

        # Right Panel UI
        self.create_right_panel()

    def create_left_panel(self):
        ttk.Label(self.left_panel, text="Concepts").pack(anchor=tk.W, pady=5)

        # Concept list
        self.concept_listbox = tk.Listbox(self.left_panel)
        self.concept_listbox.pack(fill=tk.BOTH, expand=True)
        self.concept_listbox.bind("<<ListboxSelect>>", self.select_concept)

        # Add Concept button
        ttk.Button(self.left_panel, text="Add Concept", command=self.add_concept).pack(fill=tk.X, pady=5)

        # Search functionality
        ttk.Label(self.left_panel, text="Search").pack(anchor=tk.W, pady=5)
        self.search_entry = ttk.Entry(self.left_panel)
        self.search_entry.pack(fill=tk.X)
        ttk.Button(self.left_panel, text="Search", command=self.search_concept).pack(fill=tk.X, pady=5)

    def create_right_panel(self):
        # Editing selected concept
        ttk.Label(self.right_panel, text="Selected Concept").pack(anchor=tk.W, pady=5)
        ttk.Label(self.right_panel, text="Code").pack(anchor=tk.W)
        self.code_entry = ttk.Entry(self.right_panel)
        self.code_entry.pack(fill=tk.X, pady=2)

        ttk.Label(self.right_panel, text="Display").pack(anchor=tk.W)
        self.display_entry = ttk.Entry(self.right_panel)
        self.display_entry.pack(fill=tk.X, pady=2)

        # Properties section
        ttk.Label(self.right_panel, text="Properties").pack(anchor=tk.W, pady=5)
        self.property_listbox = tk.Listbox(self.right_panel)
        self.property_listbox.pack(fill=tk.BOTH, expand=True, pady=2)

        ttk.Button(self.right_panel, text="Add Property", command=self.add_property).pack(fill=tk.X, pady=5)

        # Load and Save buttons
        ttk.Button(self.right_panel, text="Load CodeSystem", command=self.load_codesystem).pack(fill=tk.X, pady=5)
        ttk.Button(self.right_panel, text="Save CodeSystem", command=self.save_codesystem).pack(fill=tk.X, pady=5)

    def load_codesystem(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filepath:
            return
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                self.codesystem = CodeSystem(**data)
                self.refresh_concepts()
                messagebox.showinfo("Success", "CodeSystem loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CodeSystem: {e}")

    def save_codesystem(self):
        if not self.codesystem:
            messagebox.showerror("Error", "No CodeSystem loaded.")
            return
        filepath = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")], defaultextension=".json")
        if not filepath:
            return
        try:
            with open(filepath, "w") as f:
                json.dump(self.codesystem.dict(), f, indent=2)
                messagebox.showinfo("Success", "CodeSystem saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CodeSystem: {e}")

    def refresh_concepts(self):
        self.concept_listbox.delete(0, tk.END)
        if self.codesystem and self.codesystem.concept:
            for concept in self.codesystem.concept:
                self.concept_listbox.insert(tk.END, f"{concept.code}: {concept.display}")

    def add_concept(self):
        if not self.codesystem:
            messagebox.showerror("Error", "No CodeSystem loaded.")
            return
        new_concept = {"code": "new_code", "display": "New Concept"}
        self.codesystem.concept.append(new_concept)
        self.refresh_concepts()

    def select_concept(self, event):
        if not self.codesystem or not self.codesystem.concept:
            return
        index = self.concept_listbox.curselection()
        if index:
            self.selected_concept = self.codesystem.concept[index[0]]
            self.code_entry.delete(0, tk.END)
            self.code_entry.insert(0, self.selected_concept.code)
            self.display_entry.delete(0, tk.END)
            self.display_entry.insert(0, self.selected_concept.display or '')
            self.refresh_properties()

    def refresh_properties(self):
        self.property_listbox.delete(0, tk.END)
        if self.selected_concept and self.selected_concept.property:
            for prop in self.selected_concept.property:
                self.property_listbox.insert(tk.END, f"{prop.code}: {prop.value}")

    def add_property(self):
        if not self.selected_concept:
            messagebox.showerror("Error", "No concept selected.")
            return
        new_property = {"code": "new_property", "value": "value"}
        self.selected_concept.property.append(new_property)
        self.refresh_properties()

    def search_concept(self):
        search_term = self.search_entry.get()
        self.concept_listbox.delete(0, tk.END)
        if self.codesystem and self.codesystem.concept:
            for concept in self.codesystem.concept:
                if search_term.lower() in (concept.code or "").lower() or search_term.lower() in (concept.display or "").lower():
                    self.concept_listbox.insert(tk.END, f"{concept.code}: {concept.display}")

if __name__ == "__main__":
    app = CodeSystemEditor()
    app.mainloop()
