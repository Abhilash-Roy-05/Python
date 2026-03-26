import numpy as np
import math
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

class Transformer3D:
    """Mathematical engine for 3D transformations using homogeneous coordinates."""
    
    def translation_matrix(self, tx, ty, tz):
        return np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])

    def scaling_matrix(self, sx, sy, sz):
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    def rotation_x_matrix(self, angle_degrees):
        rad = math.radians(angle_degrees)
        c, s = math.cos(rad), math.sin(rad)
        return np.array([
            [1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]
        ])

    def rotation_y_matrix(self, angle_degrees):
        rad = math.radians(angle_degrees)
        c, s = math.cos(rad), math.sin(rad)
        return np.array([
            [c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]
        ])

    def rotation_z_matrix(self, angle_degrees):
        rad = math.radians(angle_degrees)
        c, s = math.cos(rad), math.sin(rad)
        return np.array([
            [c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]
        ])

    def reflection_xy_matrix(self):
        return np.diag([1, 1, -1, 1])

    def reflection_yz_matrix(self):
        return np.diag([-1, 1, 1, 1])

    def reflection_xz_matrix(self):
        return np.diag([1, -1, 1, 1])

    def apply_matrix_to_points(self, points, matrix):
        """Applies a 4x4 matrix to a list of [x, y, z] points."""
        points_hom = np.hstack([points, np.ones((len(points), 1))])
        transformed_hom = np.dot(points_hom, matrix.T)
        return transformed_hom[:, :3]

class TransformerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Transformer Visualizer")
        self.root.geometry("1100x750")
        
        self.transformer = Transformer3D()
        
        # Initial geometry
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6),
            (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        self.generate_cuboid(1, 1, 1) # Default cube
        
        self.setup_ui()
        self.update_plot()

    def generate_cuboid(self, w, h, d):
        """Creates vertices for a cuboid of given dimensions starting at origin."""
        self.original_vertices = np.array([
            [0, 0, 0], [w, 0, 0], [w, h, 0], [0, h, 0],
            [0, 0, d], [w, 0, d], [w, h, d], [0, h, d]
        ])
        self.current_vertices = self.original_vertices.copy()

    def setup_ui(self):
        # Main Layout: Left panel for controls, Right panel for plot
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.control_panel = ttk.LabelFrame(self.main_frame, text="Controls", padding="10")
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # --- Shape Generator ---
        ttk.Label(self.control_panel, text="Shape Selector:", font=('Helvetica', 10, 'bold')).pack(pady=(10, 0))
        
        # Shape type dropdown
        shape_type_frame = ttk.Frame(self.control_panel)
        shape_type_frame.pack(pady=5)
        ttk.Label(shape_type_frame, text="Type:").pack(side=tk.LEFT, padx=2)
        self.shape_type = tk.StringVar(value="Cube")
        self.shape_combo = ttk.Combobox(shape_type_frame, textvariable=self.shape_type, 
                                        values=["Cube", "Cuboid"], width=10, state="readonly")
        self.shape_combo.pack(side=tk.LEFT, padx=2)
        self.shape_combo.bind("<<ComboboxSelected>>", self.on_shape_type_changed)
        
        # Dimension inputs frame
        self.dim_frame = ttk.Frame(self.control_panel)
        self.dim_frame.pack(pady=5)
        
        # Cube size input (shown for Cube)
        self.cube_size_frame = ttk.Frame(self.dim_frame)
        ttk.Label(self.cube_size_frame, text="Size:").pack(side=tk.LEFT, padx=2)
        self.cube_size_entry = self.add_entry(self.cube_size_frame, "1")
        
        # Cuboid dimension inputs (shown for Cuboid)
        self.cuboid_dim_frame = ttk.Frame(self.dim_frame)
        ttk.Label(self.cuboid_dim_frame, text="W:").pack(side=tk.LEFT, padx=2)
        self.w_entry = self.add_entry(self.cuboid_dim_frame, "1")
        ttk.Label(self.cuboid_dim_frame, text="H:").pack(side=tk.LEFT, padx=2)
        self.h_entry = self.add_entry(self.cuboid_dim_frame, "1")
        ttk.Label(self.cuboid_dim_frame, text="D:").pack(side=tk.LEFT, padx=2)
        self.d_entry = self.add_entry(self.cuboid_dim_frame, "1")
        
        # Show appropriate inputs based on initial selection
        self.update_dimension_inputs()
        
        ttk.Button(self.control_panel, text="Create Shape", command=self.apply_new_shape).pack(pady=5)

        ttk.Separator(self.control_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # --- Translation ---
        ttk.Label(self.control_panel, text="Translation (tx, ty, tz):", font=('Helvetica', 10, 'bold')).pack(pady=(10, 0))
        trans_frame = ttk.Frame(self.control_panel)
        trans_frame.pack()
        self.tx_entry = self.add_entry(trans_frame, "0")
        self.ty_entry = self.add_entry(trans_frame, "0")
        self.tz_entry = self.add_entry(trans_frame, "0")
        ttk.Button(self.control_panel, text="Apply Translation", command=self.apply_translation).pack(pady=5)

        # --- Scaling ---
        ttk.Label(self.control_panel, text="Scaling (sx, sy, sz):", font=('Helvetica', 10, 'bold')).pack(pady=(10, 0))
        scale_frame = ttk.Frame(self.control_panel)
        scale_frame.pack()
        self.sx_entry = self.add_entry(scale_frame, "1")
        self.sy_entry = self.add_entry(scale_frame, "1")
        self.sz_entry = self.add_entry(scale_frame, "1")
        ttk.Button(self.control_panel, text="Apply Scaling", command=self.apply_scaling).pack(pady=5)

        # --- Rotation ---
        ttk.Label(self.control_panel, text="Rotation (Angle, Axis):", font=('Helvetica', 10, 'bold')).pack(pady=(10, 0))
        rot_frame = ttk.Frame(self.control_panel)
        rot_frame.pack()
        self.rot_angle = self.add_entry(rot_frame, "45")
        self.rot_axis = tk.StringVar(value="Z")
        ttk.Combobox(rot_frame, textvariable=self.rot_axis, values=["X", "Y", "Z"], width=5).pack(side=tk.LEFT)
        ttk.Button(self.control_panel, text="Apply Rotation", command=self.apply_rotation).pack(pady=5)

        # --- Reflection ---
        ttk.Label(self.control_panel, text="Reflection:", font=('Helvetica', 10, 'bold')).pack(pady=(10, 0))
        refl_frame = ttk.Frame(self.control_panel)
        refl_frame.pack()
        ttk.Button(refl_frame, text="XY", width=5, command=lambda: self.apply_reflection("XY")).pack(side=tk.LEFT, padx=2)
        ttk.Button(refl_frame, text="YZ", width=5, command=lambda: self.apply_reflection("YZ")).pack(side=tk.LEFT, padx=2)
        ttk.Button(refl_frame, text="XZ", width=5, command=lambda: self.apply_reflection("XZ")).pack(side=tk.LEFT, padx=2)

        ttk.Separator(self.control_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        ttk.Button(self.control_panel, text="Reset to Current Shape", command=self.reset).pack(pady=5)

        # --- Plot Panel ---
        self.plot_panel = ttk.Frame(self.main_frame)
        self.plot_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = plt.figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def add_entry(self, parent, default):
        entry = ttk.Entry(parent, width=6)
        entry.insert(0, default)
        entry.pack(side=tk.LEFT, padx=2)
        return entry

    def get_xyz(self, ex, ey, ez):
        try:
            return float(ex.get()), float(ey.get()), float(ez.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return None

    def on_shape_type_changed(self, event=None):
        """Called when shape type dropdown changes."""
        self.update_dimension_inputs()
    
    def update_dimension_inputs(self):
        """Show/hide dimension inputs based on selected shape type."""
        shape = self.shape_type.get()
        
        # Hide both frames first
        self.cube_size_frame.pack_forget()
        self.cuboid_dim_frame.pack_forget()
        
        # Show appropriate frame
        if shape == "Cube":
            self.cube_size_frame.pack()
        else:  # Cuboid
            self.cuboid_dim_frame.pack()
    
    def apply_new_shape(self):
        """Create a new shape based on the selected type."""
        shape = self.shape_type.get()
        
        if shape == "Cube":
            try:
                size = float(self.cube_size_entry.get())
                self.generate_cuboid(size, size, size)
                self.update_plot()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for size.")
        else:  # Cuboid
            dims = self.get_xyz(self.w_entry, self.h_entry, self.d_entry)
            if dims:
                self.generate_cuboid(*dims)
                self.update_plot()

    def apply_translation(self):
        vals = self.get_xyz(self.tx_entry, self.ty_entry, self.tz_entry)
        if vals:
            self.apply_and_update(self.transformer.translation_matrix(*vals))

    def apply_scaling(self):
        vals = self.get_xyz(self.sx_entry, self.sy_entry, self.sz_entry)
        if vals:
            self.apply_and_update(self.transformer.scaling_matrix(*vals))

    def apply_rotation(self):
        try:
            angle = float(self.rot_angle.get())
            axis = self.rot_axis.get()
            if axis == "X": matrix = self.transformer.rotation_x_matrix(angle)
            elif axis == "Y": matrix = self.transformer.rotation_y_matrix(angle)
            else: matrix = self.transformer.rotation_z_matrix(angle)
            self.apply_and_update(matrix)
        except ValueError:
            messagebox.showerror("Error", "Invalid angle.")

    def apply_reflection(self, plane):
        if plane == "XY": matrix = self.transformer.reflection_xy_matrix()
        elif plane == "YZ": matrix = self.transformer.reflection_yz_matrix()
        else: matrix = self.transformer.reflection_xz_matrix()
        self.apply_and_update(matrix)

    def apply_and_update(self, matrix):
        self.current_vertices = self.transformer.apply_matrix_to_points(self.current_vertices, matrix)
        self.update_plot()

    def reset(self):
        self.current_vertices = self.original_vertices.copy()
        self.update_plot()

    def update_plot(self):
        self.ax.clear()
        
        # Plot Original (Gray)
        for e in self.edges:
            p1, p2 = self.original_vertices[e[0]], self.original_vertices[e[1]]
            self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='gray', alpha=0.3)
        
        # Plot Transformed (Blue)
        for e in self.edges:
            p1, p2 = self.current_vertices[e[0]], self.current_vertices[e[1]]
            self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='blue', linewidth=2)
            
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title("3D Transformation View")
        
        # Auto-scale axis limits
        all_pts = np.vstack([self.original_vertices, self.current_vertices])
        x_min, x_max = all_pts[:,0].min(), all_pts[:,0].max()
        y_min, y_max = all_pts[:,1].min(), all_pts[:,1].max()
        z_min, z_max = all_pts[:,2].min(), all_pts[:,2].max()
        
        max_range = np.array([x_max-x_min, y_max-y_min, z_max-z_min]).max() / 2.0
        mid_x = (x_max+x_min) * 0.5
        mid_y = (y_max+y_min) * 0.5
        mid_z = (z_max+z_min) * 0.5
        
        # Ensure minimum range for small objects
        if max_range < 1: max_range = 1.0
        
        self.ax.set_xlim(mid_x - max_range, mid_x + max_range)
        self.ax.set_ylim(mid_y - max_range, mid_y + max_range)
        self.ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = TransformerApp(root)
    root.mainloop()
