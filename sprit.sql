SELECT id from kostenstelle where name = "Auto";
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-09-01 10:00:00', "ausgaben",55.56 ,19 , "tanken", "tag");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-10-16 10:00:00', "ausgaben",47.80 ,19 , "tanken", "tag");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-11-05 10:00:00', "ausgaben",58.10 ,19 , "tanken", "tag");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-12-12 10:00:00', "ausgaben",52.00 ,19 , "tanken", "tag");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2017-01-28 10:00:00', "ausgaben",60.03 ,19 , "tanken", "tag")

Sprit
55,56   16.09.1916
47,80   16.10.1916
58,10   05.11.1916
52,00   12.12.1
60,03   28.01.16


12 Euro pro Monat blabla

INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2017-01-05 10:00:00', "einnahmen",12 ,19 , "blablacar", "tag");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-12-05 10:00:00', "einnahmen",12 ,19 , "blablacar", "tag");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-11-05 10:00:00', "einnahmen",12 ,19 , "blablacar", "tag");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-10-05 10:00:00', "einnahmen",12 ,19 , "blablacar", "tag");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-09-05 10:00:00', "einnahmen",12 ,19 , "blablacar", "tag")


#den brauchts
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-01-01 10:00:00', "einnahmen",0 ,1 , "den brauchts für das jahr", "jahr");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-01-01 10:00:00', "ausgaben",0 ,1 , "den brauchts für das jahr", "jahr");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-01-01 10:00:00', "einnahmen",0 ,1 , "den brauchts für das jahr", "tag");
INSERT INTO eintrag (erstellt, kostenart, betrag, kostenstelle_id, kommentar, abschreibung) VALUES ('2016-01-01 10:00:00', "ausgaben",0 ,1 , "den brauchts für das jahr", "tag")

