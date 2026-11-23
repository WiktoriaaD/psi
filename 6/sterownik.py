import matplotlib.pyplot as plt
import numpy as np

#DANE
POZIOMY_OSOB = [1, 5, 9]
POZIOMY_WILGOTNOSCI = [25, 55, 85] 
POZIOMY_TEMPERATURY = [18, 25, 32] 
# ==============================================================================


def gauss(x, c, sigma):
    return np.exp(-0.5 * ((x - c) / sigma) ** 2)


#wejscia
temp_centers, temp_sigma = [18.0, 25.0, 32.0], 3.5
wilg_centers, wilg_sigma = [30.0, 55.0, 80.0], 14.0
osob_centers, osob_sigma = [1.0, 5.0, 9.0], 2.2

#wyjscie
y_grid = np.linspace(0, 100, 101)
moc_mf = [gauss(y_grid, c, 12.0) for c in [10.0, 30.0, 50.0, 70.0, 90.0]]


def oblicz_moc(temp, wilg, osoby):
    #rozmycie
    mu_t = [gauss(temp, c, temp_sigma) for c in temp_centers]
    mu_w = [gauss(wilg, c, wilg_sigma) for c in wilg_centers]
    mu_o = [gauss(osoby, c, osob_sigma) for c in osob_centers]

    #wnioskowanie
    zagregowane = np.zeros_like(y_grid)
    for i in range(3):  # temperatura (1.0)
        for j in range(3):  # Wilgotnośc (0.5)
            for k in range(3):  #osoby (waga 0.25)
                
                aktywacja = mu_t[i] * mu_w[j] * mu_o[k]

                # wazona
                wynik = 1.0 * i + 0.5 * j + 0.25 * k
                idx_wyjscia = int(round((wynik / 3.5) * 4))

                zbior_reguly = np.minimum(aktywacja, moc_mf[idx_wyjscia])
                zagregowane = np.maximum(zagregowane, zbior_reguly)
#wyostrzanie
    return np.sum(y_grid * zagregowane) / (np.sum(zagregowane) + 1e-12)


# rysujaca
def rysuj_zestaw(tytul_okna, poziomy, x_zakres, y_zakres, x_label, y_label, tryb):
    X, Y = np.meshgrid(x_zakres, y_zakres)
    fig = plt.figure(figsize=(15, 4.8))
    fig.canvas.manager.set_window_title(tytul_okna)

    for idx, stala in enumerate(poziomy, 1):
        Z = np.zeros_like(X)
        for r in range(X.shape[0]):
            for c in range(X.shape[1]):
                if tryb == "osoby":
                    Z[r, c] = oblicz_moc(X[r, c], Y[r, c], stala)
                elif tryb == "wilg":
                    Z[r, c] = oblicz_moc(X[r, c], stala, Y[r, c])
                elif tryb == "temp":
                    Z[r, c] = oblicz_moc(stala, X[r, c], Y[r, c])

        ax = fig.add_subplot(1, 3, idx, projection="3d")
        ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
        ax.set_title(f"{tytul_okna}: {stala}")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_zlabel("Moc (%)")
        ax.set_zlim(0, 100)

    plt.tight_layout()


T_os = np.linspace(16, 34, 30)
W_os = np.linspace(20, 90, 30)
O_os = np.linspace(0, 10, 30)

# okienka
rysuj_zestaw(
    "Stała liczba osób",
    POZIOMY_OSOB,
    T_os,
    W_os,
    "Temp (°C)",
    "Wilg (%)",
    "osoby",
)
rysuj_zestaw(
    "Stała wilgotność (%)",
    POZIOMY_WILGOTNOSCI,
    T_os,
    O_os,
    "Temp (°C)",
    "Osoby",
    "wilg",
)
rysuj_zestaw(
    "Stała temperatura (°C)",
    POZIOMY_TEMPERATURY,
    W_os,
    O_os,
    "Wilg (%)",
    "Osoby",
    "temp",
)

plt.show()
