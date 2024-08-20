# Screen Monitor App

## Descrizione
Screen Monitor App è un'applicazione Python con interfaccia grafica (GUI) progettata per monitorare l'attività dello schermo. Utilizza la libreria OpenCV per rilevare cambiamenti significativi sullo schermo e può eseguire azioni automatiche in risposta a questi cambiamenti. L'app è dotata di un menu intuitivo per la configurazione delle impostazioni e la navigazione delle varie funzionalità.

## Prerequisiti
Prima di eseguire l'applicazione, assicurati di avere installato le seguenti librerie Python:

- `tkinter`: Libreria per l'interfaccia grafica.
- `opencv-python`: Utilizzata per l'elaborazione delle immagini.
- `requests`: Per effettuare richieste HTTP, come il controllo degli aggiornamenti.
- `mss`: Per catturare screenshot.
- `numpy`: Per la manipolazione di array, necessaria per l'elaborazione delle immagini.
- `pyautogui`: Per l'automazione della GUI.
- `pygetwindow`: Per la gestione delle finestre GUI.
- `Pillow`: Per la gestione delle immagini.
- `screeninfo`: Per ottenere informazioni sui monitor collegati.

## Installazione
Puoi installare le librerie necessarie eseguendo il seguente comando:

```bash
pip install -r requirements.txt
