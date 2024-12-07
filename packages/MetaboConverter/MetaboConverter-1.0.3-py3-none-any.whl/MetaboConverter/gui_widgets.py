import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class WidgetsSetup:
    def create_widgets(self):
        """
        Create and configure all the widgets in the main application window.

        This function initializes various buttons and labels in the GUI, such as opening files, clearing data, viewing saved groups, exporting groups, and performing t-tests.
        These widgets are configured with their respective commands and initial states.

        Input:
        - None

        Returns:
        - None
        """
        # Button to open the file
        self.open_button = tk.Button(self, text="Open Excel File", command=self.load_file)
        self.open_button.pack(pady=10)

        # Label for file path
        self.file_label = tk.Label(self, text="No file selected", wraplength=400)
        self.file_label.pack(pady=10)

        # Button to select sample info sheet (added)
        self.sample_info_button = tk.Button(self, text="Select Sample Info Sheet", command=self.select_sample_info_sheet, state='disabled')
        self.sample_info_button.pack(pady=5)

        # Button to select intestine groups to group (added)
        self.group_intestine_button = tk.Button(self, text="Group Intestine Groups", command=self.group_intestine_groups, state='disabled')
        self.group_intestine_button.pack(pady=5)

        # Button to clear data
        self.clear_button = tk.Button(self, text="Clear Data", command=self.clear_sheets)
        self.clear_button.pack(pady=10)

        # Button to view saved groups
        self.view_groups_button = tk.Button(self, text="View Saved Groups", command=self.view_saved_groups)
        self.view_groups_button.pack(pady=5)

        # Button to export saved groups
        self.export_groups_button = tk.Button(self, text="Export Saved Groups", command=self.export_saved_groups, state='disabled')
        self.export_groups_button.pack(pady=5)

        # Button to perform t-test analysis
        self.t_test_button = tk.Button(self, text="Perform T-Test", command=self.perform_t_test, state='disabled')
        self.t_test_button.pack(pady=5)

    def display_data(self, data: pd.DataFrame = pd.DataFrame(), title: str = "Data Display"):
        """
        Display a pandas DataFrame in a new top-level window using a Treeview widget.

        This function creates a new window that shows the data in a tabular format using Tkinter's Treeview widget.

        Input:
        - data (pd.DataFrame): The pandas DataFrame to be displayed.
        - title (str): The title for the new display window.

        Returns:
        - None
        """
        # Create a new top-level window for displaying data
        display_window = tk.Toplevel(self)
        display_window.title(title)
        display_window.geometry("800x400")

        # Create a Treeview widget for displaying the data
        tree = ttk.Treeview(display_window)
        tree.pack(expand=True, fill='both', pady=10)

        # Define columns
        tree["column"] = list(data.columns)
        tree["show"] = "headings"

        # Create headings based on the columns of the dataframe
        for col in data.columns:
            tree.heading(col, text=col)

        # Insert rows into the treeview
        for index, row in data.iterrows():
            tree.insert("", "end", values=list(row))

    def clear_sheets(self):
        """
        Clear all loaded data and reset the user interface.

        This function clears all the loaded data from the imported file, cleaned data, sample info, weights, and saved groups.
        It also resets the labels and disables buttons to indicate that there is no active data.

        Input:
        - None

        Returns:
        - None
        """
        # Clear all data and reset UI
        self.imported_data = {}
        self.cleaned_data = None
        self.sample_info_sheet = None
        self.weights = None
        self.saved_groups = {}
        self.file_label.config(text="No file selected")

        # Disable buttons
        self.sample_info_button.config(state='disabled')
        self.group_intestine_button.config(state='disabled')
        self.export_groups_button.config(state='disabled')
        self.t_test_button.config(state='disabled')

        messagebox.showinfo("Cleared", "All data has been cleared.")
