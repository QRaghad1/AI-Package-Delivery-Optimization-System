
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from package import Package
from vehicle import Vehicle
from main import run_algorithm_and_get_results
import matplotlib.pyplot as plt

packages = []
vehicles = []

def run_app():
    def update_capacity_entries():
        for widget in vehicle_frame.winfo_children():
            widget.destroy()

        try:
            count = int(vehicle_count_entry.get())
            capacity_entries.clear()
            for i in range(count):
                ttk.Label(vehicle_frame, text=f"🚚 Vehicle {i+1} Capacity (kg):", background=frame_bg, foreground='white', font=label_font).grid(row=i, column=0, sticky='w', pady=2)
                entry = ttk.Entry(vehicle_frame, width=10, font=input_font)
                entry.insert(0, "20")
                entry.grid(row=i, column=1, padx=5, pady=2)
                capacity_entries.append(entry)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of vehicles.")

    def set_vehicles():
        vehicles.clear()
        try:
            for entry in capacity_entries:
                capacity = int(entry.get())
                if capacity <= 0:
                    raise ValueError
                vehicles.append(Vehicle(capacity))
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid, positive capacities for all vehicles.")

    def add_package():
        try:
            x = float(dest_x_entry.get())
            y = float(dest_y_entry.get())
            weight = float(weight_entry.get())
            priority = int(priority_entry.get())

            if weight <= 0:
                messagebox.showerror("Error", "Weight must be positive")
                return

            if not (1 <= priority <= 5):
                messagebox.showerror("Error", "Priority must be between 1 and 5")
                return

            pkg = Package(x, y, weight, priority)
            packages.append(pkg)
            package_list.insert(tk.END, f"📍 ({x}, {y}) | ⚖️ {weight}kg | 🔝 Priority {priority}")
            for e in [dest_x_entry, dest_y_entry, weight_entry, priority_entry]:
                e.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers in all fields")

    def draw_routes(vehicles):
        plt.close('all')
        colors = ['#8b3a3a', '#5a1a1a', '#c94c4c', '#a63232', '#cc7a7a']
        shop = (0, 0)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(*shop, c='black', label='Warehouse', s=200, marker='s')

        for idx, vehicle in enumerate(vehicles):
            if not vehicle.packages:
                continue

            color = colors[idx % len(colors)]
            x_coords = [shop[0]] + [p.to_x for p in vehicle.packages] + [shop[0]]
            y_coords = [shop[1]] + [p.to_y for p in vehicle.packages] + [shop[1]]

            ax.plot(x_coords, y_coords, marker='o',
                    label=f'Vehicle {idx+1} ({vehicle.current_load()}/{vehicle.capacity}kg)',
                    color=color, linewidth=2, markersize=8)

            for pkg_num, pkg in enumerate(vehicle.packages, 1):
                ax.annotate(str(pkg_num), (pkg.to_x, pkg.to_y),
                            textcoords="offset points", xytext=(0, 5), ha='center')

        ax.set_title('Delivery Route Optimization')
        ax.set_xlabel('X Coordinate (km)')
        ax.set_ylabel('Y Coordinate (km)')
        ax.grid(True)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def on_run():
        if not vehicles:
            messagebox.showerror("Error", "Please set vehicles first")
            return
        if not packages:
            messagebox.showerror("Error", "Please add packages first")
            return

        try:
            algo = algo_var.get()
            result_vehicles, result_cost, unassigned = run_algorithm_and_get_results(
                algo, [v.capacity for v in vehicles], packages)

            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            total_distance = 0

            result_text.insert(tk.END, "📦 Delivery Optimization Results 📦\n", "header")
            result_text.insert(tk.END, "=" * 60 + "\n\n")

            for i, vehicle in enumerate(result_vehicles, 1):
                vehicle.calculate_route_distance()
                total_distance += vehicle.route_distance

                result_text.insert(tk.END,
                                   f"🚚 Vehicle {i} (Capacity: {vehicle.capacity}kg | Load: {vehicle.current_load()}kg)\n",
                                   "vehicle_header")
                result_text.insert(tk.END, f"🚣️ Route distance: {vehicle.route_distance:.2f}km\n")
                result_text.insert(tk.END, "📦 Packages:\n")

                for pkg_num, pkg in enumerate(vehicle.packages, 1):
                    result_text.insert(tk.END,
                                       f"  {pkg_num}. To ({pkg.to_x}, {pkg.to_y}) | Weight: {pkg.weight}kg | Priority: {pkg.priority}\n")

                result_text.insert(tk.END, "\n")

            result_text.insert(tk.END, "=" * 60 + "\n", "footer")
            result_text.insert(tk.END,
                               f"🌟 Total Cost: {result_cost:.8f} | Total Distance: {total_distance:.2f}km\n", "footer")
            result_text.config(state=tk.DISABLED)
            draw_routes(result_vehicles)

            if unassigned:
                messagebox.showwarning("Unassigned Packages",
                           f"{len(unassigned)} package(s) could not be assigned due to capacity limits.")
                result_text.config(state=tk.NORMAL)
                result_text.insert(tk.END, "\n❌ The following packages could not be delivered because they exceed capacity:\n", "unassigned")
                for pkg in unassigned:
                   result_text.insert(tk.END, f" - ({pkg.to_x}, {pkg.to_y}) | ⚖️ {pkg.weight}kg | Priority: {pkg.priority}\n")
                   result_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    # ---------- GUI Setup ----------
    root = tk.Tk()
    root.title("Advanced Delivery Route Optimizer")
    root.geometry("900x980")
    root.configure(bg='#fbeaec')

    capacity_entries = []

    # Styling
    frame_bg = '#5a1a1a'
    button_bg = '#000000'
    button_fg = '#000000'
    label_font = ('Arial', 12, 'bold')
    input_font = ('Arial', 12)
    header_font = ('Arial', 14, 'bold')

    style = ttk.Style()
    style.configure('TFrame', background=frame_bg)
    style.configure('TLabel', background=frame_bg, foreground='white', font=label_font)
    style.configure('TButton', font=('Arial', 11, 'bold'), background=button_bg, foreground=button_fg)
    style.map('TButton', background=[('active', '#732222')])

    main_frame = ttk.Frame(root, padding=10, style='TFrame')
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Vehicle Configuration
    vehicle_config_frame = ttk.LabelFrame(main_frame, text="🚚 Vehicle Configuration", padding=10, style='TFrame')
    vehicle_config_frame.pack(fill=tk.X, pady=5)

    ttk.Label(vehicle_config_frame, text="Number of Vehicles:").grid(row=0, column=0, sticky='w')
    vehicle_count_entry = ttk.Entry(vehicle_config_frame, width=5, font=input_font)
    vehicle_count_entry.insert(0, "3")
    vehicle_count_entry.grid(row=0, column=1, sticky='w', padx=5)

    ttk.Button(vehicle_config_frame, text="Set Vehicle Entries", command=update_capacity_entries).grid(row=0, column=2, padx=10)
    ttk.Button(vehicle_config_frame, text="Confirm Vehicles", command=set_vehicles).grid(row=0, column=3, padx=10)

    vehicle_frame = ttk.Frame(vehicle_config_frame, style='TFrame')
    vehicle_frame.grid(row=1, column=0, columnspan=4, pady=5, sticky='w')

    # Package Info
    package_frame = ttk.LabelFrame(main_frame, text="📦 Package Information", padding=10, style='TFrame')
    package_frame.pack(fill=tk.X, pady=5)

    dest_x_entry, dest_y_entry, weight_entry, priority_entry = [ttk.Entry(package_frame, font=input_font) for _ in range(4)]

    ttk.Label(package_frame, text="Destination X:").grid(row=0, column=0, sticky='w')
    dest_x_entry.grid(row=0, column=1, padx=5)
    ttk.Label(package_frame, text="Destination Y:").grid(row=1, column=0, sticky='w')
    dest_y_entry.grid(row=1, column=1, padx=5)
    ttk.Label(package_frame, text="Weight (kg):").grid(row=2, column=0, sticky='w')
    weight_entry.grid(row=2, column=1, padx=5)
    ttk.Label(package_frame, text="Priority (1=Highest, 5=Lowest):").grid(row=3, column=0, sticky='w')
    priority_entry.grid(row=3, column=1, padx=5)

    ttk.Button(package_frame, text="Add Package", command=add_package).grid(row=4, column=0, columnspan=2, pady=5)

    package_list = tk.Listbox(package_frame, height=6, width=60, font=('Arial', 11))
    package_list.grid(row=5, column=0, columnspan=2, pady=5)

    # Algorithm selection
    algo_frame = ttk.Frame(main_frame, style='TFrame')
    algo_frame.pack(fill=tk.X, pady=5)

    algo_var = tk.StringVar(value='sa')
    ttk.Label(algo_frame, text="Algorithm:").grid(row=0, column=0, sticky='w')
    algo_menu = ttk.Combobox(algo_frame, textvariable=algo_var, values=['sa', 'ga'], width=10, font=input_font, state='readonly')
    algo_menu.grid(row=0, column=1, padx=5)

    ttk.Button(algo_frame, text="Run Optimization", command=on_run).grid(row=0, column=2, padx=10)

    # Result frame
    result_frame = ttk.LabelFrame(main_frame, text="📊 Optimization Results", padding=10, style='TFrame')
    result_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    result_text = tk.Text(result_frame, height=20, width=85, wrap=tk.WORD,
                          font=('Consolas', 11), padx=5, pady=5, bg='#fff0f5', fg='black')
    result_text.pack(fill=tk.BOTH, expand=True)

    result_text.tag_config("header", foreground="#a63232", font=header_font)
    result_text.tag_config("vehicle_header", foreground="#e8a5b4", font=label_font)
    result_text.tag_config("footer", foreground="#000000", font=label_font)

    scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()

if __name__== "__main__":
    run_app()