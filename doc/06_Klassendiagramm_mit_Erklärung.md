# 6 Klassendiagramm mit Erläuterung
## 6.1 Ausgangsversion des Klassendiagramms

Als Grundlage für die objektorientierte Umsetzung wurde ein Klassendiagramm erstellt. Ziel war es, die in der Aufgabenstellung beschriebenen Rollen, Funktionen und Datenstrukturen in ein möglichst einfaches und übersichtliches Modell zu überführen.

Die erste Modellversion orientierte sich stark an der textlichen Beschreibung der Fallstudie. Im Zentrum stand die Verwaltung von projektspezifischen Informationen innerhalb einer zentralen Wissensablage.

Das Klassendiagramm bestand aus folgenden Klassen:

- Projekt
- Wissensablage
- Projektmitarbeiter
- Projektleiter (Spezialisierung)
- Mitarbeiter (Spezialisierung)

Der Fokus dieser Version lag darauf, die funktionalen Anforderungen in möglichst wenigen Klassen abzubilden und die Komplexität gering zu halten.

## 6.2 Klassenbeschreibung der Ausgangsversion
Projekt

Die Klasse Projekt repräsentiert ein Projekt innerhalb der Firma. Sie enthält sämtliche Stammdaten, die bei der Projekteröffnung erfasst werden.

Attribute:
- Name
- Kunde
- Kernanforderungen
- zugeteilte Mitarbeitende
- Tags

Methoden:
- Projekt anlegen
- Projekt bearbeiten

Die Klasse Projekt erfüllt damit direkt die in der Aufgabenstellung geforderte Möglichkeit zur Projekteröffnung und bildet die logische Zuordnungseinheit für alle projektspezifischen Wissenseinträge.

Wissensablage

Die Klasse Wissensablage repräsentiert die zentrale Verwaltungseinheit der Applikation. Fachlich entspricht sie der in der Aufgabenstellung beschriebenen Funktionalität, innerhalb eines Projektes Informationen zu erfassen, zu kommentieren und zu durchsuchen.

Attribute:
- Projekte
- Posts
- Kommentare

Methoden:
- Post erstellen
- Post kommentieren
- Post bearbeiten
- Post löschen
- Projekt zuweisen
- Post suchen

In dieser ersten Modellversion bündelt die Wissensablage den Hauptteil der fachlichen Logik. Sie übernimmt sowohl die Verwaltung von Projekten als auch die Verwaltung von Posts und Kommentaren.

Dieses Vorgehen war bewusst gewählt, um:
- das Modell übersichtlich zu halten
- Verantwortlichkeiten zentral zu bündeln
- eine schnelle Umsetzung zu ermöglichen

Projektmitarbeiter

Die Klasse Projektmitarbeiter beschreibt Personen, welche in Projekten mitarbeiten und mit der Wissensablage interagieren.

Attribute:
- Name
- Email
- Tags

Methoden:
- Registrieren
- Projekt beitreten

Diese Klasse repräsentiert die Benutzerrollen im System. Eine detaillierte Benutzerverwaltung mit Login oder Rechtekonzept war jedoch nicht Teil der Aufgabenstellung.

Projektleiter

Projektleiter ist eine Spezialisierung von Projektmitarbeiter.

Zusätzliche Methoden:
- Projekt anlegen
- Mitarbeiter hinzufügen
- Projekt beenden

Damit wird modelliert, dass der Projektleiter erweiterte Rechte besitzt.

Mitarbeiter

Mitarbeiter ist ebenfalls eine Spezialisierung von Projektmitarbeiter und verfügt über grundlegende Funktionen wie:

- Projekt beitreten

## 6.3 Beziehungen und Kardinalitäten
Beziehung Projektmitarbeiter zu Wissensablage

Zwischen Projektmitarbeiter und Wissensablage wurde eine Beziehung mit der Kardinalität N zu N modelliert.

Begründung:
- Mehrere Mitarbeitende können mit mehreren Projekten interagieren.
- Ein Projekt enthält mehrere Mitarbeitende.

Beziehung Wissensablage zu Projekt

Zwischen Wissensablage und Projekt wurde eine Beziehung mit 1 zu 1 modelliert.

Begründung:
- Jede Wissensablage gehört eindeutig zu einem Projekt.
- Ein Projekt besitzt genau eine Wissensablage.

Diese Modellierung entsprach der Idee, die Wissensablage als projektspezifische zentrale Verwaltungseinheit zu verstehen.

## 6.4 Bewertung der Ausgangsversion

