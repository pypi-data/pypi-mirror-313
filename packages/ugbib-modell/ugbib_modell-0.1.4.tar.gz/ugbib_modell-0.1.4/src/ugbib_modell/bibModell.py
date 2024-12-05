import psycopg2
import psycopg2.errors
import sys
import platform
import copy

from timeit import default_timer as timer
from datetime import timedelta, datetime

#####################################################################
###   Logger herstellen
#####################################################################
import logging, logging.handlers
logger = logging.getLogger()

from ugbib_divers.bibGlobal import glb

# from Modell import * soll nur folgende Elemente importieren:
__all__ = [
    'textFeld', 'numFeld', 'idFeld',
    'dateFeld', 'timeFeld', 'datetimeFeld',
    'boolFeld',
    'Modell',
    'Relation',
    'BlankToNone',
    'setSearchPath',
]

Plattform = platform.node()
if Plattform == 'cg-test':
    # Wir befinden uns auf dem Hetzner-Server
    PSQL_Server       = 'localhost'
else:
    PSQL_Server       = 'hetzner'
PSQL_Port         = '22555'
PSQL_Database     = 'cg'

def DB_Fehler(Fehler):
    """DB_Fehler - erzeugt aus einem Fehler eine lesbare Fehlermeldung
    
        Erzeugt aus einem Fehler eine lesbare Fehlermeldung
        
        Parameter
            Fehler    Instanz von...
                          ... psycopg2.Error    Im Fall von DB-Fehlern
                          ... Exception         Im Fall von Python Fehlern
    """
    if isinstance(Fehler, psycopg2.Error):
        Meldung = 'DB Fehler: {}'.format(Fehler.pgerror)
    else:
        Meldung = 'Problem: {}'.format(Fehler)
    return Meldung

class Feld():
    """Feld - Bildet ein einzelnes Feld einer Tabelle (Model) ab
    
        Implementiert nur die Grundstruktur eines Feldes.
        Für jeden Typ gibt es abgeleitete Klassen.
        Das Feld enthält nur die Metadaten, nicht den Wert aus der DB o.ä. Der
        wird in den Instanzen von Modell abgebildet.
    """
    
    def __init__(self, tabFeld):
        """__init__(self, tabFeld)
        
            Parameter
                tabFeld   Name der Tabellenspalte (z.B. 'name', 'vorname')
                          in der SQL-Tabelle
            
            Attribute
                Typ       Typ des Feldes
                tabFeld   s. Parameter
        """
        self.tabFeld = tabFeld
        self.Typ = None
    
    def __str__(self):
        return '{} ({})'.format(self.tabFeld, self.Typ)

class textFeld(Feld):
    """textFeld - Feld für den Typ text
    
        Parameter
    """
    
    def __init__(self, tabFeld):
        super().__init__(tabFeld)
        self.Typ = 'text'

class numFeld(Feld):
    """numFeld - Feld für den Typ number (int, real, float usw.)
    """
    
    def __init__(self, tabFeld):
        super().__init__(tabFeld)
        self.Typ = 'num'

class idFeld(Feld):
    """idFeld - Feld für den Typ number (nur int ist sinnvoll), speziell für ID-Feld
        
        Ist identisch mit numFeld, unterscheidet sich nur in den Widgets, die
        readonly eingerichtet werden.
    """
    
    def __init__(self, tabFeld):
        super().__init__(tabFeld)
        self.Typ = 'num'

class dateFeld(Feld):
    """dateFeld - Feld für den Typ date
    """
    
    def __init__(self, tabFeld):
        super().__init__(tabFeld)
        self.Typ = 'date'

class timeFeld(Feld):
    """timeFeld - Feld für den Typ time
    """
    
    def __init__(self, tabFeld):
        super().__init__(tabFeld)
        self.Typ = 'time'

class datetimeFeld(Feld):
    """datetimeFeld - Feld für den Typ datetime
    """
    
    def __init__(self, tabFeld):
        super().__init__(tabFeld)
        self.Typ = 'datetime'

class boolFeld(Feld):
    """boolFeld - Feld für den Typ bool
    """
    
    def __init__(self, tabFeld):
        super().__init__(tabFeld)
        self.Typ = 'bool'

