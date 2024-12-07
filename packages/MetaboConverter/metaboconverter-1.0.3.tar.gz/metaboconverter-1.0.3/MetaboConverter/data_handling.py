import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class DataProcessing:
    def load_file(self):
        """
        Open a file dialog to load an Excel file and select raw data.

        Input:
        - None

        Returns:
        - None
        """
        # Open file dialog to load Excel file
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

        if file_path:
            # Load Excel sheets
            try:
                excel_data = pd.read_excel(file_path, sheet_name=None)
                self.imported_data = excel_data
                self.file_label.config(text=file_path)

                # Step 1: Select raw data sheet
                self.select_raw_data_sheet()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load the file: {e}")

    def select_raw_data_sheet(self):
        """
        Create a window to prompt the user to select a raw data sheet.

        Input:
        - None

        Returns:
        - None
        """
        # Ask user to select raw data sheet
        raw_data_window = tk.Toplevel(self)
        raw_data_window.title("Select Raw Data Sheet")
        raw_data_window.geometry("400x200")

        sheet_label = tk.Label(raw_data_window, text="Select the raw data sheet:")
        sheet_label.pack(pady=5)

        self.selected_raw_data_sheet = tk.StringVar(raw_data_window)
        sheet_dropdown = ttk.Combobox(raw_data_window, textvariable=self.selected_raw_data_sheet)
        sheet_dropdown['values'] = list(self.imported_data.keys())
        sheet_dropdown.pack(pady=5)

        select_button = tk.Button(raw_data_window, text="Select Sheet", command=lambda: self.process_raw_data(raw_data_window))
        select_button.pack(pady=10)

    def process_raw_data(self, raw_data_window: tk.Toplevel):
        """
        Process the selected raw data sheet by extracting it and prompting for further cleaning.

        Input:
        - raw_data_window (tk.Toplevel): The window to be destroyed after selecting the sheet.

        Returns:
        - None
        """
        sheet_name = self.selected_raw_data_sheet.get()
        if sheet_name:
            self.raw_data = self.imported_data[sheet_name]
            raw_data_window.destroy()

            # Step 2: Ask user to select name column for removing duplicates
            self.select_name_column()
        else:
            messagebox.showwarning("Warning", "Please select a raw data sheet.")

    def select_name_column(self):
        """
        Create a window to prompt the user to select the name column for removing duplicates.

        Input:
        - None

        Returns:
        - None
        """
        # Ask user to select the name column
        name_window = tk.Toplevel(self)
        name_window.title("Select Name Column")
        name_window.geometry("400x200")

        column_label = tk.Label(name_window, text="Select the column for removing duplicates (e.g., Name column):")
        column_label.pack(pady=5)

        self.selected_name_column = tk.StringVar(name_window)
        column_dropdown = ttk.Combobox(name_window, textvariable=self.selected_name_column)
        column_dropdown['values'] = list(self.raw_data.columns)
        column_dropdown.pack(pady=5)

        remove_button = tk.Button(name_window, text="Remove Duplicates", command=lambda: self.remove_duplicates(name_window))
        remove_button.pack(pady=10)

    def remove_duplicates(self, name_window: tk.Toplevel):
        """
        Remove duplicates from the raw data based on the selected name column.

        Input:
        - name_window (tk.Toplevel): The window to be destroyed after selecting the column.

        Returns:
        - None
        """
        selected_column = self.selected_name_column.get()
        if selected_column:
            # Remove duplicates based on selected column, keep first
            self.cleaned_data = self.raw_data.drop_duplicates(subset=[selected_column], keep='first')
            self.name_column = selected_column

            # Close window and proceed to next step
            name_window.destroy()
            messagebox.showinfo("Info", "Duplicates removed. Data has been cleaned.")

            # Step 3: Display cleaned data
            self.display_data(self.cleaned_data, "Cleaned Raw Data")

            # Enable button to select sample info sheet
            self.sample_info_button.config(state='normal')
        else:
            messagebox.showwarning("Warning", "Please select a column to proceed.")

    def select_sample_info_sheet(self):
        """
        Create a window to prompt the user to select the sample info sheet.

        Input:
        - None

        Returns:
        - None
        """
        sample_info_window = tk.Toplevel(self)
        sample_info_window.title("Select Sample Info Sheet")
        sample_info_window.geometry("400x200")

        sheet_label = tk.Label(sample_info_window, text="Select the sample info sheet:")
        sheet_label.pack(pady=5)

        self.selected_sample_info_sheet = tk.StringVar(sample_info_window)
        sheet_dropdown = ttk.Combobox(sample_info_window, textvariable=self.selected_sample_info_sheet)
        sheet_dropdown['values'] = list(self.imported_data.keys())
        sheet_dropdown.pack(pady=5)

        select_button = tk.Button(sample_info_window, text="Select Sheet", command=lambda: self.process_sample_info_sheet(sample_info_window))
        select_button.pack(pady=10)

    def process_sample_info_sheet(self, sample_info_window: tk.Toplevel):
        """
        Processes the selected sample info sheet and normalizes the concentration data.

        Input:
        - sample_info_window (tk.Toplevel): The window to be destroyed after selecting the sample info sheet.

        Returns:
        - None
        """
        sheet_name = self.selected_sample_info_sheet.get()
        if sheet_name:
            self.sample_info_sheet = self.imported_data[sheet_name]
            sample_info_window.destroy()
            self.normalize_concentration()
        else:
            messagebox.showwarning("Warning", "Please select a sample info sheet.")

    def normalize_concentration(self):
        """
        Normalize the concentration data by the sample weight from the sample info sheet.

        Input:
        - None

        Returns:
        - None
        """
        try:
            # Extract specific columns from sample info sheet
            intestine_groups = self.sample_info_sheet.iloc[1:, 3].values
            weights = self.sample_info_sheet.iloc[1:, 4].values

            # Normalize raw data by weight
            concentration_columns = [col for col in self.cleaned_data.columns if col in intestine_groups]
            normalized_data = self.cleaned_data.copy()

            for idx, group in enumerate(intestine_groups):
                if group in concentration_columns:
                    normalized_data[group] = normalized_data[group] / weights[idx]

            self.cleaned_data = normalized_data
            messagebox.showinfo("Info", "Normalization complete.")

            # Step 6: Display normalized data
            self.display_data(self.cleaned_data, "Normalized Data")

            # Enable button to group intestine groups
            self.group_intestine_button.config(state='normal')
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during normalization: {e}")
