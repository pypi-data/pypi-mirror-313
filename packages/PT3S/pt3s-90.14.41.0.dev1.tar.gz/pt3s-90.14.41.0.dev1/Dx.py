"""

"""

import shapely
import geopandas
#import doctest
#import unittest
#import argparse
import sqlite3
import pyodbc
import math
#import glob
import logging
#import struct
#import base64
#import time
#import h5py
#import tables
import numpy as np
import pandas as pd
import re
import sys
import os

import uuid

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import or_
#from sqlalchemy import select
from sqlalchemy import text

import inspect

#import warnings
__version__ = '90.14.25.0.dev1'

# warnings.filterwarnings("ignore")


# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S')
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context:', '.'))
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format(
        'in MODULEFILE: Not __main__ Context: ', '__name__: ', __name__, " ."))

try:
    from PT3S import Xm
except ImportError:
    logger.debug("{0:s}{1:s}".format(
        'ImportError: ', 'from PT3S import Xm - trying import Xm instead ... maybe pip install -e . is active ...'))
    import Xm


try:
    from PT3S import dxAndMxHelperFcts
except ImportError:
    logger.debug("{0:s}{1:s}".format(
        'ImportError: ', 'from PT3S import dxAndMxHelperFcts - trying import dxAndMxHelperFcts instead ... maybe pip install -e . is active ...'))
    import dxAndMxHelperFcts

#vVBEL_edges =['ROHR','VENT','FWVB','FWES','PUMP','KLAP','REGV','PREG','MREG','DPRG','PGRP']
#vVBEL_edgesD=[''    ,'DN'  ,''    ,'DN'  ,''    ,'DN'  ,'DN'  ,'DN'  ,'DN'  ,'DN'  ,'']

try:
    from PT3S import dxDecodeObjsData
except:
    import dxDecodeObjsData

def fXk(row):
        """
        :param row: a df's row     
        :return: (pk,rk,tk)                
        """    
        xk=str(uuid.uuid1().int>>63)
        return(xk,xk,xk)

class DxError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def fimportFromSIR3S(dx
                    ,OBJSrc
                    ,qSrc
                    ,objSrc
                    ,objDst  
                    ,logRows=True
                    ):       
    """
    work on object to import and/or decision if import at all 
    
    :param dx: Dx object of Dst
    :type dx: Dx.Dx 
    :param OBJSrc: 
    :type OBJSrc: sqlalchemy.orm.decl_api.DeclarativeMeta
    :param qSrc: the query which delivered the objects from Src
    :type qSrc: sqlalchemy.orm.query.Query     
    :param objSrc: the object from Src 
    :type objSrc: sqlalchemy.ext.automap         
    :param objDst: the object to import in Dst
    :type objDst: sqlalchemy.ext.automap 
    :param logRows: decide if fcts shall generate Log-Output
    :type logRows: bool, optional, default=True   
    
    :return: (objDst,toImport) 

    .. note::         
        At the time the function is called, objDst is already completely generated from objSrc (taking into account the specifications for e.g. fk-transfers from Templates). Whether objDst should really be imported and if so what further changes need to be made can often only be decided on a project-specific basis. Furthermore the decision may not be possible at object level alone, but all objects of the type must be taken into account, possibly even the entire model. Therefore, the Dst's dx and Src's connections are passed to make project-specific imports (via project-specific fimportFromSIR3S-functions) more flexible and powerful.
    """           
    
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    #logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

    try:
        
        objTYPE=OBJSrc.__table__.name
        
        cols=dx.dataFrames[objTYPE].columns.to_list()
        
        # LogRow
        logRow=f"{objTYPE}"
        for attr in cols:            
            value=getattr(objDst,attr)  
            logRow=f"{logRow} {attr} {value}"        
        if logRows:
            logger.debug(f"{logStr} {logRow}")
            
        return(objDst,True)

    except Exception as e:
       logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
           logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
       logger.error(logStrFinal)

    finally:
       pass
       #logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))


