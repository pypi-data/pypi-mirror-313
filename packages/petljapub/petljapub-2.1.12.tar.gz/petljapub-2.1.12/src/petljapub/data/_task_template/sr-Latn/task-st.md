---
title: $TASK_NAME
timelimit: 1.0 # u sekundama
memlimit: 64   # u MB
owner: $TASK_OWNER # vlasnik je onaj ko radi na zadatku
origin: # može ostati prazno, koristi se kada postoji potreba navodjenja izvora
tags: [] # svaki zadatak treba da je označen tagovima prema dogovorenoj listi tagova
status: IZRADA # jedan od: "IZRADA", "PREGLED" ili "KOMPLETAN".
status-od: $DATE # datum u formatu YYYY-MM-DD od kada je zadatak u navedenom statusu
solutions:
  - name: ex0
    lang: [cpp]
    desc: ""
    tags: []
    # expected-status: OK   # оčekivani status rešenja: OK, TLE, WA, RTE
    # expected-score: 100   # očekivani broj poena
---

Tekst zadatka.

## Ulaz

Opis ulaznih podataka.

## Izlaz

Opis izlaznih podataka.

## Primer

### Ulaz

~~~
0
~~~

### Izlaz

~~~
0
~~~
