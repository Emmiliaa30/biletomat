import json
import os

# FUNKCJE STRUKTURALNE
def wczytaj_cennik(sciezka):
    try:
        with open(sciezka, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Błąd: Nie znaleziono pliku cennik.json!")
        return None

def pobierz_znak(komunikat):
    while True:
        wejscie = input(komunikat).strip().lower()
        if len(wejscie) == 1:
            return wejscie
        print("Błąd: Wpisz tylko jeden znak!")

def wyswietl_koszyk(koszyk):
    if not koszyk:
        print("\nKoszyk jest pusty.")
        return 0
    suma = 0
    print("\n--- TWÓJ KOSZYK ---")
    for bilet in koszyk:
        print(f"- {bilet['nazwa']}: {bilet['cena']:.2f} PLN")
        suma += bilet['cena']
    print(f"RAZEM: {suma:.2f} PLN")
    return suma

def proces_platnosci(suma):
    print(f"\nDo zapłaty: {suma:.2f} PLN")
    while True:
        try:
            # Uwaga: Kwota płatności to jedyny moment, gdzie wpisujemy więcej znaków
            # (zgodnie z logiką maszyny przyjmującej banknoty/monety)
            wpłata = float(input("Wrzuć pieniądze (podaj kwotę): "))
            if wpłata < suma:
                print(f"Niewystarczająca kwota. Brakuje {(suma - wpłata):.2f} PLN")
                suma -= wpłata
            else:
                reszta = wpłata - suma
                print(f"Dziękujemy! Wydaję resztę: {reszta:.2f} PLN")
                print("Bilety zostały wydrukowane.")
                break
        except ValueError:
            print("Błąd: Podaj poprawną liczbę!")

def symulator():
    cennik = wczytaj_cennik('cennik.json')
    if not cennik: return
    
    koszyk = []
    sciezka_wyboru = [] # Przechowuje aktualny poziom w menu (np. ["normalny", "czasowy"])

    while True:
        # Pobierz aktualny poziom cennika na podstawie sciezki
        poziom = cennik
        for klucz in sciezka_wyboru:
            poziom = poziom[klucz]

        print(f"\n--- MENU: {' / '.join(sciezka_wyboru).upper() if sciezka_wyboru else 'START'} ---")
        
        opcje = list(poziom.keys())
        mapa_wyboru = {}

        # Wyświetlanie opcji
        for i, opcja in enumerate(opcje):
            klawisz = str(i + 1)
            mapa_wyboru[klawisz] = opcja
            cena = f"({poziom[opcja]} PLN)" if isinstance(poziom[opcja], (int, float)) else ""
            print(f"[{klawisz}] {opcja} {cena}")

        print("[K] Zobacz koszyk i zapłać")
        print("[R] Resetuj wybór / Powrót")
        print("[X] Wyjdź")

        znak = pobierz_znak("Wybór: ")

        if znak == 'x':
            break
        elif znak == 'r':
            sciezka_wyboru = []
        elif znak == 'k':
            suma = wyswietl_koszyk(koszyk)
            if suma > 0:
                decyzja = pobierz_znak("Czy chcesz zapłacić? (t/n): ")
                if decyzja == 't':
                    proces_platnosci(suma)
                    koszyk = []
                    sciezka_wyboru = []
        elif znak in mapa_wyboru:
            wybrany_klucz = mapa_wyboru[znak]
            if isinstance(poziom[wybrany_klucz], dict):
                sciezka_wyboru.append(wybrany_klucz)
            else:
                # To jest bilet (wartość liczbowa)
                bilet = {"nazwa": f"{' '.join(sciezka_wyboru)} {wybrany_klucz}", "cena": poziom[wybrany_klucz]}
                koszyk.append(bilet)
                print(f"DODANO: {bilet['nazwa']}")
                sciezka_wyboru = [] # Powrót do menu głównego po dodaniu
        else:
            print("Nieprawidłowy znak!")

if __name__ == "__main__":
    symulator()