class Dx():
    """SIR 3S Access/SQLite to pandas DataFrames.

    Args:
        * dbFile (str): SIR 3S Access/SQLite File
            * wird wie angegeben gesucht
            * ohne Pfadangabe wird im aktuellen Verz. gesucht und (wenn das Fehl schlaegt) im uebergeordneten

    Attributes:
        * dbFile: verwendetes dbFile
        
        * QGISmodelXk: Modell-Pk des in QGIS anzuzeigenden Modells (wird von den QGIS-Views ausgewertet)

        * dataFrames: enthaelt alle gelesenen Tabellen und konstruierten Views

        * viewSets: fasst View- bzw. Tabellennamen zu Kategorien zusammen; dient zur Uebersicht bei Bedarf
            * allTables
            * pairTables
            * pairViews_BZ
            * pairViews_ROWT  
            * pairViews_ROWD
            * notPairTables
            * notPairTablesProbablyNotSir3sTables
            * notPairViews
            * notPairViewsProbablyNotSir3sTables

        * zu den Spaltennamen der Views:
            * grundsaetzlich die Originalnamen - aber ...
                * bei den _BVZ_ Views:
                    * :_BZ, wenn Spalten Namensgleich
                * Datenebenen:
                    * _VMBZ,_VMVARIANTE,_VMBASIS, wenn Spalten Namensgleich
                * CONT:
                    * immer _CONT
                * VKNO:
                    * immer _VKNO
                * VBEL:
                    * immer _i und _k fuer die Knotendaten

        * V3-Views i.e. dataFrames['V3_KNOT']
            * V3_KNOT: Knoten: "alle" Knotendaten      
            * V3_ROHR: Knoten: "alle" Rohrdaten  
            * V3_FWVB: Knoten: "alle" FWVB-Daten

            * V3_SWVT
                * 1 Zeile pro ZEIT und W; cols sind NAMEn der SWVT 
            * V3_RSLW_SWVT
                * 1 Zeile pro RSLW der aktiv eine SWVT referenziert

            * V3_VBEL: Kanten: "alle" Verbindungselementdaten des hydr. Prozessmodells
                * Multiindex:
                    * OBJTYPE
                    * OBJID (pk)
                * Graph Example:
                    * vVbel=self.dataFrames['V3_VBEL'].reset_index()
                    * G=nx.from_pandas_edgelist(df=vVbel, source='NAME_i', target='NAME_k', edge_attr=True) 
                    * vKnot=self.dataFrames['V3_KNOT']
                    * nodeDct=vKnot.to_dict(orient='index')
                    * nodeDctNx={value['NAME']:value|{'idx':key} for key,value in nodeDct.items()}
                    * nx.set_node_attributes(G,nodeDctNx)
                    
            * V3_DPKT: ausgewaehlte Daten von Datenpunkten
            * V3_RKNOT: Knotendaten des Signalmodells
                * Kn: Knotenname
                * OBJTYPE: der Typname des Elementes des Signalmodells z.B. RADD
            * V3_RRUES: 
                * wie V_BVZ_RUES - mit folgenden zusaetzlichen Spalten:
                    * pk_DEF	
                    * IDUE_DEF	
                    * OBJTYPE_SRC      RXXX-Objekttyp der das Signal definiert welches die Ue repraesentiert	                    
                    * Kn_SR            Signal fuer das die Ue ein Alias ist (KA des RXXX)
                    * NAME_CONT_SRC    Block in dem das Signal definiert wird (das RXXX-Element liegt)

            * V3_RVBEL: Kantendaten des Signalmodells
                * Multiindex:
                    * OBJTYPE_i
                    * OBJTYPE_k                
                * RUES-RXXX sind in den Spalten 'OBJTYPE_i','OBJID_i','Kn_i','KnExt_i','NAME_CONT_i' durch die RUES-Quelle ersetzt
                * Graph Example:
                    * vRVbel=self.dataFrames['V3_RVBEL'].reset_index()
                    * GSig=nx.from_pandas_edgelist(df=vRVbel, source='Kn_i', target='Kn_k', edge_attr=True, create_using=nx.DiGraph())
                    * nodeDct=vRknot.to_dict(orient='index')
                    * nodeDctNx={value['Kn']:value|{'idx':key} for key,value in nodeDct.items()}
                    * nx.set_node_attributes(GSig,nodeDctNx)
                                    
        * viewSets['pairViews_BZ']:
            * ['V_BVZ_ALLG'
            ...
            *, 'V_BVZ_WIND']
        * viewSets['pairViews_ROWS']:
            * ['V_BVZ_ANTE'
            ...
            *, 'V_BVZ_ZEP1', 'V_BVZ_ZEP2']
        * viewSets['pairViews_ROWT']:
            * ['V_BVZ_LFKT'
            ...
            *, 'V_BVZ_RCPL' # da RCPL_ROWT existiert "landet" RCPL bei den ROWTs
            ...
            , 'V_BVZ_WTTR']
            * enthalten alle Zeiten
            * Spalte lfdNrZEIT beginnt mit 1 fuer die chronologisch 1. Zeit (na_position='first')
        * viewSets['pairViews_ROWD']:
            * ['V_BVZ_DTRO']
        * viewSets['notPairViews']:
            * ['V_AB_DEF', 'V_AGSN', 'V_ARRW', 'V_ATMO'
            *, 'V_BENUTZER', 'V_BREF'
            *, 'V_CIRC', 'V_CONT', 'V_CRGL'
            *, 'V_DATENEBENE', 'V_DPGR_DPKT', 'V_DPKT', 'V_DRNP'
            *, 'V_ELEMENTQUERY'
            *, 'V_FSTF', 'V_FWBZ'
            *, 'V_GKMP', 'V_GMIX', 'V_GRAV', 'V_GTXT'
            *, 'V_HAUS'
            *, 'V_LAYR', 'V_LTGR'
            *, 'V_MODELL', 'V_MWKA'
            *, 'V_NRCV'
            *, 'V_OVAL'
            *, 'V_PARV', 'V_PGPR', 'V_PLYG', 'V_POLY', 'V_PROZESSE', 'V_PZON'
            *, 'V_RCON', 'V_RECT', 'V_REGP', 'V_RMES_DPTS', 'V_ROHR_VRTX', 'V_RPFL', 'V_RRCT'
            *, 'V_SIRGRAF', 'V_SOKO', 'V_SPLZ', 'V_STRASSE', 'V_SYSTEMKONFIG'
            *, 'V_TIMD', 'V_TRVA'
            *, 'V_UTMP'
            *, 'V_VARA', 'V_VARA_CSIT', 'V_VARA_WSIT', 'V_VERB', 'V_VKNO', 'V_VRCT'
            *, 'V_WBLZ']
    Raises:
        DxError
    """

    def __init__(self, dbFile):

        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.#########'))

        try:
            if os.path.exists(dbFile):
                if os.access(dbFile, os.W_OK):
                    pass
                else:
                    logger.debug(
                        "{:s}dbFile: {:s}: Not writable.".format(logStr, dbFile))
                    if os.access(dbFile, os.R_OK):
                        pass
                    else:
                        logStrFinal = "{:s}dbFile: {:s}: Not readable!".format(
                            logStr, dbFile)
                        raise DxError(logStrFinal)
            else:
                # pruefen, ob dbFile im uebergeordneten Verzeichnis existiert
                logger.debug("{:s}dbFile: {:s}: Not existing! Suche im uebergeordneten Verz. ...".format(
                    logStr, dbFile))

                dbFileAlt = dbFile
                dbFile = os.path.join('..', dbFileAlt)
                if os.path.exists(dbFile):
                    if os.access(dbFile, os.W_OK):
                        pass
                    else:
                        logger.debug(
                            "{:s}dbFile: {:s}: Not writable.".format(logStr, dbFile))
                        if os.access(dbFile, os.R_OK):
                            pass
                        else:
                            logStrFinal = "{:s}dbFile: {:s}: Not readable!".format(
                                logStr, dbFile)
                            raise DxError(logStrFinal)
                else:
                    logStrFinal = "{:s}dbFile: {:s}: Not existing!".format(
                        logStr, dbFile)
                    raise DxError(logStrFinal)

            # das dbFile existiert und ist lesbar
            logger.info("{:s}dbFile (abspath): {:s} exists readable ...".format(
                logStr, os.path.abspath(dbFile)).replace('wolters','aUserName').replace('jablonski','aUserName'))

            self.dbFile = dbFile

            # Access oder SQLite
            dummy, ext = os.path.splitext(dbFile)

            if ext == '.mdb':
                Driver = [x for x in pyodbc.drivers() if x.startswith(
                    'Microsoft Access Driver')]
                if Driver == []:
                    logStrFinal = "{:s}{:s}: No Microsoft Access Driver!".format(
                        logStr, dbFile)
                    raise DxError(logStrFinal)

                # ein Treiber ist installiert
                conStr = (
                    r'DRIVER={'+Driver[0]+'};'
                    r'DBQ='+dbFile+';'
                )
                logger.debug("{0:s}conStr: {1:s}".format(logStr, conStr))

                # Verbindung ...
                if True:
                    from sqlalchemy.engine import URL
                    connection_url = URL.create(
                        "access+pyodbc", query={"odbc_connect": conStr})
                    logger.debug("{0:s}connection_url type: {1:s}".format(
                        logStr, str(type(connection_url))))
                    from sqlalchemy import create_engine
                    engine = create_engine(connection_url)
                    logger.debug("{0:s}engine type: {1:s}".format(
                        logStr, str(type(engine))))
                    con = engine.connect()
                    logger.debug("{0:s}con type: {1:s}".format(
                        logStr, str(type(con))))

                    if True:
                        from sqlalchemy import inspect
                        insp = inspect(engine)
                        tableNames = insp.get_table_names()  # insp.get_view_names()
                        cur = con
                    else:
                        cur = con
                        tableNames = engine.table_names()
                else:
                    con = pyodbc.connect(conStr)
                    cur = con.cursor()
                    # all Tables in DB
                    tableNames = [
                        table_info.table_name for table_info in cur.tables(tableType='TABLE')]
                    viewNames = [
                        table_info.table_name for table_info in cur.tables(tableType='VIEW')]

            elif ext == '.db3':
                con = sqlite3.connect(dbFile)
                cur = con.cursor()
                cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table';")
                l = cur.fetchall()
                tableNames = [x for x, in l]

                cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='view';")
                l = cur.fetchall()
                viewNames = [x for x, in l]

            else:
                logStrFinal = "{:s}dbFile: {:s} ext: {:s}: unbekannter DB-Typ (.mdb und .db3 sind zulaessig)".format(
                    logStr, dbFile, ext)
                raise DxError(logStrFinal)

            logger.debug("{0:s}tableNames: {1:s}".format(
                logStr, str(tableNames)))
            allTables = set(tableNames)

            logger.debug("{0:s}viewNames: {1:s}".format(
                logStr, str(viewNames)))
            #allViews = set(viewNames)

            # pandas DataFrames
            self.dataFrames = {}

            # Mengen von Typen von Tabellen und Views
            pairTables = set()
            pairViews = set()
            pairViews_BZ = set()
            pairViews_ROWS = set()
            pairViews_ROWT = set()
            pairViews_ROWD = set()

            # SIR 3S Grundtabellen und -views lesen
            try:
                dfViewModelle = pd.read_sql(fHelperSqlText(
                    'select * from VIEW_MODELLE'), con)
                self.dataFrames['VIEW_MODELLE'] = dfViewModelle
            except pd.io.sql.DatabaseError as e:
                logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                    logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
                logger.error(logStrFinal)
                raise DxError(logStrFinal)

            try:
                dfCONT = pd.read_sql(fHelperSqlText('select * from CONT'), con)
            except pd.io.sql.DatabaseError as e:
                logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                    logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
                logger.error(logStrFinal)
                raise DxError(logStrFinal)

            # try:
            #     dfKNOT = pd.read_sql(fHelperSqlText('select * from KNOT'), con)
            # except pd.io.sql.DatabaseError as e:
            #     logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
            #         logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
            #     logger.error(logStrFinal)
            #     raise DxError(logStrFinal)

            # Paare
            for pairType in ['_BZ', '_ROWS', '_ROWT', '_ROWD']:
                logger.debug(
                    "{0:s}pair-tables: pairType: {1:s}:".format(logStr, pairType))
                #tablePairsBVBZ=[(re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_info.table_name).group('BV'),table_info.table_name) for table_info in cur.tables(tableType='TABLE') if re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_info.table_name) != None]
                tablePairsBVBZ = [(re.search('(?P<BV>[A-Z,1,2,_]+)('+pairType+')$', table_name).group('BV'), table_name)
                                  for table_name in tableNames if re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$', table_name) != None]
                for (BV, BZ) in tablePairsBVBZ:

                    if BV not in tableNames:
                        logger.debug(
                            "{0:s}BV: {1:s}: BV-Tabelle gibt es nicht (BZ: {2:s}). Falsche Paar-Ermittlung? Weiter. ".format(logStr, BV,BZ))
                        continue
                    if BZ not in tableNames:
                        logger.debug(
                            "{0:s}BZ: {1:s}: BZ-Tabelle gibt es nicht (BZ: {2:s}). Falsche Paar-Ermittlung? Weiter. ".format(logStr, BZ, BV))
                        continue

                    #if BZ == 'PGRP_PUMP_BZ':  # BV: PUMP BVZ: PGRP_PUMP_BZ V: V_PUMP - Falsch!; wird unten ergaenzt
                    #    continue

                    # TabellenNamen in entspr. Mengen abspeichern
                    pairTables.add(BV)
                    pairTables.add(BZ)

                    # VName
                    VName = 'V_BVZ_'+BV

                    dfBV, dfBZ, dfBVZ = fHelper(
                        con, BV, BZ, dfViewModelle, dfCONT, pairType, ext)

                    rows, cols = dfBVZ.shape
                    logger.debug("{0:s}BV: {1:12s} BVZ: {2:12s} V: {3:15s} constructed with {4:8d} rows and {5:3d} cols.".format(
                        logStr, BV, BZ, VName, rows, cols))

                    self.dataFrames[BV] = dfBV
                    self.dataFrames[BZ] = dfBZ
                    self.dataFrames[VName] = dfBVZ

                    # ViewName in entspr. Menge abspeichern
                    pairViews.add(VName)
                    if pairType == '_BZ':
                        pairViews_BZ.add(VName)
                    elif pairType == '_ROWS':
                        pairViews_ROWS.add(VName)
                    elif pairType == '_ROWT':
                        pairViews_ROWT.add(VName)
                    elif pairType == '_ROWD':
                        pairViews_ROWD.add(VName)

            # BVZ-Paare Nachzuegler
            # for (BV, BZ) in [('PGRP_PUMP', 'PGRP_PUMP_BZ'), ('RMES_DPTS', 'RMES_DPTS_BZ')]:

            #     dfBV, dfBZ, dfBVZ = fHelper(
            #         con, BV, BZ, dfViewModelle, dfCONT, '_BZ', ext)

            #     VName = 'V_BVZ_'+BV
            #     self.dataFrames[VName] = dfBVZ

            #     rows, cols = dfBVZ.shape
            #     logger.debug("{0:s}BV: {1:s} BVZ: {2:s} V: {3:s} fertig mit {4:d} Zeilen und {5:d} Spalten.".format(
            #         logStr, BV, BZ, VName, rows, cols))

            #     pairTables.add(BV)
            #     pairTables.add(BZ)

            #     pairViews.add(VName)
            #     pairViews_BZ.add(VName)

            # Nicht-Paare
            notInPairTables = sorted(allTables-pairTables)
            notInPairTablesW = [  # W: "Sollwert"; erwartete SIR 3S Tabellen, die nicht Paare sind
                # ,'DPKT' # ab 90-12 ein Paar
                'AB_DEF', 'AGSN', 'ARRW', 'ATMO', 'BENUTZER', 'BREF', 'CIRC', 'CONT', 'CRGL', 'DATENEBENE', 'DPGR_DPKT', 'DRNP', 'ELEMENTQUERY', 'FSTF', 'FWBZ', 'GEOMETRY_COLUMNS'  # 90-12
                # ,'MWKA' # nicht 90-12
                # ,'RMES_DPTS'#, 'RMES_DPTS_BZ'
                # , 'VARA_CSIT', 'VARA_WSIT'
                , 'GKMP', 'GMIX', 'GRAV', 'GTXT', 'HAUS', 'LAYR', 'LTGR', 'MODELL', 'NRCV', 'OVAL', 'PARV', 'PGPR', 'PLYG', 'POLY', 'PROZESSE', 'PZON', 'RCON', 'RECT', 'REGP', 'ROHR_VRTX', 'RPFL', 'RRCT', 'SIRGRAF', 'SOKO', 'SPLZ', 'STRASSE', 'SYSTEMKONFIG', 'TIMD', 'TRVA', 'UTMP', 'VARA', 'VERB', 'VKNO', 'VRCT', 'WBLZ']

            # erwartete SIR 3S Tabellen, die nicht Paare sind
            notPairTables = set()
            notPairViews = set()
            
            logger.debug(
            "{0:s}tables which are not pair-tables:".format(logStr))            
            
            for tableName in notInPairTablesW:

                if tableName not in tableNames:
                    logger.debug(
                        "{0:s}tableName: {1:s}: Tabelle gibt es nicht - falsche Annahme in diesem Modul bzgl. der existierenden SIR 3S Tabellen? Weiter. ".format(logStr, tableName))
                    continue

                sql = 'select * from '+tableName
                try:
                    df = pd.read_sql(fHelperSqlText(sql, ext), con)
                    self.dataFrames[tableName] = df
                    notPairTables.add(tableName)
                except:  # pd.io.sql.DatabaseError as e:
                    logger.info(
                        "{0:s}sql: {1:s}: Fehler?! Weiter. ".format(logStr, sql))
                    continue

                df = fHelperCONTetc(df, tableName, '', dfViewModelle, dfCONT,
                                    'erwartete SIR 3S Tabellen, die nicht Paare sind')

                VName = 'V_'+tableName
                
                rows, cols = df.shape
                logger.debug("{0:s}table: {1:16s} V: {2:20s} constructed with {3:8d} rows and {4:3d} cols.".format(
                    logStr, tableName, VName, rows, cols))                
                
                
                
                #logger.debug("{0:s}V: {1:s}".format(logStr, VName))
                self.dataFrames[VName] = df
                notPairViews.add(VName)

            # unerwartete Tabellen
            notPairViewsProbablyNotSir3sTables = set()
            notPairTablesProbablyNotSir3sTables = set()
            for tableName in set(notInPairTables)-set(notInPairTablesW):

                logger.debug("{0:s}tableName: {1:s}: Tabelle keine SIR 3S Tabelle aus Sicht dieses Moduls. Trotzdem lesen. ".format(
                    logStr, tableName))

                sql = 'select * from '+tableName
                try:
                    df = pd.read_sql(fHelperSqlText(sql, ext), con)
                    self.dataFrames[tableName] = df
                    notPairTablesProbablyNotSir3sTables.add(tableName)
                except pd.io.sql.DatabaseError:
                    logger.debug(
                        "{0:s}sql: {1:s}: Fehler?! Weiter. ".format(logStr, sql))
                    continue

                df = fHelperCONTetc(
                    df, tableName, '', dfViewModelle, dfCONT, 'unerwartete Tabellen')

                VName = 'V_'+tableName
                logger.debug("{0:s}V: {1:s}".format(logStr, VName))
                self.dataFrames[VName] = df
                notPairViewsProbablyNotSir3sTables.add(VName)

            self.viewSets = {}

            self.viewSets['allTables'] = sorted(allTables)
            self.viewSets['pairTables'] = sorted(pairTables)

            self.viewSets['pairViews'] = sorted(pairViews)
            self.viewSets['pairViews_BZ'] = sorted(pairViews_BZ)
            self.viewSets['pairViews_ROWS'] = sorted(pairViews_ROWS)
            self.viewSets['pairViews_ROWT'] = sorted(pairViews_ROWT)
            self.viewSets['pairViews_ROWD'] = sorted(pairViews_ROWD)

            self.viewSets['notPairTables'] = sorted(notPairTables)
            self.viewSets['notPairTablesProbablyNotSir3sTables'] = sorted(
                notPairTablesProbablyNotSir3sTables)
            self.viewSets['notPairViews'] = sorted(notPairViews)
            self.viewSets['notPairViewsProbablyNotSir3sTables'] = sorted(
                notPairViewsProbablyNotSir3sTables)

            con.close()
  
            # #############################################################
            # #############################################################
            self.dfLAYR=self._dfLAYR()    

            # #############################################################
            # #############################################################

            # V_BVZ_ROHR um u.a. DN erweitern
            # #############################################################
            logger.debug("{0:s}expanding {1:s} with NAME_DTRO, DN, DI, DA, S, KT, PN, Am2, Vm3 ...".format(
                logStr, 'V_BVZ_ROHR'))
            
            dfSrc=self.dataFrames['V_BVZ_ROHR']

            if 'pk_BZ' in self.dataFrames['V_BVZ_DTRO'].keys():
                df1 = pd.merge(dfSrc, self.dataFrames['V_BVZ_DTRO'],
                              left_on='fkDTRO_ROWD', right_on='pk_BZ', suffixes=('', '_DTRO'))                
                df2 = pd.merge(dfSrc, self.dataFrames['V_BVZ_DTRO'],
                              left_on='fkDTRO_ROWD', right_on='tk_BZ', suffixes=('', '_DTRO'))
                
                if df1.empty or df2.shape[0]>df1.shape[0]:
                    df=df2
                else:
                    df=df1
                    
            elif 'pk_BV' in self.dataFrames['V_BVZ_DTRO'].keys():
                df1 = pd.merge(dfSrc, self.dataFrames['V_BVZ_DTRO'],
                              left_on='fkDTRO_ROWD', right_on='pk_BV', suffixes=('', '_DTRO'))
                df2 = pd.merge(dfSrc, self.dataFrames['V_BVZ_DTRO'],
                              left_on='fkDTRO_ROWD', right_on='tk_BV', suffixes=('', '_DTRO'))
                
                if df1.empty or df2.shape[0]>df1.shape[0]:
                    df=df2
                else:
                    df=df1
                    
            df = df.filter(items=dfSrc.columns.to_list(
            )+['NAME', 'DN', 'DI', 'DA', 'S', 'KT', 'PN'])
            df.rename(columns={'NAME': 'NAME_DTRO'}, inplace=True)
            
            df['Am2']=df.apply(lambda row: math.pow(row['DI']/1000,2)*math.pi/4,axis=1)
            df['Vm3']=df.apply(lambda row: row['Am2']*row['L'] ,axis=1)
            
            logger.debug(f"{logStr}expanding V_BVZ_ROHR: rows before: {dfSrc.shape[0]} rows now: {df.shape[0]}")
                        
            self.dataFrames['V_BVZ_ROHR'] = df

            # weitere Erweiterungen zu V3_ROHR
            # #############################################################
            logger.debug("{0:s}V3_ROHR: expanding {1:s} with  NAME_LTGR, NAME_STRASSE, tk_i, NAME_i, tk_k, NAME_k ...".format(
                logStr, 'V_BVZ_ROHR'))            
                                
            extV = df

            for dfRefStr, fkRefStr, refName in zip(['LTGR', 'STRASSE'], ['fkLTGR', 'fkSTRASSE'], ['LTGR', 'STRASSE']):
                dfRef = self.dataFrames[dfRefStr]

                extV = extV.merge(dfRef.add_suffix('_'+refName), left_on=fkRefStr, right_on='pk' +
                                  '_'+refName, how='left').filter(items=extV.columns.to_list()+['NAME'+'_'+refName])
            
                
            # Knotennamen
            vKNOT=self.dataFrames['V_BVZ_KNOT']
            extV=pd.merge(extV,vKNOT.add_suffix('_i')[['tk_i','NAME_i']], left_on='fkKI', right_on='tk_i')
            extV=pd.merge(extV,vKNOT.add_suffix('_k')[['tk_k','NAME_k']], left_on='fkKK', right_on='tk_k')
            
            
            self.dataFrames['V3_ROHR'] = extV

            # V3_SWVT
            # #############################################################
            logger.debug("{0:s}{1:s}: expanding V_BVZ_SWVT ...".format(logStr, 'V3_SWVT'))

            # 1 Zeile pro RSLW der aktiv eine SWVT referenziert
            # NAME_SWVT_Nr gibt an, um die wie-vielte Referenz derselben SWVT es sich handelt
            # NAME_SWVT_NrMax gibt die max. Anzahl der Referenzierungen an; typischerwweise sollte NAME_SWVT_NrMax=1 sein für alle SWVT
            # (ZEIT, count)	... (W, max) sind Aggregate der referenzierten SWVT

            #vRSLW = self.dataFrames['V_BVZ_RSLW']

            # .sort_values(by=['pk','NAME','ZEIT'])
            vSWVT = self.dataFrames['V_BVZ_SWVT']

            for i, r in vSWVT[
                pd.isnull(vSWVT['ZEIT'])
                |
                pd.isnull(vSWVT['W'])
            ].iterrows():

                logger.debug("{:s}{:s} {:s}: ZEIT und/oder W sind Null?!: ZEIT: {!s:s} W: {!s:s}: Null-Wert(e) wird (werden) auf 0. gesetzt.".format(
                    logStr, 'vSWVT', r['NAME'], r['ZEIT'], r['W']))

            # die erste Zeit wird oft mit NaN gelesen obwohl sie mit 0. eingegeben ist
            vSWVT['ZEIT'] = vSWVT['ZEIT'].fillna(0.)
            # Werte mit NaN kann es iegentlich nicht geben ?! ...
            vSWVT['W'] = vSWVT['W'].fillna(0.)

            vSWVT = vSWVT.sort_values(by=['pk', 'NAME', 'ZEIT'])

            V3_SWVT = vSWVT.pivot_table(
                index='ZEIT', columns='NAME', values='W', aggfunc='last')
            self.dataFrames['V3_SWVT'] = V3_SWVT

            # V3_ROWT
            # #############################################################
            logger.debug("{0:s}{1:s}: combining ROWT_tables like V_BVZ_LFKT, V_BVZ_PVAR, ...".format(logStr, 'V3_ROWT'))
            valColName = {'V_BVZ_LFKT': 'LF', 'V_BVZ_PHI1': 'PHI', 'V_BVZ_PUMD': 'N', 'V_BVZ_PVAR': 'PH', 'V_BVZ_QVAR': 'QM', 'V_BVZ_TEVT': 'T'
                          }
            dfs = []
            for view in self.viewSets['pairViews_ROWT']:

                df = self.dataFrames[view]

                if df.empty:
                    continue

                if 'ZEIT' in df.columns.to_list():
                    # print(view)

                    if view in valColName.keys():
                        vCN = valColName[view]
                    else:
                        vCN = 'W'

                    df = df.rename(columns={vCN: 'value'})

                    df = df[['NAME', 'ZEIT', 'value']]

                    # die erste Zeit wird oft mit NaN gelesen obwohl sie mit 0. eingegeben ist
                    df['ZEIT'] = df['ZEIT'].fillna(0.)

                    # print(df[['NAME','ZEIT','value']].head())

                    dfs.append(df)

            dfAll = pd.concat(dfs)
            self.dataFrames['V3_ROWT'] = dfAll.pivot_table(
                index='ZEIT', columns='NAME', values='value', aggfunc='last')

            # V3_TFKT
            # #############################################################
            logger.debug("{0:s}{1:s}: ...".format(logStr, 'V3_TFKT'))
            self.dataFrames['V3_TFKT'] = self.dataFrames['V_BVZ_TFKT'][[
                'NAME', 'X', 'Y']].pivot_table(index='X', columns='NAME', values='Y', aggfunc='last')

            # V3_RSLW_SWVT
            # #############################################################
            logger.debug("{0:s}{1:s}: combining RSLW and SWVT ...".format(logStr, 'V3_RSLW_SWVT'))

            vRSLW = self.dataFrames['V_BVZ_RSLW']

            vRSLW_SWVTAll = pd.merge(vRSLW, vSWVT.add_suffix(
                '_SWVT'), left_on='fkSWVT', right_on='pk_SWVT')
            # die aktiv eine Sollwerttabelle referenzieren ...
            vRSLW_SWVTAll = vRSLW_SWVTAll[vRSLW_SWVTAll['INDSLW'].isin([1])]
            # .copy(deep=True) #  nur 1 Zeile pro Sollwerttabelle
            vRSLW_SWVT = vRSLW_SWVTAll[vRSLW_SWVTAll['lfdNrZEIT_SWVT'].isin([
                                                                            1])]

            vRSLW_SWVT = vRSLW_SWVT.copy(deep=True)

            vRSLW_SWVT['NAME_SWVT_Nr'] = vRSLW_SWVT.groupby(
                by=['NAME_SWVT'])['NAME_SWVT'].cumcount()+1
            vRSLW_SWVT['NAME_SWVT_NrMax'] = vRSLW_SWVT.groupby(
                by=['NAME_SWVT'])['NAME_SWVT_Nr'].transform(pd.Series.max)

            #  Aggregate einer SWVT
            df = vSWVT.groupby(by=['NAME']).agg(
                {'ZEIT': ['count', 'first', 'min', 'last', 'max'], 'W': ['count', 'first', 'min', 'last', 'max']
                 }
            )
            df.columns = df.columns.to_flat_index()

            # diese Aggregate verfuegbar machen
            self.dataFrames['V3_RSLW_SWVT'] = pd.merge(
                vRSLW_SWVT, df, left_on='NAME_SWVT', right_on='NAME')

            # V3_KNOT
            # #############################################################
            logger.debug("{0:s}{1:s}: expanding V_BVZ_KNOT with NAME_LFKT, NAME_PVAR, NAME_PZON,NAME_QVAR,NAME_UTMP,NAME_FSTF,NAME_FQPS ...".format(logStr, 'V3_KNOT'))

            vKNOT = pd.merge(self.dataFrames['V_BVZ_KNOT'], self.dataFrames['V_VKNO'].add_suffix(
                '_VKNO'), left_on='tk', right_on='fkKNOT_VKNO', how='left')

            extV = vKNOT
            for dfRefStr, fkRefStr, refName in zip(['LFKT', 'PVAR', 'PZON', 'QVAR', 'UTMP', 'FSTF', 'FQPS'], ['fkLFKT', 'fkPVAR', 'fkPZON', 'fkQVAR', 'fkUTMP', 'fkFSTF', 'fkFQPS'], ['LFKT', 'PVAR', 'PZON', 'QVAR', 'UTMP', 'FSTF', 'FQPS']):
                dfRef = self.dataFrames[dfRefStr]

                extV = extV.merge(dfRef.add_suffix('_'+refName), left_on=fkRefStr, right_on='pk' +
                                  '_'+refName, how='left').filter(items=extV.columns.to_list()+['NAME'+'_'+refName])
            self.dataFrames['V3_KNOT'] = extV

            # V3_FWVB
            # #############################################################
            logger.debug("{0:s}{1:s}: expanding V_BVZ_FWVB with NAME_LFKT, NAME_ZEP1VL, NAME_ZEP1RL, NAME_TEVT, NAME_TRFT, tk_i, NAME_i, tk_k, NAME_k, ...".format(logStr, 'V3_FWVB'))
            extV_BVZ_FWVB = self.dataFrames['V_BVZ_FWVB']
            for dfRefStr, fkRefStr, refName in zip(['LFKT', 'ZEP1', 'ZEP1', 'TEVT', 'TRFT'], ['fkLFKT', 'fkZEP1VL', 'fkZEP1RL', 'fkTEVT', 'fkTRFT'], ['LFKT', 'ZEP1VL', 'ZEP1RL', 'TEVT', 'TRFT']):
                dfRef = self.dataFrames[dfRefStr]
                extV_BVZ_FWVB = extV_BVZ_FWVB.merge(dfRef.add_suffix(
                    '_'+refName), left_on=fkRefStr, right_on='pk'+'_'+refName, how='left').filter(items=extV_BVZ_FWVB.columns.to_list()+['NAME'+'_'+refName])
                
            # Knotennamen
            extV_BVZ_FWVB=pd.merge(extV_BVZ_FWVB,vKNOT.add_suffix('_i')[['tk_i','NAME_i']], left_on='fkKI', right_on='tk_i')
            extV_BVZ_FWVB=pd.merge(extV_BVZ_FWVB,vKNOT.add_suffix('_k')[['tk_k','NAME_k']], left_on='fkKK', right_on='tk_k')
                          
                
            self.dataFrames['V3_FWVB'] = extV_BVZ_FWVB

            # V3_:ROHR,KNOT,FWVB: filterTemplateObjects
            # #############################################################
            logger.debug("{0:s}{1:s} filterTemplateObjects ...".format(logStr, 'V3_:ROHR,KNOT,FWVB:'))
            self._filterTemplateObjects()

            # #############################################################
            # VBEL (V3_VBEL) - "alle" Verbindungselementdaten des hydr. Prozessmodells; Knotendaten mit _i und _k
            logger.debug("{0:s}{1:s}: ...".format(logStr, 'V3_VBEL'))

            vVBEL_UnionList = []
            for vName in self.viewSets['pairViews_BZ']:

                m = re.search('^(V_BVZ_)(\w+)', vName)
                OBJTYPE = m.group(2)

                dfVBEL = self.dataFrames[vName]
                if 'fkKI' in dfVBEL.columns.to_list():
                    
                    df = pd.merge(dfVBEL, vKNOT.add_suffix('_i'), left_on='fkKI', right_on='tk_i'
                                  )

                    #logger.debug("{0:s}{1:s} in VBEL-View mit fkKI ({2:d},{3:d}) ...".format(
                    #    logStr, OBJTYPE, df.shape[0], df.shape[1]))

                    if df.empty:
                        df = pd.merge(dfVBEL, vKNOT.add_suffix('_i'), left_on='fkKI', right_on='pk_i'
                                      )
                        #if not df.empty:
                        #    logger.debug("{0:s}{1:s} in VBEL-View mit fkKI per pk! ({2:d},{3:d}) ...".format(
                        #        logStr, OBJTYPE, df.shape[0], df.shape[1]))
                        #else:
                        #    logger.debug("{0:s}{1:s} in VBEL-View mit fkKI LEER! ({2:d},{3:d}) ...".format(
                        #        logStr, OBJTYPE, df.shape[0], df.shape[1]))

                    if 'fkKK' in df.columns.to_list():
                        df = pd.merge(df, vKNOT.add_suffix('_k'), left_on='fkKK', right_on='tk_k'
                                      )

                        if df.empty:
                            df = pd.merge(dfVBEL, vKNOT.add_suffix('_k'), left_on='fkKK', right_on='pk_k'
                                          )
                            #if not df.empty:
                            #    logger.debug("{0:s}{1:s} in VBEL-View mit fkKI und fkKK per pk! ({2:d},{3:d}) ...".format(
                            #        logStr, OBJTYPE, df.shape[0], df.shape[1]))
                            #else:
                            #    logger.debug("{0:s}{1:s} in VBEL-View mit fkKI und fkKK LEER! ({2:d},{3:d}) ...".format(
                            #        logStr, OBJTYPE, df.shape[0], df.shape[1]))

                        # m=re.search('^(V_BVZ_)(\w+)',vName)
                        # OBJTYPE=m.group(2)
                        df = df.assign(OBJTYPE=lambda x: OBJTYPE)

                        if df.shape[0] > 0:
                            logger.debug("{0:s}{1:s} final in V3_VBEL-View ({2:d},{3:d}) ...".format(
                                logStr, OBJTYPE, df.shape[0], df.shape[1]))
                            
                        vVBEL_UnionList.append(df)
                        
                    elif 'KNOTK' in df.columns.to_list():
                        # Nebenschlusselement
                        pass
                        df = pd.merge(df, vKNOT.add_suffix('_k'), left_on='fkKI', right_on='tk_k'
                                      )
                        # m=re.search('^(V_BVZ_)(\w+)',vName)
                        # OBJTYPE=m.group(2)
                        df = df.assign(OBJTYPE=lambda x: OBJTYPE)

                        #logger.debug(
                        #    "{0:s}{1:s} (Nebenschluss) in VBEL-View ...".format(logStr, OBJTYPE))
                        vVBEL_UnionList.append(df)

            vVBEL = pd.concat(vVBEL_UnionList)
            vVBEL = Xm.Xm.constructNewMultiindexFromCols(
                df=vVBEL, mColNames=['OBJTYPE', 'tk'], mIdxNames=['OBJTYPE', 'OBJID'])
            vVBEL.sort_index(level=0, inplace=True)
            self.dataFrames['V3_VBEL'] = vVBEL

            # #############################################################
            # V3_DPKT
            logger.debug("{0:s}{1:s} ...".format(logStr, 'V3_DPKT'))
            # DPKT (V3_DPKT) - relevante Datenpunktdaten
            if 'V_BVZ_DPKT' in self.dataFrames.keys():
                vDPKT = self.dataFrames['V_BVZ_DPKT']
            elif 'V_DPKT' in self.dataFrames.keys():
                vDPKT = self.dataFrames['V_DPKT']


            vDPKT_DPGR1 = pd.merge(
                vDPKT, self.dataFrames['V_DPGR_DPKT'], left_on='tk', right_on='fkDPKT', suffixes=('', '_DPGR1'))

            vDPKT_DPGR = pd.merge(
                vDPKT_DPGR1, self.dataFrames['V_BVZ_DPGR'], left_on='fkDPGR', right_on='tk', suffixes=('', '_DPGR'))

            try:
                self.dataFrames['V3_DPKT'] = vDPKT_DPGR[[
                    'pk', 'tk', 'OBJTYPE', 'fkOBJTYPE', 'ATTRTYPE', 'EPKZ', 'TITLE', 'UNIT', 'FLAGS', 'CLIENT_ID',
                    'CLIENT_FLAGS', 'OPCITEM_ID', 'DESCRIPTION',

                    'NAME1',
                    'NAME2',
                    'NAME3',

                    'FACTOR',
                    'ADDEND',
                    'DEVIATION',
                    'CHECK_ALL',
                    'CHECK_MSG',
                    'CHECK_ABS',
                    'LOWER_LIMIT',
                    'UPPER_LIMIT',
                    'LIMIT_TOLER'                 # ---
                    , 'tk_DPGR', 'NAME'
                ]].drop_duplicates().reset_index(drop=True)

                v3_dpkt = self.dataFrames['V3_DPKT']
                v3_dpkt = v3_dpkt.sort_values(
                    by=['tk', 'NAME']).groupby(by='tk').first()
                v3_dpkt = v3_dpkt[
                    ~v3_dpkt['fkOBJTYPE'].isin(['-1', -1])
                ]
                self.dataFrames['V3_DPKT'] = v3_dpkt.reset_index()

            except Exception as e:
                logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                    logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
                logger.debug(logStrFinal)

                self.dataFrames['V3_DPKT'] = vDPKT_DPGR[[
                    'pk', 'OBJTYPE'                    # ,'fkOBJTYPE'
                    , 'ATTRTYPE', 'EPKZ', 'TITLE', 'UNIT', 'FLAGS'                    # ,'CLIENT_ID'
                    # ,'OPCITEM_ID'
                    , 'DESCRIPTION'                 # ---
                    , 'pk_DPGR', 'NAME'
                ]].drop_duplicates().reset_index(drop=True)

            # #############################################################
            # RXXX (RKNOT,RRUES,RVBEL)
            try:

                logger.debug("{0:s}{1:s} ...".format(logStr, 'V3_RKNOT'))

                # RXXX-Nodes but RUES-Nodes
                vRXXX_nodes = ['RSLW', 'RMES', 'RHYS', 'RLVG', 'RLSR', 'RMMA', 'RADD',
                               'RMUL', 'RDIV', 'RTOT', 'RPT1', 'RINT', 'RPID', 'RFKT', 'RSTN']
                vRXXX_UnionList = []
                for NODE in vRXXX_nodes:
                    vName = 'V_BVZ_'+NODE
                    if vName in self.dataFrames:
                        vRXXX = self.dataFrames[vName]
                        if vRXXX is None:
                            pass
                        else:
                            vRXXX['OBJTYPE'] = NODE
                            vRXXX_UnionList.append(vRXXX)
                vRXXX = pd.concat(vRXXX_UnionList)
                vRXXX = vRXXX.rename(columns={'KA': 'Kn'})

                # all RXXX-Nodes
                V3_RKNOT_UnionList = []
                # [['OBJTYPE','BESCHREIBUNG','Kn','NAME','pk']])
                V3_RKNOT_UnionList.append(vRXXX)
                V3_RKNOT = pd.concat(V3_RKNOT_UnionList).reset_index(drop=True)
                self.dataFrames['V3_RKNOT'] = V3_RKNOT

                # RUES
                logger.debug("{0:s}{1:s} ...".format(logStr, 'V3_RRUES'))
                # wahre Quelle (wahre SRC) ermitteln
                #  Ues sind nur Aliase fuer Signale (fuer Knoten)
                #  fuer jede Alias-Definition den wahren Signalnamen (Knotennamen) ermitteln

                # alle Ues
                vRUES = self.dataFrames['V_BVZ_RUES']
                
                if not vRUES[~vRUES['pk'].isin([-1,'-1'])].empty:
                                
                    # alle Kanten (alle Signalverbindungen)
                    vCRGL = self.dataFrames['V_CRGL']
                    # Ue-Definitionen per Kante (per Signal):
                    vRUESDefs = pd.merge(
                        vRUES, vCRGL, left_on='pk', right_on='fkKk', suffixes=('', '_Edge'))
                    if vRUESDefs.empty:
                        logger.debug(
                            "{0:s}vRUES: Referenz zu pk leer?! ...".format(logStr))
                        vRUESDefs = pd.merge(
                            vRUES, vCRGL, left_on='tk', right_on='fkKk', suffixes=('', '_Edge'))
                    else:
                        rows, dummy = vRUESDefs.shape
                        df2 = pd.merge(vRUES, vCRGL, left_on='tk',
                                       right_on='fkKk', suffixes=('', '_Edge'))
                        rows2, dummy = df2.shape
                        if rows2 >= rows:
                            #logger.debug(
                            #    "{0:s}vRUES:: Referenz zu pk nicht leer aber tk findet mindestens genausoviel Treffer ...".format(logStr))
                            vRUESDefs = df2
                            
                            
                    # Kontrollausgaben
                    #logger.debug("{logStr:s}vRUESDefs: {vRUESDefs:s}".format(logStr=logStr,vRUESDefs=vRUESDefs.to_string()))      
                    
                    #logger.debug("{logStr:s}V3_RKNOT: {V3_RKNOT:s}".format(logStr=logStr,V3_RKNOT=V3_RKNOT.to_string()))      
                       
                    def get_UE_SRC(UeName  # Name der Ue deren SRC gesucht wird
                                   , dfUes  # alle Ues (Defs und Refs)
                                   , dfUesDefs  # alle Signalverbindungen die Ues definieren
                                   ):
                        """
                        gibt per df diejenige Zeile von dfUesDefs zurueck die schlussendlich UeName definiert
                        fkKi ist dann die wahre Quelle von UeName
                        fkKi verweist dabei _nicht auf eine andere Ue, d.h. verkettete Referenzen werden bis zur wahren Quelle aufgeloest
                        """
    
                        df = dfUesDefs[dfUesDefs['IDUE'] == UeName]
    
                        if df['fkKi'].iloc[0] in dfUes['tk'].to_list():
                            
                            # die SRC der Ue ist eine Ue
                            #logger.debug("Die SRC der Ue {:s} ist eine Ue - die Ue-Def:\n{:s}".format(
                            #    UeName, str(df[['IDUE', 'pk', 'rkRUES', 'fkKi', 'fkKk']].iloc[0])))
    
                            # die Referenz
                            df = dfUes[dfUes['pk'] == df['fkKi'].iloc[0]]
                            df = dfUes[dfUes['pk'] ==
                                       df['rkRUES'].iloc[0]]  # die SRC
    
                            # print("{:s}".format((str(df[['IDUE','pk'
                            #                                                                      ,'rkRUES'
                            #                            #                                          ,'fkKi','fkKk'
                            #                            ]].iloc[0]))))
    
                            # Rekursion bis zur wahren Quelle
                            df = get_UE_SRC(df['IDUE'].iloc[0], dfUes, dfUesDefs
                                            )
                        else:
                            pass
                            # Log wieder AUS
                            #logger.debug("Die SRC der Ue {:s} gefunden -die Ue-Def:\n{:s}".format(
                            #    UeName, str(df[['IDUE', 'pk', 'rkRUES', 'fkKi', 'fkKk']].iloc[0])))
    
                        return df
    
                    # fuer jede Ue-Definition die SRC bestimmen
    
                    dcts = []
                    for index, row in vRUESDefs.iterrows():
    
                        dfX = get_UE_SRC(row['IDUE']  # Name der Ue deren SRC gesucht wird
                                         , vRUES  # Ues
                                         , vRUESDefs  # Ue-Definitionen per Kante
                                         )
                        
                        #logger.debug("{logStr:s}dfX: {dfX:s}".format(logStr=logStr,dfX=dfX.to_string()))      
                                            
                        # df['fkKi'] ist die SRC
                        df=pd.DataFrame()                                        
                        
                        df = V3_RKNOT[V3_RKNOT['pk'] == dfX['fkKi'].iloc[0]]
                        if df.empty:
                            
                            #logger.debug(
                            #    "{0:s}V3_RKNOT: Referenz zu pk leer?! ...".format(logStr))
    
                            df = V3_RKNOT[V3_RKNOT['tk'] == dfX['fkKi'].iloc[0]]
                        else:
                            df2 = V3_RKNOT[V3_RKNOT['tk'] == dfX['fkKi'].iloc[0]]
    
                            rows, dummy = df.shape
                            rows2, dummy = df2.shape
    
                            if rows2 >= rows:
                                #logger.debug(
                                #    "{0:s}V3_RKNOT: Referenz zu pk nicht leer aber tk findet mindestens genausoviel Treffer ...".format(logStr))
                                df = df2
                        
                        if df.empty:                        
                             logger.info("{:s}{:12s} {:s}: UE-Symbol ohne Referenz?!".format(logStr,row['IDUE'],row['NAME_CONT']))        
    
                             dct = {'pk_DEF': row['pk'], 'tk_DEF': row['tk'], 'IDUE_DEF': row['IDUE']                           #
                                    , 'OBJTYPE_SRC': None, 'OBJID_SRC': None, 'Kn_SRC': None, 'NAME_CONT_SRC': None
                                    }
                             ### dcts.append(dct) #?!
                                                         
                        else:
    
                             dct = {'pk_DEF': row['pk'], 'tk_DEF': row['tk'], 'IDUE_DEF': row['IDUE']                           #
                                   , 'OBJTYPE_SRC': df['OBJTYPE'].iloc[0], 'OBJID_SRC': df['pk'].iloc[0], 'Kn_SRC': df['Kn'].iloc[0], 'NAME_CONT_SRC': df['NAME_CONT'].iloc[0]
                                   }
                             dcts.append(dct)
    
                        # break
                    vRUESDefsSRCs = pd.DataFrame.from_dict(dcts)
                    
                    # UE-Symbole ohne Referenzen sind hier nicht enthalten
                    #logger.debug("{logStr:s}vRUESDefsSRCs: {vRUESDefsSRCs:s}".format(logStr=logStr,vRUESDefsSRCs=vRUESDefsSRCs.sort_values(by=['IDUE_DEF']).to_string())) 
                    
                    # Ausgabe, wo das Ue nicht so heisst wie die Quelle ...
                    for index, row in vRUESDefsSRCs.sort_values(by=['IDUE_DEF']).iterrows():
                        
                        if row['IDUE_DEF'] != row['Kn_SRC']:
                            pass
                            #logger.debug("{logStr:s}IDUE_DEF: {IDUE_DEF!s:s} != Kn_SRC: {Kn_SRC!s:s} - ggf. ungewollt? ...".format(logStr=logStr
                            #        ,IDUE_DEF=row['IDUE_DEF']
                            #        ,Kn_SRC=row['Kn_SRC']
                            #            )) 
                        
                    # fuer alle Defs die wahre Quelle angeben
                    #vRUES: self.dataFrames['V_BVZ_RUES']
                    V3_RUES = pd.merge(vRUES.copy(deep=True), vRUESDefsSRCs, left_on='IDUE', right_on='IDUE_DEF', how='left')
                    
                    #logger.debug("{logStr:s}V3_RUES Schritt 1: {V3_RUES:s}".format(logStr=logStr,V3_RUES=V3_RUES[['NAME_CONT','IDUE','IDUE_DEF','Kn_SRC','rkRUES']].sort_values(by=['IDUE_DEF']).to_string())) 
    
                    # fuer alle Refs ebenfalls die wahre Quelle angeben
                    for index, row in V3_RUES.iterrows():
                        #logger.debug("{logStr:s}{IDUE_DEF!s:s}".format(logStr=logStr,IDUE_DEF=row['IDUE_DEF'])) 
                        
                        
                        #logger.debug("{logStr:s}IDUE_DEF: {IDUE_DEF!s:s}, Kn_SRC: {Kn_SRC!s:s}".format(logStr=logStr
                        #        ,IDUE_DEF=row['IDUE_DEF']
                        #        ,Kn_SRC=row['Kn_SRC']
                        #            ))                     
                                            
                        if pd.isnull(row['IDUE_DEF']):
                                                                                             
                            rkRUES = row['rkRUES']
                            
                            dfx=vRUESDefsSRCs[vRUESDefsSRCs['tk_DEF']== rkRUES]
                            
                            (Treffer,dummy)=dfx.shape
    
                            #logger.debug("{logStr:s}IDUE_DEF ist NULL, rkRUES: {rkRUES:s}, Treffer: {Treffer:d}".format(logStr=logStr                                
                            #        ,rkRUES=row['rkRUES']
                            #        ,Treffer=Treffer
                            #            ))  
                                                    
                            if Treffer == 0:
    
                                #logger.debug("{logStr:s}IDUE_DEF ist NULL, rkRUES: {rkRUES:s}, KEIN Treffer?!".format(logStr=logStr                                
                                #        ,rkRUES=row['rkRUES']                                    
                                #            ))   
                                continue
                                                                        
                            if Treffer > 1:
                                pass
                                #logger.debug("{logStr:s}IDUE_DEF ist NULL, rkRUES: {rkRUES:s}, MEHR als 1 Treffer: {Treffer:d}?!".format(logStr=logStr                                
                                #        ,rkRUES=row['rkRUES']
                                #        ,Treffer=Treffer
                                #            ))                              
                                                    
                            s = dfx.iloc[0]                            
        
                            V3_RUES.loc[index, 'pk_DEF'] = s['pk_DEF']
                            V3_RUES.loc[index, 'IDUE_DEF'] = s['IDUE_DEF']
                            V3_RUES.loc[index, 'OBJTYPE_SRC'] = s['OBJTYPE_SRC']
                            V3_RUES.loc[index, 'Kn_SRC'] = s['Kn_SRC']
                            V3_RUES.loc[index,'NAME_CONT_SRC'] = s['NAME_CONT_SRC']
    
                            
                    self.dataFrames['V3_RRUES'] = V3_RUES
                    #logger.debug("{logStr:s}V3_RRUES final: {V3_RUES:s}".format(logStr=logStr
                    #                                                            ,V3_RUES=V3_RUES[['NAME_CONT','NAME_CONT_SRC','OBJTYPE_SRC','IDUE','IDUE_DEF','Kn_SRC','rkRUES','pk_DEF']].sort_values(by=['IDUE_DEF']).to_string()))                 
    
                    # RKNOT voruebergehend erweitern um RUES um nachfolgend alle Kanten ausreferenzieren zu koennen
                    #logger.debug("{0:s}expanding V3_KNOT with V3_RRUES temporarily to construct V3_RVBEL ...".format(logStr))
    
                    V3_RKNOT = self.dataFrames['V3_RKNOT']
                    vRUES = self.dataFrames['V_BVZ_RUES']
                    vRUES = pd.merge(vRUES, vRUES, how='left', left_on='rkRUES',
                                     right_on='tk', suffixes=('', '_rkRUES'))
                    vRUES['Kn'] = vRUES.apply(
                        lambda row: row.IDUE if row.IOTYP == '1' else row.IDUE_rkRUES, axis=1)
                    vRUES['OBJTYPE'] = 'RUES'
                    vRUES['BESCHREIBUNG'] = None
                    V3_RKNOT = pd.concat([V3_RKNOT, vRUES[[
                                         'OBJTYPE', 'Kn', 'BESCHREIBUNG', 'pk', 'tk', 'NAME_CONT', 'IDUE', 'IOTYP']]]).reset_index(drop=True)
                
                # alle RXXX-Kanten
                logger.debug("{0:s}{1:s} ...".format(logStr, 'V3_RVBEL'))
                
                howMode = 'left'
                V_CRGL = self.dataFrames['V_CRGL']
                
                V3_RVBEL = pd.merge(V_CRGL, V3_RKNOT.add_suffix(
                    '_i'), left_on='fkKi', right_on='tk_i', how=howMode).filter(items=V_CRGL.columns.to_list()+['OBJTYPE_i','pk_i','tk_i','Kn_i','NAME_CONT_i'])
                V3_RVBEL['KnExt_i'] = V3_RVBEL['Kn_i'] + \
                    '_'+V3_RVBEL['OBJTYPE_i']
                    
                V3_RVBEL = pd.merge(V3_RVBEL, V3_RKNOT.add_suffix(
                    '_k'), left_on='fkKk', right_on='tk_k', how=howMode).filter(items=V3_RVBEL.columns.to_list()+['OBJTYPE_k','pk_k','tk_k','Kn_k','NAME_CONT_k'])
                V3_RVBEL['KnExt_k'] = V3_RVBEL['Kn_k'] + \
                    '_'+V3_RVBEL['OBJTYPE_k']

                V3_RVBEL = Xm.Xm.constructNewMultiindexFromCols(df=V3_RVBEL, mColNames=[
                                                                'OBJTYPE_i', 'OBJTYPE_k', 'pk'], mIdxNames=['OBJTYPE_i', 'OBJTYPE_k', 'OBJID'])

                V3_RVBEL = V3_RVBEL[~V3_RVBEL.index.get_level_values(
                    'OBJTYPE_k').isin(['RUES'])]

                V3_RVBEL = V3_RVBEL[~
                                    (
                                        (V3_RVBEL.index.get_level_values(
                                            'OBJTYPE_i').isin(['RUES']))
                                        &
                                        (V3_RVBEL.index.get_level_values(
                                            'OBJTYPE_k').isin(['RUES']))
                                    )
                                    ]


                if not vRUES[vRUES['pk'].isin([-1])].empty:
                
                    # RUES-Verbindungen zur Quelle hin aufloesen ...                
                    #logger.debug("{0:s}{1:s} RUES-Verbindungen zur Quelle hin aufloesen ...".format(logStr, 'V3_RVBEL'))
    
                    V3_RVBEL = V3_RVBEL.reset_index()
                    V3_RRUES = self.dataFrames['V3_RRUES']
                    for index, row in V3_RVBEL[V3_RVBEL['OBJTYPE_i'].isin(['RUES'])].iterrows():
                        
                        dfx=V3_RRUES[V3_RRUES['tk'] == row['fkKi']]
                        (Treffer,dummy)=dfx.shape
                        
                        if Treffer == 0:                   
                            logger.debug("{logStr:s}OBJTYPE_i: {OBJTYPE_i:s} Kn_i: {Kn_i:s}  KEIN Treffer?!".format(logStr=logStr                                
                                    ,OBJTYPE_i=row['OBJTYPE_i']      
                                    ,Kn_i=row['Kn_i']      
                                        ))   
                            continue
                                                                    
                        if Treffer > 1:
                            logger.debug("{logStr:s}OBJTYPE_i: {OBJTYPE_i:s} Kn_i: {Kn_i:s}  MEHR als 1 Treffer: {Treffer:d}?!".format(logStr=logStr                                
                                    ,OBJTYPE_i=row['OBJTYPE_i']      
                                    ,Kn_i=row['Kn_i']      
                                    ,Treffer=Treffer
                                        ))                           
                                                                                          
                        s = dfx.iloc[0]
                        
                        #logger.debug("{logStr:s}OBJTYPE_i: {OBJTYPE_i:s} Kn_i: {Kn_i:s} Treffer: {Treffer!s:s}?!".format(logStr=logStr                                
                        #        ,OBJTYPE_i=row['OBJTYPE_i']      
                        #        ,Kn_i=row['Kn_i']      
                        #        ,Treffer=s
                        #            ))         
    
                        V3_RVBEL.loc[index, 'OBJTYPE_i'] = s['OBJTYPE_SRC']
                        # V3_RVBEL.loc[index,'OBJID_i']=s['OBJID_SRC']
                        V3_RVBEL.loc[index, 'Kn_i'] = s['Kn_SRC']
                        V3_RVBEL.loc[index, 'KnExt_i'] = str(s['Kn_SRC']) + \
                            '_'+str(s['OBJTYPE_SRC'])
                        V3_RVBEL.loc[index, 'NAME_CONT_i'] = s['NAME_CONT_SRC']

                
                    V3_RVBEL=V3_RVBEL[~pd.isnull(V3_RVBEL['tk'])]
                    V3_RVBEL = Xm.Xm.constructNewMultiindexFromCols(df=V3_RVBEL, mColNames=[
                                                                    'OBJTYPE_i', 'OBJTYPE_k', 'OBJID'], mIdxNames=['OBJTYPE_i', 'OBJTYPE_k', 'OBJID'])
                
                
                V3_RVBEL=V3_RVBEL[~V3_RVBEL.index.get_level_values(2).isin([-1,'-1'])]
                
                self.dataFrames['V3_RVBEL'] = V3_RVBEL
                                
                # Modell-Pk des in QGIS anzuzeigenden Modells    
                # ============================================
                sk=self.dataFrames['SYSTEMKONFIG']  
                try:
                    self.QGISmodelXk=sk[sk['ID'].isin([3,3.])]['WERT'].iloc[0]
                except:
                    logger.info("{logStr:s} SYSTEMKONFIG ID 3 not defined. Value(ID=3) is supposed to define the Model which is used in QGIS. Now QGISmodelXk is undefined ...".format(logStr=logStr))
                    self.QGISmodelXk=None
                
            except Exception as e:
                logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                    logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
                logger.debug(logStrFinal)

        except Exception as e:
            logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
            logger.error(logStrFinal)
            raise DxError(logStrFinal)
        finally:
            logger.debug("{0:s}{1:s}".format(logStr, '_Done.#########'))


    def _dfLAYR(self):
        """
        dfLAYR is a dx object Attribute.
                
        .. note::             
            Groups (also called Layers) are used in SIR 3S as a feature for data access, data filtering and grouping. 
            
            The returned dfLAYR (one row per LAYR and OBJ) has the following columns:
                
                 LAYR:
                     - pk
                     - tk
                     - LFDNR (numeric)
                     - NAME
                
                 LAYR-Info:
                     - AnzDerObjekteInGruppe
                     - AnzDerObjekteDesTypsInGruppe
                
                 OBJ:
                     - TYPE
                     - ID
                
                 OBJ-Info:
                     - NrDesObjektesDesTypsInGruppe
                     - NrDesObjektesInGruppe
                     - GruppenDesObjektsAnz
                     - GruppenDesObjektsNamen       
                      
        """   
                
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug(f"{logStr}Start.") 
        
        try: 
            dfLAYR=pd.DataFrame()
            dfLAYR=dxDecodeObjsData.Layr(self)                                   
            return dfLAYR     
        except DxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.debug(logStrFinal) 
            raise DxError(logStrFinal)                       
        finally:
            logger.debug(f"{logStr}_Done.") 

    def MxSync(self, mx):
        """
        adds mx2Idx to V3_KNOT, V3_ROHR, V3_FWVB, V3_VBEL, etc.
        adds mx2NofPts, dL to V3_ROHR          
        """

        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:

            for dfName, resType in zip(['V3_KNOT', 'V3_ROHR', 'V3_FWVB'], ['KNOT', 'ROHR', 'FWVB']):

                if mx.mx2Df[mx.mx2Df['ObjType'].str.match(resType)].empty:
                    logger.debug(
                        "{:s}resType: {:s} hat keine mx2-Eintraege.".format(logStr, resType))
                    continue
                else:
                    pass
                    #logger.debug(
                    #    "{:s}resType: {:s} ...".format(logStr, resType))

                # mx2Idx ergaenzen

                # Liste der IDs in Mx2
                xksMx = mx.mx2Df[
                    (mx.mx2Df['ObjType'].str.match(resType))
                    &  # nur wg. ROHRe erf.
                    ~(mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
                ]['Data'].iloc[0]

                # xk: pk oder tk
                xkTypeMx = mx.mx2Df[
                    (mx.mx2Df['ObjType'].str.match(resType))
                    &  # nur wg. ROHRe erf.
                    ~(mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
                ]['AttrType'].iloc[0].strip()

                # lesen
                df = self.dataFrames[dfName]

                # Liste der xks
                xksXm = df[xkTypeMx]

                # zugeh. Liste der mx2Idx in df
                mxXkIdx = [xksMx.index(xk) for xk in xksXm]

                if resType == 'ROHR':

                    # Liste der N_OF_POINTS in Mx2
                    nopMx = mx.mx2Df[
                        (mx.mx2Df['ObjType'].str.match(resType))
                        &
                        (mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
                    ]['Data'].iloc[0]

                    # zugeh. Liste der NOfPts in df
                    nopXk = [nopMx[mx2Idx] for mx2Idx in mxXkIdx]

                    # Spalte mx2NofPts anlegen 
                    df['mx2NofPts'] = pd.Series(nopXk)
                    # Spalte dL anlegen 
                    df['dL'] = df['L'].astype(float)/(df['mx2NofPts']-1)
                    
                    
                # Spalte mx2Idx als letzte Spalte anlegen
                df['mx2Idx'] = pd.Series(mxXkIdx)
        
            # V3_VBEL
            # ####################
    
            try: 
    
                # new col mx2Idx in dfVBEL
                dfVBEL=self.dataFrames['V3_VBEL']
                dfVBEL=dfVBEL.assign(mx2Idx=lambda x: -1)
                dfVBEL['mx2Idx'].astype('int64',copy=False)
    
                # all edges
                for edge in [edge for edge in 
                             #['ROHR','VENT','FWVB','FWES','PUMP','KLAP','REGV','PREG','MREG','DPRG','PGRP']
                             dfVBEL.index.unique(level=0).to_list()
                             ]:
                     try:    
                         
                         
                         if mx.mx2Df[mx.mx2Df['ObjType'].str.match(edge)].empty:
                             logger.debug(
                                 "{:s}resType: {:s} hat keine mx2-Eintraege.".format(logStr, edge))
                             continue
                         else:
                             pass
                             #logger.debug(
                             #    "{:s}resType: {:s} ...".format(logStr, resType))
                         
                         
                         
                         
                         
                         # die Schluessel
                         xksEDGEMx=mx.mx2Df[
                                    (mx.mx2Df['ObjType'].str.match(edge))
                             ]['Data'].iloc[0]
    
                         # der Schluesselbezug 'tk' oder 'xk'
                         xkTypeMx=mx.mx2Df[
                                    (mx.mx2Df['ObjType'].str.match(edge))
                             ]['AttrType'].iloc[0].strip()
    
                         # Sequenz der Schluessel in V3_VBEL   
                         if xkTypeMx == 'tk':
                            xksEDGEXm=dfVBEL.loc[(edge,),:].index.get_level_values(0).values #dfVBEL.loc[(edge,),xkTypeMx]
                         else:
                            # pk
                            xksEDGEXm=dfVBEL.loc[(edge,),'pk'].values#dfVBEL.loc[(edge,),:].index
    
                         #logger.debug("{0:s}{1:s}: xkTypeMx: {2:s}".format(logStr,edge,xkTypeMx))   
                         #logger.debug("{0:s}{1:s}: xksEDGEXm: {2:s}".format(logStr,edge,str(xksEDGEXm.tolist())))   
                         #logger.debug("{0:s}{1:s}: xksEDGEMx: {2:s}".format(logStr,edge,str(xksEDGEMx)))      
                                          
                         mxXkEDGEIdx=[xksEDGEMx.index(xk) for xk in xksEDGEXm]
                         
                         dfVBEL.loc[(edge,),'mx2Idx']=mxXkEDGEIdx
    
                     except Exception as e:
                        logStrEdge="{:s}Exception: Line: {:d}: {!s:s}: {:s}: mx2Idx for {:s} failed. mx2Idx = -1.".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e),edge)            
                        logger.debug(logStrEdge) 
                                                                                                                   
            except Exception as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))            
                logger.error(logStrFinal) 
                              
            finally:
                #logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
                self.dataFrames['V3_VBEL']=dfVBEL

        except Exception as e:
            logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
            logger.error(logStrFinal)
            raise DxError(logStrFinal)
        finally:
            logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))


    def MxAdd(self, mx, addNodeData=True, addNodeDataSir3sVecIDReExps=['^KNOT~\*~\*~\*~PH$','^KNOT~\*~\*~\*~H$','^KNOT~\*~\*~\*~T$','^KNOT~\*~\*~\*~RHO$']):
        """
        adds Vec-Results using mx' getVecAggsResultsForObjectType to V3_KNOT, V3_ROHR, V3_FWVB, V3_VBEL, ggf. weitere

        returns dct V3s; keys: V3_KNOT, V3_ROHR, V3_FWVB, V3_VBEL, ggf. weitere
        source: V3_KNOT, V3_ROHR, V3_FWVB, V3_VBEL, ggf. weitere      

        columns: 
            einzelne Strings (Sachdaten) und Tupel (Ergebnisdaten)
            bei addNodeData sind bei den VBEL die ergaenzten Knotenergebnisspalten auch Strings mit _i/_k am Ende            
        """

        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:
            
            V3 = {}
            dfKnotRes=pd.DataFrame()
            
            for dfName, resType in zip(['V3_KNOT', 'V3_ROHR', 'V3_FWVB'], ['^KNOT', '^ROHR~', '^FWVB']):
                # Ergebnisse lesen
                
                logger.debug(f"{logStr}dfName: {dfName}: read Results:")
                
                try:
                
                    dfRes = mx.getVecAggsResultsForObjectType(resType)
                    
                    if not dfRes.empty:
    
                        #logger.debug("{0:s}dfRes: {1:s}".format(logStr,dfRes.to_string()))
        
                        if dfName == 'V3_KNOT' and addNodeData:
        
                            # df mit Knotenergebnissen merken
                            dfKnotRes = dfRes
                            # gewünschte Ergebnisspalten von Knoten
                            Sir3sIDs = dfKnotRes.columns.get_level_values(1)
                            
                            Sir3sIDsMatching=[]
                            for addNodeDataSir3sVecIDReExp in addNodeDataSir3sVecIDReExps:
                                Sir3sIDsMatching = Sir3sIDsMatching + [Sir3sID for Sir3sID in Sir3sIDs if re.search(
                                    addNodeDataSir3sVecIDReExp, Sir3sID) != None]
                                                
                            # die zur Ergänzung gewünschten Ergebnisspalten von Knoten
                            dfKnotRes = dfKnotRes.loc[:, (slice(
                                None), Sir3sIDsMatching, slice(None), slice(None))]
                                         
                            dfKnotRes.columns = dfKnotRes.columns.to_flat_index()
                    
                        dfRes.columns = dfRes.columns.to_flat_index()
        
                        #Sachspalten lesen
                        df = self.dataFrames[dfName]
        
                        # Ergebnisspalten ergänzen                
                        V3[dfName] = df.merge(
                                dfRes, left_on='tk', right_index=True, how='left')  
                    
                    else:
                        V3[dfName] = self.dataFrames[dfName]

                except Exception as e:
                     logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                         logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
                     logger.debug(logStrFinal)

            if addNodeData and not dfKnotRes.empty:

                for dfName in ['V3_ROHR', 'V3_FWVB']:
                    
                    logger.debug(f"{logStr}dfName: {dfName}: addNodeData:")
                    
                    try:                    
                        df = V3[dfName]
                        
                        df = pd.merge(df, dfKnotRes.add_suffix(
                            '_i'), left_on='fkKI', right_index=True, how='left')   
                        df = pd.merge(df, dfKnotRes.add_suffix(
                            '_k'), left_on='fkKK', right_index=True, how='left')   
                             
                        V3[dfName] = df
                        
                    except Exception as e:
                         logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                             logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
                         logger.debug(logStrFinal)
            
                                            
            # V3_VBEL
            # ####################
    
            dfVBEL=self.dataFrames['V3_VBEL']
            logger.debug(f"dfVBEL before edge loop:\n{df}")
            
            #logger.debug("{0:s}dfVBEL: {1:s}".format(logStr,dfVBEL.head().to_string()))
            
            # QM
            dfOBJTYPEs=mx.getVecAggsResultsForAttributeType()
            
            # all edges
            dfs=[]
            for edge in [edge for edge in dfVBEL.index.unique(level=0).to_list()]:
                  try:    
                                                          
                    df=dfOBJTYPEs[edge]
                    logger.debug(f"df after df=dfOBJTYPEs[edge]:\n{df}")
                    #logger.debug(f"{logStr}{edge}: {type(df)}")
                    
                    df.columns=df.columns.to_flat_index()
                    df.columns = [str(col) for col in df.columns]
                    logger.debug(f"df after df.columns = [str(col) for col in df.columns]:\n{df}")
                    for col in df.columns.tolist():
                        logger.debug(f"{col} {type(col)}\n")
                    #df.columns = [str(col) for col in df.columns]
                    #df = df.rename(columns=lambda x: x + '_df')
                    
                    newCols=df.columns.to_list()
                    logger.debug(f"df after df.columns:\n{df}")
                    
                    df=pd.merge(dfVBEL.loc[(edge,),:],df,left_index=True,right_index=True,suffixes=('_VBEL','')).filter(items=newCols,axis=1)
                    logger.debug(f"df after merge:\n{df}")
                    
                    df['OBJID']=df.index
                    df['OBJTYPE']=edge
                    logger.debug(f"df after new OBJID OBJTYPE cols:\n{df}")
                    
                    #logger.debug(f"{logStr}{edge}: {type(df)}")
                    #logger.debug(f"{logStr}{edge}: {df.head()}")
                    
                    #logger.debug(f"df before constructNewMultiindexFromCols data types:\n{df.dtypes}")
                    #logger.debug(f"df before constructNewMultiindexFromCols dimensions: {df.shape}")
                    #logger.debug(f"df before constructNewMultiindexFromCols:\n{df}")
                    df=dxAndMxHelperFcts.constructNewMultiindexFromCols(df)
                                        
                    #df=pd.merge(dfVBEL.loc[(edge,),:],df,left_index=True,right_index=True)
                    dfs.append(df)
                     
                    #for newCol in newCols: 
                    #    pass
                    #dfVBEL.loc[(edge,),newCols]=df[newCols].values

                  except Exception as e:                               
                    logStrEdge="{:s}Exception: Line: {:d}: {!s:s}: {:s}: Edge-Type {:s}: adding Vec-Results failed.".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e),edge)            
                    logger.debug(logStrEdge)             
            
            if len(dfs) > 0:
                dfVBEL=pd.merge(dfVBEL,pd.concat(dfs),left_index=True, right_index=True,how='left')
            
            logger.debug("{0:s}dfVBEL nach concat: {1:s}".format(logStr,dfVBEL.head().to_string()))
            logger.debug(f"dfKnotRes before addNodeData:\n{dfKnotRes}")# contains QM Data
            
            if addNodeData:
                
                dfVBEL = pd.merge(dfVBEL, dfKnotRes.add_suffix('_i'), left_on='fkKI', right_index=True, how='left')
                dfVBEL = pd.merge(dfVBEL, dfKnotRes.add_suffix('_k'), left_on='fkKK', right_index=True, how='left')
                                                                                                                      
            V3['V3_VBEL'] = dfVBEL
            
            logger.debug(f"dfVBEL before return:\n{dfVBEL}")
                                    
            return V3

        except Exception as e:
            logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
            logger.error(logStrFinal)
            raise DxError(logStrFinal)
        finally:
            logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))
            #return V3

    def ShpAdd(self, shapeFile, crs='EPSG:25832', onlyObjectsInContainerLst=['M-1-0-1'], addNodeData=False, NodeDataKey='pk'):
        """
        returns dct with (hopefully) plottable GeoDataFrames; keys: V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere
        source: V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere

        adds Geometry from shapeFile (3S Shapefile-Export) to V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere

        geometry is set to shapeFile's column geometry
        crs is set to crs

        auch wenn SIR 3S ab N zukuenftig nativ eine Geometriespalte haelt, kann es sinnvoll sein 
        fuer bestimmte Darstellungszwecke Geometrien (zu generieren) und hier zuzuordnen 

        V3_FWVB:
            Geometry: LineString is converted to Point 
        V3_ROHR and V3_FWVB:
            if addNodeData: all V3_KNOT Data is added as columns named with postfix _i and _k

        """

        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:
            shpGdf = geopandas.read_file(shapeFile)
            shpGdf.set_crs(crs=crs, inplace=True, allow_override=True)

            shpGdf = shpGdf[['3SPK', 'TYPE', 'geometry']]
            shpGdf.rename(columns={'TYPE': 'TYPE_shp'}, inplace=True)

            V3 = {}
            try:
                for dfName, shapeType in zip(['V3_KNOT', 'V3_ROHR', 'V3_FWVB'], ['KNOT', 'ROHR', 'FWVB']):
                    df = self.dataFrames[dfName]
                    if 'geometry' in df.columns.to_list():
                        df = df.drop(columns='geometry')
                    df = df.merge(shpGdf[shpGdf.TYPE_shp == shapeType], left_on='pk', right_on='3SPK', how='left').filter(
                        items=df.columns.to_list()+['geometry'])
                    gdf = geopandas.GeoDataFrame(df, geometry='geometry')
                    gdf.set_crs(crs=crs, inplace=True, allow_override=True)
                    gdf = gdf[
                        # nur Objekte fuer die das shapeFile eine Geometrieinformation geliefert hat
                        ~(gdf['geometry'].isin([None, '', np.nan]))
                        &
                        # keine Objekte in z.B. Stationen
                        (gdf['NAME_CONT'].isin(onlyObjectsInContainerLst))
                    ]
                    V3[dfName] = gdf
            except Exception as e:
                logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                    logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
                logger.debug(logStrFinal)
                # empty DataFrame if problem occured
                V3[dfName] = pd.DataFrame()

            # Nacharbeiten FWVB
            if 'V3_FWVB' in V3.keys():
                gdf = V3['V3_FWVB']
                for index, row in gdf.iterrows():
                    if not pd.isnull(row['geometry']):
                        if isinstance(row['geometry'], shapely.geometry.linestring.LineString):
                            gdf.loc[index, 'geometry'] = row['geometry'].centroid
                V3['V3_FWVB'] = gdf

            # Nacharbeiten addNodeData
            if addNodeData:
                for dfName in ['V3_ROHR', 'V3_FWVB']:
                    df = V3[dfName]
                    df = pd.merge(df, self.dataFrames['V3_KNOT'].add_suffix(
                        '_i'), left_on='fkKI', right_on=NodeDataKey+'_i')
                    df = pd.merge(df, self.dataFrames['V3_KNOT'].add_suffix(
                        '_k'), left_on='fkKK', right_on=NodeDataKey+'_k')
                    V3[dfName] = df

        except Exception as e:
            logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
            logger.error(logStrFinal)
            raise DxError(logStrFinal)

        finally:
            logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))
            return V3

    def _filterTemplateObjects(self):
        """        
        filters TemplateObjects 
        in V3_KNOT, V3_ROHR, V3_FWVB
        """

        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:
            for dfName in ['V3_KNOT', 'V3_ROHR', 'V3_FWVB']:
                df = self.dataFrames[dfName]
                (rows,dummy)=df.shape
                if 'KENNUNG' in df.columns.to_list():
                    df = df[(df['KENNUNG'] >= 0)
                            |
                            (pd.isnull(df['KENNUNG']))
                            ]
                else:
                    df = df[~df['BESCHREIBUNG'].str.contains('^Templ',na=False)]
                
                logger.debug(f"{logStr}{dfName}: Zeilen vorher: {rows} Zeilen jetzt: {df.shape[0]}")
                
                self.dataFrames[dfName] = df

        except Exception as e:
            logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
            logger.error(logStrFinal)
            raise DxError(logStrFinal)
        finally:
            pass
            logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))

    def _vROHRVecs(self, vROHR, mx):
        """Adds MX-ROHR-VEC-Results in dfVecAggs as cols to df.

        Args:
            vROHR: df (i.a. dataFrames['V3_ROHR'])
            cols expected in vROHR (call MxSync to add this cols to dataFrames['V3_ROHR']):
                mx2Idx
                mx2NofPts

        Returns:
            df with 
                vROHR's cols 
                IptIdx (S(tart), 0,1,2,3,... ,E(nde))
                x: fortl. Rohrachskoordinate errechnet aus L und mx2NofPts
                cols with MX-ROHR-VEC-Results i.e. (STAT, ROHR~*~*~*~MVEC, 2022-09-28 13:24:00, 2022-09-28 13:24:00)                          
        """

        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:

            df = pd.DataFrame()

            # alle MX-ROHR-VEC-Results in dfVecAggs
            dfT = mx.dfVecAggs.loc[(slice(None), mx.getRohrVektorkanaeleIpkt(), slice(
                None), slice(None)), :].transpose()
            dfT.columns = dfT.columns.to_flat_index()
            # cols= (STAT, ROHR~*~*~*~MVEC, 2022-09-28 13:24:00, 2022-09-28 13:24:00) ...
            # idx= 0,1,2,3,...

            # dfT mit mx2Idx annotieren, damit merge vROHR moeglich
            # dfT mit IptIdx annotieren, damit IPKT-Sequenz leichter lesbar
            rVecMx2Idx = []
            IptIdx = []

            # Mx2-Records sind in Mx2-Reihenfolge und muessen auch so annotiert werden ...
            for row in vROHR.sort_values(['mx2Idx']).itertuples():
                oneVecIdx = np.empty(row.mx2NofPts, dtype=int)
                oneVecIdx.fill(row.mx2Idx)
                rVecMx2Idx.extend(oneVecIdx)

                oneLfdNrIdx = ['S']
                if row.mx2NofPts > 2:
                    oneLfdNrIdx.extend(np.arange(row.mx2NofPts-2, dtype=int))
                oneLfdNrIdx.append('E')
                IptIdx.extend(oneLfdNrIdx)

            dfTCols = dfT.columns.to_list()
            dfT['mx2Idx'] = rVecMx2Idx
            dfT['IptIdx'] = IptIdx

            # merge
            df = pd.merge(vROHR, dfT, how='inner',
                          left_on='mx2Idx', right_on='mx2Idx')

            # x
            df['dx'] = df.apply(lambda row: row.L/(row.mx2NofPts-1), axis=1)
            df['x'] = df.groupby('mx2Idx')['dx'].cumsum()
            df['x'] = df.apply(lambda row: row.x-row.dx, axis=1)

            # Reorg der Spalten
            df = df.filter(items=vROHR.columns.to_list() +
                           ['IptIdx', 'x']+dfTCols)

        except Exception as e:
            logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
            logger.debug(logStrFinal)

        finally:
            logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))
            return df

    def _vROHRVrtx(self, vROHR, mx):
        """Adds MX-ROHR-VRTX-Results in dfVecAggs as cols to df.

        Args:
            vROHR: df (i.a. dataFrames['V3_ROHR'])


        Returns:
            df with 
                vROHR's cols 
                VRTX-Cols:
                    pk_Vrtx
                    fk_Vrtx
                    XKOR
                    YKOR
                    ZKOR
                    LFDNR
                    mx2IdxVrtx        
                        the df is sorted by mx2IdxVrtx (should be equal to sort by ROHR, VRTX-LFDNR)
                s: fortl. Rohrachskoordinate errechnet aus VRTX
                cols with MX-ROHR-VRTX-Results i.e. (STAT, ROHR_VRTX~*~*~*~M, 2022-09-28 13:24:00, 2022-09-28 13:24:00)                          
        """

        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:

            df = pd.DataFrame()

            # alle MX-ROHR-VRTX-Results in dfVecAggs
            dfT = mx.dfVecAggs.loc[(slice(None), mx.getRohrVektorkanaeleVrtx(), slice(
                None), slice(None)), :].transpose()
            dfT.columns = dfT.columns.to_flat_index()
            # cols= (STAT, ROHR~*~*~*~MVEC, 2022-09-28 13:24:00, 2022-09-28 13:24:00) ...
            # idx= 0,1,2,3,...

            # Liste der VRTX-PKs in MX2
            xksMx = mx.mx2Df[
                (mx.mx2Df['ObjType'].str.match('ROHR_VRTX'))
            ]['Data'].iloc[0]

            vROHR_VRTX = self.dataFrames['V_ROHR_VRTX']
            # diese Liste sollte leer sein:
            l = [x for x in xksMx if x not in vROHR_VRTX['pk'].values]
            if len(l) != 0:
                logger.error(
                    "{:s}Es gibt Verweise in MX2 die auf keinen VRTX-Wegpunkt zeigen?!".format(logStr))

            # -1 aussortieren
            # keine Sachdaten VRTX-Wegpunkte ohne Nennung in MX-VRTX
            vROHR_VRTX_eff = vROHR_VRTX[vROHR_VRTX['pk'].isin(xksMx)]

            # nur die Sach-ROHRe die Sach-Wegpunkte haben
            vROHR_eff = vROHR[vROHR['pk'].isin(vROHR_VRTX_eff['fk'].values)]

            # Wegpunkte
            df = pd.merge(vROHR_eff, vROHR_VRTX_eff.filter(items=['pk',
                                                                  'fk',
                                                                  'XKOR',
                                                                  'YKOR',
                                                                  'ZKOR',
                                                                  'LFDNR',
                                                                  ]), left_on='pk', right_on='fk', suffixes=('', '_Vrtx'))

            # Vorbereitung fuer Merge mit MX
            df['mx2IdxVrtx'] = [xksMx.index(xk) for xk in df['pk_Vrtx'].values]

            # Merge mit MX
            # df=pd.merge(df,dfT,how='inner',left_on='mx2IdxVrtx',right_index=True)

            df.sort_values(by=['mx2IdxVrtx'], inplace=True)
            df.reset_index(drop=True, inplace=True)

            # s errechnen

            dfTmp = df[['pk', 'LFDNR', 'XKOR', 'YKOR', 'ZKOR']]

            dfTmp['XKOR'] = dfTmp.groupby(
                ['pk'])['XKOR'].shift(periods=1, fill_value=0)
            dfTmp['YKOR'] = dfTmp.groupby(
                ['pk'])['YKOR'].shift(periods=1, fill_value=0)
            dfTmp['ZKOR'] = dfTmp.groupby(
                ['pk'])['ZKOR'].shift(periods=1, fill_value=0)

            dfTmp.rename(
                columns={'XKOR': 'DXKOR', 'YKOR': 'DYKOR', 'ZKOR': 'DZKOR'}, inplace=True)

            dfTmp = pd.concat([df[['mx2IdxVrtx', 'pk', 'L', 'LFDNR', 'XKOR', 'YKOR', 'ZKOR']], dfTmp[[
                              'DXKOR', 'DYKOR', 'DZKOR']]], axis=1)

            dfTmp['DXKOR'] = dfTmp.apply(lambda row: math.fabs(
                row.XKOR-row.DXKOR) if row.DXKOR > 0 else 0, axis=1)
            dfTmp['DYKOR'] = dfTmp.apply(lambda row: math.fabs(
                row.YKOR-row.DYKOR) if row.DYKOR > 0 else 0, axis=1)
            dfTmp['DZKOR'] = dfTmp.apply(lambda row: math.fabs(
                row.ZKOR-row.DZKOR) if row.DZKOR > 0 else 0, axis=1)

            dfTmp['ds'] = dfTmp.apply(lambda row: math.sqrt(math.pow(
                row.DZKOR, 2)+math.pow(math.sqrt(math.pow(row.DXKOR, 2)+math.pow(row.DYKOR, 2)), 2)), axis=1)
            dfTmp['s'] = dfTmp.groupby('pk')['ds'].cumsum()

            df = pd.concat([df, dfTmp[['s']]], axis=1)

            # Merge mit MX
            df = pd.merge(df, dfT, how='inner',
                          left_on='mx2IdxVrtx', right_index=True)

        except Exception as e:
            logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
            logger.debug(logStrFinal)

        finally:
            logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))
            return df

    def dbFileMutable(self):       
        """
        Checks if dbFile is mutable
                
        :return: True/False       
        """           
        
        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:
            if os.path.exists(self.dbFile):
                if os.access(self.dbFile, os.W_OK):                    
                    # das dbFile existiert und ist lesbar
                    logger.debug("{:s}dbFile: {:s} exists and is mutable".format(
                        logStr, self.dbFile))                
                    return True            
                else:
                    logger.debug("{:s}dbFile: {:s} exists but is not mutable".format(
                        logStr, self.dbFile))                         
                    return False
            else:
                logger.debug("{:s}dbFile: {:s} not existing".format(
                    logStr, self.dbFile))                         
                return False                                       
        except Exception as e:
           logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
               logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
           logger.error(logStrFinal)    
        finally:
           logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))                             


    def update(self,dfUpd,updInverseValue=None):       
        """
        Updates dbFile (SQLite only)
        
        :param dfUpd: df with update data 
        :type dfUpd: df                 
        :param updInverseValue: value to use for attribValue for inverse objects  
        :type updInverseValue: ?, optional, default=None 
        
        :return: rowsAffectedTotal
        
        .. note:: 
            Comprehensive changes to model data should be made via the SIR 3S user interface. Or via the SIR 3S import interfaces which - depending on type/operation/parameterization - can also overwrite (update) existing model data. Nonetheless, scripted model changes can be helpful.

        .. note:: 
            dfUpd's cols used:            
                - table i.e. 'FWVB'
                - attrib i.e. 'W0'
            dfUpd's cols optional:         
                - attribValue, default=dfUpd[attrib] 
                - xk, default='tk'
                - xkValue, default=dfUpd[xk] 
            row-wise:
                - set attrib to attribValue in table where xk is xkValue
                - update an attribute of an object
            updInverseValue:
                - set attrib to updInverseValue for all objects of type table not mentioned in dfUpd                
        """           
        
        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:
            if not self.dbFileMutable():            
                logStrFinal="{:s}dbFile: {:s}: not existing or not mutable".format(logStr,self.dbFile)   
                raise DxError(logStrFinal)
                       
            dummy, ext = os.path.splitext(self.dbFile)

            if ext != '.db3':
                 logStrFinal = "{:s}Function only implemented for SQLite (.db3)".format(logStr)
                 raise DxError(logStrFinal)                
                           
            con = sqlite3.connect(self.dbFile)
            
            def updateFct(con,sql,OBJID,VALUE):
                """
                """
                
                rowsAffected=None
                
                cur = con.cursor()
                cur.execute(sql,(VALUE,OBJID))
                rowsAffected=cur.rowcount
                con.commit()

                return rowsAffected
                       
            dfUpd=dfUpd.copy(deep=True)
            
            cols=dfUpd.columns.to_list()
            if 'attribValue' not in cols:
                dfUpd['attribValue']=dfUpd.apply(lambda row: row[row['attrib']],axis=1)
            if 'xk' not in cols:
                dfUpd['xk']='tk'
            if 'xkValue' not in cols:
                dfUpd['xkValue']=dfUpd.apply(lambda row: row[row['xk']],axis=1)
            
            rowsAffectedTotal=0  
            
            try:                
                for index, row in dfUpd.iterrows():
                    sqlCmd = '''UPDATE {table:s} SET {attrib:s} = ? WHERE {xk:s} = ?'''.format(table=row['table'],attrib=row['attrib'],xk=row['xk'])
                    logStrSql="sqlCmd: {sqlCmd:s}:  attribValue:{attribValue:s} xkValue:{xkValue:s} ...".format(sqlCmd=sqlCmd,attribValue=str(row['attribValue']),xkValue=str(row['xkValue']))
                    logger.debug("{:s}{:s}".format(logStr,logStrSql))
                    rowsAffected=updateFct(con,sqlCmd,row['xkValue'],row['attribValue'])
                    logger.debug("{:s}rowsAffected: {:s}".format(logStr,str(rowsAffected)))
                    rowsAffectedTotal=rowsAffectedTotal+rowsAffected
                    
                if updInverseValue!= None:
                    
                    for (table,attrib,xk),rowDummy in dfUpd.groupby(by=['table','attrib','xk']).count().iterrows():                            
                        logger.debug("{:s}UpdInverse: {:s} {:s} {:s}".format(logStr,table,attrib,xk))
                        tabDf=self.dataFrames[table]
                        tabDf=tabDf[~pd.isnull(tabDf[xk])]
                        tabDf=tabDf[~tabDf[xk].isin([-1,'-1'])]
                        dfUpdInv=tabDf[~tabDf[xk].isin(dfUpd['xkValue'])]
                    
                        for index,row in dfUpdInv.iterrows():
                             sqlCmd = '''UPDATE {table:s} SET {attrib:s} = ? WHERE {xk:s} = ?'''.format(table=table,attrib=attrib,xk=xk)
                             logStrSql="sqlCmd: {sqlCmd:s}: attribValue:{attribValue:s} xkValue:{xkValue:s} ...".format(sqlCmd=sqlCmd,attribValue=str(updInverseValue),xkValue=str(row[xk]))
                             logger.debug("{:s}{:s}".format(logStr,logStrSql))
                             rowsAffected=updateFct(con,sqlCmd,row[xk],updInverseValue)
                             logger.debug("{:s}rowsAffected: {:s}".format(logStr,str(rowsAffected)))
                             rowsAffectedTotal=rowsAffectedTotal+rowsAffected
                                                    
            except Exception as e:
                logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                    logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
                logger.error(logStrFinal)

            finally:
                con.close()
            
            return rowsAffectedTotal

        except Exception as e:
           logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
               logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
           logger.error(logStrFinal)
    
        finally:
           logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))      
           #return rowsAffectedTotal
       
       
    def insert(self,table,dfIns,xkFct=fXk):       
        """
        Inserts into a dbFile's table (SQLite only)
        
        :param table: table to insert to 
        :type table: str 
        :param dfIns: df with insert data 
        :type dfIns: df   
        :param xkFct: func to call row-wise to obtain (pk, rk, tk) for an record to insert
        :type xkFct: func, optional, default=Dx.fXk      
        
        :return: rowsAffected, dfIns (a copy of dfIns; cols pk, rk, tk: inserted values; cols pkOrig, rkOrig, tkOrig: original values)

        .. note:: 
            New model mass data should be created via the SIR 3S import interfaces. Nevertheless, generating model mass data via script can be helpful.

        .. note:: 
            dfIns' cols used:            
                - all cols which are also cols of table                
            row-wise:
                - insert into table                
        """           
        
        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:
            if not self.dbFileMutable():            
                logStrFinal="{:s}dbFile: {:s}: not existing or not mutable".format(logStr,self.dbFile)   
                raise DxError(logStrFinal)
                       
            dummy, ext = os.path.splitext(self.dbFile)

            if ext != '.db3':
                 logStrFinal = "{:s}Function only implemented for SQLite (.db3)".format(logStr)
                 raise DxError(logStrFinal)             
            

            rowsAffected=None
                                       
            dfToIns=self.dataFrames[table]
            cols=dfToIns.columns.to_list()
            colList=':'+cols[0]
            for col in cols[1:]:
                colList=colList+','+':'+col
            sql = '''INSERT OR REPLACE INTO {table:s} VALUES({colList:s})'''.format(table=table,colList=colList)
            logger.debug("{:s}sql: {:s}".format(logStr,sql))
            
            # Kopie der einzufuegenden Zeilen
            dfIns=dfIns.copy(deep=True).reset_index(drop=True)
            # # Original-Xks merken
            # for col in ['pk','rk','tk']:
            #     if col in cols:
            #         dfIns[col+'Orig']=dfIns[col]
            
            data=dfIns.to_dict(orient='records')
            
            # Original-Xks merken
            for col in ['pk','rk','tk']:
                if col in cols:
                    dfIns[col+'Orig']=dfIns[col]            
            
            for index,recordDct in enumerate(data):            
                row=dfIns.loc[index,:]
                (pk,rk,tk)=xkFct(row)
                for xkValue,xkCol in zip((pk,rk,tk),['pk','rk','tk']):
                    if xkCol in cols:
                        # Xks setzen 
                        recordDct[xkCol]=xkValue  
                        # Xks merken
                        dfIns.loc[index,xkCol]=xkValue 
            data=tuple(data)   
            logger.debug("{:s}data: {:s}".format(logStr,str(data)))
                                
            con = sqlite3.connect(self.dbFile)
            
            def insertFct(con,sql,data):
                """
                """
                
                rowsAffected=None
                
                cur = con.cursor()
                cur=cur.executemany(sql, data)
                rowsAffected=cur.rowcount
                con.commit()
            
                return rowsAffected            
                                    
            try:                                
                rowsAffected=insertFct(con,sql,data)                                                      
            except Exception as e:
                logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
                    logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
                logger.error(logStrFinal)

            finally:
                con.close()
            
            return rowsAffected,dfIns 

        except Exception as e:
           logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
               logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
           logger.error(logStrFinal)
    
        finally:
           logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))      
           #return rowsAffected        

    def importFromSIR3S(self
                        ,dbSrc
                        ,tablesToImport=['STRASSE','LTGR','DTRO','DTRO_ROWD','KNOT','KNOT_BZ','ROHR','ROHR_BZ','FWVB','FWVB_BZ','LAYR']
                        ,fksNotToFillWithDstTemplateValues=['fkKI','fkKK','fkDTRO_ROWD','fkLTGR','fkSTRASSE']
                        ,fctsToCall={'*':fimportFromSIR3S}
                        ,fctsToCallLogging=True
                        ):       
        """
        Import data from an other SIR 3S Model (SQLite only)
        
        :param dbSrc: SIR 3S dbFile to import from
        :type dbSrc: str 
        :param tablesToImport: tabNames to import from
        :type tablesToImport: list of tabNames, optional, default=['STRASSE','LTGR','DTRO','DTRO_ROWD'
                                                                   ,'KNOT','KNOT_BZ','ROHR','ROHR_BZ','FWVB','FWVB_BZ'
                                                                   ,'LAYR']
        :param fksNotToFillWithDstTemplateValues: colNames starting with fk not to set to the corresponding Dst-Template-Value
        :type fksNotToFillWithDstTemplateValues: list of fk starting colNames, optional, default=['fkKI','fkKK','fkDTRO_ROWD','fkLTGR','fkSTRASSE']
        :param fctsToCall: dct of functions to call before import
        :type fctsToCall: dct of functions, optional, default={'*':fimportFromSIR3S}; f('*') is called if defined and then the object-specific f(OBJ) is called if defined
        :param fctsToCallLogging: decide if fctsToCall shall generate Log-Output
        :type fctsToCallLogging: bool, optional, default=True
        
        .. note:: 
            Model data from annother SIR 3S Model should be imported via the SIR 3S export/import interfaces. 
            I.e. export in Src Sdf/Csv, import in Dst the exported Sdf/Csv. Or copy in Src and paste in Dst. Or export/import SIR 3S Blocks. 
            Nevertheless, importing from another Model via script can be helpful.

        .. note::              
            Template-Objects are Objects with col 'KENNUNG' < 0.
            Template-Objects are not copied from Src to Dst.
            For objects with Templates defined all Non-Null fk-Starting Template-Attributes from Dst are set except for: fksNotToFillWithDstTemplateValues.
            It follows that i.e. for KNOT(_BZ), ROHR(_BZ), FWVB(_BZ) fkDE is set to the corresponding fkDE Dst-Template-Attribute if defined.
            For all objects fkDE is finally set to fkBASIS(fkBZ) of the SYSTEMKONFIG(3)-Model if SYSTEMKONFIG(3) is defined.
            
        .. note::              
            Dst and Src: SIR 3S Version and CRS (coordinate reference system) should be identical, QGIS-Export should be done (to ensure correct and matching GEOMWKBs in Dst and Src).          
            
        """           
        
        logStr = "{0:s}.{1:s}: ".format(
            self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

        try:
            
            SrcDb=dbSrc
            engineSrc = create_engine("sqlite:///"+SrcDb)
            BaseSrc = automap_base()      
            BaseSrc.prepare(autoload_with=engineSrc)
            sessionSrc = Session(engineSrc)
            
            OBJsSrc=[]
            for t in tablesToImport:
                for c in BaseSrc.classes:
                    if t==c.__table__.name:
                        OBJsSrc.append(c)                    
                        break
            #OBJsSrc=[BaseSrc.classes.STRASSE,BaseSrc.classes.LTGR,BaseSrc.classes.DTRO,BaseSrc.classes.DTRO_ROWD,BaseSrc.classes.KNOT,BaseSrc.classes.KNOT_BZ,BaseSrc.classes.ROHR,BaseSrc.classes.ROHR_BZ,BaseSrc.classes.FWVB,BaseSrc.classes.FWVB_BZ,BaseSrc.classes.LAYR]
            
            engineDst = create_engine("sqlite:///"+self.dbFile)
            BaseDst = automap_base()
            BaseDst.prepare(autoload_with=engineDst)
            sessionDst = Session(engineDst)     
            
            OBJsDst=[]
            for t in tablesToImport:
                for c in BaseDst.classes:
                    if t==c.__table__.name:
                        OBJsDst.append(c)                          
                        break
            #OBJsDst=[BaseDst.classes.STRASSE,BaseDst.classes.LTGR,BaseDst.classes.DTRO,BaseDst.classes.DTRO_ROWD,BaseDst.classes.KNOT,BaseDst.classes.KNOT_BZ,BaseDst.classes.ROHR,BaseDst.classes.ROHR_BZ,BaseDst.classes.FWVB,BaseDst.classes.FWVB_BZ,BaseDst.classes.LAYR]
            
            if self.QGISmodelXk != None:
                stmt = select(text('fkBASIS,fkBZ from VIEW_MODELLE where pk={:s}'.format(self.QGISmodelXk)))
                #print(stmt)
                
                with engineDst.connect() as conn:
                    result = conn.execute(stmt).fetchall()
                    for row in result:
                        #print(row)
                        break
                (fkBASIS,fkBZ)=row   
                #print((fkBASIS,fkBZ))   
            
            #fksNotFilledWithTemplateValues=['fkKI','fkKK','fkDTRO_ROWD','fkLTGR','fkSTRASSE']
            if self.QGISmodelXk != None:
                fksNotToFillWithDstTemplateValues=fksNotToFillWithDstTemplateValues+['fkDE']
                
            # Template Handling    
            OBJDstTemplates={}
            for OBJSrc,OBJDst in zip(OBJsSrc,OBJsDst):
                objTYPE=OBJSrc.__table__.name
                #print(objTYPE)
                
                OBJDstcols=[column.key for column in OBJDst.__table__.columns]    
                if 'KENNUNG' in OBJDstcols:
                    for objTemplateDst in sessionDst.query(OBJDst) \
                        .filter(OBJDst.KENNUNG<0):
                        #logger.debug(f"{logStr}{objTYPE}: Template Handling: ...")
                        break # das erste gefundene Template dient als Vorlage
                
                    objTemplateDstfkAttribs=[]
                    objTemplateSrcpks=[]
                    
                    for name,value in inspect.getmembers(objTemplateDst,lambda a:not(inspect.isfunction(a))):
                        if re.search('^_',name) == None and (isinstance(value,str) or isinstance(value,int) or isinstance(value,float)) :
                            if re.search('^fk',name) != None: 
                                if name not in fksNotToFillWithDstTemplateValues:
                                    logger.debug(f"{logStr}{objTYPE:12s}: Template Handling: attr: {name:12s} will be set to Dst-Template-value: {getattr(objTemplateDst,name)}")
                                    #print(name,getattr(objTemplateDst,name))
                                    objTemplateDstfkAttribs.append(name)    
                    
                    for objTemplateSrc in sessionSrc.query(OBJSrc) \
                        .filter(OBJSrc.KENNUNG<0):
                        objTemplateSrcpks.append(objTemplateSrc.pk) # pks aller Template-Objekte merken
                    
                    OBJDstTemplates[objTYPE]=(OBJDstcols,objTemplateDst,objTemplateDstfkAttribs,objTemplateSrcpks,None)                     
                    
            # Templates in BZ-Tabellen finden          
            for OBJSrc,OBJDst in zip(OBJsSrc,OBJsDst):
                objTYPE=OBJSrc.__table__.name
                #print(objTYPE)
                
                if re.search('_BZ$',objTYPE) == None:
                    continue # keine BZ-Tabelle
                
                BobjType=re.sub('_BZ$','',objTYPE)
                if BobjType in OBJDstTemplates.keys():
                    
                    #print(objTYPE,BobjType)
                    pass 
                    
                    (OBJDstcols,objTemplateDst,objTemplateDstfkAttribs,objTemplateSrcpks,dummy) =  OBJDstTemplates[BobjType]     
                    
                    for objTemplateDstBZ in sessionSrc.query(OBJSrc).filter(OBJSrc.pk.not_in([-1,'-1']))\
                        .filter(OBJSrc.fk.in_(objTemplateSrcpks)):
                        pass
                        #print('Template')
                        break # das erste gefundene Template dient als Vorlage       
                    
                    OBJDstTemplates[BobjType]=(OBJDstcols,objTemplateDst,objTemplateDstfkAttribs,objTemplateSrcpks,objTemplateDstBZ)
             
            # Copy
            for OBJSrc,OBJDst in zip(OBJsSrc,OBJsDst):
                
                objTYPE=OBJSrc.__table__.name
                #print(objTYPE)
                    
                OBJSrccols=[column.key for column in OBJSrc.__table__.columns]    
                    
                if objTYPE in OBJDstTemplates.keys(): # table has templates
               
                    (OBJDstcols,objTemplateDst,objTemplateDstfkAttribs,objTemplateSrcpks,dummy) =  OBJDstTemplates[objTYPE]     
                    
                    #logger.debug(f"{logStr}{objTYPE:12s}: Template Handling: attrs: {objTemplateDstfkAttribs} will be set to Template-values ...")
                    if self.QGISmodelXk != None:
                        logger.debug(f"{logStr}{objTYPE:12s}: attr: fkDE will be set to fkBASIS: {fkBASIS}")    
            
                    objDstPks=[]
                    for objDst in sessionDst.query(OBJDst):
                        objDstPks.append(objDst.pk) # pks in Ziel-DB merken             
                        
                    q1=sessionSrc.query(OBJSrc).filter(OBJSrc.pk.not_in([-1,'-1']))
                    q2=q1.filter(or_(OBJSrc.KENNUNG>0, OBJSrc.KENNUNG == None))
                    q=q2.filter(OBJSrc.pk.not_in(objDstPks))
                    
                    logger.debug(f"{logStr}{objTYPE:12s}: {q.count()} to copy (not copied because Templates: {q1.count()-q2.count()}) (not to copy because pk exists already in Dst: {q2.count()-q.count()})")                                         
                    
                    #for objSrc in sessionSrc.query(OBJSrc) \
                    #    .filter(or_(OBJSrc.KENNUNG>0, OBJSrc.KENNUNG == None))\
                    #    .filter(OBJSrc.pk.not_in([-1,'-1'])):
                        
                    for objSrc in q:                        
                        
                        objDst=OBJDst()
                        for attr in OBJSrccols:                
                            setattr(objDst,attr,getattr(objSrc,attr))                
                                            
                        # override Src-values with Dst-values for all template-attributes   
                        for attr in objTemplateDstfkAttribs:                
                            setattr(objDst,attr,getattr(objTemplateDst,attr))
                            
                        if self.QGISmodelXk != None:
                             for attr in ['fkDE']:
                                setattr(objDst,attr,fkBASIS)
                                
                        toImport=True
                        if '*' in fctsToCall.keys():
                            (objDst,toImport)=fctsToCall['*'](self,OBJSrc,q,objSrc,objDst,fctsToCallLogging)                                
                        if objTYPE in fctsToCall.keys() and toImport:
                            (objDst,toImport)=fctsToCall[objTYPE](self,OBJSrc,q,objSrc,objDst,fctsToCallLogging)                                    
                        if toImport:
                            sessionDst.add(objDst)                                                                                                                                 
                    
                else:  
                    BobjType=re.sub('_BZ$','',objTYPE)
                    if BobjType in OBJDstTemplates.keys():
                        pass # table maybe references templates
                    
                        (OBJDstcols,objTemplateDst,objTemplateDstfkAttribs,objTemplateSrcpks,objTemplateDstBZ) =  OBJDstTemplates[BobjType]     
                        
                        if self.QGISmodelXk != None:
                            logger.debug(f"{logStr}{objTYPE:12s}: attr: fkDE will be set to fkBZ   : {fkBZ}")    
                    
                    
                        objDstPks=[]
                        for objDst in sessionDst.query(OBJDst):
                            objDstPks.append(objDst.pk) # pks in Ziel-DB merken   
                                        
                        q1=sessionSrc.query(OBJSrc).filter(OBJSrc.pk.not_in([-1,'-1']))                        
                        q2=q1.filter(OBJSrc.fk.not_in(objTemplateSrcpks))
                        q=q2.filter(OBJSrc.pk.not_in(objDstPks))
                        logger.debug(f"{logStr}{objTYPE:12s}: {q.count()} to copy (not to copy because (referencing) Templates: {q1.count()-q2.count()}) (not to copy because pk exists already in Dst: {q2.count()-q.count()})")                     
                    
                        #for objSrc in sessionSrc.query(OBJSrc).filter(OBJSrc.pk.not_in([-1,'-1']))\
                        #.filter(OBJSrc.fk.not_in(objTemplateSrcpks)):
            
                        for objSrc in q:
                            objDst=OBJDst()
                            for attr in OBJSrccols:                
                                setattr(objDst,attr,getattr(objSrc,attr))                
                    
                            #for attr in ['fkDE']:                    
                            #    setattr(objDst,attr,getattr(objTemplateDstBZ,attr))        
                                
                            if self.QGISmodelXk != None:
                                 for attr in ['fkDE']:
                                    setattr(objDst,attr,fkBZ)
                            else:
                                 for attr in ['fkDE']:                    
                                    setattr(objDst,attr,getattr(objTemplateDstBZ,attr))      
                                    
                                    
                            toImport=True
                            if '*' in fctsToCall.keys():
                                (objDst,toImport)=fctsToCall['*'](self,OBJSrc,q,objSrc,objDst,fctsToCallLogging)                                
                            if objTYPE in fctsToCall.keys() and toImport:
                                (objDst,toImport)=fctsToCall[objTYPE](self,OBJSrc,q,objSrc,objDst,fctsToCallLogging)                                    
                            if toImport:
                                sessionDst.add(objDst)                                     
                                                                                                            
                    else:

                        if self.QGISmodelXk != None:
                            logger.debug(f"{logStr}{objTYPE:12s}: attr: fkDE will be set to fkBASIS: {fkBASIS}")                            
 
                        objDstPks=[]
                        for objDst in sessionDst.query(OBJDst):
                            objDstPks.append(objDst.pk) # pks in Ziel-DB merken            
                        
                        q1=sessionSrc.query(OBJSrc).filter(OBJSrc.pk.not_in([-1,'-1']))                        
                        q=q1.filter(OBJSrc.pk.not_in(objDstPks))
                        logger.debug(f"{logStr}{objTYPE:12s}: {q.count()} to copy (not to copy because pk exists already in Dst: {q1.count()-q.count()})") 
                        for objSrc in q:
            
                            objDst=OBJDst()
                            for attr in OBJSrccols:                
                                setattr(objDst,attr,getattr(objSrc,attr))     
                                
                            if self.QGISmodelXk != None:
                                 for attr in ['fkDE']:
                                    setattr(objDst,attr,fkBASIS)
                                    
                            toImport=True
                            if '*' in fctsToCall.keys():
                                (objDst,toImport)=fctsToCall['*'](self,OBJSrc,q,objSrc,objDst,fctsToCallLogging)                                
                            if objTYPE in fctsToCall.keys() and toImport:
                                (objDst,toImport)=fctsToCall[objTYPE](self,OBJSrc,q,objSrc,objDst,fctsToCallLogging)                                    
                            if toImport:
                                sessionDst.add(objDst)            
                    
                logger.debug(f"{logStr}{objTYPE:12s}: {len(sessionDst.new)} queued to copy (not queued because fctsToCall: {q.count()-len(sessionDst.new)})")
                sessionDst.commit()
            
            sessionDst.close()
            sessionSrc.close()
    
        except Exception as e:
           logStrFinal = "{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(
               logStr, sys.exc_info()[-1].tb_lineno, type(e), str(e))
           logger.error(logStrFinal)
    
        finally:
           logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))



    def setLayerContentTo(self,layerName,df):          
        """
        Updates content of layerName to df's-content
        
        :param layerName: name of an existing layer
        :type layerName: str
        
        :return: rowsAffected
        
        .. note:: 
            Groups or layers are used in SIR 3S as a feature for data access, data filtering and grouping. The assignment of objects to groups should be done (explicit) via the SIR 3S user interface or (implicit) via the SIR 3S import interfaces. Nonetheless, scripted assignment can be useful.

        .. note:: 
            df's cols used:            
                - TYPE 
                - ID                 
        """           
                
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            
            rowsAffected=None
            
            layr=self.dataFrames['LAYR']            
            dfTmp=layr[layr['NAME'].isin([layerName])]
                        
            if dfTmp.empty:                
                logger.debug("{0:s}Layer {1:s} not existing. Maybe (Re-)Processing the dbFile to Dx is necessary...".format(logStr,layerName)) 
            elif dfTmp.shape[0]>1:
                logger.debug("{0:s}LayerName {1:s}: matching rows: {2:s}".format(logStr,layerName,dfTmp.to_string()))                 
                logger.info("{0:s}Layer(name) {1:s} not unique: No Updates ...".format(logStr,layerName)) 
            else:
            
                ###xk=dfTmp['tk'].iloc[0]
                
                
                dfUpd=df.copy(deep=True)
                
                dfUpd['table']='LAYR'
                dfUpd['attrib']='OBJS'
                dfUpd['attribValue']=dfUpd.apply(lambda row: "{:s}~{:s}\t".format(row['TYPE'],row['ID']).encode('utf-8'),axis=1)
                                                
                tk=dfTmp['tk'].iloc[0]
                dfUpd['xk']='tk'
                dfUpd['xkValue']=tk    
                
                dfUpd2=dfUpd.groupby(by=['xkValue']).agg({'xkValue': 'first'
                                                    ,'table': 'first'
                                                    ,'attrib': 'first'
                                                    ,'xk': 'first'
                                                    ,'attribValue': 'sum'}).reset_index(drop=True)
                
                dfUpd2['attribValue']=dfUpd2['attribValue'].apply(lambda x: x.rstrip())
                  
                rowsAffected=self.update(dfUpd2)  
                
                return rowsAffected
        
        except DxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise DxError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))      



