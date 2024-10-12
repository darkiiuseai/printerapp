import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from tkinter import ttk
import win32ui
import win32print
import win32con
from PIL import Image, ImageTk
from PyPDF2 import PdfReader
from docx import Document
import os
import zipfile
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class PrinterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Application d'Impression")

        self.file_list = []
        self.history = []
        self.load_user_preferences()

        self.create_widgets()
        self.populate_printer_list()

    def create_widgets(self):
        # Sélection de l'imprimante
        self.printer_label = tk.Label(self.master, text="Sélectionner une imprimante:")
        self.printer_label.pack()
        self.printer_name = tk.StringVar()
        self.printer_menu = tk.OptionMenu(self.master, self.printer_name, [])
        self.printer_menu.pack()

        # Ajout de fichiers
        self.add_file_button = tk.Button(self.master, text="Ajouter un fichier", command=self.add_file)
        self.add_file_button.pack()

        self.add_multiple_files_button = tk.Button(self.master, text="Ajouter plusieurs fichiers", command=self.add_multiple_files)
        self.add_multiple_files_button.pack()

        # Aperçu avant impression
        self.preview_button = tk.Button(self.master, text="Aperçu avant impression", command=self.preview_files)
        self.preview_button.pack()

        # Options de planification
        self.schedule_frame = tk.Frame(self.master)
        self.schedule_frame.pack()
        self.schedule_label = tk.Label(self.schedule_frame, text="Planifier l'impression (JJ/MM/AAAA HH:MM):")
        self.schedule_label.pack(side=tk.LEFT)
        self.schedule_entry = tk.Entry(self.schedule_frame)
        self.schedule_entry.pack(side=tk.LEFT)

        # Qualité d'impression
        self.quality_label = tk.Label(self.master, text="Qualité d'impression:")
        self.quality_label.pack()
        self.quality_var = tk.StringVar(value='Normal')
        self.quality_options = ['Économie', 'Normal', 'Haute qualité']
        self.quality_menu = tk.OptionMenu(self.master, self.quality_var, *self.quality_options)
        self.quality_menu.pack()

        # Option recto verso
        self.duplex_var = tk.BooleanVar(value=False)
        self.duplex_check = tk.Checkbutton(self.master, text="Impression recto-verso", variable=self.duplex_var)
        self.duplex_check.pack()

        # Sauvegarder les configurations
        self.save_config_button = tk.Button(self.master, text="Sauvegarder Configurations", command=self.save_print_configuration)
        self.save_config_button.pack()

        # Charger les configurations
        self.load_config_button = tk.Button(self.master, text="Charger Configurations", command=self.load_print_configuration)
        self.load_config_button.pack()

        # Historique d'impression
        self.history_label = tk.Label(self.master, text="Historique des impressions:")
        self.history_label.pack()
        self.history_listbox = tk.Listbox(self.master, height=5)
        self.history_listbox.pack()

        self.clear_history_button = tk.Button(self.master, text="Effacer l'historique", command=self.clear_print_history)
        self.clear_history_button.pack()

        # Filigrane
        self.watermark_var = tk.StringVar()
        self.watermark_label = tk.Label(self.master, text="Ajouter un filigrane (optionnel) :")
        self.watermark_label.pack()
        self.watermark_entry = tk.Entry(self.master, textvariable=self.watermark_var)
        self.watermark_entry.pack()

        # Bouton Imprimer
        self.print_button = tk.Button(self.master, text="Imprimer", command=self.print_files)
        self.print_button.pack()

    def populate_printer_list(self):
        """Liste les imprimantes disponibles."""
        printers = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
        self.printer_menu['menu'].delete(0, 'end')
        for printer in printers:
            self.printer_menu['menu'].add_command(label=printer, command=tk._setit(self.printer_name, printer))

    def add_file(self):
        """Ajouter un fichier à la liste."""
        file_path = filedialog.askopenfilename(filetypes=[("Tous les fichiers", "*.*")])
        if file_path:
            self.file_list.append(file_path)
            messagebox.showinfo("Fichier ajouté", f"{file_path} a été ajouté.")

    def add_multiple_files(self):
        """Ajouter plusieurs fichiers à la liste."""
        file_paths = filedialog.askopenfilenames(filetypes=[("Tous les fichiers", "*.*")])
        if file_paths:
            self.file_list.extend(file_paths)
            messagebox.showinfo("Fichiers ajoutés", f"{len(file_paths)} fichier(s) ajouté(s).")

    def preview_files(self):
        """Affiche un aperçu des fichiers avant impression."""
        if self.file_list:
            preview = "\n".join(self.file_list)
            messagebox.showinfo("Aperçu avant impression", f"Fichiers sélectionnés:\n{preview}")
        else:
            messagebox.showwarning("Aperçu", "Aucun fichier sélectionné.")

    def print_files(self):
        """Imprime les fichiers sélectionnés."""
        if not self.file_list:
            messagebox.showwarning("Erreur", "Aucun fichier à imprimer.")
            return

        # Récupérer les paramètres d'impression
        printer_name = self.printer_name.get()
        quality = self.quality_var.get()
        duplex = self.duplex_var.get()
        watermark_text = self.watermark_var.get()

        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        hdc.StartDoc("Impression de fichiers")
        hdc.StartPage()

        for file_path in self.file_list:
            self.print_individual_file(hdc, file_path, watermark_text)

        hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()

        # Mise à jour de l'historique
        self.update_print_history(self.file_list)
        self.file_list = []

    def print_individual_file(self, hdc, file_path, watermark_text):
        """Imprime un fichier individuel avec éventuellement un filigrane."""
        if file_path.endswith(".txt"):
            with open(file_path, "r") as f:
                content = f.read()
            hdc.TextOut(100, 100, content)
        elif file_path.endswith((".jpg", ".jpeg", ".png")):
            img = Image.open(file_path)
            img = img.convert("RGB")
            img.save("temp_img.bmp")
            hdc.BitBlt((0, 0), img.size, win32ui.CreateBitmapFromImage("temp_img.bmp"))
        # Ajoutez d'autres formats selon besoin (PDF, DOCX...)
        
        # Ajouter le filigrane si spécifié
        if watermark_text:
            hdc.TextOut(500, 500, watermark_text)

    def schedule_printing(self):
        """Planifie l'impression."""
        schedule_time = self.schedule_entry.get()
        try:
            scheduled_datetime = datetime.strptime(schedule_time, "%d/%m/%Y %H:%M")
            current_datetime = datetime.now()
            if scheduled_datetime > current_datetime:
                delay = (scheduled_datetime - current_datetime).total_seconds()
                self.master.after(int(delay * 1000), self.print_files)
                messagebox.showinfo("Planification", f"L'impression est planifiée pour {schedule_time}.")
            else:
                messagebox.showwarning("Erreur", "La date doit être dans le futur.")
        except ValueError:
            messagebox.showerror("Erreur", "Format de date invalide.")

    def save_print_configuration(self):
        """Sauvegarde les configurations d'impression."""
        config = {
            'printer_name': self.printer_name.get(),
            'quality': self.quality_var.get(),
            'duplex': self.duplex_var.get(),
            'schedule_time': self.schedule_entry.get(),
            'watermark': self.watermark_var.get()
        }
        with open('print_config.json', 'w') as f:
            json.dump(config, f)
        messagebox.showinfo("Sauvegarde", "Configurations sauvegardées.")

    def load_print_configuration(self):
        """Charge les configurations depuis un fichier."""
        try:
            with open('print_config.json', 'r') as f:
                config = json.load(f)
            self.printer_name.set(config['printer_name'])
            self.quality_var.set(config['quality'])
            self.duplex_var.set(config['duplex'])
            self.schedule_entry.delete(0, tk.END)
            self.schedule_entry.insert(0, config['schedule_time'])
            self.watermark_var.set(config['watermark'])
            messagebox.showinfo("Chargement", "Configurations chargées.")
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Aucune configuration trouvée.")

    def update_print_history(self, file_list):
        """Met à jour l'historique d'impression."""
        for file in file_list:
            self.history.append(f"Imprimé : {file}")
            self.history_listbox.insert(tk.END, f"Imprimé : {file}")

    def clear_print_history(self):
        """Efface l'historique d'impression."""
        self.history_listbox.delete(0, tk.END)
        self.history = []

    def load_user_preferences(self):
        """Charge les préférences utilisateur."""
        try:
            with open('user_preferences.txt', 'r') as f:
                preferences = json.load(f)
                self.printer_name.set(preferences.get('printer_name', ''))
        except FileNotFoundError:
            pass

    def send_email_notification(self, recipient_email):
        """Envoie un email après l'impression."""
        message = MIMEMultipart()
        message['From'] = "your_email@gmail.com"
        message['To'] = recipient_email
        message['Subject'] = "Notification d'impression"
        body = "Vos fichiers ont été imprimés avec succès."
        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_password")
        text = message.as_string()
        server.sendmail("your_email@gmail.com", recipient_email, text)
        server.quit()
        messagebox.showinfo("Email envoyé", "Une notification par email a été envoyée.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrinterApp(root)
    root.mainloop()
