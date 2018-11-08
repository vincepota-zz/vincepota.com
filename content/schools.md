Title: La scuola italiana: cosa dicono gli open data [Italian]
Date: 2018-08-07 10:20
Category: Data Science
Tags: school, data-mining, python, plotly, maps

## Premessa

Gli open data (i “dati aperti”), cioè quelli liberamente accessibili a chiunque attraverso la
rete, sono una straordinaria risorsa per la società in cui viviamo in quanto danno agli individui
il potere di ottenere informazioni direttamente dalla fonte, senza filtri e senza preconcetti. Per far ciò, è ovviamente richiesta
un pò di dimestichezza con l'informatica e la programmazione, ma entrambi sono diventati molti più accessibili rispetto a 20 anni fa.
Per dimostrarlo, in seguito analizzerò gli open data della scuola italiana utilizzando semplici tecniche di esplorazione dati.

Faccio questo per una serie di motivi:

- Il dataset è promettente e ben compilato, con variabili che permetteranno di avere un’istantanea del sistema scuola.
- Non ho trovato alcuna analisi panoramica di questo dataset. Alcuni giornali hanno pubblicato solo analisi specifiche su alcune sezioni dei dati.
- Spero che i dati ci svelino cose che non sapevamo prima.
- Voglio dimostrare il potenziale del metodo scientifico applicato ai dati ed anche di come questa combinazione possa darci informazioni interessanti.