def fHelperSqlText(sql, ext='.db3'):
    if ext != '.db3':
        from sqlalchemy import text
        return text(sql)
    else:
        return sql


def fHelper(con, BV, BZ, dfViewModelle, dfCONT, pairType, ext):

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    #logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))
    
    # BV, BZ, BVZ #################

    sql = 'select * from '+BV
    try:
        dfBV = pd.read_sql(fHelperSqlText(sql, ext), con)
    except pd.io.sql.DatabaseError as e:
        logStrFinal = "{0:s}sql: {1:s}: Fehler?!".format(logStr, sql)
        raise DxError(logStrFinal)

    sql = 'select * from '+BZ
    try:
        dfBZ = pd.read_sql(fHelperSqlText(sql, ext), con)
    except pd.io.sql.DatabaseError as e:
        logStrFinal = "{0:s}sql: {1:s}: Fehler?!".format(logStr, sql)
        raise DxError(logStrFinal)
        

    #logger.debug(
    #"{0:s}Quelle BV: {1:s} Quelle BZ: {2:s} BV Zeilen: {3:d} BZ Zeilen: {4:d}".format(logStr, BV, BZ, dfBV.shape[0], dfBZ.shape[0]))            
        

    dfBVZ = pd.merge(dfBZ, dfBV, left_on=['fk'], right_on=[
                     'pk'], suffixes=('_BZ', ''))
    
    #logger.debug("{0:s}dfBVZ: {1:s}".format(logStr,dfBVZ.to_string()))    

    if 'tk' in dfBV.columns.to_list():
        dfBVZ_tk = pd.merge(dfBZ, dfBV, left_on=['fk'], right_on=[
                            'tk'], suffixes=('_BZ', ''))

        if dfBVZ_tk.shape[0] > dfBVZ.shape[0]:
            #logger.debug("{0:s}BV: {1:s} BZ: {2:s}: BVZ-Resultat mit tk > als mit pk. tk-Resultat wird verwendet.".format(logStr, BV, BZ))
            dfBVZ = dfBVZ_tk
        elif dfBVZ_tk.shape[0] == dfBVZ.shape[0]:
            pass
        else:
            pass

    if dfBVZ.empty:
        pass
        #logger.debug("{0:s}BV: {1:s} BZ: {2:s}: BVZ-Resultat LEER ?!".format(logStr, BV, BZ))
    else:
        pass
        #logger.debug(
        #"{0:s}BVZ resultierende Zeilen: {1:d}".format(logStr, dfBVZ.shape[0]))            

    newCols = dfBVZ.columns.to_list()
    dfBVZ = dfBVZ.filter(items=[col for col in dfBV.columns.to_list(
    )]+[col for col in newCols if col not in dfBV.columns.to_list()])

    # CONT etc. #############################
    dfBVZ = fHelperCONTetc(dfBVZ, BV, BZ, dfViewModelle, dfCONT, pairType)
    
    dfBVZ=dfBVZ.reset_index(drop=True)

    if dfBVZ.empty:
        pass
        #logger.debug("{0:s}BV: {1:s} BZ: {2:s}: BVZ-Resultat LEER nach CONT etc?!".format(logStr, BV, BZ))
    else:
        pass
        #logger.debug(
        #"{0:s}BVZ resultierende Zeilen nach CONT etc.: {1:d}".format(logStr, dfBVZ.shape[0]))              
        
    #logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))
    return dfBV, dfBZ, dfBVZ


