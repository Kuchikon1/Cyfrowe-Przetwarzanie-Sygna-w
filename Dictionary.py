#--------------------------- Lista Sygnałów ---------------------------

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

#--------------------------- Lista Konwersji ---------------------------

conversions = {
    "S": "(S) Próbkowanie równoramienne",
    "Q1": "(Q1) Kwantyzacja równoramienna z obcięciem",
    "Q2": "(Q2) Kwantyzacja równoramienna z zaokrągleniem",
    "R1": "(R1) Ekstrapolacja zerowego rzędu",
    "R2": "(R2) Interpolacja pierwszego rzędu",
    "R3": "(R3) Rekonstruckaj w opraciu o funkcję sinc",
    "C1": "(C1) Błąd średniokwadratowy",
    "C2": "(C2) Stosunek sygnał - szum",
    "C3": "(C3) Szczytowy stosunek sygnał - szum",
    "C4": "(C4) Maksymalna różnica",
    "A": "(A) Aliasing"
}

# Parametry dla konwersji
conversion_param_entries = {}

# Skróty dla parametrów konwersji
conversion_param_abbreviations = {
    "Częstotliwość próbkowania (f)": "f",
    "Liczba poziomów kwantyzacji (kw)": "kw",
    "Liczba sąsiadów (nb)": "nb",
}

# Mapowanie parametrów dla konwersji
conversions_params_map = {
    "S": ["f"],
    "Q1": ["kw"],
    "Q2": ["kw"],
    "R1": ["nb"],
    "R2": ["nb"],
    "R3": ["nb"],
    "C1": ["nb"],
    "C2": ["nb"],
    "C3": ["nb"],
    "C4": ["nb"],
    "A": ["nb"]
}