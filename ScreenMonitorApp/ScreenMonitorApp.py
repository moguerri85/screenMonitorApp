# -*- mode: python ; coding: utf-8 -*-

import tkinter as tk
import os
import configparser
import cv2
import requests
import threading
import time
import mss
import numpy as np
import pyautogui
import pygetwindow as gw
import ctypes
from ctypes import wintypes
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, font
from screeninfo import get_monitors



# URL dell'API delle release di GitHub
GITHUB_RELEASES_API_URL = "https://api.github.com/repos/moguerri85/screenMonitorApp/releases/latest"

CURRENT_VERSION = "1.1.1"  # Versione corrente dell'app

# Definisci le proprietà del font
font_family = "Arial"
font_size = 12
font_style = "bold"

class ScreenMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Monitor App")
        # Impostazioni di default
        self.monitor_index = tk.IntVar(value=1)  # Default to second monitor
        self.sensitivity = tk.DoubleVar(value=500000)  # Sensibilita al cambiamento
        self.tabs_to_navigate = tk.IntVar(value=0)  # Numero di tab per raggiungere il monitor
        self.rights_to_navigate = tk.IntVar(value=1)  # Numero di frecce destra per selezionare il monitor

        self.monitoring = False

        # Crea il menu
        self.create_menu()
        
        #Carico il main
        self.open_main()

        # Carica impostazioni all'avvio
        self.load_settings()

        # Controlla aggiornamenti all'avvio
        self.check_for_updates()

    def create_menu(self):
        # Creazione della barra dei menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Creazione del menu "File"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        # Aggiunta della voce "Impostazioni" al menu "File"
        file_menu.add_command(label="Main", command=self.open_main)

        # Aggiunta della voce "Impostazioni" al menu "File"
        file_menu.add_command(label="Impostazioni", command=self.open_settings)

        # Aggiunta della voce "Esci" al menu "File"
        file_menu.add_command(label="Esci", command=self.exit_app)

    def exit_app(self):
        # Conferma dell'uscita
        if messagebox.askokcancel("Esci", "Vuoi davvero uscire dall'applicazione?"):
            self.root.quit()   

    def open_main(self):
        # Imposta le dimensioni massime della finestra
        #self.root.maxsize(850, 300)
        self.root.minsize(850, 300)

        # Frame Main
        main_frame = ttk.LabelFrame(root, text="Operazione")
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        style = ttk.Style()
        style.configure("MyStyleStart.TButton", font=("Arial", 12, "bold"), background="white")
        style.configure("MyStyleStop.TButton", font=("Arial", 12, "bold"), background="white")
        style.configure("MyStylePulisci.TButton", font=("Arial", 12, "bold"), background="white")

        # Pulsante per avviare il monitoraggio
        start_button = ttk.Button(main_frame, text="Avvia Monitoraggio", command=self.start_monitoring, style="MyStyleStart.TButton")
        start_button.grid(row=1, column=0, padx=5, pady=5)

        # Pulsante per interrompere il monitoraggio
        stop_button = ttk.Button(main_frame, text="Interrompi Monitoraggio", command=self.stop_monitoring, style="MyStyleStop.TButton")
        stop_button.grid(row=1, column=1, padx=5, pady=5)

        # Create a frame to hold the image
        self.image1_frame = ttk.LabelFrame(main_frame, text="Immagine Principale")
        self.image1_frame.grid(row=2, column=0, columnspan=1, padx=5, pady=5)

        # Create a label to display the image (initially empty)
        self.image1_label = ttk.Label(self.image1_frame, image="")
        self.image1_label.grid(row=2, column=0)

        # Create a frame to hold the image
        self.image2_frame = ttk.LabelFrame(main_frame, text="Immagine Corrente")
        self.image2_frame.grid(row=2, column=1, columnspan=1, padx=5, pady=5)

        # Create a label to display the image (initially empty)
        self.image2_label = ttk.Label(self.image2_frame, image="")
        self.image2_label.grid(row=2, column=1)

        # Etichetta per lo stato
        self.label = ttk.Label(root, text="Pronto")
        self.label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        #Frame coountdown
        countdown_frame = ttk.LabelFrame(root, text="Messaggi")
        countdown_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        # Creiamo un'area di testo per visualizzare i messaggi
        self.text_area = tk.Text(countdown_frame, height=10, width=50)
        self.text_area.grid(row=1, column=2, padx=5, pady=5)
        #self.text_area.pack()
        # Pulsante per pulire i messaggi
        pulisci_button = ttk.Button(countdown_frame, text="Pulisci i messaggi", command=self.pulisci_messaggi, style="MyStylePulisci.TButton")
        pulisci_button.grid(row=2, column=2, padx=5, pady=5)


    def open_settings(self):
        # Frame per le impostazioni
        settings_frame = ttk.LabelFrame(root, text="Impostazioni")
        settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


        settings_frame.grid_rowconfigure(2, weight=1)
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=1)

        # Menu a tendina per selezionare il monitor       
        monitor_label = ttk.Label(settings_frame, text="Seleziona il Monitor:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        monitors = [f"Monitor {i+1}" for i in range(len(get_monitors()))]
        monitor_menu = ttk.Combobox(settings_frame, values=monitors)
        monitor_menu.grid(row=0, column=1, padx=5, pady=5)

        # Configura la Combobox per salvare l'indice del monitor
        try:
            monitor_menu.current(self.monitor_index.get())  # Imposta il monitor selezionato
        except Exception as e:
            messagebox.showerror("Errore Monitor", f"Errore durante la selezione del monitor: {str(e)}")
        monitor_menu.bind("<<ComboboxSelected>>", lambda event: self.monitor_index.set(monitor_menu.current()))

        # Sensibilità
        sensitivity_label = ttk.Label(settings_frame, text="Sensibilita':")
        sensitivity_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        sensitivity_scale = ttk.Scale(settings_frame, variable=self.sensitivity, from_=100000, to=1000000, orient="horizontal")
        sensitivity_scale.grid(row=2, column=1, padx=5, pady=5)

        # Tabs per navigare
        tabs_label = ttk.Label(settings_frame, text="Numero di Tabs per raggiungere il monitor:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tabs_entry = ttk.Entry(settings_frame, textvariable=self.tabs_to_navigate).grid(row=3, column=1, padx=5, pady=5)

        # Frecce a destra per selezionare il monitor
        rights_label = ttk.Label(settings_frame, text="Numero di Frecce Destra per selezionare il monitor:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        rights_entry = ttk.Entry(settings_frame, textvariable=self.rights_to_navigate).grid(row=4, column=1, padx=5, pady=5)

        # Pulsante per salvare le impostazioni
        save_button = ttk.Button(settings_frame, text="Salva Impostazioni", command=self.save_settings)
        save_button.grid(row=5, column=0, padx=5, pady=5)

        # Pulsante per caricare le impostazioni
        load_button = ttk.Button(settings_frame, text="Carica Impostazioni", command=self.load_settings)
        load_button.grid(row=5, column=1, padx=5, pady=5)

    def cambia_colore(self, azione):
        style = ttk.Style()
        if "start" in azione:
            style.configure("MyStyleStart.TButton", background="red")
            style.configure("MyStyleStop.TButton", background="white")
        else:
            style.configure("MyStyleStart.TButton", background="white")
            style.configure("MyStyleStop.TButton", background="white")

    def start_monitoring(self):
        self.cambia_colore("start")
        
        self.monitoring = True
        self.pulisci_messaggi()  # Elimina tutto il testo
        self.text_area.insert(tk.END, "Monitoraggio avviato..." + "\n")
        self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso
        self.label.config(text="Monitoraggio avviato...")
        
        # Esegui il monitoraggio in un thread separato
        self.monitor_thread = threading.Thread(target=self.monitoring_monitor)
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.cambia_colore("stop")
        self.monitoring = False
        self.pulisci_messaggi()  # Elimina tutto il testo
        self.text_area.insert(tk.END, "Monitoraggio interrotto." + "\n")
        self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso
        self.label.config(text="Monitoraggio interrotto.")

    def monitoring_monitor(self):
        # Capture the initial image of the second screen
        self.initial_img = self.capture_screen()
        self.update_image1(self.initial_img)
        self.sharing = False

        while self.monitoring:
            self.current_img = self.capture_screen()
            # Update the image on the label
            self.update_image2(self.current_img)

            if self.detect_change(self.initial_img, self.current_img):
                if not self.sharing:
                    self.pulisci_messaggi()  # Elimina tutto il testo
                    self.text_area.insert(tk.END, "Cambiamento rilevato! Avvio della condivisione dello schermo su Zoom..." + "\n")
                    self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso
                    #self.label.config(text="Cambiamento rilevato! Avvio della condivisione dello schermo su Zoom...")
                    self.sharing = True

                    self.countdown_thread = threading.Thread(target=self.countdown(5, "inizia"))
                    self.start_zoom_sharing()
                    
                    self.countdown_thread.start()
                    # Attende che entrambi i thread finiscano
                    self.countdown_thread.join()
                    
            else:
                if self.sharing:
                    self.text_area.insert(tk.END, "Schermo tornato allo stato iniziale. Interruzione della condivisione su Zoom..." + "\n")
                    self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso
                    #self.label.config(text="Schermo tornato allo stato iniziale. Interruzione della condivisione su Zoom...")
                    self.sharing = False
                    self.countdown_thread = threading.Thread(target=self.countdown(5, "inizia"))
                    self.stop_zoom_sharing()
                    self.countdown_thread.start()
                    # Attende che entrambi i thread finiscano
                    self.countdown_thread.join()
                    
            time.sleep(2)  # Check every 2 seconds

    def capture_screen(self):
        with mss.mss() as sct:
            monitor = get_monitors()[self.monitor_index.get()]
            monitor_info = {"top": monitor.y, "left": monitor.x, 
                            "width": monitor.width, "height": monitor.height}
            img = sct.grab(monitor_info)
            return np.array(img)

    def update_image1(self, img):
        # Convert the NumPy array to a PIL Image object
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Assuming BGR format
        pil_image = Image.fromarray(img_rgb)

        # Resize the image if necessary (adjust dimensions as needed)
        resized_image = pil_image.resize((100, 70), Image.LANCZOS)  # Example resize

        # Convert the PIL Image to a PhotoImage object for Tkinter display
        image_tk = ImageTk.PhotoImage(resized_image)

        # Update the image label with the new image
        self.image1_label.config(image=image_tk)
        self.image1_label.image = image_tk  # Keep a reference to avoid garbage collection   

    def update_image2(self, img):
        # Convert the NumPy array to a PIL Image object
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Assuming BGR format
        pil_image = Image.fromarray(img_rgb)

        # Resize the image if necessary (adjust dimensions as needed)
        resized_image = pil_image.resize((100, 70), Image.LANCZOS)  # Example resize

        # Convert the PIL Image to a PhotoImage object for Tkinter display
        image_tk = ImageTk.PhotoImage(resized_image)

        # Update the image label with the new image
        self.image2_label.config(image=image_tk)
        self.image2_label.image = image_tk  # Keep a reference to avoid garbage collection  

    def detect_change(self, img1, img2):
        diff = np.sum(np.abs(img1 - img2))
        return diff > self.sensitivity.get()

    def start_zoom_sharing(self):
        try:
            # Porta la finestra di Zoom in primo piano (assicurati che Zoom sia già in primo piano)
            # Questo potrebbe essere fatto manualmente o tramite pyautogui con le scorciatoie
            #Trova la finestra di Zoom per titolo (modifica il titolo se necessario)
            zoom_windows = gw.getWindowsWithTitle("Zoom Riunione")
            if zoom_windows:
                print(f"Trovate {len(zoom_windows)} finestre di Zoom.")
                # Porta la finestra di Zoom in primo piano
                zoom_windows = zoom_windows[0]
                zoom_windows.activate()  # Porta la finestra in primo piano

                time.sleep(1)  # Aggiunge un piccolo ritardo per sicurezza

                # Simula la combinazione di tasti per avviare la condivisione dello schermo
                pyautogui.hotkey('alt', 's')  # Su Windows/Linux
                time.sleep(1)

                # Naviga nella finestra di selezione della condivisione
                for _ in range(self.tabs_to_navigate.get()):
                    pyautogui.press('tab')
                    time.sleep(1)

                for _ in range(self.rights_to_navigate.get()):
                    pyautogui.press('right')
                    time.sleep(1)

                pyautogui.press('enter')
                self.text_area.insert(tk.END, "Condivisione dello schermo su Zoom avviata." + "\n")
                self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso
                #self.label.config(text="Condivisione dello schermo su Zoom avviata.")
                
            else:
                self.text_area.insert(tk.END, "Finestra di zoom non trovata." + "\n")
                self.text_area.insert(tk.END, "Verificare e\\o effettuare condivisione manualmente." + "\n")
                self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso
                
                #self.label.config(text="Finestra di zoom non trovata.")
            
        except Exception as e:
            self.unblock_mouse()
            self.text_area.insert(tk.END, f"Errore durante l'avvio della condivisione: {e}" + "\n")
            self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso
            #self.label.config(text=f"Errore durante l'avvio della condivisione: {e}")
            self.stop_zoom_sharing()

    def stop_zoom_sharing(self):        
        try:
            zoom_windows = gw.getWindowsWithTitle("Comandi riunione con condivisione schermo")
            if zoom_windows:
                # Porta la finestra di Zoom in primo piano
                zoom_window = zoom_windows[0]
                zoom_window.activate()  # Porta la finestra in primo piano
                time.sleep(1)  # Aggiunge un piccolo ritardo per sicurezza

                # Simula la combinazione di tasti per avviare la condivisione dello schermo
                pyautogui.hotkey('alt', 's')  # Su Windows/Linux
                self.text_area.insert(tk.END, f"Condivisione termata." + "\n")
                self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso
            else:
                self.text_area.insert(tk.END, "Finestra di zoom non trovata." + "\n")
                self.text_area.insert(tk.END, "Verificare e\\o interrompere la condivisione manualmente." + "\n")
                self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso

        except Exception as e:
            self.unblock_mouse()
            self.text_area.insert(tk.END, f"Errore durante il tentativo di fermare la condivisione su Zoom: {e}" + "\n")
            self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso

    def save_settings(self):
        # Ottieni la directory principale dell'utente
        appdata_path = os.path.join(os.getenv('APPDATA'), 'ScreenMonitorApp')
        settings_path = os.path.join(appdata_path, 'settings.ini')
        config = configparser.ConfigParser()
        config['Settings'] = {
            'monitor_index': self.monitor_index.get(),
            'sensitivity': self.sensitivity.get(),
            'tabs_to_navigate': self.tabs_to_navigate.get(),
            'rights_to_navigate': self.rights_to_navigate.get()
        }
        with open(settings_path, 'w') as configfile:
            config.write(configfile)
        self.label.config(text="Impostazioni salvate con successo.")

    def countdown(self, seconds, azione):

        start_time = time.time()
        self.block_mouse()
        while seconds > 0:
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            # Controllo se è trascorso un secondo intero
            if elapsed_time >= 1:
                seconds -= 1
                start_time = current_time  # Resetta il timer di inizio per il prossimo secondo
                self.text_area.insert(tk.END, f"Condivisione schermo {azione} tra {seconds} secondi..." + "\n")
                self.text_area.insert(tk.END, f"Non effettuare altre operazioni con il mouse o tastiera" + "\n")
                self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso

        self.unblock_mouse()
        self.text_area.insert(tk.END, f"Operazione completata" + "\n")
        self.text_area.yview(tk.END)  # Scorri l'area di testo verso il basso
        
    def load_settings(self):
        # Ottieni la directory principale dell'utente
        appdata_path = os.path.join(os.getenv('APPDATA'), 'ScreenMonitorApp')
        settings_path = os.path.join(appdata_path, 'settings.ini')
        config = configparser.ConfigParser()
        try:
            if not os.path.exists(settings_path):
                config['Settings'] = {'monitor_index': '0', 'sensitivity': '500000', 'tabs_to_navigate': '0', 'rights_to_navigate': '1'}

                self.write_file(config)
                self.label.config(text="File ini creato.")
                self.load_settings()
            else:    
                config.read(settings_path)
                self.monitor_index.set(config.getint('Settings', 'monitor_index', fallback=1))
                self.sensitivity.set(config.getfloat('Settings', 'sensitivity', fallback=500000))
                self.tabs_to_navigate.set(config.getint('Settings', 'tabs_to_navigate', fallback=0))
                self.rights_to_navigate.set(config.getint('Settings', 'rights_to_navigate', fallback=1))

                self.label.config(text="Impostazioni caricate.")
        except FileNotFoundError:
            self.label.config(text="Nessuna impostazione trovata. Utilizzando le impostazioni predefinite.")

    def write_file(self, config):
        # Ottieni la directory principale dell'utente
        user_home = os.path.expanduser("~")
        settings_dir = os.path.join(user_home, 'ScreenMonitorApp')
        settings_path = os.path.join(settings_dir, 'settings.ini')
        with open(settings_path, "w") as file:
            config.write(file)

    def check_for_updates(self):
        try:
            response = requests.get(GITHUB_RELEASES_API_URL)
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release['tag_name']
            if self.is_newer_version(latest_version, CURRENT_VERSION):
                download_url = latest_release['html_url']
                if messagebox.askyesno("Aggiornamento Disponibile", f"Disponibile una nuova versione ({latest_version}). Vuoi scaricarla?"):
                    self.download_update(download_url)
            else:
                self.label.config(text="Nessun aggiornamento disponibile.")
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                self.label.config(text="Nessuna release trovata sul repository GitHub.")
            else:
                self.label.config(text=f"Errore HTTP durante il controllo degli aggiornamenti: {http_err}")
        except requests.RequestException as e:
            self.label.config(text=f"Errore durante il controllo degli aggiornamenti: {e}")
    
    def is_newer_version(self, latest_version, current_version):
        latest_version_tuple = tuple(map(int, latest_version.strip('v').split('.')))
        current_version_tuple = tuple(map(int, current_version.strip('v').split('.')))
        return latest_version_tuple > current_version_tuple

    def download_update(self, url):
        import webbrowser
        webbrowser.open(url)
        
    # Definisci la funzione WinAPI ClipCursor
    user32 = ctypes.windll.user32

    def block_mouse(self):
        # Definisci il rettangolo (left, top, right, bottom) in cui il mouse può muoversi.
        # Se vuoi bloccare il mouse in una posizione fissa, imposta left = right e top = bottom.
        rect = wintypes.RECT()
        rect.left = 0    # Modifica queste coordinate in base alla tua esigenza
        rect.top = 0
        rect.right = 0
        rect.bottom = 0
        
        self.user32.ClipCursor(ctypes.byref(rect))  # Limita il mouse alla posizione specificata
        self.label.config(text=f"Mouse bloccato")

    def unblock_mouse(self):
        # Sblocca il mouse consentendo il movimento libero
        self.user32.ClipCursor(None)
        self.label.config(text=f"Mouse sbloccato")

    def pulisci_messaggi(self):
        self.text_area.delete(1.0, tk.END)  # Elimina tutto il testo

def ensure_settings_file():
    # Ottieni la directory principale dell'utente
    appdata_path = os.path.join(os.getenv('APPDATA'), 'ScreenMonitorApp')
    settings_path = os.path.join(appdata_path, 'settings.ini')

    # Se il file non esiste, crearlo con valori predefiniti
    if not os.path.exists(settings_path):
        config = configparser.ConfigParser()
        config['Settings'] = {'monitor_index': '0', 'sensitivity': '500000', 'tabs_to_navigate': '0', 'rights_to_navigate': '1'}
        
        # Creare la cartella se non esiste
        os.makedirs(appdata_path, exist_ok=True)
        
        # Scrivere il file
        with open(settings_path, 'w') as configfile:
            config.write(configfile)
            
        print(f"File di configurazione creato: {settings_path}")
    else:
        print(f"File di configurazione esistente: {settings_path}")

if __name__ == "__main__":
    root = tk.Tk()
    ensure_settings_file()
    app = ScreenMonitorApp(root)
    root.mainloop()
