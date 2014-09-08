
# Projekt: Movie ratings

V tomto projekte máte k dispozícii dáta o tom ako jednotliví ľudia hodnotia filmy.
Vašou úlohou je vytvoriť model, ktorý bude predpovedať hodnotenia filmov.


## Súbory

Súbory typu ``csv`` reprezentujú tabuľky dát. Každý riadok v súbore predstavuje riadok v tabuľke.
Jednotlivé hodnoty v riadkoch sú oddelené čiarkami. Prvý riadok typicky obsahuje názvy stĺpcov.

- ``baseline.py`` - obsahuje implementáciu jednoduchého baseline modelu, ktorý pre každý film predikuje jeho priemerné hodnotenie.
Baseline spustíte pomocou príkazu ``python baseline.py``. Taktiež tu nájdetie funkcie na načítanie dát a vypočítanie hodnotiacej metriky.
- ``ratings-train.csv`` obsahuje dáta určené na trénovanie modelu. Každý riadok predstavuje trojicu *film*, *užívateľ*, *hodnotenie*.
- ``ratings-test.csv`` obsahuje dáta určené na testovanie modelu.
- ``movies.csv`` - obsahuje mapovanie číselných id filmov na ich názvy a žánre. Tento súbor nie je potrebný k trénovaniu modelu, ale môže poslúžiť pri vizualizáciach.

## Metrika úspešnosti

Na vyhodnotenie úspešnosti modelu budeme používať metriku zvanú **Root Mean Squared Error** (RMSE).
Viac informácií nájdete na [wikipédií](http://en.wikipedia.org/wiki/Root-mean-square_deviation). 

Taktiež súbor ``baseline.py`` obsahuje funkciu, ktorá spočíta RMSE.


## Ciele

Baseline má na testovacej sade RMSE 0.9790.
Pomocou vylepšenia baselinu by sa vám mohlo podariť dosiahnuť RMSE okolo 0.9.
Vyskúšajte dosiahnuť RMSE 0.88 alebo lepšie.
