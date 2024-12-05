import plotly.graph_objects as go 

def zplane(z, p):
    """
        Trace les zéros et pôles pour les systèmes en temps discret.

        Cette fonction trace les zéros spécifiés dans le vecteur colonne `z` et les pôles spécifiés
        dans le vecteur colonne `p` dans une nouvelle figure.


        Parameters
        ----------
        z : array_like
            Zéros et pôles. Peut être des vecteurs colonne ou des matrices.
        p : array_like
            Zéros et pôles. Peut être des vecteurs colonne ou des matrices.


        Example
        -------
        >>> from msicpe.tns import zplane
        >>> import numpy as np
        >>> z = np.array([1,1j])
        >>> p = np.array([0.,0.9j])
        >>> zplane(z, p)
        """
    
    fig = go.Figure()
    
    # Add circle
    fig.add_shape(type="circle",    line_color="blue",     x0=-1, y0=-1, x1=1, y1=1 )
    
    # Add zeros
    fig.add_trace(go.Scatter(mode='markers', 
                             name="zeros",
                             marker=dict(symbol="circle-open", size=10, line=dict(width=2, color="DarkSlateGrey")), 
                             x=z.real, 
                             y=z.imag))
    
    # Add poles
    fig.add_trace(go.Scatter(mode='markers', 
                             name="poles",
                             marker=dict(symbol="x-thin", size=10, line=dict(width=2, color="DarkSlateGrey")),  
                             x=p.real, 
                             y=p.imag))
    
    # Set figure properties
    fig.update_layout(
    width = 500,
    height = 500,
    title = "Diagramme Pôles-Zéros")
    
    
    fig.update_yaxes(range=[None, None], zeroline=True, zerolinecolor='Gray', showgrid=True, gridwidth=1, gridcolor='LightGray', scaleanchor="x",    scaleratio=1  )
    fig.update_xaxes(range=[None, None], zeroline=True, zerolinecolor='Gray', showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    fig.show()