class Modell():
    """Modell - Bildet eine SQL-Tabele ab
    
        Abstrakte Klasse. Für jede SQL-Tabelle muss eine eigene von Modell abgeleitete Klasse
        erstellt werden.
        
        Jede abgeleitete Klasse muss folgendes definieren:
        
            1.  __init__(self, id=None, holen=False) muss
                a)  Tabelle
                    _tab auf den Tabellennamen setzen (z.B. 'tbl_person')
                b)  Felder
                    _felder
                    Liste der Tabellenfelder, jeweils Instanz von einer
                    abgeleiteten Klass von Feld (z.B. textFeld('vorname')
                c)  Klassen Attribut keyFeldNavi setzen. Damit wird das Feld
                    festgelegt, über das Datensätze bevorzugt identifiziert
                    werden. I.d.R. kann das 'id' sein, aber auch
                    'kurz_bez' o.ä. Insb. dient es später als Brücke zwischen
                    Navi und Detailansicht.
                c)  super().__init(tab, __class__, Felder=Felder, id=id, holen=holen)
                    aufrufen.
            2.  Optional, aber sehr empfohlen,
                __str__(self) definieren, z.B.
                    return '{}, {}'.format(self.name, self.vorname)
            3.  Schließlich muss die neu definierte Klasse einmal Klasse.Init()
                aufrufen. Damit werden Initialisierungen aufgerufen, die 
                Klassenattribute von Klasse setzen.

        Parameter
            tab       Name der SQL-Tabelle (ohne Schema. z.B. 'tbl_person')
            Klasse    Zeigt auf die Klasse, die von Modell abgeleitet wird.
                      Dieser Parameter wird beim Aufruf durch __class__ erzeugt
                      Damit wird ermöglicht, dass Modell.__init__
            Felder    Liste der Tabellenfelder (Instanzen von Feld
                      bzw. von den abgeleiteten Klassen)
                      Achtung: Es wird vorausgesetzt, dass jede SQL-Tabelle ein
                      Feld id als primären Schlüssel hat. Dieses Feld muus
                      trotzdem in der Liste der Felder mit aufgeführt sein.
                      Dieses Feld muss das erste Feld sein.
            id        Falls nicht None, wird die ID auf diesen Wert gesetzt.
                      !!! Beachte das Zusammenspiel mit holen !!!
            holen     Falls außerdem holen=True, wird versucht, den entsprechenden
                      Datensatz aus der DB zu holen.
                      Falls holen=False (Default), dient die Instanz i.d.R. dazu,
                      sie gleich anschließend mit save in die DB zu schreiben
                      (insert oder update)
        
        Attribute
            _tab          s.o. tab
            _felder       s.o. Felder
            xxx           Für jedes Feld xxx in _felder hält xxx den Wert des Feldes
            _xxx          Das entsprechende Feld (Instanz von Feld bzw. von einer der
                          abgeleiteten Klassen)
            _relationen   Dictionary von Relationen (Instanzen von Relation)
            W             ModelWidgetsDict
                          So können die Standard-Widgets einer Instanz von Modell
                          abgerufen werden:
                          Person.W.tabFeld.WF für Formulare bzw.
                          Person.W.tabFeld.WT für Tabllenartige Formulare
        
        Attribute, die von abgeleiteten Klassen definiert werden (vgl. weiter oben,
        was von der abgeleiteten Klasse definiert werden muss)
            tab       Name der SQL-Tabelle (ohne Schema, z.B. 'tbl_person')
            Felder    Liste der Tabellenfelder, jeweils Instanz von einer
                      abgeleiteten Klass von Feld (z.B. textFeld('vorname')
    """
    
    def __init__(self, id=None, holen=False):
        """__init__ - Initialisierung bei Instanziierung
        """
        # Wir prüfen, ob Init aufgerufen wurde
        if not self.InitGelaufen:
            sys.exit('Init fuer {} nicht aufgerufen'.format(self))
        # Für jedes Feld ein Attribut hinzufügen
        #
        #     ???   Brauchen wir das wirklich, wenn Init gelaufen ist???
        #
        for F in self._felder:
            # Der Wert des Feldes (initial None)
            setattr(self, F.tabFeld, None)
        # ggf. ID setzen und...
        if id is not None:
            self.id = id
            # ... und Datensatz aus der DB holen
            if holen:
                self.getByID(id)
    
        
    def __str__(self):
        """__str__(self) - Lesbare Darstellung
        
            Sollte in aller Regel überladen werden.
        """
        return 'ID = {}'.format(str(self.id))
        
    
    @staticmethod
    def Init(Klasse):
        """Init - Initialisierung bei der Ableitung von Klassen
        
            Wird ein Modell abgeleitet, z.B. class Person(), so müssen _tab und _felder,
            optional auch _relationen,
            im Kopf der neuen Klasse definiert sein. Etwa so in einer Datei Modelle.py:
            
                class Person(Modell):
                    _tab = 'tbl_person'
                    _felder = [
                        idFeld('id'),
                        textFeld('name'),
                        textFeld('vorname'),
                        textFeld('geschlecht'),
                        ]
                    _relationen = [
                        Relation('geschlecht', Geschlecht, 'kurz_bez')
                        ]
                        
            Wird dann die abgeleitete Klasse importiert, so muss unbedingt einmal Init dieser
            Klasse aufgerufen werden, etwa so:
            
                from Modelle import Person, Geschlecht
                Person.Init(Person)
                Geschlecht.Init(Geschlecht)
        """
        # Wir merken uns, dass für die Klasse Init aufgerufen wurde
        Klasse.InitGelaufen = True
        # Für jedes Feld F...
        for F in Klasse._felder:
            # ... ein Klassen-Attribut mit dem Feld selbst hinzufügen
            setattr(Klasse, '_{}'.format(F.tabFeld), F)
    
        
    def WerteAlsDict(self):
        """WerteAlsDict - Liefert Dict der aktuellen Werte
        """
        return {F.tabFeld : getattr(self, F.tabFeld) for F in self._felder}
    
    
    def WerteAlsListe(self):
        """WerteAlsListe - Liefert Liste der aktuellen Werte
        """
        return [getattr(self, F.tabFeld) for F in self._felder]
        
    
    def ListeFelderMitID(self):
        """ListeFelderMitID - Liste der Felder mit Primärschlüssel id
        
            Wird insb. für SQL benötigt
        """
        return [F.tabFeld for F in self._felder]
        
    
    def ListeFelderOhneID(self):
        """ListeFelderOhneID - Liste der Felder ohne den Primärschlüssel id
        
            Wird insb. für SQL benötigt
        """
        return self.ListeFelderMitID()[1:]
        
    
    def ListeWerteMitID(self):
        """ListeWerteMitID - Liste der Werte mit Primärschlüssel id
        
            Wird insb. für SQL benötigt
        """
        return [getattr(self, F.tabFeld) for F in self._felder]
        
    
    def sqlListeWerteMitID(self):
        """sqlListeWerteMitID - Liste der Werte in '' mit Primärschlüssel id
        
            Wird insb. für SQL benötigt
        """
        return ["'{}'".format(W) for W in self.ListeWerteMitID()]
        
        
    def ListeWerteOhneID(self):
        """ListeWerteOhneID - Liste der Werte ohne Primärschlüssel id
        
            Wird insb. für SQL benötigt
        """
        return self.ListeWerteMitID()[1:]
        
    
    def sqlListeWerteOhneID(self):
        """sqlListeWerteOhneID - Liste der Werte in "" ohne Primärschlüssel id
        
            Wird insb. für SQL benötigt
        """
        return self.sqlListeWerteMitID()[1:]
        
        
    def PlatzhalterOhneID(self):
        """PlatzhalterOhneID - Liste von ? für SQL-Statements
        
            Wird (wohl nur) für SQL-Statements benötigt
        """
        return ['%s' for F in range(len(self._felder) - 1)]
        
    
    def getByID(self, id):
        """getByID - Holt Datensatz aus der DB per id
            
            Parameter
                id        id des Datensatzes, der geholt werden soll
        """
        Erfolg = False
        sql = """
            select {felder}
            from {tabelle}
            where id = %s
        """.format(
                felder = ', '.join(self.ListeFelderMitID()),
                tabelle = self._tab)
        logger.debug('ID: {}. SQL: {}'.format(id, sql))
        
        with glb.DB.cursor() as Cur:
            Cur.execute(sql, (str(id),))
            Ergebnis = Cur.fetchone()
            glb.DB.commit()
            if Ergebnis is not None:
                Erfolg = True
                i = 0
                for F in self._felder:
                    setattr(self, F.tabFeld, Ergebnis[i])
                    i += 1
        
        return Erfolg
        
    
    def getByKey(self, keyFeld, keyWert):
        """getByKey - Holt Datensatz aus der DB per key
        
            keyFeld : Feld in der DB, nach dem gesucht werden soll.
                      Typischerweise ist das eine (eindeutige) Kurzbezeichnung.
                      Es wird unterstellt, dass dieses Feld unique ist.
                      Sicherheitshalber wird aber die Suche auf einen Datensatz
                      beschränkt (LIMIT 1). D.h. das Ergebnis kann unerwartet ausfallen,
                      wenn das Feld nicht unique ist.
            keyWert : Wert, nach dem gesucht werden soll.
        """
        Erfolg = False
        sql = """
            select {felder}
            from {tabelle}
            where {keyFeld} = %s
            limit 1
        """.format(
                felder = ', '.join(self.ListeFelderMitID()),
                tabelle = self._tab,
                keyFeld = keyFeld)
        logger.debug('SQL: {}'.format(sql))
        with glb.DB.cursor() as Cur:
            Cur.execute(sql, (keyWert,))
            Ergebnis = Cur.fetchone()
            glb.DB.commit()
            if Ergebnis is not None:
                Erfolg = True
                i = 0
                for F in self._felder:
                    setattr(self, F.tabFeld, Ergebnis[i])
                    i += 1
        return Erfolg
        
    
    def save(self):
        """save - Schreibt den Datensatz in die DB (insert oder update, je nach id)
        
            Schreibt den Datensatz in die DB. Dabei wird als SQL-Statement verwendet:
                insert    falls id None oder ''
                update    sonst, d.h. id gibt es schon.
            
            Nebeneffekt im Falle von insert:
                id wird auf die id des neu gespeicherten Datensatzes gesetzt
            
            Ergebnis je nach...
                insert erfolgreich
                    id des neu gespeicherten Datensatzes
                update erfolgreich
                    None
                insert oder update nicht erfolgreich
                    von PostgreSQL geworfene Exception
            
            Falls eine andere als von PostgreSQL geworfene Exception auftritt,
            wird diese ausgelöst.
                
            Das Ergebnis ist so gewählt, dass man daran ablesen kann, was passiert ist:
                type(Ergebnis) == int     insert (erfolgreich)
                Ergebnis is None          update (erfolgreich)
                type(Ergebnis) == str     PostgreSQL hat Exception geworfen
        """
        Ergebnis = None
        with glb.DB.cursor() as Cur:
            logger.debug('Modell.save ID:{}'.format(str(self.id)))
            if self.id is None or self.id == '':
                logger.debug('Modell.save, insert Zweig')
                sql = """
                    insert into {tabelle} ({felder})
                    values ({Platzhalter})
                    returning id
                """.format(
                        tabelle = self._tab,
                        felder = ', '.join(self.ListeFelderOhneID()),
                        Platzhalter = ', '.join(self.PlatzhalterOhneID()))
                try:
                    logger.debug('Model.save SQL: {}'.format(
                          Cur.mogrify(sql, (self.ListeWerteOhneID()))))
                    Cur.execute(sql, (self.ListeWerteOhneID()))
                    self.id = Cur.fetchone()[0]
                    glb.DB.commit()
                    Ergebnis = self.id
                except psycopg2.Error as Fehler:
                    Ergebnis = DB_Fehler(Fehler)
                    glb.DB.rollback()
                except:
                    raise
            else:
                logger.debug('Modeell.save, update Zweig')
                sql = """
                    update {tabelle}
                    set ({felder}) = ({platzhalter})
                    where id = %s
                """.format(
                        tabelle = self._tab,
                        felder = ', '.join(self.ListeFelderOhneID()),
                        platzhalter = ', '.join(self.PlatzhalterOhneID()))
                try:
                    logger.debug('Model.save SQL: {}'.format(
                          Cur.mogrify(sql, self.ListeWerteOhneID() + [self.id,])))
                    Cur.execute(sql, self.ListeWerteOhneID() + [self.id,])
                    glb.DB.commit()
                    Ergebnis = None
                except psycopg2.Error as Fehler:
                    Ergebnis = DB_Fehler(Fehler)
                    glb.DB.rollback()
                except:
                    raise
        return Ergebnis
    
    
    def delete(self):
        """delete - Löscht den Datensatz aus der DB
        
            1. Löscht den Datensatz aus der DB (delete),
            2. setzt im Erfolgsfall alle Feler auf None
            3. und liefert als Ergebnis im Falle des Erfolges None, sonst
               eine brauchbare Fehlermeldung, i.d.R. die von PostgreSQL.
            
            Die Nachricht soll geeignet sein, mit flask.flash an den
            Enbenutzer weitergegeben zu werden. Der Fall None (Erfolg) sollte
            von der aufrufenden Routine abgefangen werden.
        """
        Ergebnis = None
        if self.id is not None and self.id != '':
            with glb.DB.cursor() as Cur:
                sql = """
                    delete from {tabelle}
                    where id = %s
                """.format(tabelle = self._tab)
                logger.debug('SQL: {}'.format(sql))
                try:
                    Cur.execute(sql, (self.id,))
                    glb.DB.commit()
                    Ergebnis = 'Datensatz erfolgreich gelöscht.'
                except psycopg2.Error as Fehler:
                    Ergebnis = DB_Fehler(Fehler)
                    glb.DB.rollback()
                except:
                    raise
                else:
                    for F in self._felder:
                        F.Wert = None
        return Ergebnis
    
    
    def getAll(self, Filter=None, Sort=None):
        """getAll - Gibt alle Zeilen der Tabelle als Liste von Instanzen des Modells zurück
        
            Problem?: Es wäre schöner, wenn getAll als statische Klassen-Methode
            definiert werden könnte. Das geht aber nicht, weil die Struktur
            des Modells bekannt sein muss, d.h. es muss eine Instanz (self)
            vorhanden sein. Sonst kann z.B. auch clone() nicht funktionieren.
            
            Parameter:
                Filter    String, der in die (sonst leere) SQL-where-Klausel eingefügt
                          werden kann.
                          Achtung: Es ist dafür zu sorgen, dass hier keine
                          Benutzereingaben verwendet werden, bzw. dass sie gegen
                          SQL injection attacks geprüft sind.
                          Bsp.: 'person_id = 5'
                Sort      String, der in die (sonst leere) SQL-order-Klausel eingefügt
                          werden kann.
                          Achtung: Es ist dafür zu sorgen, dass hier keine
                          Benutzereingaben verwendet werden, bzw. dass sie gegen
                          SQL injection attacks geprüft sind.
                          Bsp.: 'ort, name, vorname'
        """
        # Wir messen die Zeit, die getAll braucht
        start = timer()
        # Ggf. Filter berücksichtigen
        if Filter is None:
            sqlFilter = ''
        else:
            sqlFilter = ' where {} '.format(Filter)
        # Ggf. Sortierung berücksichtigen
        if Sort is None:
            sqlSort = ''
        else:
            sqlSort = ' order by {} '.format(Sort)
        sql = """
            select {felder}
            from {tabelle}
            {filter} {sort}
        """.format(
                tabelle   = self._tab,
                felder    = ', '.join(self.ListeFelderMitID()),
                filter    = sqlFilter,
                sort      = sqlSort)
        with glb.DB.cursor() as Cur:
            Cur.execute(sql)
            Zeilen = Cur.fetchall()
            glb.DB.commit()
            Liste = []
            for Zeile in Zeilen:
                M = self.clone()
                i = 0
                for F in self._felder:
                    setattr(M, F.tabFeld, Zeile[i])
                    i += 1
                Liste.append(M)
        end = timer()
        logger.debug('Modell.getAll brauchte (Zeit) {} (H:MM:SS)'.format(
                            timedelta(seconds=end-start)))
        return Liste
    
    def FactoryGetterAuswahl(self, keyFeldNavi, labelFelder, filterFelder=None, Sort=None):
        """FactoryGetterAuswahl - Liefert Getter für Auswahl (Navi)
            
            Parameter
                keyFeldNavi   Feld aus der Tabelle, das später
                              zur Identifikation des Datensatzes dienen kann.
                              Das ist v.a. für den Navi eines Formulars, i.a.
                              sonst für Schnittstellen relevant.
                              Bsp.: id, kurz_bez
                              Typ: str
                labelFelder   Tupel/Liste von Feldern, aus denen ein Label
                              zusammengesetzt werden kann.
                              Bsp.: (name, vorname, ort)
                filterFelder  Tupel/Liste von Feldern, nach denen ggf. gefiltert
                              werden soll.
                              Typ: Tupel/Liste von Feldern
                              Bsp.: ('name', 'vorname', 'plz')
                              Default: None. In diesem Fall wird labelFelder verwendet
                Sort          Vgl. Sort von getAll
        """
        
        def Getter(Filter=None):
            """Getter - Liefert Auswahl für Navi
            
                Getter wird nie direkt aufgerufen. Getter wird stattdessen
                als Ergebnis der FactoryGetterAuswahl zurückgegeben, s.d.
                dieser Getter dann an das Navi weitergereicht werden kann.
                
                Parameter
                    Filter    String, nach dem ggf. gesucht werden soll. Sonst None
            """
            if Filter is None or Filter.strip() == '':
                FilterSQL = None
            else:
                FilterFelder = filterFelder if filterFelder is not None else labelFelder
                FilterSQL = "lower({}) like '%{}%'".format(' || '.join(FilterFelder), Filter.lower())
            Zeilen = self.getAll(FilterSQL, Sort)
            Ergebnis = []
            for Zeile in Zeilen:
                key = getattr(Zeile, self.keyFeldNavi)
                label = ', '.join([str(getattr(Zeile, feld)) for feld in labelFelder])
                Ergebnis.append((key, label))
            return Ergebnis
        
        return Getter
    
    def FactoryGetterValues(self):
        """FactoryGetterValues - Liefert Getter für WerteAlsDict
        
        """
        
        def Getter(keyValue=None):
            M = self.clone()
            if self.keyFeldNavi == 'id':
                M.getByID(keyValue)
            else:
                M.getByKey(self.keyFeldNavi, keyValue)
            return M.WerteAlsDict()
        
        return Getter
    
    def FactorySaverValues(self):
        """FactorySaverValues - Liefert Saver für Dictionary der Werte
        
            Gegenstück zu FactoryGetterValues
            Liefert einen Saver, der die Werte aus einem Dictionary in dem Modell
            sichert (save).
            
            Der Saver gibt gibt den Rückgabewert von save zurück. Vgl. dort
            
            Beachte:
                Der Saver hat den beabsichtigten Nebeneffekt, dass in dem Dict das
                Feld zu keyFeldNavi auf den Wert nach dem Speichern gesetzt wird.
                Das ist relevant, wenn der Datensatz neu angelegt wird, folglich
                noch keine id (oder eben keinen Wert für keyFeldNavi) hat. Der wird
                auf diesem Wege zurückgegeben.
        """
        
        def Saver(values):
            """Saver
            
                Parameter
                    values      Dict von Werten, z.B. aus einem Formular
                                Es ist sicherzustellen, dass alle Attribute des
                                Modells in values vorkommen. Sonst sind undefinierte
                                Ergebnisse oder Fehler möglich.
                
                Ergebnis        Vgl. Rückgabewert von save
            """
            M = self.clone()
            for tabFeld in values:
                setattr(M, tabFeld, values[tabFeld])
            ergebnis = M.save()
            values[self.keyFeldNavi] = getattr(M, self.keyFeldNavi)
            return ergebnis
        
        return Saver
    
    def FactoryDeleterValues(self):
        """FacroryDeleterValues - Liefert Deleter für Datensatz
        
            Liefert einen Deleter der einen Datensatz aus der DB löscht.
            
            Der Deleter gibt eine lesbare Nachricht (Flash in Anlehnung an Flask)
            über den Erfolg des DELETE zurück.
        """
        
        def Deleter(values):
            """Deleter
            
                Parameter
                    values      Dict von Werten, z.B. aus einem Formular.
                                Tatsächlich ist letztlich nur der Wert von id in 
                                values relevant.
                
                Ergebnis        lesbare Nachricht (Flash in Anlehnung an Flask)
                                über den Erfolg des INSERT/UPDATE
                                Geeignet zum Logging oder als Nachricht an den
                                User.
            """
            M = self.clone()
            for tabFeld in values:
                setattr(M, tabFeld, values[tabFeld])
            return M.delete()
            
        return Deleter
    
    def FactoryGetterChoices(self, keyFeld):
        """FactoryGetterChoices - Liefert Getter für mögliche Werte für Radio/Select
        
            Parameter
                keyFeld     Feld, für das mögliche Werte (i.d.R. durch eine Relation)
                            in einem Select- oder RadioSet-Widget zur Auswahl angeboten
                            werden sollen.
                            Bsp.: 'farbe'
        """
        
        def Getter():
            if keyFeld in self._relationen:
                return self._relationen[keyFeld].getChoices()
            else:
                return None
        
        return Getter
    
    def FactoryGetterDicts(self, keyFeld=None, FilterFelder=None, Sort=None):
        """FactoryGetterDicts - Liefert verschiedene Getter für FormList
            
            Je nach keyFeld ist der Getter für FormListeN1 oder FormListe.
            
            keyFeld ist None
                Der Getter liefert später alle Datensätze des Modells,
                die dem Filter entsprechen. Diese Variante ist für normale
                Listenansichten vorgesehen.
            keyFeld ist str (also nicht None, sondern ein echtes Feld
                Der Getter liefert später alle Datensätze des Modells,
                deren keyFeldNavi den Wert von
                keyValue haben. Damit werden dann z.B. für n-1 Relationen Listen von Formularen 
                gebildet. keyFeld ist i.d.R. id, kann aber bei der Instanziierung von Modell
                z.B. auf kurz_bez gesetzt werden.
                In diesem Fall wird Filter ignoriert
            
            Bsp.:
                Für das Modell Personen gibt es die n-  Relation
                    Person <-- PersonGruppe --> Gruppe
                Der linke Teil dieser Relation neben einem Hauptformular (Person) als
                Unterformular, d.h. als Liste von Formularen (FormListe) gezeigt werden.
                D.h. aus PersonGruppe werden alle Datensätze gesucht, für die person_id = Person.id
                ist. Der Getter liefert diese Datensätze als Liste von Dicts, aus denen dann
                die Formulare hergestellt werden können.
        """
        
        def Getter(Filter=None):
            """Getter - 
            
                Parameter
                    filter    Filter für die Auswahl
            """
            if Filter is None or Filter.strip() == '':
                FilterSQL = None
            else:
                FilterSQL = "lower({}) like '%{}%'".format(
                                ' || '.join(FilterFelder),
                                Filter.lower())
            Liste = self.getAll(Filter=FilterSQL, Sort=Sort)
            logger.debug(Liste)
            return [m.WerteAlsDict() for m in Liste]
        
        def GetterByKey(keyValue):
            """GetterByKey- 
            
                Parameter
                    keyValue    Wert, den keyFeldNavi in allen gesammelten Datensätzen haben muss
            """
            Liste = self.getAll(Filter=f'{keyFeld} = {keyValue}', Sort=Sort)
            for m in Liste:
                logger.debug(m.WerteAlsDict())
            return [m.WerteAlsDict() for m in Liste]
        
        if keyFeld is None:
            return Getter
        else:
            return GetterByKey
    
    def getSome(self):
        """getSome - Holt eine beliebige Zeile aus der Tabelle
        
            Nur zu Testzwecken, um die Modelle zu checken.
            Vgl. z.B. Tagung/Modelle.py ganz am Ende
        """
        sql = 'select id from {tabelle} limit 1'.format(tabelle = self._tab)
        with glb.DB.cursor() as Cur:
            Cur.execute(sql)
            ID = Cur.fetchone()[0]
            glb.DB.commit()
            M = self.clone()
            M.getByID(ID)
            return M
    
    
    def clone(self):
        """clone - Erzeugt identische, aber neue Kopie der Instanz
        
            Es geht vor allem darum, dass alle dynamisch erzeugten Attribute, d.h.
            die Felder der DB-Tabelle, mit übernommen werden.
        """
        return copy.deepcopy(self)
        
    
    def Relationen(self):
        """Relationen - Liefert Liste der Relationen des Modells
        """
        return self._relationen
        

    def getChoices(self, Relation_bez):
        """getChoices - Liefert Liste von Tupeln für Radio- und Select-Widgets
        
            Bsp.: [('M', 'M: Mitglied'), ('Pr', 'Pr: Priester in der CG')]
            Geeignet für Radio- und Select-Widgets, vgl. WTForms.
        """
        return self._relationen[Relation_bez].getChoices()


