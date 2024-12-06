# ListWizard

ListWizard je Python knjižnica za analizu, uređivanje i manipulaciju listama, osmišljena kako bi rad s listama bio jednostavan i intuitivan.

---

## Značajke i Primjeri

### 1. **Statistika**
Izračunajte osnovne statističke vrijednosti liste brojeva, uključujući sumu, srednju vrijednost, medijan, mod, raspon, varijancu i standardnu devijaciju.

**Primjer**:
```python
from listwizard import ListWizard

statistike = ListWizard.calculate_statistics([1, 2, 2, 3, 4])
print(statistike)
```

**Rezultat**:
```python
{
    'sum': 12,
    'mean': 2.4,
    'median': 2,
    'mode': 2,
    'range': 3,
    'variance': 1.04,
    'std_dev': 1.0198039027185568
}
```

---

### 2. **Frekvencija Elemenata**
Pronađite koliko se puta svaki element pojavljuje u listi.

**Primjer**:
```python
frekvencija = ListWizard.element_frequency(["a", "b", "a", "c", "b", "b"])
print(frekvencija)
```

**Rezultat**:
```python
{'a': 2, 'b': 3, 'c': 1}
```

---

### 3. **Sličnost Listi**
Izračunajte postotak sličnosti između dviju lista na temelju zajedničkih elemenata.

**Primjer**:
```python
slicnost = ListWizard.list_similarity([1, 2, 3], [3, 4, 5])
print(f"Sličnost: {slicnost}%")
```

**Rezultat**:
```python
Sličnost: 20.0%
```

---

### 4. **Sortiranje**
Sortirajte listu prema prilagođenom ključu ili obrnutom redoslijedu.

**Primjer**:
```python
sortirano = ListWizard.sort_list([5, 2, 8, 1], reverse=True)
print(sortirano)
```

**Rezultat**:
```python
[8, 5, 2, 1]
```

---

### 5. **Miješanje**
Nasumično izmiješajte elemente liste.

**Primjer**:
```python
izmjesano = ListWizard.shuffle_list([1, 2, 3, 4, 5])
print(izmjesano)
```

**Rezultat**:
```python
[4, 1, 5, 2, 3]
```

---

### 6. **Uklanjanje Duplikata**
Automatski uklonite duplikate iz liste uz očuvanje redoslijeda.

**Primjer**:
```python
jedinstvena_lista = ListWizard.unique_list([1, 2, 2, 3, 4, 4, 5])
print(jedinstvena_lista)
```

**Rezultat**:
```python
[1, 2, 3, 4, 5]
```

---

### 7. **Umetanje Elemenata**
Umetnite element na određenu poziciju u listi.

**Primjer**:
```python
nova_lista = ListWizard.insert_at([1, 2, 3], 99, 1)
print(nova_lista)
```

**Rezultat**:
```python
[1, 99, 2, 3]
```

---

### 8. **Cirkularno Pomicanje**
Rotirajte elemente liste ulijevo ili udesno za određeni broj pozicija.

**Primjer**:
```python
pomaknuto = ListWizard.circular_shift([1, 2, 3, 4], 2)
print(pomaknuto)
```

**Rezultat**:
```python
[3, 4, 1, 2]
```

---

### 9. **Spajanje Listi**
Pametno spojite više lista u jednu, bez duplikata.

**Primjer**:
```python
spojena_lista = ListWizard.merge_lists([1, 2], [2, 3], [3, 4])
print(spojena_lista)
```

**Rezultat**:
```python
[1, 2, 3, 4]
```

---

### 10. **Pretvaranje Liste u String**
Pretvorite listu u čitljiv niz s prilagođenim separatorom.

**Primjer**:
```python
string_lista = ListWizard.list_to_string([1, 2, 3], separator=" | ")
print(string_lista)
```

**Rezultat**:
```python
"1 | 2 | 3"
```

---

## Instalacija
Instalirajte knjižnicu pomoću ```pip```-a:
```bash
pip install listwizard
```