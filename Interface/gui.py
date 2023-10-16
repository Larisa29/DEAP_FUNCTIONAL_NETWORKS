import os
import pandas as pd
import re
from configurations.config import ROOT_DIR
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Graphs.graph_visualization import GraphHandler
from PIL import ImageTk, Image

bands = ['Alpha', 'Beta']
connectivity_types = ["PLI", "WPLI", "coherence"]
deap_subjects_path = os.path.join(ROOT_DIR, "Data", "DEAP Subjects")

def get_emotion(selected_subject, selected_trial):
    """
    Functie necesara pentru a extrage clasa asociata unui subiect si trial specific, pe baza scorurilor din fisierul
    participant_ratings_class.csv.
    """
    # verific daca userul e fericit pe baza scorurilor stocate in fisierul participant_ratings_class
    participant_class_path = os.path.join(ROOT_DIR, "Data", "participant_ratings_class.csv")
    participant_class_df = pd.read_csv(participant_class_path)
    subject_id = selected_subject[-2:]
    if subject_id[0] == '0':
        subject_id = subject_id[1:]
    subject_id = int(subject_id)
    trial_id = int(selected_trial.split(" ")[-1])

    emotion = participant_class_df.query("Participant_id == @subject_id and Trial == @trial_id")['Emotion'].values[0]
    if emotion == 1:
        return "fericire"
    else:
        return "tristete"

class Application(tk.Frame):
    """
    Clasa Application este destinata interfetei grafice.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Retele functionale")
        #setez dimensiunea ferestrei
        self.master.geometry('1100x700')

        self.title_label = tk.Label(self.master, text="Vizualizare grafuri", font=("Helvetica", 16))
        self.title_label.pack(pady=15)

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(padx=50, pady=50)

        # frame pentru combobox-uri
        self.combobox_frame = tk.Frame(self.main_frame, bd=1, relief=tk.SOLID)
        self.combobox_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # frame pentru canvas
        self.canvas_frame = tk.Frame(self.main_frame, bd=1, relief=tk.SOLID)
        self.canvas_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.subjects = sorted(os.listdir(deap_subjects_path))

        label1 = tk.Label(self.combobox_frame, text="Participant:")
        label1.grid(row=0, column=0, sticky="E", padx=10, pady=10)
        self.cb1 = ttk.Combobox(self.combobox_frame, values=self.subjects)
        self.cb1.grid(row=0, column=1, padx=10, pady=10)

        label2 = tk.Label(self.combobox_frame, text="Trial:")
        label2.grid(row=1, column=0, sticky="E", padx=10, pady=10)
        self.cb2 = ttk.Combobox(self.combobox_frame)
        self.cb2.grid(row=1, column=1, padx=10, pady=10)

        label3 = tk.Label(self.combobox_frame, text="Metoda conectivitate:")
        label3.grid(row=2, column=0, sticky="E", padx=10, pady=10)
        self.cb3 = ttk.Combobox(self.combobox_frame)
        self.cb3.grid(row=2, column=1, padx=10, pady=10)

        label4 = tk.Label(self.combobox_frame, text="Banda de frecventa:")
        label4.grid(row=3, column=0, sticky="E", padx=10, pady=10)
        self.cb4 = ttk.Combobox(self.combobox_frame)
        self.cb4.grid(row=3, column=1, padx=10, pady=10)

        # adaug evenimente pentru a actualiza valorile combobox-urilor in functie de selectiile anterioare
        self.cb1.bind('<<ComboboxSelected>>', self.update_cb2_values)
        self.cb2.bind('<<ComboboxSelected>>', self.update_cb3_values)
        self.cb3.bind('<<ComboboxSelected>>', self.update_cb4_values)

        self.show_graph_button = tk.Button(self.combobox_frame, text="Show Graph", command=self.show_graph)
        self.show_graph_button.grid(row=4, columnspan=2, padx=10, pady=10)

        self.text_label = tk.Label(self.combobox_frame, text="Emotie:")
        self.text_label.grid(row=5, column=0, sticky="E", padx=10, pady=10)
        self.text_entry = ttk.Entry(self.combobox_frame, state='readonly')
        self.text_entry.grid(row=5, column=1, padx=10, pady=10)

        self.canvas_label = tk.Label(self.canvas_frame, width=800, height=650, bd=0, highlightthickness=0)
        self.canvas_label.pack(padx=10, pady=10)
        self.canvas_label.config(bg="white")

    def update_cb2_values(self, event):
        selected_subject = self.cb1.get()
        subfolders_path = os.path.join(deap_subjects_path, selected_subject, 'Trials')
        subfolders = sorted(os.listdir(subfolders_path))
        print(subfolders)
        self.cb2['values'] = subfolders
        self.cb2.set("")

    def update_cb3_values(self, event):
        selected_subfolder = self.cb2.get()
        values_for_cb3 = connectivity_types
        self.cb3.set('')
        self.cb3['values'] = values_for_cb3

    def update_cb4_values(self, event):
        selected_subfolder = self.cb3.get()
        values_for_cb4 = bands
        self.cb4.set('')
        self.cb4['values'] = values_for_cb4

    def show_graph(self):
        """
        Functia este responsabila cu plasarea efectiva a grafurilor in interfata si cu vizualizarea optiunilor din combobox-uri.
        """
        selected_subject = self.cb1.get()
        selected_trial = self.cb2.get()
        selected_connectivity_measure = self.cb3.get()
        selected_band = self.cb4.get()
        graph_data_path = os.path.join(ROOT_DIR, deap_subjects_path, selected_subject, "Trials", selected_trial, selected_connectivity_measure,f'{selected_connectivity_measure}_results_for_{selected_band}_band.csv')

        # verificare completare combobox-uri
        if not all([self.cb1.get(), self.cb2.get(), self.cb3.get(), self.cb4.get()]):
            messagebox.showerror("Error", "Selectati o varianta pentru toate combobox-urile!")
            return

        graph_handler = GraphHandler(graph_data_path)
        graph = graph_handler.create_graph()
        graph_handler.visualize_graph(graph)
        emotion = get_emotion(selected_subject, selected_trial)
        self.text_entry.configure(state='normal')
        # sterg textul existent din campul de text
        self.text_entry.delete(0, 'end')
        # adaug textul returnat de functie in campul de text
        self.text_entry.insert(0, emotion)
        self.text_entry.configure(state='readonly')
        image = Image.open("graph.png")
        image = image.resize((850, 450))
        photo = ImageTk.PhotoImage(image)
        self.canvas_label.configure(image=photo)
        self.canvas_label.image = photo