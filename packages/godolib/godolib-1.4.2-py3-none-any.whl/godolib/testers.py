from statsmodels.tsa.stattools import adfuller

class StationarityTester():
    """
    Esta clase se utiliza para evaluar la estacionariedad de una serie de tiempo
    utilizando la prueba de Dickey-Fuller aumentada (ADF). Si el p-valor de la
    prueba es mayor que un umbral específico, la serie se considera no 
    estacionaria.
    """

    def __init__(self, threshold):
        """
        Inicializa la clase StationarityTester con un umbral de significancia.

        Args:
            threshold (float): El valor umbral para el p-valor de la prueba ADF. 
            Si el p-valor es mayor que este umbral, se considerará que la serie 
            no es estacionaria.
        """
        self.threshold = threshold
    def evaluate(self, X, y=None):
        """
        Evalúa si una serie de tiempo es estacionaria o no, basándose en la 
        prueba ADF (Dickey-Fuller aumentada).

        Args:
            X (pd.Series o np.ndarray): Los valores de la serie de tiempo a evaluar.
            y (None): Este parámetro no se utiliza, pero está presente para 
            mantener la compatibilidad con el método 'evaluate' en otros contextos.

        Returns:
            evaluation (bool): True si la serie es no estacionaria (p-valor > threshold),
            False si la serie es estacionaria (p-valor <= threshold).
        """
        values = X.values
        adf_test = adfuller(values)
        if adf_test[1] > self.threshold:
            evaluation = True
        else:
            evaluation = False
        return evaluation