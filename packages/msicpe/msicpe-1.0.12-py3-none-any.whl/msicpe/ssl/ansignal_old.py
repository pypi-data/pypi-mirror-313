import tkinter as tk
from tkinter import filedialog
import numpy as np
import plotly.subplots as sp
import os

class SignalAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Signal Analyzer")

        # Label for signal selection
        signal_label = tk.Label(master, text="""Select a Signal (Enter a number between 1 and 6):
            1: Cri sonar de chauve-souris
            2: Décollage d'avion
            3: Vibrations moteur
            4: Echos SONAR
            5: Parole : 'éléphant'
            6: EEG""")
        signal_label.pack()

        # Entry box for signal selection
        self.signal_entry = tk.Entry(master, width=5)
        self.signal_entry.pack()

        # Frame for Load button
        load_frame = tk.Frame(master)
        load_frame.pack()

       # Button to analyze the selected signal
        self.analyze_button = tk.Button(load_frame, text="Analyze Selected Signal", command=self.select_signal)
        self.analyze_button.pack(side = tk.LEFT)

        # Load button
        self.load_button = tk.Button(load_frame, text="Analyze Loaded Files", command=self.load_signal)
        self.load_button.pack(side =  tk.RIGHT)

        # Frame for Load Cursor
        load_cursor = tk.Frame(master)
        load_cursor.pack()

        # Cursor
        self.decimation_var = tk.IntVar(value=1)  # Fréquence d'échantillonnage par défaut
        decimation_label = tk.Label(load_cursor, text="Decimation Ratio:")
        decimation_label.pack(side = tk.LEFT)
        self.decimation_slider = tk.Scale(load_cursor, from_=1, to=32, orient=tk.HORIZONTAL, 
                                              variable=self.decimation_var,
                                              command=self.update_frequency_label)
        self.decimation_slider.pack(side = tk.RIGHT)


        self.frequency_label = tk.Label(master, text="Selected Sampled Frequency: - ")
        self.frequency_label.pack()
    
        # Display button
        self.display_button = tk.Button(master, text="Display Signal", command=self.display_signal, state=tk.DISABLED)
        self.display_button.pack()

        # Data attributes
        self.signal = None
        self.sampling_rate = None

    # Function to handle signal selection
    def select_signal(self):
        signal_files = {
            1: 'cs2',
            2: 'avion',
            3: 'vib',
            4: 'coque',
            5: 'elephant',
            6: 'EEG1'
        }
        try:
            chsig = int(self.signal_entry.get())
            if chsig in signal_files:
                self.signal = np.load(os.path.join(os.path.dirname(__file__), signal_files[chsig] + '_signal.npy')).flatten()
                self.sampling_rate = np.load(os.path.join(os.path.dirname(__file__), signal_files[chsig] + '_fe.npy')).flatten()[0]
                self.title = signal_files[chsig]  # Get signal name
            else:
                self.show_error("Please enter a valid number between 1 and 6.")
        except ValueError:
            self.show_error("Please enter a valid integer.")
        self.update_frequency_label()
        self.display_button.config(state=tk.NORMAL)

    def load_signal(self):
        file_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file_path:
            self.signal = np.load(file_path).flatten()
        file_path = filedialog.askopenfilename(filetypes=[("NumPy files", "*.npy")])
        if file_path:
            self.sampling_rate = np.load(file_path).flatten()[0]
        self.update_frequency_label()
        self.display_button.config(state=tk.NORMAL)

    def update_frequency_label(self, event=None):
        try: 
            decimation_level = self.decimation_var.get()
            if self.sampling_rate is not None:
                frequency = int(self.sampling_rate / decimation_level)
                self.frequency_label.config(text=f"Selected Sampled Frequency: {frequency} Hz")
        except ValueError:
            pass  # Handle case where input is not an integer

    def display_signal(self):
        if self.signal is not None:
            if self.sampling_rate is not None:
                t = np.arange(len(self.signal)) / self.sampling_rate
                s = self.signal[::self.decimation_var.get()]

                # Calculate and plot frequency spectrum
                r = np.ceil(np.log2(len(s)))  # Calculer la puissance de 2 supérieure
                nfft = int(2 ** (r+1))  # Taille de la FFT
                z = np.abs(np.fft.fft(s, nfft))  # Calculer la FFT et prendre la valeur absolue
                S = z[:nfft // 2] ** 2  # Spectre en amplitude
                freq = np.arange(nfft // 2) * (self.sampling_rate / nfft)  # Fréquence normalisée

                # Create subplots
                fig = sp.make_subplots(rows=3, cols=1,
                                    subplot_titles=('Time Domain Signal', 'Frequency Spectrum', 'Frequency Spectrum (log scale)'),
                                    vertical_spacing=0.1)

                # Add Time Domain plot
                fig.add_scatter(x=t, y=s, mode='lines', name='Signal', row=1, col=1)
                fig.update_yaxes(title_text='Amplitude', row=1, col=1)
                fig.update_xaxes(title_text='Time (s)', row=1, col=1)

                # Add Frequency Spectrum plot (Linear Scale)
                fig.add_scatter(x=freq, y=S, mode='lines', name='Spectrum', row=2, col=1)
                fig.update_yaxes(title_text='Magnitude', row=2, col=1)
                fig.update_xaxes(title_text='Frequency (Hz)', row=2, col=1)

                # Add Frequency Spectrum plot (Log Scale)
                fig.add_scatter(x=freq, y=10 * np.log10(S/np.max(S)), name='Spectrum (dB)',row=3, col=1)
                fig.update_yaxes(title_text='Magnitude (dB)', range = [-25,2], row=3, col=1)
                fig.update_xaxes(title_text='Frequency (Hz)', row=3, col=1)

                # Update layout
                fig.update_layout(title='Signal Analysis', height=600, width=900, 
                                template='plotly_white')
                fig.show()

    def show_error(self, message):
        error_window = tk.Toplevel(self.master)
        error_window.title("Error")
        tk.Label(error_window, text=message).pack(padx=20, pady=20)
        tk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=5)

def ansignal_old(): 
    root = tk.Tk()
    app = SignalAnalyzerApp(root)
    root.mainloop()
