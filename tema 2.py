import csv
import os

glosar = {}

def afiseaza_meniu():
    print("\n=== GLOSAR INTERACTIV ===")
    print("1. Adăugare termen")
    print("2. Căutare exactă")
    print("3. Căutare parțială")
    print("4. Actualizare termen")
    print("5. Ștergere termen")
    print("6. Afișare completă")
    print("7. Statistici")
    print("8. Salvare în CSV")
    print("9. Încărcare din CSV")
    print("0. Ieșire")
    print("========================")

def adauga_termen():
    termen = input("Introduceți termenul: ").strip().lower()
    if not termen:
        print("Eroare: Termenul nu poate fi gol.")
        return
    if termen in glosar:
        print(f"Eroare: Termenul '{termen}' există deja.")
        return
    definitie = input("Introduceți definiția: ").strip()
    categorie = input("Introduceți categoria: ").strip()
    exemplu = input("Introduceți exemplul: ").strip()
    if not definitie or not categorie:
        print("Eroare: Definiția și categoria sunt obligatorii.")
        return
    glosar[termen] = {
        "definiție": definitie,
        "categorie": categorie,
        "exemplu": exemplu
    }
    print(f"Termenul '{termen}' a fost adăugat cu succes.")

def cautare_exacta():
    termen = input("Introduceți termenul de căutat: ").strip().lower()
    if termen in glosar:
        info = glosar[termen]
        print(f"\nTermen: {termen}")
        print(f"  Definiție: {info['definiție']}")
        print(f"  Categorie: {info['categorie']}")
        print(f"  Exemplu: {info['exemplu']}")
    else:
        print(f"Termenul '{termen}' nu a fost găsit.")

def cautare_partiala():
    fragment = input("Introduceți fragmentul de căutat: ").strip().lower()
    if not fragment:
        print("Eroare: Fragmentul nu poate fi gol.")
        return
    rezultate = []
    for termen in glosar:
        if fragment in termen:
            rezultate.append(termen)
    if rezultate:
        print(f"\nTermeni găsiți ({len(rezultate)}):")
        for termen in sorted(rezultate):
            info = glosar[termen]
            print(f"  - {termen} ({info['categorie']})")
    else:
        print("Nu s-au găsit termeni care să conțină fragmentul specificat.")

def actualizeaza_termen():
    termen = input("Introduceți termenul de actualizat: ").strip().lower()
    if termen not in glosar:
        print(f"Eroare: Termenul '{termen}' nu există.")
        return
    print("\nCâmpuri disponibile:")
    print("1. definiție")
    print("2. categorie")
    print("3. exemplu")
    optiune = input("Alegeți câmpul de actualizat (1-3): ").strip()
    campuri = {"1": "definiție", "2": "categorie", "3": "exemplu"}
    if optiune not in campuri:
        print("Eroare: Opțiune invalidă.")
        return
    camp = campuri[optiune]
    valoare_noua = input(f"Introduceți noua valoare pentru '{camp}': ").strip()
    if not valoare_noua:
        print("Eroare: Valoarea nu poate fi goală.")
        return
    glosar[termen][camp] = valoare_noua
    print(f"'{camp}' pentru termenul '{termen}' a fost actualizat.")

def sterge_termen():
    termen = input("Introduceți termenul de șters: ").strip().lower()
    if termen in glosar:
        confirmare = input(f"Sigur doriți să ștergeți '{termen}'? (da/nu): ").strip().lower()
        if confirmare == "da":
            del glosar[termen]
            print(f"Termenul '{termen}' a fost șters.")
        else:
            print("Operațiune anulată.")
    else:
        print(f"Eroare: Termenul '{termen}' nu există.")

def afiseaza_complet():
    if not glosar:
        print("Glosarul este gol.")
        return
    print(f"\n=== GLOSAR COMPLET ({len(glosar)} termeni) ===")
    for termen in sorted(glosar.keys()):
        info = glosar[termen]
        print(f"\n{termen.upper()}")
        print(f"  Definiție: {info['definiție']}")
        print(f"  Categorie: {info['categorie']}")
        print(f"  Exemplu: {info['exemplu']}")

def afiseaza_statistici():
    if not glosar:
        print("Glosarul este gol. Nu există statistici.")
        return
    total = len(glosar)
    categorii = {}
    for info in glosar.values():
        cat = info["categorie"]
        categorii[cat] = categorii.get(cat, 0) + 1
    print(f"\n=== STATISTICI ===")
    print(f"Număr total de termeni: {total}")
    print("\nDistribuție pe categorii:")
    for cat in sorted(categorii.keys()):
        print(f"  {cat}: {categorii[cat]} termeni")

def salveaza_csv():
    nume_fisier = input("Introduceți numele fișierului CSV: ").strip()
    if not nume_fisier:
        nume_fisier = "glosar.csv"
    if not nume_fisier.endswith(".csv"):
        nume_fisier += ".csv"
    try:
        with open(nume_fisier, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["termen", "definiție", "categorie", "exemplu"])
            for termen, info in glosar.items():
                writer.writerow([termen, info["definiție"], info["categorie"], info["exemplu"]])
        print(f"Glosar salvat în '{nume_fisier}'.")
    except Exception as e:
        print(f"Eroare la salvare: {e}")

def incarca_csv():
    nume_fisier = input("Introduceți numele fișierului CSV: ").strip()
    if not nume_fisier:
        nume_fisier = "glosar.csv"
    if not nume_fisier.endswith(".csv"):
        nume_fisier += ".csv"
    if not os.path.exists(nume_fisier):
        print(f"Eroare: Fișierul '{nume_fisier}' nu există.")
        return
    try:
        global glosar
        glosar_temp = {}
        with open(nume_fisier, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                termen = row["termen"].strip().lower()
                glosar_temp[termen] = {
                    "definiție": row["definiție"],
                    "categorie": row["categorie"],
                    "exemplu": row["exemplu"]
                }
        glosar = glosar_temp
        print(f"Glosar încărcat din '{nume_fisier}' ({len(glosar)} termeni).")
    except Exception as e:
        print(f"Eroare la încărcare: {e}")

def main():
    while True:
        afiseaza_meniu()
        optiune = input("Alegeți o opțiune: ").strip()
        if optiune == "1":
            adauga_termen()
        elif optiune == "2":
            cautare_exacta()
        elif optiune == "3":
            cautare_partiala()
        elif optiune == "4":
            actualizeaza_termen()
        elif optiune == "5":
            sterge_termen()
        elif optiune == "6":
            afiseaza_complet()
        elif optiune == "7":
            afiseaza_statistici()
        elif optiune == "8":
            salveaza_csv()
        elif optiune == "9":
            incarca_csv()
        elif optiune == "0":
            print("La revedere!")
            break
        else:
            print("Opțiune invalidă. Încercați din nou.")

if __name__ == "__main__":
    main()