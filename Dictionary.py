# Mapowanie sygnałów
signal_map = {
    "S1": "Szum o rozkładzie jednostajnym",
    "S2": "Szum Gaussowski",
    "S3": "Sygnał sinusoidalny",
    "S4": "Sygnał sinusoidalny wyprostowany jednopołówkowo",
    "S5": "Sygnał sinusoidalny wyprostowany dwupołówkowo",
    "S6": "Sygnał prostokątny",
    "S7": "Sygnał prostokątny symetryczny",
    "S8": "Sygnał trójkątny",
    "S9": "Skok jednostkowy",
    "S10": "Impuls jednostkowy",
    "S11": "Szum impulsowy"
}

# Początkowa lista parametrów
param_entries = {}

# Skróty dla parametrów
param_abbreviations = {
    "Amplituda (A)": "A",
    "Czas początkowy (t1)": "t1",
    "Czas trwania sygnału (d)": "d",
    "Okres podstawowy (T)": "T",
    "Współczynnik wypełnienia (kw)": "kw",
    "Czas skoku (ts)": "ts",
    "Numer próbki dla której następuje skos (ns)": "ns",
    "numer pierwszej próbki (n1)": "n1",
    "Częstotliwość próbkowania (f)": "f",
    "Prawdopodobieństwo wystąpienia A (p)": "p"
}

# Mapowanie parametrów dla sygnałów
signal_params_map = {
    "S1": ["A", "t1", "d"],
    "S2": ["A", "t1", "d"],
    "S3": ["A", "T", "t1", "d"],
    "S4": ["A", "T", "t1", "d"],
    "S5": ["A", "T", "t1", "d"],
    "S6": ["A", "T", "t1", "d", "kw"],
    "S7": ["A", "T", "t1", "d", "kw"],
    "S8": ["A", "T", "t1", "d", "kw"],
    "S9": ["A", "t1", "d", "ts"],
    "S10": ["A", "ns", "n1", "d", "f"],
    "S11": ["A", "t1", "d", "f", "p"]
}