import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import os

class AdditionalFeatures:
    def group_intestine_groups(self):
        """
        Creates a new window for the user to select columns for grouping.
        
        Input:
        - None
        
        Returns:
        - None
        """
        # Create a new window to select columns to group
        group_window = tk.Toplevel(self)
        group_window.title("Select Intestine Groups to Group")
        group_window.geometry("800x400")

        # Add a listbox to select multiple columns for grouping
        grouping_label = tk.Label(group_window, text="Select the intestine groups to group together:")
        grouping_label.pack(pady=5)

        self.selected_columns = tk.StringVar(value=list(self.cleaned_data.columns))
        column_listbox = tk.Listbox(group_window, listvariable=self.selected_columns, selectmode='multiple', exportselection=False)
        column_listbox.pack(pady=5, expand=True, fill='both')

        # Add an entry field to input the group name
        group_name_label = tk.Label(group_window, text="Enter a name for the grouped columns:")
        group_name_label.pack(pady=5)

        self.group_name_entry = tk.Entry(group_window)
        self.group_name_entry.pack(pady=5)

        # Add a button to save the selected columns as a separate table
        save_button = tk.Button(group_window, text="Save Grouped Columns", command=lambda: self.save_grouped_columns(column_listbox))
        save_button.pack(pady=10)

    def save_grouped_columns(self, column_listbox: tk.Listbox):
        """
        Saves the selected columns as a separate group for further analysis.
        
        Input:
        - column_listbox (tk.Listbox): The listbox widget containing selectable columns.
        
        Returns:
        - None
        """
        selected_indices = column_listbox.curselection()
        selected_columns = [column_listbox.get(i) for i in selected_indices]

        if not selected_columns or not self.name_column:
            messagebox.showwarning("Warning", "Please select columns to group and ensure a name column was set.")
            return

        group_name = self.group_name_entry.get()

        if not group_name:
            messagebox.showwarning("Warning", "Please provide a name for the group.")
            return

        # Ensure that the Name column is included in the grouped columns
        if self.name_column not in selected_columns:
            selected_columns.insert(0, self.name_column)

        # Save the selected columns as a separate DataFrame
        grouped_data = self.cleaned_data[selected_columns]
        self.saved_groups[group_name] = grouped_data

        messagebox.showinfo("Group Saved", f"Grouped columns have been saved as '{group_name}'.")

        # Enable button to export saved groups and perform t-test
        self.export_groups_button.config(state='normal')
        self.t_test_button.config(state='normal')

    def perform_t_test(self):
        """
        Performs a t-test analysis between saved groups of data.
        
        Input:
        - None
        
        Returns:
        - None
        """
        if len(self.saved_groups) < 2:
            messagebox.showwarning("Warning", "At least two groups are required to perform t-tests.")
            return

        results = []
        group_names = list(self.saved_groups.keys())

        # Compare each pair of saved groups
        for i in range(len(group_names)):
            for j in range(i + 1, len(group_names)):
                group_1 = self.saved_groups[group_names[i]]
                group_2 = self.saved_groups[group_names[j]]

                common_metabolites = group_1[self.name_column]
                t_test_results = []

                # Perform t-test for each metabolite
                for metabolite in common_metabolites:
                    values_1 = group_1.loc[group_1[self.name_column] == metabolite].iloc[:, 1:].values.flatten()
                    values_2 = group_2.loc[group_2[self.name_column] == metabolite].iloc[:, 1:].values.flatten()
                    t_stat, p_val = ttest_ind(values_1, values_2, equal_var=False)
                    t_test_results.append([metabolite, t_stat, p_val])

                t_test_df = pd.DataFrame(t_test_results, columns=['Metabolite', 'T-Statistic', 'P-Value'])

                # Adjust p-values using Benjamini-Hochberg correction
                t_test_df['Adjusted P-Value'] = np.minimum(1, t_test_df['P-Value'] * len(t_test_df) / (np.arange(1, len(t_test_df) + 1)))

                # Separate upregulators and downregulators
                significant_up = t_test_df[(t_test_df['Adjusted P-Value'] < 0.05) & (t_test_df['T-Statistic'] > 0)]
                significant_down = t_test_df[(t_test_df['Adjusted P-Value'] < 0.05) & (t_test_df['T-Statistic'] < 0)]

                results.append((group_names[i], group_names[j], significant_up, significant_down))

        # Save the t-test results in an Excel file with separate sheets for upregulated and downregulated results
        directory_path = filedialog.askdirectory()
        if directory_path:
            file_path = os.path.join(directory_path, "t_test_significant_results.xlsx")
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                for group_1, group_2, significant_up, significant_down in results:
                    # Save significant upregulators and downregulators in separate sheets
                    up_sheet_name = f"{group_1}_vs_{group_2}_upregulated"
                    down_sheet_name = f"{group_1}_vs_{group_2}_downregulated"
                    significant_up.to_excel(writer, sheet_name=up_sheet_name, index=False)
                    significant_down.to_excel(writer, sheet_name=down_sheet_name, index=False)

            messagebox.showinfo("T-Test Completed", "T-tests performed and significant results saved to Excel file.")

    def view_saved_groups(self):
        """
        Displays saved groups for the user to view.

        Input:
        - None

        Returns:
        - None
        """
        if not self.saved_groups:
            messagebox.showinfo("No Saved Groups", "No groups have been saved yet.")
            return

        saved_window = tk.Toplevel(self)
        saved_window.title("Saved Groups")
        saved_window.geometry("400x300")

        for group_name in self.saved_groups.keys():
            group_button = tk.Button(saved_window, text=f"View {group_name}", command=lambda name=group_name: self.display_saved_group(name))
            group_button.pack(pady=5)

    def display_saved_group(self, group_name: str):
        """
        Displays a saved group in a new window.

        Input:
        - group_name (str): The name of the group to be displayed.

        Returns:
        - None
        """
        grouped_data = self.saved_groups[group_name]
        self.display_data(grouped_data, group_name)    

    def export_saved_groups(self):
        """
        Exports saved groups into an Excel file with each group as a separate sheet.

        Input:
        - None

        Returns:
        - None
        """
        if not self.saved_groups:
            messagebox.showinfo("No Saved Groups", "No groups have been saved yet.")
            return

        # Ask user to select a directory to save the Excel file
        directory_path = filedialog.askdirectory()

        if directory_path:
            # Create a file path in the selected directory
            file_path = os.path.join(directory_path, "saved_groups.xlsx")

            # Create an Excel writer object
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                # Write each group to a separate sheet
                for group_name, grouped_data in self.saved_groups.items():
                    grouped_data.to_excel(writer, sheet_name=group_name, index=False)

            messagebox.showinfo("Export Successful", f"Saved groups have been exported to '{file_path}'.")