class Relation():
    """Relation - Beschreibt Relation eines Modells zu einem anderen Modell
    
          Jedes Modell hat eine (möglicherweise leere) Liste (Dictionary) von Relationen, die
          jeweils eine Verknüpfung zu einem anderen Modell beschreibt.
          
          Solch eine Relation bildet den Fall ab, dass ein Feld des Modells in der
          SQL-DB mit der Eigenschaft "references ..." definiert ist.
          Es ist also eine n-1-Relation.
          
          Realisiert wird das durch Feld.Relation, d.h. jedes Feld eines Modells
          kann eine Relation haben. ???
          
          Zunächst ist nur der Fall implementiert, dass die Verknüpfung über genau
          ein Feld erfolgt (typischerweise id oder kurz_bez).
          
          Die Liste aller Relationen eines Modells kann über die Funktion
          Modell.Relationen() abgerufen werden.
          
          Parameter
              tabFeld       Tabellenfeld, das auf eine andere Tabelle (Modell) zeigt
                            z.B. 'geschlecht'
                            Typ: str
              ZielModell    Modell (Tabelle), auf das verwiesen wird
                            z.B. Geschlecht
                            Typ: von Modell abgeleitetes Modell
              ZielTabFeld   Tabellenfeld im ZielModell, auf das verwiesen wird
                            z.B. 'kurz_bez'
                            Typ: str
          
          Attribute
              tabFeld       + siehe Parameter
              ZielModell    +
              ZielTabFeld   +
              
              _sqlAnzeige   SQL-Schnipsel für die Anzeige in einer Werte-Auswahl
                            Bsp.: "name || ', ' || vorname || '(' || stadt || ')'"
                            Typ: str
                            Default: self.ZielTabFeld
                            Wird später als 'label' in den Widgets verwendet
              _SQLsort      SQL-Schmipsel für Sortierung
                            Bsp.: 'order by name, vorname'
    """
    def __init__(self, tabFeld, ZielModell, ZielTabFeld, NoneErlaubt=False):
        self.tabFeld = tabFeld
        self.ZielModell = ZielModell
        self.ZielTabFeld = ZielTabFeld
        self.NoneErlaubt = NoneErlaubt
        self._SQLanzeige = self.ZielTabFeld
        self._SQLsort = ''
        
    
    def __str__(self):
        return('Relation: Feld: {} - ZielModell: {} - ZielFeld: {}'.format(self.tabFeld,
              self.ZielModell, self.ZielTabFeld))
    
    
    def __enter__(self):
        return self
    
    
    def __exit__(self, exc_type, exc_value, traceback):
        return True
    
    
    def setSQLanzeige(self, sql):
        self._SQLanzeige = sql
    
    
    def setSQLsort(self, sql):
        self._SQLsort = sql
    
    
    def _MoeglicheWerte(self):
        """MoeglicheWerte - Liefert mögliche Werte für die Relation
            
            Liest aus der Ziel-Tabelle die möglichen Werte der Relation
        
            Ergebnis: Liste von Tupeln als Zwischenergebnis
                      für SelectAuswahl und RadioAuswahl
        """
        sql = """
            select {Key} as key, {Anzeige} as anzeige
            from {Tabelle} {Sort}
          """.format(
                  Key = self.ZielTabFeld,
                  Anzeige = self._SQLanzeige,
                  Tabelle = self.ZielModell._tab,
                  Sort=self._SQLsort)
        with glb.DB.cursor() as Cur:
            Cur.execute(sql)
            Ergebnis = Cur.fetchall()
            glb.DB.commit()
            Liste = []
            if self.NoneErlaubt:
                Liste.append(['', '--'])
            for (key, anzeige) in Ergebnis:
                Liste.append([key, anzeige])
        return Liste
    
    
    def getChoices(self):
        """getChoices - Liefert die Choices für Radio- oder Select-Widgets
        
            Dabei kann noch eine Vorbearbeitung implementiert werden.
        """
        # Mögliche Vorbearbeitung
        return self._MoeglicheWerte()
        

###
###   Helfer, Filter u.a.
###
def BlankToNone(s):
    """BlankToNone - Macht None aus einem leeren String
        
        Wird als Filter für WTForms verwendet.
        
        In der Regel in dem Fall, dass ein IntegerField NULL/None zulässt.
        Das ist z.B. dann der Fall, wenn es mit Optional validiert wird.
        In diesem Fall gibt aber das Formular '' (also einen leeren String)
        zurück, der dann durch None ersetzt werden muss.
    """
    return s or None

def setSearchPath(searchPath):
    """setSearchPath - Setzt für den aktuellen User den search_path in der PostgreSQL-DB
    """
    sql = f'set search_path to {searchPath}'
    logger.debug(f'{sql=}')
    try:
        with glb.DB.cursor() as Cur:
            Cur.execute(sql)
        glb.DB.commit()
    except Exception as e:
        logger.error(f'setSearchPath fehlgeschlagen: {e}')
        return False
    return True
