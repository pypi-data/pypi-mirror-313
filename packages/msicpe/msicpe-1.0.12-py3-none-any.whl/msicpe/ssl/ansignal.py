import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import os
import plotly.subplots as sp
from multiprocessing import Process
import time


def run_dash():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    decimationRatio=-1

    # Création des sous-graphiques
    fig = sp.make_subplots(rows=3, cols=1, subplot_titles=[
        "Time Domain Signal", "Frequency Spectrum", "Log Scale Spectrum"
    ])

    # Dictionnaire des fichiers de signaux
    signal_files = {
        'Cri sonar de chauve-souris': 'cs2',
        'Décollage d\'avion': 'avion',
        'Vibrations moteur': 'vib',
        'Echos Sonar': 'coque',
        'Parole': 'elephant',
        'EEG': 'EEG1'
    }

    # Layout de l'application
    app.layout = dbc.Container([
        html.H1("Signal Analyzer", className="text-center mt-4"),
        
        # Sélection du signal
        dbc.InputGroup([
            dbc.Col(dbc.Row([
                dbc.Col([
                #     html.Label("""Select a Signal (Enter a number between 1 and 6):
                # 1: Cri sonar de chauve-souris
                # 2: Décollage d'avion
                # 3: Vibrations moteur
                # 4: Echos SONAR
                # 5: Parole : 'éléphant'
                # 6: EEG"""),
                #     dcc.Input(id="signal-selector", type="number", min=1, max=6, step=1, placeholder="1 to 6"),
                    
                    html.Label("Select a Signal"),
                    dcc.Dropdown(['Cri sonar de chauve-souris', 'Décollage d\'avion', 'Vibrations moteur','Echos Sonar','Parole','EEG'], '',id="signal-selector"),
                    dbc.Button("Analyze Selected Signal", id="analyze-signal-btn", color="primary", className="mt-2"),
                ], className="text-center", width=6)
            ], className="mb-4 text-center"), width="6"),
            # Chargement de fichiers
            dbc.Col(dbc.Row([
                dbc.Col([
                    dbc.Label("Or upload signal and sampling rate files:"),
                    dcc.Upload(
                        id="upload-signal",
                        children=html.Div(["Drag and Drop or ", html.A("Select Signal File (.npy)")]),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "marginBottom": "10px",
                        }
                    ),
                    dcc.Upload(
                        id="upload-sampling-rate",
                        children=html.Div(["Drag and Drop or ", html.A("Select Sampling Rate File (.npy)")]),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "marginBottom": "10px",
                        }
                    ),
                ], width=6)
            ], className="mb-4 text-center"), width="6")  
        ], className="text-center mt-4"),
        # Sélection de la décimation
        dbc.Row([
            dbc.Col([
                html.H1("Decimation Ratio:", className="text-center mt-4"),
                dcc.Slider(id="decimation-slider", min=1, max=32, step=1, value=1,
                        marks={i: str(i) for i in range(1, 33)}),
                html.Div(id="selected-frequency", className="mt-2"),
            ], width=12)
        ], className="text-center mb-4"),
        
        # Bouton pour afficher le signal
        # dbc.Row([
        #     dbc.Col([
        #         dbc.Button("Display Signal", id="display-signal-btn", color="success", disabled=True, className="mt-2"),
        #     ], width=12)
        # ], className="mb-4 text-center"),
        
        # Graphiques
        dbc.Row([
            dbc.Col([html.H1("Resulting Plots:", className="text-center mt-4"),
                    dcc.Graph(id="signal-plot",figure=fig)
                # dcc.Loading(dcc.Graph(id="signal-plot",figure=fig), type="circle"),
            ], width=12)
        ]),
        html.Br(),
        dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Store(id="current-data",data={'isDisplayed':False, 'decimationRatio':-1})], fluid=True)

    # Variables globales pour stocker les données
    signal_data = {"signal": None, "sampling_rate": None, "title": None}

    # Callback combiné pour gérer la sélection de signal ou le chargement de fichiers
    @app.callback(
        [Output("selected-frequency", "children"),Output('interval-component','interval'),Output('current-data', 'data'),Output("signal-plot", "figure")],
        [Input("analyze-signal-btn", "n_clicks"),
        Input("upload-signal", "contents"),
        Input("upload-sampling-rate", "contents"),Input('current-data', 'data'),Input('interval-component', 'n_intervals')],
        [State("signal-selector", "value"),State("decimation-slider", "value")],
        prevent_initial_call=True
    )
    def update_signal(n_clicks, uploaded_signal, uploaded_rate, data, n_intervals,signal_choice,decimation_ratio):
        if signal_choice and n_clicks:
            # Chargement du signal préconfiguré
            if signal_choice not in signal_files:
                print(signal_choice)
                return "Please select a valid signal number (1 to 6).",60*1000 ,data, fig
            try:
                signal_path = os.path.join(os.path.dirname(__file__), signal_files[signal_choice] + "_signal.npy")
                rate_path = os.path.join(os.path.dirname(__file__), signal_files[signal_choice] + "_fe.npy")
                signal_data["signal"] = np.load(signal_path).flatten()
                signal_data["sampling_rate"] = np.load(rate_path).flatten()[0]
                signal_data["title"] = signal_files[signal_choice]
                data['isDisplayed']=True
                data['decimationRatio']=decimation_ratio            
                signal = signal_data["signal"]
                sampling_rate = signal_data["sampling_rate"] / data['decimationRatio']
                decimated_signal = signal[::decimation_ratio]
                t = np.arange(len(decimated_signal)) / sampling_rate
                
                # Calcul du spectre
                nfft = int(2 ** np.ceil(np.log2(decimated_signal.size)))
                spectrum = np.abs(np.fft.fft(decimated_signal, nfft))[:nfft // 2] ** 2
                freqs = np.linspace(0, sampling_rate / 2, nfft // 2)
                if len(fig.data)==0:
                    # Signal temporel
                    fig.add_scatter(x=t, y=decimated_signal, mode="lines", row=1, col=1)
                    # Spectre en fréquence
                    fig.add_scatter(x=freqs, y=spectrum, mode="lines", row=2, col=1)
                    # Spectre log
                    fig.add_scatter(x=freqs, y=10 * np.log10(spectrum / np.max(spectrum)), mode="lines", row=3, col=1)
                else:
                    # Signal temporel
                    fig.data[0].x=t
                    fig.data[0].y=decimated_signal
                    # Spectre en fréquence
                    fig.data[1].x=freqs
                    fig.data[1].y=spectrum
                    # Spectre log
                    fig.data[2].x=freqs
                    fig.data[2].y=10 * np.log10(spectrum / np.max(spectrum))
                fig.update_layout(height=800, title="Signal Analysis", template="plotly_white")
                return f"Sampling Rate: {int(sampling_rate)} Hz", 1000, data, fig
            except Exception as e:
                return f"Error loading signal: {str(e)}",60*1000 ,data, fig
        elif uploaded_signal and uploaded_rate:
            # Gestion des fichiers uploadés
            try:
                signal_data["signal"] = np.load(uploaded_signal)  # Remplacer par le contenu du fichier uploadé
                signal_data["sampling_rate"] = np.load(uploaded_rate)            
                data['isDisplayed']=True
                data['decimationRatio']=decimation_ratio            
                signal = signal_data["signal"]
                sampling_rate = signal_data["sampling_rate"] / data['decimationRatio']
                decimated_signal = signal[::decimation_ratio]
                t = np.arange(len(decimated_signal)) / sampling_rate
                
                # Calcul du spectre
                nfft = int(2 ** np.ceil(np.log2(len(decimated_signal))))
                spectrum = np.abs(np.fft.fft(decimated_signal, nfft))[:nfft // 2] ** 2
                freqs = np.linspace(0, sampling_rate / 2, nfft // 2)
                # Signal temporel
                fig.data[0].x=tuple(t)
                fig.data[0].y=tuple(decimated_signal)
                # Spectre en fréquence
                fig.data[1].x=tuple(freqs)
                fig.data[1].y=tuple(spectrum)
                # Spectre log
                fig.data[2].x=tuple(freqs)
                fig.data[2].y=tuple(10 * np.log10(spectrum / np.max(spectrum)))
                fig.update_layout(height=800, title="Signal Analysis", template="plotly_white")
                return f"Sampling Rate: {int(sampling_rate)} Hz", 1000,data, fig
            except Exception as e:
                return f"Error loading uploaded files: {str(e)}",60*1000 ,data, fig
        return "Please provide valid inputs.",60*1000 ,data, fig
    app.run_server(debug=True, use_reloader=False)


# Function to stop the server
def stop_server(pid):
    if sys.platform == 'win32':
        import signal
        os.kill(pid, signal.CTRL_C_EVENT)
    else:    
        logging.info("Sending shutdown request")
        os.kill(pid, 9)
        # requests.post('http://127.0.0.1:8050/shutdown')
    

def ansignal():#timeout=120):
    """
    Affichage pour comprendre les effets de la décimation
    
    Parameters
    ----------
    timeout : float
        Délai avant la fin d'exécution de la fonction
    """ 
    server_proc = Process(target=run_dash, 
                            name='dash_server', 
                            daemon=True)

    server_proc.start()
    pid = server_proc.pid
    
    # # # Run for 60 seconds
    # time.sleep(timeout)

    # # # Stop the Dash server by terminating the entire program
    # print("Stopping Dash server...")
    # stop_server(pid)
    # #lol, you sure you know what you're doing?
    # os.kill(os.getpid(), signal.SIGTERM)