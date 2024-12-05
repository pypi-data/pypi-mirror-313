import numpy as np

def _impulse_noise(sig,ratio):
    # Generating noise
    # Generate a noise sample consisting of values that are a little higer or lower than a few randomly selected values in the original data. 
    noise_sample = np.random.default_rng().uniform(0.75*max(sig), max(sig), int(ratio*len(sig)))
    # Generate an array of zeros with a size that is the difference of the sizes of the original data an the noise sample.
    zeros = np.zeros(len(sig) - len(noise_sample))
    # Add the noise sample to the zeros array to obtain the final noise with the same shape as that of the original data.
    noise = np.concatenate([noise_sample, zeros])
    # Shuffle the values in the noise to make sure the values are randomly placed.
    np.random.shuffle(noise)
    # Obtain data with the noise added.
    return noise

def load_signal(fileName,dataKey=None):
    """
    LoadSignal charge le signal échantillonné et sa fréquence d'échantillonnage d'un fichier fourni.
    
    Puis, il est transformé comme suit :
    
    sig = int8(128*(sig-np.mean(sig)))
    
    Enfin, il est sous-échantilloné pour réduire le nombre de points

    Parameters
    ----------
    fileName : string
        chemin vers le fichier contenant le signal
                
    dataKey : string, optional
        clé du signal à extraire du fichier (car les fichiers "Sensor_data.csv" et "rayonnement-solaire-vitesse-vent-tri-horaires-regionaux" contiennent plusieurs clés)
        
    Returns
    -------
    Fs : float64
        fréquence d'échantillonagé du signal 
    
    sig : ndarray
        signal lu dans le fichier
    """
    Fs=None
    sig=None
    if ".wav" in fileName:
        from scipy.io import wavfile
        Fs, sig = wavfile.read(fileName)
        sig = 255 * sig
        Fs = Fs
        Fs = Fs/2
        sig=sig[::2].flatten()
        sig=sig.flatten()
    elif "EEG.csv" in fileName:
        import pandas as pd
        dataKey="EEG"
        data=pd.read_csv(fileName)
        Fs=1/np.mean(data['Time'].values[1:]-data['Time'].values[:-1]).astype(float)
        sig=data[dataKey].values
        sig = sig*64 + _impulse_noise(sig,0.001)
            
    elif "_data.csv" in fileName:
        import re
        import pandas as pd
        with open(fileName, "r") as f:
            content=f.readlines()
            pattern = '"\d+,\d+"'
            for c in range(len(content)):
                result = re.findall(pattern, content[c])
                new = [i.replace('"','').replace(',','.') for i in result]
                for i in range(len(result)):
                    content[c]=content[c].replace(result[i],new[i])
        with open(fileName, "w") as f:
            f.write(''.join(content))
        data=pd.read_csv(fileName)
        data['Timestamp']=data['Timestamp'].values.astype('datetime64[s]')
        data['Timestamp']=data['Timestamp'].values-data['Timestamp'].values[0]
        Fs= 1/np.mean(data['Timestamp'].values[1:]-data['Timestamp'].values[:-1]).astype(float)
        if dataKey is not None:#=="Abs Humidity(g/m³)":
            try:
                sig=data[dataKey].values-np.mean(data[dataKey].values)
                sig = sig*128/(max(sig))
                sig = sig[::12]
                Fs = Fs/12
                sig = sig + _impulse_noise(sig,0.01)
            except KeyError:
                raise KeyError('Please select a dataKey from the following ones : '+', '.join(data.columns[1:]))
        else:
            raise ValueError('Please select a dataKey from the following ones : '+', '.join(data.columns[1:]))
    elif '_rayonnement-solaire-vitesse-vent-tri-horaires-regionaux' in fileName:
        import pandas as pd
        with open(fileName, "r") as f:
            content=f.readlines()
            for c in range(len(content)):
                content[c]=content[c].replace('+02:00','').replace('+01:00','')
        with open(fileName, "w") as f:
            f.write(''.join(content))
        data=pd.read_csv(fileName,delimiter=";")
        data['Date']=data['Date'].values.astype('datetime64[s]')
        data['Date']=data['Date'].values-data['Date'].values[0]
        Fs=1/np.mean(data['Date'].values[1:]-data['Date'].values[:-1]).astype(float)
        if dataKey=='Vitesse du vent à 100m (m/s)':
            try:
                if dataKey=='Vitesse du vent à 100m (m/s)':
                    sig=data[dataKey].values-np.mean(data[dataKey].values)
                    sig = sig*128/(max(sig))
                    sig = sig[2::16]
                    Fs = Fs/16
                else:
                    sig=data[dataKey].values-np.mean(data[dataKey].values)
                    sig = sig*255/(max(sig))
                    sig = sig[2::64]
                    Fs = Fs/64
            except KeyError:
                raise KeyError('Please select a dataKey from the following ones : '+', '.join(data.columns[1:]))
        else:
            raise KeyError('Please select the dataKey "Vitesse du vent à 100m (m/s)"')
    sig = sig.astype(np.int8)
    sig = sig.flatten()
    return Fs, sig
