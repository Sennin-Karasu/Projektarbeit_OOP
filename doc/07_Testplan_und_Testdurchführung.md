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
| ID   | Anforderung                            | Testfall (was?)                                          | Kriterium (Bestehen)                                             | Ergebnis                                                                                                                                      | Einstufung |
|------|----------------------------------------|----------------------------------------------------------|------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|------------|
| T-01 | Projekt eröffnen                       | Projekt mit allen Pflichtfeldern erstellen               | Projekt erscheint in Liste und bleibt nach Neustart erhalten     | Kann kein neues Projekt starten                                                                                                               | Major      |
| T-02 | Projekt eröffnen benötigt alle Angaben | Projekt ohne alle Pflichtfelder erstellen                | Das Projekt kann nicht erstellt werden, ohne alle Pflichtfelder  |                                                                                                                                               |            |
| T-03 | Angaben Validieren                     | Die im Projekt angegebnen Infos werden korrekt angezeigt | Alle Informationen stimmen mit eingegeben überein                |                                                                                                                                               |            |
| T-04 | Pflichtfelder validieren               | Projekt speichern ohne alle Angagben                     | Speichern wird verhindert und Fehelrmeldung                      |                                                                                                                                               |            |
| T-05 | Information Text                       | Text Information mit 1-3 Tags anlegen                    | Information erscheint in Tabelle und Detailansicht               | Text Information konnte erstellt werden und alle Tags und Infos sind vorhande                                                                 | IO         |
| T-06 | Information Bild URL                   | Bild URL speichern                                       | URL wird klickbar dargestellt                                    | Die URL ist anklickbar und funktioniert auch. Problem: nur 1 Link pro Information möglich                                                     | Minor      |
| T-07 | Information Dokument URL               | Dokument URL speichern                                   | URL wird korrekt angezeigt                                       | Die URl ist anklickbar und funktioniert auch. Problem: nur 1 Link pro Information möglich                                                     | Minor      |
| T-08 | Maximal drei Tags                      | Vier Tags eingeben                                       | Speichern wird verhindert                                        | Es hat nur 3 Eingabefelder für Tags. Somit auch nur 3 möglich                                                                                 | IO         |
| T-09 | Kommentar hinzufügen                   | Kommentar zu Information speichern                       | Kommentar erscheint unter Detailansicht                          | Kommentar erscheint                                                                                                                           | IO         |
| T-10 | Kommentararten unterscheiden           | Ergänzung und Korrektur speichern                        | Unterschiedliche Darstellung sichtbar                            | Kommentare werden Gelb Hervorgehoben.                                                                                                         | IO         |
| T-11 | Tag Suche                              | Nach vorhandenem Tag suchen                              | Alle passenden Informationen erscheinen                          | Tags werden nach erstellung gespeichert und mann kann nach Tags suchen.                                                                       | IO         | 
| T-12 | Persistenz                             | Anwendung neu starten                                    | Alle Daten bleiben erhalten                                      | Alle Daten bleiben erhallten. Jedoch müssen wir eine Funktion implementieren welche es uns ermöglicht Informationen und Kommentare zu löschen | Critical   |   



!!! Wichtig einbauen der Funktion, dass man Informationen und Kommentare löschen kann.
# 7.3 Zusammenfassung der Testergebnisse

Die Tests haben uns einiges aufgezeigt. 
So haben wir zum einen erkannt, dass wir gar keine Lösch-Funktion für die Projekte eingebaut haben. 
Auch die Major Bugs wurden von uns erkannt und behoben, wie folgend zu sehen ist:

| ID   | Erstes Ergebnis                                          | Einstufung | konkreter Fehler                                                                        | Behebung                                                    | Ergebniss nach behebung                                     | Einstufung |
| ---- | -------------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------- | ---------- |
| T-01 | Konnte kein neues Projekt gestartet bzw. geöffnet werden | Major      | ProjectDialog nutzte falsches Widget (`kind_combo`) -> Crash -> Projektanlage unmöglich | Dialogklassen getrennt, ProjectDialog.data() korrigiert     | Projekt lässt sich erstellen und bleibt gespeichert!        | I.O        |
|      |                                                          |            |                                                                                         |                                                             |                                                             |            |
| T-12 | Persistenz, Anwendung neu starten                        | Critical   | Persistenz funktioniert, allerdings kann ein Projekt nicht gelöscht werden.             | Implementierung einer Lösch Funktion für den Projektleiter. | Ein Projekt kann durch 2 fache Bestätigung gelöscht werden. | I.O        |
|      |                                                          |            |                                                                                         |                                                             |                                                             |            |

