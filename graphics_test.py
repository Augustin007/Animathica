import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.text as mtext

class CanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LaTeX Canvas")
        
        self.figure, self.ax = plt.subplots()
        self.figure.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.axis('off')
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.texts = {}
        
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.selected_text = None
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.rotating = False
        
    def spawn(self, latex_str, x, y, rotation=0):
        text = self.ax.text(x, y, f'${latex_str}$', fontsize=15, rotation=rotation, color='white', ha='center', va='center', picker=True)
        self.texts[text] = {"drag": False, "rotate": False}
        self.canvas.draw()
        return text
        
    def despawn(self, text):
        text.remove()
        del self.texts[text]
        self.canvas.draw()
        
    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        if event.key == 'shift':
            for text in self.texts:
                if text.contains(event)[0]:
                    self.selected_text = text
                    self.dragging = True
                    bbox = text.get_window_extent()
                    self.offset_x = bbox.x0 - event.x
                    self.offset_y = bbox.y0 - event.y
                    break
        elif event.key == 'control':
            for text in self.texts:
                if text.contains(event)[0]:
                    self.selected_text = text
                    self.rotating = True
                    self.start_angle = event.x
                    break
    
    def on_release(self, event):
        self.dragging = False
        self.rotating = False
        self.selected_text = None
    
    def on_motion(self, event):
        if not self.selected_text:
            return
        if self.dragging:
            x, y = event.x + self.offset_x, event.y + self.offset_y
            inv = self.ax.transData.inverted()
            x_data, y_data = inv.transform((x, y))
            self.selected_text.set_position((x_data, y_data))
            self.canvas.draw()
        elif self.rotating:
            delta_angle = (event.x - self.start_angle) / 5  # Arbitrary rotation sensitivity
            current_rotation = self.selected_text.get_rotation()
            self.selected_text.set_rotation(current_rotation + delta_angle)
            self.start_angle = event.x
            self.canvas.draw()

def mainloop():
    # lines = gather_lines(app.texts) : Uses positions and symbols to convert spawned symbols to nested structure according to lines in order of operations [[4,+,1],=,[2,+,3]] # Only do updating symbols?
    # When it requires calculation, CAS(line) which converts it into a CAS object.

    root.update()
    root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = CanvasApp(root)
    app.spawn(r'\int_{a}^{b} f(x)\,dx', 0.2, 0.8)
    app.spawn(r'e^{i\pi} + 1 = 0', 0.5, 0.5)
    mainloop()

