from cgitb import text
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figureCanvas
from src.JsonReader import Json
from src.regression import Regression

class GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.frame_btn = tk.Frame(self.root, bg="white")
        self.frame_graph = tk.Frame(self.root, bg="white")
        self.canvas = None
        self.table = None
        self.data_to_predict = None
        self.predicted_data = None
        self.data = {}
        self.already_draw = False
        self.already_draw_select = False
        
        self.frame_btn.pack(side=tk.LEFT, expand=True, padx=20)
        self.frame_graph.pack(side=tk.RIGHT, expand=True)
    
    def start(self):
        self.root.title("Algorithms")
        self.root.geometry("770x450")
        self.root.configure(bg="white")

        if (len(self.data) > 0) and not self.already_draw_select:
            self.already_draw_select = True
            select_label = tk.Label(self.frame_btn, text="Select an algorithm to opereta the data", bg="white", font="Arial 10")
            select_label.pack()
            select_algorithm = ttk.Combobox(
                self.frame_btn,
                state="readonly",
                values=["Id3", "Apriori", "FPGrowth", "Decision tree", "K-Means", "SVM"],
            )
            select_algorithm.pack()
        elif not self.already_draw:
            self.already_draw = True
            load_file_btn = tk.Button(self.frame_btn, text="Load File", command=self.readFile)
            load_file_btn.pack()
            load_console_btn = tk.Button(self.frame_btn, text="Insert data in console", command=self.insert_data)
            load_console_btn.pack()

        """self.root.title("Linear Regression")
        self.root.geometry("770x450")
        self.root.configure(bg="white")

        load_label = tk.Label(self.frame_btn, text="Select a JSON file with the data to operate", bg="white", font="Arial 10")
        load_label.pack()

        load_file_btn = tk.Button(self.frame_btn, text="Load File", command=self.readFile)
        load_file_btn.pack()

        graph_label = tk.Label(self.frame_graph, text="Linear Regression Graph", font="Arial 15 bold", bg="white")
        graph_label.pack(pady=0)

        self.graph("", "", [], [], Regression([], []))"""

        self.root.mainloop()

    def readFile(self):
        path = askopenfile(mode='r', filetypes=[('JSON Files', '*.json')])
        
        if path is not None:
            self.data = Json(path.name).read()
            self.root.after(1, self.start)
            # self.executeRegression(x_name, y_name, x_data, y_data, data_to_predict)
    
    def insert_data(self):
        self.data = input("Insert the data in JSON format: ")
        self.root.after(1, self.start)

    def executeRegression(self, x_name, y_name, x_data, y_data, data_to_predict):
        regression = Regression(x_data, y_data)
        regression.start()
        predicted_data = regression.predict(data_to_predict)
        
        print("For {} = {} the predicted {} is {}".format(x_name, data_to_predict, y_name, predicted_data))
    
        x_data.append(data_to_predict)
        y_data.append(predicted_data)

        self.graph(x_name, y_name, x_data, y_data, regression)

    def graph(self, x_name, y_name, x_data, y_data, regression):
        self.drawTable(x_name, y_name, x_data, y_data, x_data[-1] if len(x_data) > 0 else 0, y_data[-1] if len(y_data) > 0 else 0)
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        canvas = figureCanvas(figure, self.frame_graph)
        ax.clear()
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.canvas = canvas
        
        ax.scatter(x_data, y_data, color='red')
        ax.plot(x_data, regression.predict_list(x_data), color='green')
        ax.set_title("{} vs {}".format(x_name, y_name))
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)

    def drawTable(self, x_name, y_name, x_data, y_data, data_to_predict, predicted_data):
        if self.table is not None:
            self.table.destroy()
            self.data_to_predict.destroy()
            self.predicted_data.destroy()

        table = ttk.Treeview(self.frame_btn, columns=(x_name, y_name), show="headings")
        table.column(x_name, width=100, anchor="center")
        table.column(y_name, width=100, anchor="center")
        table.heading(x_name, text=x_name)
        table.heading(y_name, text=y_name)

        for i in range(len(x_data) - 1):
            table.insert("", tk.END, values=(x_data[i], y_data[i]))

        data_to_predict_label = tk.Text(self.frame_btn, height=1, font="Arial 10", bg="white", width=20, borderwidth=0)
        data_to_predict_label.tag_configure("bold", font="Arial 10 bold")
        data_to_predict_label.insert(tk.END, "Data to predict: ", "bold")
        data_to_predict_label.insert(tk.END, data_to_predict)

        predicted_data_label = tk.Text(self.frame_btn, height=1, font="Arial 10", bg="white", width=20, borderwidth=0)
        predicted_data_label.tag_configure("bold", font="Arial 10 bold")
        predicted_data_label.insert(tk.END, "Predicted data: ", "bold")
        predicted_data_label.insert(tk.END, predicted_data)
        
        self.table = table
        self.data_to_predict = data_to_predict_label
        self.predicted_data = predicted_data_label
        table.pack(pady=30)
        data_to_predict_label.pack(pady=10)
        predicted_data_label.pack(pady=10)
