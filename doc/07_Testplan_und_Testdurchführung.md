Diagramm einfügen
Beziehungen erklären
Warum keine Polymorphie verwendet wurde
Warum Enums verwendet wurden

Das deckt UML Analyse ab.




# 7 Testplan und Testdurchführung
## 7.1 Teststrategie

Die Tests wurden auf zwei Ebenen durchgeführt:
- Funktionale Tests der Fachlogik über die Service Schicht
- Manuelle Systemtests über die grafische Benutzeroberfläche

Ziel der Tests ist die vollständige Überprüfung aller in der Aufgabenstellung definierten Anforderungen.

Die Einstufung erfolgt nach folgendem Schema:
- Critical  
Kritische Abweichung, Abnahme nicht möglich
- Major  
Hauptfehler, muss vor Abgabe behoben werden
- Minor  
Nebenfehler, Funktion grundsätzlich gegeben


## 7.2 Testmatrix
| Anforderung                  | Testfall (was?)                                          | Kriterium (Bestehen)                                         | Ergebnis             | Einstufung |
|------------------------------|----------------------------------------------------------|--------------------------------------------------------------|----------------------|-----------|
|                              |                                                          |                                                              |       |  |
| Projekt eröffnen             | Projekt mit allen Pflichtfeldern erstellen               | Projekt erscheint in Liste und bleibt nach Neustart erhalten |       |  |
| Angaben Validieren           | Die im Projekt angegebnen Infos werden korrekt angezeigt | Alle Informationen stimmen mit eingegeben überein            |       |  |
| Pflichtfelder validieren     | Projekt speichern ohne alle Angagben                     | Speichern wird verhindert und Fehelrmeldung                  |       |  |
| Information Text             | Text Information mit 1-3 Tags anlegen                    | Information erscheint in Tabelle und Detailansicht           |                    |  |
| Information Bild URL         | Bild URL speichern                                       | URL wird klickbar dargestellt                                |                   |  |
| Information Dokument URL     | Dokument URL speichern                                   | URL wird korrekt angezeigt                                   |                   |  |
| Maximal drei Tags            | Vier Tags eingeben                                       | Speichern wird verhindert                                    |            |  |
| Kommentar hinzufügen         | Kommentar zu Information speichern                       | Kommentar erscheint unter Detailansicht                      |                      |
| Kommentararten unterscheiden | Ergänzung und Korrektur speichern                        | Unterschiedliche Darstellung sichtbar                        |                      |
| Tag Suche                    | Nach vorhandenem Tag suchen                              | Alle passenden Informationen erscheinen                      |                      |
| Persistenz                   | Anwendung neu starten                                    | Alle Daten bleiben erhalten                                  |                      |


# 7.3 Zusammenfassung der Testergebnisse

