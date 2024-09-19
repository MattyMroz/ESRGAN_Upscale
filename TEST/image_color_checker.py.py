import cv2
import numpy as np
import os


def is_grayscale_or_bw(image, threshold=0.05, color_threshold=0.1):
    if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
        return True

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

    diff_rg = np.abs(r - g)
    diff_rb = np.abs(r - b)
    diff_gb = np.abs(g - b)

    if (np.mean(diff_rg) < threshold) and (np.mean(diff_rb) < threshold) and (np.mean(diff_gb) < threshold):
        return True

    # Sprawdź, czy obraz ma wystarczająco dużo kolorów
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    if np.mean(hsv[:, :, 1]) < color_threshold * 255:
        return True

    return False


# Wczytaj obraz
img_path = '226.png'
if not os.path.exists(img_path):
    print(f"Błąd: Plik '{img_path}' nie istnieje. 😕")
else:
    img = cv2.imread(img_path)
    if img is None:
        print(f"Błąd: Nie można wczytać obrazu '{img_path}'. 😖")
    else:
        if is_grayscale_or_bw(img):
            print("Obraz jest czarno-biały lub w odcieniach szarości 🖤🤍")
            # Użyj modelu dla czarno-białych
        else:
            print("Obraz jest kolorowy 🌈")
            # Użyj modelu dla kolorowych

        # Dodatkowe informacje o obrazie
        print(f"Kształt obrazu: {img.shape}")
        print(f"Typ danych: {img.dtype}")
        print(f"Średnia wartość pikseli: {np.mean(img)}")
        print(f"Odchylenie standardowe pikseli: {np.std(img)}")
