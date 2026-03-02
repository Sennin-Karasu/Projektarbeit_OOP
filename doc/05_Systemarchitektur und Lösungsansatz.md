
# 5 Systemarchitektur und Lösungsansatz
## 5.1 Architekturüberblick

Zur Umsetzung der definierten Anforderungen wurde eine klar strukturierte, objektorientierte Architektur gewählt. Die Anwendung ist in logisch getrennte Verantwortungsbereiche gegliedert, um Wartbarkeit, Erweiterbarkeit und Testbarkeit zu gewährleisten.

Die Architektur besteht aus folgenden Hauptkomponenten:
- Domänenmodell
- Service Logik
- Repository zur Persistenz
- Benutzeroberfläche

Diese Struktur ermöglicht eine klare Trennung zwischen fachlicher Logik, Datenhaltung und Darstellung.

## 5.2 Domänenmodell

Das Domänenmodell bildet die fachliche Grundlage der Applikation. Es besteht aus den zentralen Klassen:
- Projekt
- Information
- Kommentar

Diese Klassen repräsentieren die fachlichen Objekte der Aufgabenstellung. Jedes Objekt besitzt klar definierte Attribute und Verantwortlichkeiten.

Beziehungen zwischen den Klassen:
- Ein Projekt enthält mehrere Informationen.
- Eine Information kann mehrere Kommentare besitzen.
- Ein Kommentar ist eindeutig einer Information zugeordnet.

Die Struktur entspricht dem erstellten Klassendiagramm und bildet die Grundlage der Implementierung.

## 5.3 Service Schicht

Die Service Schicht übernimmt die fachliche Logik der Anwendung. Sie koordiniert die Interaktion zwischen Benutzeroberfläche und Domänenmodell.

Zu den Aufgaben der Service Schicht gehören:
- Anlegen neuer Projekte
- Hinzufügen von Informationen zu Projekten
- Validierung der maximalen Anzahl von Tags
- Verarbeitung von Kommentaren, Ergänzungen und Korrekturen
- Durchführung der Tag Suche mit lockerer Logik

Durch diese Trennung bleibt die Benutzeroberfläche frei von fachlicher Logik.

## 5.4 Persistenz

Zur dauerhaften Speicherung der Daten wurde eine JSON basierte Serialisierung gewählt.

Begründung:
- Die erwartete Datenmenge ist auf etwa 100 Einträge begrenzt.
- Eine relationale Datenbank ist für diesen Prototyp nicht erforderlich.
- JSON ermöglicht eine einfache und transparente Speicherung der Objektstruktur.

Beim Beenden der Applikation werden alle Daten in einer JSON Datei gespeichert. Beim Start werden diese wieder eingelesen und in entsprechende Objekte rekonstruiert.

## 5.5 Benutzeroberfläche

Die Benutzeroberfläche wurde mit PySide6 umgesetzt. Ziel war eine übersichtliche und klar strukturierte Darstellung der Informationen.

Die Oberfläche ermöglicht:
- Auswahl und Anzeige von Projekten
- Erfassen neuer Informationen
- Kommentieren bestehender Einträge
- Durchführen der Tag Suche
- Anzeige der Detailansicht mit klarer Unterscheidung zwischen Originaltext, Ergänzung und Korrektur

Die Benutzeroberfläche greift ausschliesslich über definierte Schnittstellen auf die Service Schicht zu.

## 5.6 Begründung des Lösungsansatzes

Die gewählte Architektur erfüllt folgende Ziele:
- Klare Trennung von Verantwortlichkeiten
- Gute Testbarkeit der fachlichen Logik
- Wartbarkeit und Erweiterbarkeit
- Direkte Ableitbarkeit aus dem Klassendiagramm

Auf komplexe Entwurfsmuster oder Polymorphie wurde bewusst verzichtet, um die Lösung verständlich und überschaubar zu halten.