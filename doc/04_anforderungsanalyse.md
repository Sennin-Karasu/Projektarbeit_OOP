
# 4 Anforderungsanalyse
## 4.1 Stakeholder

Folgende Stakeholder sind von der Applikation betroffen:
Projektleiter
- Erstellt neue Projekte
- Definiert Kernanforderungen
- Nutzt gespeicherte Informationen zur Projektsteuerung

Projektmitarbeiter
- Erfassen projektbezogene Informationen
- Kommentieren bestehende Einträge
- Ergänzen oder korrigieren Inhalte
- Nutzen die Tag Suche zur Informationsbeschaffung

Unternehmen Xarelto
- Erwartet strukturierte Wissensablage
- Möchte langfristig Projektwissen sichern

## 4.2 Funktionale Anforderungen
### 4.2.1 Projektverwaltung

- Ein neues Projekt kann angelegt werden.
- Ein Projekt enthält folgende Attribute:
  - Name
  - Kunde
  - Projektleiter
  - Kernanforderungen
- Projekte werden persistent gespeichert.
- Bestehende Projekte können angezeigt werden.

### 4.2.2 Informationsverwaltung
- Informationen können einem Projekt zugeordnet werden.
- Eine Information besitzt folgende Attribute:
  - Titel
  - Typ
  - Inhalt oder URL
  - Ersteller
  - Erstellungsdatum
  - Tags
- Der Informationstyp kann sein:
  - Text
  - Bild URL
  - Dokument URL
- Pro Information sind maximal drei Tags zulässig.
- Informationen können kommentiert werden.
- Kommentare können als normale Kommentare, Ergänzungen oder Korrekturen klassifiziert werden.
- Ergänzungen und Korrekturen müssen visuell klar vom Originaltext unterscheidbar sein.

### 4.2.3 Suche

- Innerhalb eines Projektes kann nach Tags gesucht werden.
- Die Suche arbeitet mit einer lockeren Logik.
- Eine Information wird angezeigt, wenn mindestens ein eingegebener Tag übereinstimmt.

## 4.3 Nicht funktionale Anforderungen

- Die Anwendung wird als Desktop Applikation umgesetzt.
- Die Implementierung erfolgt in Python.
- Die Architektur basiert auf objektorientierten Prinzipien.
- Das Klassendiagramm bildet die Grundlage der Implementierung.
- Die Daten werden persistent mittels JSON Serialisierung gespeichert.
- Die Lösung ist für maximal etwa 100 Einträge ausgelegt.
- Die Benutzeroberfläche ist übersichtlich und verständlich gestaltet.
- Die Applikation läuft stabil ohne Datenverlust.

## 4.4 Abgrenzung

Folgende Funktionen sind nicht Bestandteil des Prototyps:
- Benutzerverwaltung oder Rollenmodell
- Mehrbenutzerbetrieb
- Datei Upload Funktion
- Optimierung für große Datenmengen
- Netzwerkanbindung oder Cloud Speicherung