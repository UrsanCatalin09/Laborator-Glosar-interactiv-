import csv
import json

def citeste_produse_csv(fisier):
    produse = {}
    try:
        with open(fisier, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                id_produs = int(row["id"])
                produse[id_produs] = {
                    "nume": row["nume"],
                    "pret": float(row["pret"]),
                    "stoc": int(row["stoc"])
                }
    except FileNotFoundError:
        print(f"Fisierul {fisier} nu a fost gasit.")
    except Exception as e:
        print(f"Eroare la citirea fisierului CSV: {e}")
    return produse

def citeste_reduceri_json(fisier):
    try:
        with open(fisier, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Fisierul {fisier} nu a fost gasit.")
    except Exception as e:
        print(f"Eroare la citirea fisierului JSON: {e}")
    return {}

def afiseaza_meniu(produse):
    print("\n--- MENIU PRODUSE ---")
    if not produse:
        print("Nu exista produse disponibile.")
        return
    for id_produs, info in produse.items():
        print(f"ID: {id_produs} | Nume: {info['nume']} | Pret: {info['pret']:.2f} lei | Stoc: {info['stoc']}")

def adauga_produs(comanda, produse, id_produs, cantitate):
    if id_produs not in produse:
        return False, "Produs inexistent."
    if cantitate <= 0:
        return False, "Cantitatea trebuie sa fie mai mare decat 0."
    cantitate_deja_comandata = comanda.get(id_produs, 0)
    stoc_real_disponibil = produse[id_produs]["stoc"] - cantitate_deja_comandata
    if cantitate > stoc_real_disponibil:
        return False, f"Cantitatea depaseste stocul disponibil. Disponibil: {stoc_real_disponibil}"
    comanda[id_produs] = cantitate_deja_comandata + cantitate
    return True, "Produs adaugat in comanda."

def scade_produs(comanda, id_produs, cantitate):
    if id_produs not in comanda:
        return False, "Produsul nu exista in comanda."
    if cantitate <= 0:
        return False, "Cantitatea trebuie sa fie mai mare decat 0."
    if cantitate > comanda[id_produs]:
        return False, "Nu poti scadea mai mult decat exista in comanda."
    comanda[id_produs] -= cantitate
    if comanda[id_produs] == 0:
        del comanda[id_produs]
    return True, "Comanda a fost actualizata."

def calculeaza_total(comanda, produse):
    total = 0
    for id_produs, cantitate in comanda.items():
        total += produse[id_produs]["pret"] * cantitate
    return total

def calculeaza_reducere(total, tip_reducere, reduceri):
    if tip_reducere == "" or tip_reducere == "fara":
        return 0
    if tip_reducere not in reduceri:
        return 0
    regula = reduceri[tip_reducere]
    prag = regula["prag"]
    tip = regula["tip"]
    valoare = regula["valoare"]
    if total < prag:
        print(f"Reducerea '{tip_reducere}' nu se aplica. Prag minim: {prag} lei.")
        return 0
    if tip == "procent":
        reducere = total * valoare / 100
    elif tip == "fix":
        reducere = valoare
    else:
        return 0
    if reducere > total:
        reducere = total
    return reducere

def genereaza_bon(comanda, produse, total, reducere):
    linii = []
    linii.append("======== BON FISCAL ========")
    for id_produs, cantitate in comanda.items():
        nume = produse[id_produs]["nume"]
        pret = produse[id_produs]["pret"]
        subtotal = pret * cantitate
        linii.append(f"{nume} | cantitate: {cantitate} | pret unitar: {pret:.2f} lei | subtotal: {subtotal:.2f} lei")
    total_final = total - reducere
    linii.append("----------------------------")
    linii.append(f"Total: {total:.2f} lei")
    linii.append(f"Reducere: {reducere:.2f} lei")
    linii.append(f"Total final: {total_final:.2f} lei")
    linii.append("============================")
    return "\n".join(linii)

def scrie_bon_txt(fisier, text_bon):
    try:
        with open(fisier, mode="w", encoding="utf-8") as f:
            f.write(text_bon)
        print(f"Bonul a fost salvat in fisierul {fisier}.")
    except Exception as e:
        print(f"Eroare la scrierea bonului: {e}")

def goleste_comanda(comanda):
    comanda.clear()

def actualizeaza_stoc(produse, comanda):
    for id_produs, cantitate in comanda.items():
        produse[id_produs]["stoc"] -= cantitate

def salveaza_produse_csv(fisier, produse):
    try:
        with open(fisier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "nume", "pret", "stoc"])
            for id_produs, info in produse.items():
                writer.writerow([id_produs, info["nume"], info["pret"], info["stoc"]])
    except Exception as e:
        print(f"Eroare la salvarea fisierului CSV: {e}")

def afiseaza_comanda(comanda, produse):
    print("\n--- COMANDA CURENTA ---")
    if not comanda:
        print("Comanda este goala.")
        return
    for id_produs, cantitate in comanda.items():
        nume = produse[id_produs]["nume"]
        pret = produse[id_produs]["pret"]
        subtotal = pret * cantitate
        print(f"{nume} | cantitate: {cantitate} | subtotal: {subtotal:.2f} lei")
    total = calculeaza_total(comanda, produse)
    print(f"Total curent: {total:.2f} lei")

def meniu_reduceri():
    print("\n--- MENIU REDUCERI ---")
    print("1 - student")
    print("2 - happy")
    print("3 - cupon")
    print("4 - fara reducere")
    print("0 - inapoi")

def main():
    produse = citeste_produse_csv("produse.csv")
    reduceri = citeste_reduceri_json("reduceri.json")
    comanda = {}
    reducere_curenta = ""

    while True:
        print("\n===== MENIU PRINCIPAL =====")
        print("1 - Afisare meniu produse")
        print("2 - Adaugare produs in comanda")
        print("3 - Scadere/eliminare produs din comanda")
        print("4 - Aplicare reducere")
        print("5 - Finalizare comanda")
        print("6 - Anulare comanda")
        print("0 - Iesire")

        optiune = input("Alege o optiune: ")

        if optiune == "1":
            afiseaza_meniu(produse)
            afiseaza_comanda(comanda, produse)

        elif optiune == "2":
            try:
                id_produs = int(input("Introdu ID produs: "))
                cantitate = int(input("Introdu cantitatea: "))
                succes, mesaj = adauga_produs(comanda, produse, id_produs, cantitate)
                print(mesaj)
            except ValueError:
                print("Date invalide. Introdu numere intregi.")

        elif optiune == "3":
            try:
                id_produs = int(input("Introdu ID produs: "))
                cantitate = int(input("Introdu cantitatea de scazut: "))
                succes, mesaj = scade_produs(comanda, id_produs, cantitate)
                print(mesaj)
            except ValueError:
                print("Date invalide. Introdu numere intregi.")

        elif optiune == "4":
            total = calculeaza_total(comanda, produse)
            if total == 0:
                print("Comanda este goala.")
                continue
            meniu_reduceri()
            alegere = input("Alege reducerea: ")
            if alegere == "1":
                reducere_curenta = "student"
                reducere = calculeaza_reducere(total, reducere_curenta, reduceri)
                print(f"Reducerea calculata: {reducere:.2f} lei")
            elif alegere == "2":
                reducere_curenta = "happy"
                reducere = calculeaza_reducere(total, reducere_curenta, reduceri)
                print(f"Reducerea calculata: {reducere:.2f} lei")
            elif alegere == "3":
                reducere_curenta = "cupon"
                reducere = calculeaza_reducere(total, reducere_curenta, reduceri)
                print(f"Reducerea calculata: {reducere:.2f} lei")
            elif alegere == "4":
                reducere_curenta = "fara"
                print("Reducerea a fost eliminata.")
            elif alegere == "0":
                continue
            else:
                print("Optiune invalida.")

        elif optiune == "5":
            if not comanda:
                print("Comanda este goala.")
                continue
            total = calculeaza_total(comanda, produse)
            reducere = calculeaza_reducere(total, reducere_curenta, reduceri)
            text_bon = genereaza_bon(comanda, produse, total, reducere)
            print("\n" + text_bon)
            scrie_bon_txt("bon.txt", text_bon)
            actualizeaza_stoc(produse, comanda)
            salveaza_produse_csv("produse.csv", produse)
            goleste_comanda(comanda)
            reducere_curenta = ""
            print("Comanda a fost finalizata.")

        elif optiune == "6":
            goleste_comanda(comanda)
            reducere_curenta = ""
            print("Comanda a fost anulata.")

        elif optiune == "0":
            print("Program inchis.")
            break

        else:
            print("Optiune invalida. Incearca din nou.")

if __name__ == "__main__":
    main()