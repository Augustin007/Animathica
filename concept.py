import tkinter as tk

class AnimathicaDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Animathica Demo")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.symbols = {}
        self.create_symbol("1", 100, 100)
        self.create_symbol("+", 150, 100)
        self.create_symbol("1", 200, 100)

        self.selected_symbol = None
        self.canvas.bind("<Button-1>", self.select_symbol)
        self.canvas.bind("<B1-Motion>", self.move_symbol)
        self.canvas.bind("<Double-1>", self.evaluate_expression)

    def create_symbol(self, text, x, y):
        symbol_id = self.canvas.create_text(x, y, text=text, font=("Courier", 24), fill="black", tags="symbol")
        self.symbols[symbol_id] = (text, x, y)
        return symbol_id

    def select_symbol(self, event):
        items = self.canvas.find_withtag("symbol")
        for item in items:
            if self.canvas.bbox(item)[0] <= event.x <= self.canvas.bbox(item)[2] and \
               self.canvas.bbox(item)[1] <= event.y <= self.canvas.bbox(item)[3]:
                self.selected_symbol = item
                break

    def move_symbol(self, event):
        if self.selected_symbol:
            self.canvas.coords(self.selected_symbol, event.x, event.y)

    def evaluate_expression(self, event):
        items = sorted(self.canvas.find_withtag("symbol"), key=lambda i: self.canvas.coords(i)[0])
        expression_parts = []
        y_coords = []

        for item in items:
            y = self.canvas.coords(item)[1]
            y_coords.append(y)
            expression_parts.append((self.canvas.itemcget(item, "text"), y))

        expression = ""
        for part, y in expression_parts:
            if part == '+':
                if abs(y - y_coords[0]) < 20:  # Allow a small vertical offset
                    expression += part
            else:
                if abs(y - y_coords[0]) < 20:  # Allow a small vertical offset
                    expression += part

        try:
            result = str(eval(expression))
            result_x = self.canvas.coords(items[-1])[0] + 50
            result_y = self.canvas.coords(items[-1])[1]
            self.create_symbol("=", result_x, result_y)
            for i, char in enumerate(result):
                self.create_symbol(char, result_x + (i + 1) * 25, result_y)
        except Exception as e:
            print(f"Error evaluating expression: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimathicaDemo(root)
    root.mainloop()

