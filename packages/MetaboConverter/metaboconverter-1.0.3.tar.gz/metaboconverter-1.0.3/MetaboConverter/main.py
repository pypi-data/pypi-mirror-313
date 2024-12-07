import tkinter as tk
from .gui_widgets import WidgetsSetup
from .data_handling import DataProcessing
from .analysis import AdditionalFeatures

def runApp():
    app = MetaboConverter()
    app.mainloop()


# Combine modules into the main class
class MetaboConverter(tk.Tk, WidgetsSetup, DataProcessing, AdditionalFeatures):
    def __init__(self):
        super().__init__()
        self.title("MetaboConverter")
        self.geometry("600x600")

        # UI Components
        self.create_widgets()

        # Data Storage
        self.imported_data = {}
        self.cleaned_data = None
        self.sample_info_sheet = None
        self.weights = None
        self.saved_groups = {}

# Making the runApp function available at package level
if __name__ == "__main__":
    runApp()