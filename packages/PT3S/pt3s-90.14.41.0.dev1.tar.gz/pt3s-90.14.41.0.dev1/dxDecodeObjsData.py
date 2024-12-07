# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 17:12:49 2024

@author: wolters
"""

import os
import sys

import re

import logging

import pandas as pd

import numpy as np

import networkx as nx

# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context:','.')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 


class dxObjsDataError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def Layr(dx):
    """Returns a df with decoded V_LAYR-Content.

    Args:
        dx: Dx-Instance 
            used: dx.dataFrames['V_LAYR']
                
    Returns:
        df:
            one row per LAYR and OBJ
            
            LAYR:
            'pk'
           ,'tk'
           ,'LFDNR' (numeric)
           ,'NAME'
           
            LAYR-Info:
           ,'AnzDerObjekteInGruppe'
           ,'AnzDerObjekteDesTypsInGruppe'    
           
            OBJ:
           ,'TYPE'
           ,'ID'
           
            OBJ-Info:
           ,'NrDesObjektesDesTypsInGruppe'
           ,'NrDesObjektesInGruppe'
           ,'GruppenDesObjektsAnz'
           ,'GruppenDesObjektsNamen'       
    
    """
    
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
    
    try: 
        
        df=pd.DataFrame()
        
        V_LAYR=dx.dataFrames['V_LAYR']
        
        V_LAYR['OBJSd']=V_LAYR.apply(lambda row: row['OBJS'].decode('utf-8').split('\t') if row['OBJS'] != None else None ,axis=1)
                
        dfs=[]
        
        for index,row in V_LAYR[~pd.isnull(V_LAYR['OBJSd'])].sort_values(by=['LFDNR']).iterrows():
            
            #logger.debug("{0:s}LAYR: {1:s}:".format(logStr,row['NAME'])) 
            
            try:
                for x in row['OBJSd']:
                    
                    if x in [None,'']:
                        continue
                    
                    #logger.debug("{0:s}LAYR OBJd {1:s}:".format(logStr,x)) 
                    
                    try:
                        m=re.search('([A-Z]{4})~(\d{19})',x)
                        TYPE=m.group(1)
                        ID=m.group(2)        
                        
                        #logger.debug("{0:s}LAYR OBJd parsed: TYPE: {1:s} ID: {2:s}".format(logStr,TYPE,ID)) 
                        
                        
                        df=pd.DataFrame(data=np.array([[row['pk'],row['tk'],row['NAME'],row['LFDNR'],TYPE,ID]]),columns=['pk','tk','NAME','LFDNR','TYPE','ID'])
                        
                        #logger.debug("{0:s}LAYR OBJd parsed df: {1:s}".format(logStr,df.to_string())) 

                        dfs.append(df)
                        
                    except:
                        
                        continue
                    
            except:
                continue        
        
        df=pd.concat(dfs)
        
        df=df.reset_index(drop=True)
        
        
        df[['LFDNR']] = df[['LFDNR']].apply(pd.to_numeric)
        df=df.sort_values(by=['LFDNR','pk','tk','NAME','TYPE','ID'])
        
        #GruppenDesObjekts
        
        #Anz
        
        #Namen
        dfg=df.groupby(by=['TYPE','ID'])['NAME'].agg(list)           
        df=pd.merge(df,dfg,left_on=['TYPE','ID'],right_index=True,suffixes=('','_X'))
        df.rename(columns={'NAME_X':'GruppenDesObjektsNamen'},inplace=True)
        df['GruppenDesObjektsNamen']=df.apply(lambda row: sorted(row['GruppenDesObjektsNamen']),axis=1)
        #Anz
        df['GruppenDesObjektsAnz']=df.apply(lambda row: len(row['GruppenDesObjektsNamen']),axis=1)
        
        df=df.sort_values(by=['LFDNR','pk','tk','NAME','TYPE','ID'])
            
        df['NrDesObjektesDesTypsInGruppe']=df.groupby(by=['pk','tk','NAME','TYPE']).cumcount()+1
        df['NrDesObjektesInGruppe']=df.groupby(by=['pk','tk','NAME']).cumcount()+1
        
        
        dfg=df.groupby(by=['pk','tk','NAME'])[['NrDesObjektesInGruppe']].max()
        df=pd.merge(df,dfg,left_on=['pk','tk','NAME'],right_index=True,suffixes=('','_X'))
        df.rename(columns={'NrDesObjektesInGruppe_X':'AnzDerObjekteInGruppe'},inplace=True)
        df=df.sort_values(by=['LFDNR','pk','tk','NAME','TYPE','ID'])


        dfg=df.groupby(by=['pk','tk','NAME','TYPE'])[['NrDesObjektesDesTypsInGruppe']].max()
        df=pd.merge(df,dfg,left_on=['pk','tk','NAME','TYPE'],right_index=True,suffixes=('','_X'))
        df.rename(columns={'NrDesObjektesDesTypsInGruppe_X':'AnzDerObjekteDesTypsInGruppe'},inplace=True)
        df=df.sort_values(by=['LFDNR','pk','tk','NAME','TYPE','ID'])
        
        
        #df['AnzDesObjektesDesTypsInGruppe']=df[].max()
        #df['AnzDerObjekteInGruppe']=df.groupby(by=['pk','tk','NAME']).count()
        
        
        df=df.reset_index(drop=True)
        
        df=df[[
            'pk'
           ,'tk'
           ,'LFDNR'
           ,'NAME'
           ,'AnzDerObjekteInGruppe'
           ,'AnzDerObjekteDesTypsInGruppe'    
           ,'TYPE'
           ,'ID'
           ,'NrDesObjektesDesTypsInGruppe'
           ,'NrDesObjektesInGruppe'
           ,'GruppenDesObjektsAnz'
           ,'GruppenDesObjektsNamen'          
            ]]
            
     
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))          
        logger.debug(logStrFinal) 
        
                                                                          
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
        return df    
    
def Wblz(dx):
    """Returns a df with decoded V_WBLZ-Content.

    Args:
        dx: Dx-Instance 
            used: dx.dataFrames['V_WBLZ']
                
    Returns:
        df:
            one row per WBLZ and OBJ
            
            LAYR:
            'pk'
           ,'tk'
           
    
    """
    
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
    
    try: 
        
        df=pd.DataFrame()
        
        V_WBLZ=dx.dataFrames['V_WBLZ']
        
        V_WBLZ['OBJSd']=V_WBLZ.apply(lambda row: row['OBJS'].decode('utf-8').split('\t') if row['OBJS'] != None else None ,axis=1)
                
        dfs=[]
        
        for index,row in V_WBLZ[~pd.isnull(V_WBLZ['OBJSd'])].sort_values(by=['NAME']).iterrows():
            
            #logger.debug("{0:s}WBLZ: {1:s}:".format(logStr,row['NAME'])) 
            
            try:
                for x in row['OBJSd']:
                    
                    if x in [None,'']:
                        continue
                    
                    #logger.debug("{0:s}LAYR OBJd {1:s}:".format(logStr,x)) 
                    
                    try:
                        m=re.search('([A-Z]{4})~(\d{19})',x)
                        TYPE=m.group(1)
                        ID=m.group(2)        
                        
                        #logger.debug("{0:s}LAYR OBJd parsed: TYPE: {1:s} ID: {2:s}".format(logStr,TYPE,ID)) 
                        
                        
                        df=pd.DataFrame(data=np.array([[row['pk'],row['tk'],row['NAME'],row['BESCHREIBUNG'],TYPE,ID]]),columns=['pk','tk','NAME','BESCHREIBUNG','TYPE','ID'])
                        
                        #logger.debug("{0:s}LAYR OBJd parsed df: {1:s}".format(logStr,df.to_string())) 

                        dfs.append(df)
                        
                    except:
                        
                        continue
                    
            except:
                continue        
        
        
        if len(dfs)==0:            
            logStrFinal="{logStr:s}no WBLZs available ...".format(logStr=logStr)     
            logger.debug(logStrFinal) 
            #raise dxObjsDataError(logStrFinal)    
            
        else:
        
            df=pd.concat(dfs)
            
            df=df.sort_values(by=['NAME','pk','tk'])
            
            df=df.reset_index(drop=True)
            
            #WblzDesKnotens
            
            #Anz
            
            #Namen
            dfg=df.groupby(by=['ID'])['NAME'].agg(list)           
            df=pd.merge(df,dfg,left_on=['ID'],right_index=True,suffixes=('','_X'))
            df.rename(columns={'NAME_X':'BilanzenDesKnotensNamen'},inplace=True)
            df['BilanzenDesKnotensNamen']=df.apply(lambda row: sorted(row['BilanzenDesKnotensNamen']),axis=1)
            #Anz
            df['BilanzenDesKnotensAnz']=df.apply(lambda row: len(row['BilanzenDesKnotensNamen']),axis=1)        
            
    
            df=df.reset_index(drop=True)
            
            df=pd.merge(df,dx.dataFrames['V_BVZ_KNOT'],left_on='ID',right_on='tk',suffixes=('','_X')).filter(items=df.columns.to_list()+['NAME_X']).rename(columns={'NAME_X':'KNAM'})
          
            df=df[[
              'pk'
             ,'tk'        
             ,'NAME'
             
             #,'AnzDerObjekteInGruppe'
             #,'AnzDerObjekteDesTypsInGruppe'    
             
             ,'TYPE'
             ,'ID'
             ,'KNAM'
             
             #,'NrDesObjektesDesTypsInGruppe'
             #,'NrDesObjektesInGruppe'
             ,'BilanzenDesKnotensNamen'
             ,'BilanzenDesKnotensAnz'          
              ]]        
           
            
     
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))          
        logger.info(logStrFinal) 
        
                                                                          
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
        return df    
    
    pass

def Agsn(dx):
    """Returns a df with decoded and supplemented V_AGSN-Content.

    Args:
        dx: Dx-Instance 
            used: V_AGSN, V3_VBEL
                
    Returns:
        df:
            one row for AGSN and OBJ (edge)
            AGSN is the German abbreviation for longitudinal sections / cuts (defined in the SIR 3S model)
            
            OBJ:
                'Pos': Position of OBJ (of the edge) in AGSN starting with 0
                'TYPE' (of the edge)
                'ID' (of the edge)

            AGSN:
                'pk'
                'tk'
                'LFDNR' (numeric)
                'NAME'
                'XL':
                   0: everything
                   1: SL (the stuff before \n)
                   2: RL (the stuff after \n)     

            supplemented Cols:
                compNr: component-Number starting with 1
                nextNODE: nextNODE in cut-direction
    """
    
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
    
    try: 
        
        df=pd.DataFrame()
        
        df=dx.dataFrames['V_AGSN']
        
        df['OBJSDec']=df.apply(lambda row: row['OBJS'].decode('utf-8') if not pd.isnull(row['OBJS']) else None,axis=1)
        
        def fVLRL(OBJSDec,idx=0):    
            try:
                if pd.isnull(OBJSDec):
                    s=None
                else:        
                    l=OBJSDec.split('\n')
                    s=l[idx]
                    s=s.lstrip().rstrip()
            except: # Exception as e:
                s=None        
            finally:
                return s      
            
        df['OBJSDecSL']=df.apply(lambda row: fVLRL(row['OBJSDec'],0),axis=1) # vor \n
        df['OBJSDecRL']=df.apply(lambda row: fVLRL(row['OBJSDec'],1),axis=1) # nach \n
        
        def fOBJTypeOBJId(OBJSDec):        
            try:
                if pd.isnull(OBJSDec):
                    l=None
                else:
                    l=[i for i in re.findall(r"([A-Z]{4})~(\d+)",OBJSDec)]
            except: # Exception as e:
                l=None                
            finally:
                return l      
            
        df['OBJSDecLst']=df.apply(lambda row: fOBJTypeOBJId(row['OBJSDec']),axis=1) # alles
        df['OBJSDecLstSL']=df.apply(lambda row: fOBJTypeOBJId(row['OBJSDecSL']),axis=1) # VL
        df['OBJSDecLstRL']=df.apply(lambda row: fOBJTypeOBJId(row['OBJSDecRL']),axis=1) # RL
        
        dfAGSNs=[]
        for index,row in df.iterrows():
            pass
            try:
                if row['OBJSDecLst'] != None:
                    
                    
                    dfAGSN=pd.DataFrame(row['OBJSDecLst'],columns =['TYPE','ID']).reset_index().rename(columns={'index':'Pos'})
                    dfAGSN['pk']=row['pk']
                    dfAGSN['tk']=row['tk']
                    dfAGSN['NAME']=row['NAME']
                    dfAGSN['LFDNR']=row['LFDNR']
                    dfAGSN['XL']=0
                    
                    dfAGSNs.append(dfAGSN)
                    
                    if row['OBJSDecLstSL'] != None:
                        dfAGSN=pd.DataFrame(row['OBJSDecLstSL'],columns =['TYPE','ID']).reset_index().rename(columns={'index':'Pos'})
                        dfAGSN['pk']=row['pk']
                        dfAGSN['tk']=row['tk']
                        dfAGSN['NAME']=row['NAME']
                        dfAGSN['LFDNR']=row['LFDNR']
                        dfAGSN['XL']=1     
        
                        dfAGSNs.append(dfAGSN)
                        
                    if row['OBJSDecLstRL'] != None:
                        dfAGSN=pd.DataFrame(row['OBJSDecLstRL'],columns =['TYPE','ID']).reset_index().rename(columns={'index':'Pos'})
                        dfAGSN['pk']=row['pk']
                        dfAGSN['tk']=row['tk']
                        dfAGSN['NAME']=row['NAME']
                        dfAGSN['LFDNR']=row['LFDNR']
                        dfAGSN['XL']=2     
        
                        dfAGSNs.append(dfAGSN)                
                                                        
            except Exception as e:
                pass
                print(e)
                
            finally:
                pass        
        
        if len(dfAGSNs)>0:
            df=pd.concat(dfAGSNs).reset_index(drop=True)
            
            df[['LFDNR']] = df[['LFDNR']].apply(pd.to_numeric)
            
            # supplement AGSN-Data
            df['compNr']=None
            df['nextNODE']=None
            
            df=pd.merge(df
               ,dx.dataFrames['V3_VBEL']           
               ,left_on=['TYPE','ID']  
               ,right_index=True 
               ,suffixes=('', '_VBEL')
            )
            
            df.sort_values(by=['LFDNR','pk','XL','Pos'],inplace=True)
            df.reset_index(inplace=True)
            
            # damit die SIR 3S Elementrichtung nach (ungerichteter) Graphenbildung in NetworkX im dataDict verfuegbar ist
            df['SIR3S_i']=df['NAME_i']
            df['SIR3S_k']=df['NAME_k']        
            
            # damit neue df-Spalten per .loc aus NetworkX im dataDict-Daten befüllbar sind
            df['index']=df.index
            
            # Schnittknotensequenz ermitteln
            
            for nr in df['LFDNR'].unique():                
                    
                    # ueber alle Layer
                    for ly in df[df['LFDNR']==nr]['XL'].unique():                                        
    
                        dfSchnitt=df[(df['LFDNR']==nr) & (df['XL']==ly)]                                      
                        #logger.debug("{0:s}Schnitt: {1:s} Nr: {2:s} Layer: {3:s}".format(logStr
                        #                                                       ,str(dfSchnitt['NAME'].iloc[0])
                        #                                                       ,str(dfSchnitt['LFDNR'].iloc[0])
                        #                                                       ,str(dfSchnitt['XL'].iloc[0])
                        #                                                      )) 
                        
                        dfSchnitt=dfSchnitt.reset_index() 
                    
                        GSchnitt=nx.from_pandas_edgelist(dfSchnitt, source='NAME_i', target='NAME_k', edge_attr=True,create_using=nx.MultiGraph())
                        
                        # ueber alle zusammenhaengenen Komponenten
                        iComp=0
                        for comp in nx.connected_components(GSchnitt):
                            iComp+=1
    
                            #logger.debug("{0:s}CompNr.: {1:s}".format(logStr,str(iComp))) 
                            
                            # Graph der Komponente
                            GSchnittComp=GSchnitt.subgraph(comp)
                            
                            GSchnittEdgeLst=sorted(GSchnittComp.edges(data=True), key=lambda x: x[2]['Pos'])                        
                            
                            # erste und letzte Kante lt. Schnittdefinition
                            u,v, datadict = GSchnittEdgeLst[0]
                            sourceKi=u
                            sourceKk=v
                            
                            u,v, datadict = GSchnittEdgeLst[-1]
                            targetKi=u
                            targetKk=v                        
                                                                              
                            #logger.debug("{0:s}First: i: {1:s} k:{2:s} ".format(logStr,sourceKi,sourceKk)) 
                            #logger.debug("{0:s}Last: i: {1:s} k:{2:s} ".format(logStr,targetKi,targetKk)) 
                            
                            # Pfad zwischen den Knoten der ersten und letzten Kante (4 Möglichkeiten)
                            # der laengste Pfad geht unabhängig von der Kantenrichtung vom ersten bis zum letzten Knoten des Schnittes
                            nlComp=nx.shortest_path(GSchnittComp,sourceKi,targetKk)
                            nlCompTmp=nx.shortest_path(GSchnittComp,sourceKk,targetKk)
                            if len(nlCompTmp)>len(nlComp):
                                nlComp=nlCompTmp
                            nlCompTmp=nx.shortest_path(GSchnittComp,sourceKi,targetKi)
                            if len(nlCompTmp)>len(nlComp):
                                nlComp=nlCompTmp
                            nlCompTmp=nx.shortest_path(GSchnittComp,sourceKk,targetKi)
                            if len(nlCompTmp)>len(nlComp):
                                nlComp=nlCompTmp                                
                            #logger.debug("{0:s}Pfad: Start: {1:s} > Ende: {2:s}".format(logStr,nlComp[0],nlComp[-1]))                         
                            
                            # Graphen zur Schnittknotensequenz 
                            GSchnittCompSP=GSchnittComp.subgraph(nlComp)
                            
                            # index-Liste der Kanten der Schnittknotensequenz 
                            idxLst=[]                        
                            
                            for u,v, datadict in sorted(GSchnittCompSP.edges(data=True), key=lambda x: x[2]['Pos']):              
                                idxLst.append(datadict['index'])
                                # SP-Kanten Ausgabe
                                                      
                            compNr=np.empty(GSchnittCompSP.number_of_edges(),dtype=int) 
                            compNr.fill(iComp)
                            
                            df.loc[idxLst,'compNr']=compNr                        
                            df.loc[idxLst,'nextNODE']=nlComp[1:]  
                                                                                            
            df=df[[
                    'Pos'
                   ,'TYPE'
                   ,'ID'
    
    
                   ,'pk'
                   ,'tk'
                   ,'LFDNR' 
                   ,'NAME'
                   ,'XL'            
                
                   ,'compNr' 
                   ,'nextNODE'                    
            ]]
        
        return df
                                                                                       
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))          
        logger.debug(logStrFinal) 
        raise
                                                                          
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))               
    
def setLayerContentTo(layerName
                     ,m
                     ,df):
    """
    layerName: Layer to update (Layer content is set to df's TYPE and ID)
    m: m.dfLAYR and m.dx.update are used
    df: cols TYPE and ID are used
    """
    
    
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
    
    try: 
        
        xk=m.dfLAYR[m.dfLAYR['NAME'].isin([layerName])]['tk'].iloc[0]
       
        dfUpd=df.copy(deep=True)
        
        dfUpd['table']='LAYR'
        dfUpd['attrib']='OBJS'
        dfUpd['attribValue']=dfUpd.apply(lambda row: "{:s}~{:s}\t".format(row['TYPE'],row['ID']).encode('utf-8'),axis=1)
        dfUpd['xk']='tk'
        dfUpd['xkValue']=xk    
        
        dfUpd2=dfUpd.groupby(by=['xkValue']).agg({'xkValue': 'first'
                                           ,'table': 'first'
                                           ,'attrib': 'first'
                                           ,'xk': 'first'
                                           , 'attribValue': 'sum'}).reset_index(drop=True)
        dfUpd2['attribValue']=dfUpd2['attribValue'].apply(lambda x: x.rstrip())
          
        m.dx.update(dfUpd2)            
 
                         
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))          
        logger.warning(logStrFinal) 
        
                                                                          
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
        return       
    
    
    
    
    

    