Die erste Version erfüllte grundsätzlich die formalen Anforderungen der Aufgabenstellung. Allerdings zeigte sich bei der praktischen Umsetzung in Python, dass folgende Probleme auftraten:
- Posts besassen viele eigene Attribute und wuchsen strukturell stark an.
- Kommentare benötigten eigene Eigenschaften und eine eindeutige Zuordnung.
- Die Validierung der maximal drei Tags war schwer sauber integrierbar.
- Die JSON Serialisierung wurde zunehmend unübersichtlich.
- Verantwortlichkeiten waren nicht klar getrennt.

Insbesondere wurde deutlich, dass die Klasse Wissensablage zu viele Aufgaben übernahm. Dadurch entstand eine Verletzung des Prinzips der klaren Verantwortlichkeit.

## 6.5 Weiterentwicklung des Klassendiagramms im Verlauf der Umsetzung

Während der Implementierung wurde erkannt, dass eine feinere fachliche Modellierung notwendig ist, um:
- die Anforderungen sauber abzubilden
- die Wartbarkeit zu erhöhen
- die Persistenz klar zu strukturieren
- die Testbarkeit zu verbessern

Folgende Anforderungen machten eine Überarbeitung notwendig:
- Jeder Post besitzt Titel, Typ, Inhalt, Tags, Autor und Datum.
- Pro Post dürfen maximal drei Tags gespeichert werden.
- Kommentare müssen eindeutig einem Post zugeordnet sein.
- Kommentare besitzen eigene Eigenschaften.
- Ergänzungen und Korrekturen müssen klar unterscheidbar sein.
- Persistenz via JSON muss eindeutig rekonstruierbar sein.

Diese Punkte führten zur Einführung zusätzlicher Klassen.

## 6.6 Erweiterte Modellierung

Zur präziseren Abbildung der Fachlogik wurden folgende Klassen eingeführt:
- Information
-Kommentar
 
Information

Die Klasse Information repräsentiert einen einzelnen Wissenseintrag innerhalb eines Projektes.

Attribute:
- id
- projekt_id
- titel
- typ
- inhalt oder URL
- Tags
- autor
- datum

Eine Information gehört eindeutig zu genau einem Projekt.

Eine Information kann mehrere Kommentare besitzen.

Durch diese eigenständige Klasse konnte:
- die maximale Anzahl von drei Tags validiert werden
ä- die Typisierung (Text, Bild URL, Dokument URL) klar modelliert werden
- die Persistenz vereinfacht werden
- die Suchfunktion strukturiert umgesetzt werden

Kommentar

Die Klasse Kommentar repräsentiert eine Ergänzung zu einer Information.

Attribute:
- id
- information_id
- art
- text
- autor
- datum

Das Attribut art erlaubt die Unterscheidung zwischen:
- Kommentar
- Ergänzung
- Korrektur

Damit wird die Anforderung erfüllt, dass Änderungen klar vom Originaltext unterscheidbar sein müssen.

## 6.7 Bezug zur Implementierung

In der konkreten Umsetzung wurden die fachlichen Klassen wie folgt realisiert:

Domänenmodell:
- Project
- Information
- Comment

Service Schicht:
- KnowledgeService
- Persistenz:
- JsonRepository

Die ursprüngliche Wissensablage wird in der Umsetzung funktional durch die Kombination aus KnowledgeService und JsonRepository abgebildet.

Die Rollen Projektleiter und Mitarbeiter wurden nicht als eigene Klassen implementiert, da die Aufgabenstellung keine Rechteverwaltung verlangt. Mitarbeitende werden daher als Namen gespeichert.

Diese Entscheidung reduziert die Komplexität und entspricht dem geforderten Prototyp Charakter.

## 6.8 OOP Prinzipien in der Umsetzung

Die überarbeitete Modellierung berücksichtigt folgende objektorientierte Prinzipien:
- Kapselung
Daten werden innerhalb klar definierter Klassen verwaltet.
- Single Responsibility
Jede Klasse besitzt eine klar definierte Aufgabe.
- Trennung von Fachlogik und Benutzeroberfläche
Die GUI greift nicht direkt auf Persistenz zu.
- Erweiterbarkeit
Neue Informationstypen oder Kommentararten könnten leicht ergänzt werden.

## 6.9 Fazit zur Modellierung

Die Weiterentwicklung des Klassendiagramms war ein wesentlicher Lernschritt im Projekt.

Die erste Version war bewusst einfach gehalten.
Im Verlauf der Umsetzung zeigte sich jedoch, dass eine feinere Strukturierung notwendig ist, um:
- fachliche Anforderungen korrekt umzusetzen
- Wartbarkeit zu gewährleisten
- Persistenz strukturiert zu realisieren
- eine saubere Testbarkeit sicherzustellen

Die iterative Anpassung des Modells entspricht einem realistischen Entwicklungsprozess und zeigt den reflektierten Umgang mit objektorientierter Analyse und Design.