Tutto il codice sorgente è open source, cioè accessibile a tutti, ed è pubblicato [qui](https://github.com/vincepota/school-me).
Gran parte dell’analisi verrà fatta con il linguaggio python. Se avete un po di dimestichezza
con questo linguaggio vi incoraggio a contribuire a questo codice.

## I dati

I dati vengono da [questo sito](http://dati.istruzione.it/opendata/opendata/). Non so come siano stati compilati o chi li abbia compilati.
Assumo che siano corretti e completi, cercando di correggerli nel caso in cui non lo siano.

I dati sono nelle seguenti categorie:

- __Anagrafica__: nome scuola, indirizzo scuola, tipologia scuola, etc.
- __Docenti__: età, tipologia (supplente, di ruolo), sesso, etc.
- __Edilizia__: anno di costruzione, accessibilità, sismicità, trasporto scolastico, etc.
- __Studenti__: età, sesso, nazionalità, etc.

Queste categorie compongono quattro datasets indipendenti che però possono essere uniti
utilizzando le informazioni che hanno in comune. Ho raggruppato tutti i dati in una banca dati (SQL database) che potete scaricare [qui](https://github.com/vincepota/school-me/blob/master/IT_schools.db).

I dati si riferiscono all’anno scolastico 2016/17. Includono sia scuole pubbliche che
paritarie (private) che siano: dell’infanzia (materne), primaria (elementari),
secondaria I grado (medie), secondaria II grado (superiori). Questo non è vero per tutte
le categorie. Ad esempio non ci sono informazioni per studenti delle scuole
dell’infanzia.

Come supplemento alla mia analisi, utilizzerò dati demografici ISTAT relativi al 1 Gennaio 2017
contenenti la popolazione legale al 09/10/2011, cioè’ la data dell’ultimo censimento,
per comune, provincia, regione e ripartizione geografica.

## Studenti: quanti sono e da dove vengono

I dati ci permettono di contare quanti studenti ci sono per regione e dividerli per nazionalità:
Italiana, Unione Europea e non Europea. La tabella di seguito mostra proprio questa analisi
demografica, e va letta cosi’ : durante l’anno accademico 2016/17, per esempio,
in Abruzzo c’erano 148,059 studenti, di cui 137,605 (87.2%) erano di nazionalità Italiana
e 10,454 (7.1%) erano di nazionalità non italiana. Di questi ultimi, 3,253 (31.1%) erano
cittadini dell’UE e 7,201 (68.9%) erano di altra nazionalità. Da notare che questi dati
si riferiscono solo a scuole primarie, secondarie di primo e secondo grado.
Cioè non ci sono le scuole dell’infanzia.

| __Regione__     | __Alunni__  | __Italiani__ | __Stranieri__ |  __EU__    | __Non-EU__ | __Italiani[%]__      | __Stranieri[%]__   | __EU[%]__          | __non-EU[%]__         |
|-------------------|---------|----------|--------------|-------|--------|--------------------|---------------------|---------------------|---------------------|
| ABRUZZO           | 148,059  | 137,605   | 10,454        | 3,253  | 7,201   | 92.9%              | 7.1%                | 31.1%               | 68.8%  |
| BASILICATA        | 69,345   | 67,036    | 2,309         | 1,102  | 1,207   | 96.7%              | 3.3%                | 47.7%               | 52.3% |
| CALABRIA          | 242,694  | 231,733   | 10,961        | 4,745  | 6,216   | 95.5%              | 4.5%                | 43.3%               | 56.6% |
| CAMPANIA          | 819,041  | 799,048   | 19,993        | 6,041  | 13,952  | 97.6%              | 2.4%                | 30.2%               | 69.8%               |
| EMILIA ROMAGNA    | 508,499  | 430,626   | 77,873        | 11,193 | 66,680  | 84.7%              | 15.3%               | 14.39%              | 85.6%               |
| FRIULI-VENEZIA G. | 131,332  | 116,387   | 14,945        | 3,673  | 11,272  | 88.6%              | 11.4%               | 24.6%               | 75.4%               |
| LAZIO             | 679,031  | 615,415   | 63,616        | 27,633 | 35,983  | 90.6%              | 9.4%                | 43.4%               | 56.5% |
| LIGURIA           | 159,385  | 140,147   | 19,238        | 2,649  | 16,589  | 87.9%              | 12.1%               | 13.8%               | 86.2%               |
| LOMBARDIA         | 1,149,475 | 984,519   | 164,956       | 23,008 | 141,948 | 85.6%              | 14.3%               | 13.9%               | 86.1%               |
| MARCHE            | 179,767  | 160,085   | 19,682        | 3,310  | 16,372  | 89.1%              | 10.9%               | 16.8%               | 83.2%               |
| MOLISE            | 33,845   | 32,629    | 1,216         | 465   | 751    | 96.3%              | 3.5%                | 38.2%               | 61.8%               |
| PIEMONTE          | 478,949  | 418,942   | 60,007        | 19,127 | 40,880  | 87.5%              | 12.5%               | 31.9%               | 68.1%  |
| PUGLIA            | 517,390  | 503,417   | 13,973        | 4,562  | 9,411   | 97.3%              | 2.7%                | 32.6%               | 67.4%               |
| SARDEGNA          | 180,059  | 175,571   | 4,488         | 1,411  | 3,077   | 97.5%              | 2.5%                | 31.4%               | 68.6%  |
| SICILIA           | 642,486  | 621,420   | 21,066        | 7,718  | 13,348  | 96.7%              | 3.3%                | 36.6%               | 63.4%               |
| TOSCANA           | 420,112  | 364,806   | 55,306        | 10,546 | 44,760  | 86.8%              | 13.2%               | 19.1%               | 80.9%               |
| UMBRIA            | 99,916   | 86,405    | 13,511        | 3,282  | 10,229  | 86.5%              | 13.5%               | 24.3%               | 75.7%               |
| VENETO            | 577,645  | 506,117   | 71,528        | 15,397 | 56,131  | 87.6%              | 12.4%               | 21.5%               | 78.5%               |


Tra le varie informazioni contenute in questa tabella, uno ha attratto la mia attenzione.
Ci sono nettamente più studenti stranieri relative agli studenti italiani nelle regioni del nord.
Questo dato è in perfetto accordo con i [dati demografici della popolazione residente](https://www.tuttitalia.it/statistiche/cittadini-stranieri-2017/)
che mostrano che i residenti stranieri aumentano andando verso nord.
La divisione tra nord e sud è evidente quando visualizziamo i dati su una mappa.
La mappa è interattiva. Sorvola sulle regioni per avere ulteriori informazioni.

<iframe width="900" height="800" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/6.embed"></iframe>

L’ Emilia Romagna è la regione con più la più alta frazione di studenti stranieri,
mentre la Campania è la regione con meno studenti stranieri relativi agli studenti
Italiani. In totale, poco più di mezzo milione di studenti (645,122) sono di nazionalità non Italiana.

Di tutti gli studenti stranieri, che percentuale è proveniente da paesi dell'Unione Europea e paesi extra europei?

<iframe width="700" height="600" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/22.embed"></iframe>

<iframe width="700" height="600" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/20.embed"></iframe>

Qui vediamo qualcosa di molto interessante: gli studenti Europei sono più numerosi al
sud, mentre gli studenti extra-europei sono più numerosi al nord. Questo è
specialmente vero per Lombardia, Emilia Romagna e Liguria per cui gli studenti europei
sono solo il 15%, mentre gli studenti extra europei sono ben l' 85-86%. Non conosco bene
le ragioni socio-demografiche di questa separazione, ma questo risultato è sicuramente
veritiero. Il nord Italia è notoriamente più multiculturale del sud Italia in quanto,
essendo più ricco, attrae persone da tutto il mondo. Se siete mai stati a Milano per poche ore,
è evidente che l' etnia della sua popolazione è più variegata rispetto, per esempio, a
Potenza.

## Scuole: quante ne sono e dove sono?

Vediamo ora quante scuole ci sono in ogni città. Per "scuola", qui si intende la scuola
istituzionale e non l'edificio fisico. Ho correlato i dati aggregati ISTAT, che mi
danno il numero di residenti per ogni provincia, con gli open data del ministero, che mi
dicono quante scuole ci sono in ogni provincia. Il grafico qui sotto mostra questa
correlazione.

<iframe width="900" height="600" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/10.embed"></iframe>

Come ci aspettiamo, più una provincia é popolosa, più scuole ci sono. La linea
tratteggiata è il modello matematico lineare che meglio rappresenta questa correlazione.
In media, c'é una scuola ogni 1,750 abitanti. Il più basso rapporto scuola per
popolazione va alla provincia di Vibo Valentia con una scuola ogni 950 abitanti; il più
alto rapporto va a Barletta-Andria-Trani con una scuola ogni 2,800 abitanti.
Da notare che il rapporto scuola popolazione qui calcolato si riferisce a tutta la
popolazione residente di tutte le età, che chiaramente varia da provincia a provincia.
Per giudicare se ci sono abbastanza scuole per provincia, si dovrebbe confrontare il
numero di scuole con la popolazione giovane (dai 6 ai 18 anni circa), cosa che qui non
ho fatto.

## Docenti: sono vecchi o giovani?

Analizziamo ora l'età dei docenti delle scuole Italiane. Questo include docenti sia
ordinari che supplenti. La tabella mostra quanti docenti ci sono per quattro fasce d'età
(i dati non ci danno l'età esatta dei docenti) e quale percentuale ciascuna fascia
rappresenta del campione totale.

| __Età__ |  __Docenti__| __Percentuale__ |
|------|--------|-------------|
|__<34__   |    56,706 | 6.6%     |
|__35-44__ |   205,513 | 24.0%    |
|__45-54__ |   295,745 | 34.0%    |
|__>54__   |   297,770 | 34.8%    |

Dai risultati è chiaro che la maggior parte dei docenti Italiani è over 40. Questo
dato è ancora più allarmante se inquadrato in un contesto mondiale come fatto
dall'Università di Cambridge [in uno studio del 2016](http://www.cambridgeassessment.org.uk/our-research/data-bytes/the-average-age-of-teachers-in-secondary-schools/).
Questo studio ha trovato che l'Italia è la nazione con i docenti più vecchi in un campione di 36
nazioni (che include nazioni da tutto il mondo come Malesia, Israele, Romania e Brasile).
I docenti giovani under 34 sono solo il 6.6% di tutti i docenti Italiani.
Dipingete nella vostra testa cosa vuol dire: se estraete a caso 100 docenti da tutte le scuole d'Italia, soltanto (circa) 7 avranno meno di 34 anni.

Il grafico qui sotto mostra come l' età dei docenti è distribuita per tipologia di scuola.

<iframe width="900" height="600" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/12.embed"></iframe>

Ad esempio, ci sono soltanto circa 5,000 docenti under 34 e ben 34,000 over 54 nelle
scuole dell'infanzia in tutta Italia. Non so come spiegare il calo di docenti over 54
della scuola primaria (linea arancione) e scuola dell'infanzia (linea blu). Posso
speculare che i docenti più anziani preferiscono essere trasferiti alle medie o
superiori per insegnare a studenti meno energetici.

Abbiamo visto che il corpo docenti nazionale è anziano, ma qualche under 34 c'è. Vediamo
quindi qual'è la provincia con i docenti più giovani d'Italia. Cioè, per ogni provincia
calcoliamo la percentuale degli under 34 rispetto a tutti i docenti in quella provincia.
Un colore più verde vuol dire più docenti giovani.

<iframe width="900" height="800" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/14.embed"></iframe>

È chiaro che il nord ovest è l'area con più docenti under 34. La prima provincia è Cuneo
con il 12.6% (il doppio rispetto alla media nazionale), seguita da Verbano-Cusio-Ossola
(11.3%), Vercelli, Mantova, Lecco, Monza-Brianza tutte intorno all' 11.1% e poi Milano
al 10.9%.

Vediamo, purtroppo, la stessa separazione geografica nord-sud che abbiamo incontrato
sopra. Al sud i docenti giovani sono pochi, pochissimi. Sono tra il 2%-3%, con ai due
estremi Siracusa (1.9%) e Barletta-Andria-Trani (5.4%).

## Edifici scolastici: come sono e quante sono a norma ?

Occupiamoci ora degli edifici scolastici. Questo
dataset contiene dati solo per le scuole pubbliche: anno di costruzione, il grado
di accessibilità, se hanno palestra e piscina, mensa, il volume, etc. Purtroppo, questo
dataset è "incompleto", cioè mancano dati. Come lo so? Per iniziare, il dataset
non contiene nessuna scuola del mio paese di origine: Casagiove. Dai dati ho calcolato
che mancano all'appello edifici da 866 comuni. Un' analisi rigorosa richiederebbe una
correzione per questo effetto di incompletezza, cosa che io non farò.

Visualizziamo qualche risultato interessante: come sono distribuiti l'anno di costruzione, la superficie in metri quadrati e il numero di piani per ogni scuola.

<iframe width="900" height="500" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/16.embed"></iframe>

Il primo grafico mostra che la maggior parte degli edifici scolastici è stata costruita
nel dopoguerra ma il picco si é raggiunto negli anni 70 fino a metà degli anni 80. Un
tipico edificio scolastico tende ad avere 2 piani, con una superficie totale di circa
7,000 metri quadrati.

Cosa molto più interessante è l'analisi della resistenza sismica degli edifici scolastici.
Cioè: quanti edifici sono stati progettati con criteri antisismici?
Prima di mostrare i risultati va fatta un' importante precisazione. I dati
ci dicono solo se un edificio è stato progettato e costruito con criteri antisismici, ma non ci dicono se
è stato adeguato successivamente. Vedi [questa risposta del
ministero](http://precisoche.blogautore.espresso.repubblica.it/2017/06/05/scuole-e-sicurezza-la-replica-del-miur-e-la-nostra-risposta/) ad un'[articolo dell'espresso](http://precisoche.blogautore.espresso.repubblica.it/2017/06/05/scuole-e-sicurezza-la-replica-del-miur-e-la-nostra-risposta/).
Ad esempio, se un edificio è stato costruito nel 1960 senza criteri antisismici ed è stato reso
antisismico nel 1980, questo edificio apparirà come "non a norma" nei dati.

Ecco i risultati:

<iframe width="900" height="500" frameborder="0" scrolling="no" src="//plot.ly/~vincenzo.pota/18.embed"></iframe>

La figura mostra il numero di edifici scolastici progettati con criteri antisismici (a
norma in arancione) o senza criteri antisismici (non a norma in blu) per quattro
diverse fasce di rischio sismico legate alla collocazione geografica della scuola. Ad
esempio, una scuola a l'Aquila è ad alto rischio sismico, mentre una scuola a Torino
non ha rischio sismico.

Il dataset contiene 36,093 edifici scolastici, di cui 4,145 (11%) sono stati costruiti a
norma, 31,662 (87%) non sono stati costruiti a norma, e 286 non hanno questa
informazione. Tuttavia, si potrebbe sostenere che edifici scolastici non a norma
costruiti in zone a bassa o assente sismicità (come il Piemonte e la Liguria) siano meno
pericolosi degli edifici non a norma costruiti in regioni ad alto rischio sismico (come
l'Abruzzo o la Calabria).

Quindi, se consideriamo solo scuole a medio o alto rischio sismico troviamo un totale
di 15,194 scuole di cui 12,184 (80%) non sono a norma e 3,010 (20%) sono a norma. Questi numeri
sono leggermente più rassicuranti di quelli relativi all'intera popolazione; ancor più se
consideriamo che un numero imprecisato di questi edifici é successivamente stato
adeguato con criteri antisismici.

# Conclusione

I dati delle scuole italiane compilati dal ministero dell'istruzione sono una preziosa
risorsa per avere un'istantanea del sistema scolastico italiano. In questo articolo ho
presentato solo alcuni del moltissimi risultati che si possono ottenere da questi dati.  

Un dataset del genere può essere utile a Regioni, Provincie e comuni per inquadrare le
loro scuole in un contesto nazionale. Oppure può essere utile a giornalisti e semplici
cittadini per trasformare i numeri in storie che possano essere divulgate ad un pubblico
non esperto. Un'analisi del genere non richiede né una laurea in statistica, né un
master in informatica. Avete bisogno solo di due importanti requisiti:

1. Abbastanza curiosità per trasformare migliaia di numeri senza senso in risultati interessanti.
2. Un minimo di dimestichezza con linguaggi di programmazione e manipolazione di dati.

Se avete i due requisiti di sopra, vi incoraggio ad esplorare il mondo degli open data ed a
condividere le vostre scoperte con la comunità.