def fHelperCONTetc(dfBVZ, BV, BZ, dfViewModelle, dfCONT, pairType):

    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    #logger.debug("{0:s}{1:s}".format(logStr, 'Start.'))

    # CONT etc. #############################

    cols = dfBVZ.columns.to_list()

    if 'fkDE_BZ' in cols:
        dfOrig = dfBVZ
        df = pd.merge(dfBVZ, dfViewModelle, left_on='fkDE_BZ', right_on='fkBZ', suffixes=('', '_VMBZ'))
        if df.empty:
            #logger.debug("{0:s}{1:s}".format(
            #    logStr, 'fkDE_BZ ist vmtl. kein BZ-Schluessel, da es sich vmtl. um keine BZ-Eigenschaft handelt sondern um eine BV-Eigenschaft; Spalten werden umbenannt und es wird nach BV-DE gesucht ...'))
            renDct = {col: col.replace('_BZ', '_BV') for col in df.columns.to_list(
            ) if re.search('_BZ$', col) != None}
            dfOrig.rename(columns=renDct, inplace=True)

            if 'fkDE' in cols:
                #logger.debug("{0:s}{1:s}".format(
                #    logStr, 'fkDE ist auch in den Spalten ...'))

                df = pd.merge(dfOrig, dfViewModelle, left_on=['fkDE'], right_on=[
                              'fkBASIS'], suffixes=('', '_VMBASIS'), how='left')
                df = pd.merge(df, dfViewModelle, left_on=['fkDE'], right_on=[
                              'fkVARIANTE'], suffixes=('', '_VMVARIANTE'), how='left')

            else:
                logger.debug("{0:s}{1:s}".format(
                    logStr, 'fkDE ist nicht in den Spalten?!'))

    else:
        if 'fkDE' in cols:  
            df = pd.merge(dfBVZ, dfViewModelle, left_on=['fkDE'], right_on=[
                          'fkBASIS'], suffixes=('', '_VMBASIS'), how='left')
            df = pd.merge(df, dfViewModelle, left_on=['fkDE'], right_on=[
                          'fkVARIANTE'], suffixes=('', '_VMVARIANTE'), how='left')
        else:
            df = dfBVZ
        
    if 'fkCONT' in cols:
        dfTmp = df.copy(deep=True)
        df = pd.merge(df, dfCONT.add_suffix('_CONT'), left_on=['fkCONT'], right_on=['pk_CONT']
                      # ,suffixes=('','_CONT')
                      )
        if df.empty:
            df = pd.merge(dfTmp, dfCONT.add_suffix('_CONT'), left_on=['fkCONT'], right_on=['tk_CONT']  # !
                          # ,suffixes=('','_CONT')
                          )
        else:
            # pk-Menge ist nicht leer; aber ggf. werden ueber tk mehr/weitere gezogen
            dfTk = pd.merge(dfTmp, dfCONT.add_suffix('_CONT'), left_on=['fkCONT'], right_on=['tk_CONT']  # !
                            # ,suffixes=('','_CONT')
                            )
            rows, cols = df.shape
            rowsTk, colsTk = dfTk.shape
            dfXk = pd.concat([df, dfTk]).drop_duplicates()
            rowsXk, colsXk = dfXk.shape
            if rowsXk > rows:
                if rowsTk == rowsXk:
                    pass
                    #logger.debug(
                    #    "{:s}rowsXk: {:d} rowsTk: {:d} rowsPk: {:d} - pk-Menge ist nicht leer; aber tk zieht alle.".format(logStr, rowsXk, rowsTk, rows))
                else:
                    # tk zieht auch nicht die volle Menge
                    logger.debug(
                        "{:s}rowsXk: {:d} rowsTk: {:d} rowsPk: {:d} - pk-Menge ist nicht leer; aber ueber tk werden NICHT alle gezogen?!".format(logStr, rowsXk, rowsTk, rows))
                df = dfXk

    if pairType == '_ROWT':
        if 'ZEIT' in df.columns.to_list():
            df['lfdNrZEIT'] = df.sort_values(['pk', 'ZEIT'], ascending=True, na_position='first').groupby([
                'pk'])['ZEIT'].cumcount(ascending=True)+1
        else:
            logger.debug(
                "{0:s}pairType ROWT: df {1:s} hat keine Spalte ZEIT? Keine Sortierung nach Zeit.".format(logStr,BV))
            df = dfBVZ

    dfBVZ = df

    #logger.debug("{0:s}{1:s}".format(logStr, '_Done.'))
    return dfBVZ
