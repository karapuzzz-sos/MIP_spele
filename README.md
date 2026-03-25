# Akmeņu spēles apraksts

## Papildu prasības
Spēles sākumā cilvēks izvēlas akmeņu skaitu diapazonā no **50 līdz 70**. Izvēlētais akmeņu skaits tiek novietots uz galda.

## Spēles noteikumi
- Abiem spēlētājiem sākumā ir:
  - 0 akmeņu
  - 0 punktu
- Spēlētāji veic gājienus pārmaiņus.
- Katram spēlētājam savā gājienā ir atļauts paņemt:
  - **2 akmeņus**  vai - **3 akmeņus**

## Punktu piešķiršana
Pēc katra gājiena tiek pārbaudīts atlikušo akmeņu skaits uz galda:
- Ja akmeņu skaits ir **pāra skaitlis** →  
   pretinieks saņem **+2 punktus**
- Ja akmeņu skaits ir **nepāra skaitlis** →  
   spēlētājs, kurš veica gājienu, saņem **+2 punktus**

## Spēles beigas
Spēle beidzas, kad uz galda vairs nav akmeņu.

## Papildu punkti
Spēles beigās katram spēlētājam pie punktiem tiek pieskaitīts viņa savākto akmeņu skaits.

## Uzvarētājs
- Ja punktu skaits abiem spēlētājiem ir vienāds → **neizšķirts**
- Ja punktu skaits atšķiras → uzvar spēlētājs ar lielāko punktu skaitu


## Spēles palaišana

Spēli var palaist gan caur Python, gan izmantojot izpildāmo failu Windows vidē.

### Projekta lejupielāde

Lai sāktu darbu ar spēli, nepieciešams lejupielādēt projektu un pāriet uz tā mapi:

```bash
git clone https://github.com/karapuzzz-sos/MIP_spele.git
cd MIP_spele
````

### Spēles palaišana ar Python

Spēli var palaist caur termināli.

Windows vidē spēles palaišanai izmanto komandu:

```bash
python main.py
```

macOS vidē spēles palaišanai izmanto komandu:

```bash
python3 main.py
```

Ja komanda `python` nedarbojas, ieteicams izmantot `python3`.

### Spēles palaišana ar .exe failu (Windows)

Windows lietotājiem ir pieejams gatavs izpildāmais fails.

Atver mapi:

```bash
cd dist
```

Palaid spēli ar komandu:

```bash
MIP_SPELE.exe
```

Vai arī palaid failu ar dubultklikšķi.

### Iespējamās problēmas

Ja Windows drošības sistēma bloķē programmu, nepieciešams nospiest **“More info”** un pēc tam **“Run anyway”**.

Ja Python komanda netiek atpazīta, pārbaudi instalāciju ar komandu:

```bash
python --version
```

vai

```bash
python3 --version
```

````



