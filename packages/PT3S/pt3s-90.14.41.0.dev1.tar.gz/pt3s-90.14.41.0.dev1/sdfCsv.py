# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:21:15 2024

@author: wolters
"""

import logging
logger = logging.getLogger('PT3S') 

import sys

import re

import pandas as pd
import numpy as np

class SdfCsv():
    """Wrapper for a model defined by an SDF-CSV-File.
    """
    def __init__(self
                 ,csvFile='aSdfCsvFile.csv'
                 ,encoding='cp1252'
    ):
        """
        :param csvFile: a SDF-CSV-File
        :type csvFile: str
        :param encoding: encoding
        :type encoding: str    
                      
        .. note:: SIR 3S imports SDF-CSV-Files. However sometimes it is convenient to have a look at the original SDF-CSV-File content with Python. I.e. to explore the original hierarchical layer structure in comparison to the flat layer structure in the SIR 3S model. Or i.e. to check against the SIR 3S SDF-CSV-File import- and export-function result. In general, one can say that the SDF-CSV format for pipe network data (for pipe network models) is so widespread in Germany that it makes sense to have an SIR 3S affine function which maps the SDF-CSV-File to pandas dfs.
                   
            The returned object has the following structure:
        
                - dataFrames: dct with dfs
                - dataFrames['FEL']: a df with the definition of the columns of all types; i.e. 'KNO' is a type                
                - dataFrames['KNO']: a df with data for objects of type 'KNO'
                - dataFramesDesc: dct with descs; i.e. dataFramesDesc['KNO']: 'Knotendaten'
                
            The returned object has the following functions:

                - getHierarchicalLayernames: returns: {originalLayername:hierarchicalLayername, ...}                          
        """
        
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            self.csvFile=csvFile
            self.encoding=encoding
            self.dataFrames,self.dataFramesDesc=self.__readSdfCsvFile()                  
                                           
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise e
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))         

    def __readSdfCsvFile(self):
        """
        :return: dfs,dataFramesDesc              
        """
        
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug(f"{logStr}Start.") 
        
        try:
            dataFrames={}
            dataFramesDesc={}
        
            with open(self.csvFile, encoding=self.encoding) as f:
                csvLines = f.readlines()
            
            csvLineNumbersWithFEL=[idx for idx,csvLine in enumerate(csvLines) if re.search('^FEL',csvLine) != None]
            #csvLinesWithFEL=[csvLine for csvLine in csvLines if re.search('^FEL',csvLine) != None]
            
            dfFEL=pd.read_csv(self.csvFile
                ,encoding=self.encoding
                ,sep=';'
                ,header=None
                ,index_col=False
                ,names=['CTY','OTY','XTY','ANAME','ATYPE','ALENGTH','APRECISION','ADESC','AUNIT']
                ,dtype={'CTY':str,'OTY':str,'XTY':str,'ANAME':str,'ATYPE':str,'ALENGTH':int,'APRECISION':int,'ADESC':str,'ANUNIT':str}           
                ,skiprows = lambda x: x not in  csvLineNumbersWithFEL
                ,on_bad_lines='warn'
               )
            cols=dfFEL.columns.to_list()
            dfFEL['lineNumber']=csvLineNumbersWithFEL
            dfFEL=dfFEL.filter(items=['lineNumber']+cols,axis=1)
            
            #nrows=10
            
            def fGetDype(row):
            
                match row['ATYPE']:                                
                    case _:
                        return str
                    
            def fGetConverter(row):
            
                match row['ATYPE']:
                    
                    case 'C':
                        return None
                    
                    case 'N':
                        
                        match row['APRECISION']:
                            
                            case 0:
                                return str.strip
                            case _:
                                return str.strip                                    
                    case _:
                        return None
            
            for OTY in sorted(dfFEL['OTY'].unique()):
                
                if OTY !=  'PRO':
                    pass
                    #continue
                    
                logger.info(f"###{OTY}###")
                
                dfFELOTY=dfFEL[dfFEL['OTY']==OTY]
                
                if dfFELOTY.empty:
                    logger.debug(f"No definition for type: {OTY}?!")
                    continue
                
                #logger.debug(f"{dfFELOTY.describe()}")
                logger.debug(f"{dfFELOTY.to_string()}")
                logger.debug(f"{dfFELOTY['ANAME'].to_list()}")
                logger.debug(f"{dfFELOTY['ATYPE'].unique()}")
                
                #print(sorted(dfFELOTY['ANAME'].to_list()))
                
                dtype={row['ANAME']:fGetDype(row) for index,row in dfFELOTY.iterrows() }
                #converters={row['ANAME']:fGetConverter(row) for index,row in dfFELOTY.iterrows() }
                #converters={key:value for (key,value) in converters.items() if value != None}
                
                csvLineNumbersWithOTY=[idx for idx,csvLine in enumerate(csvLines) if re.search('^'+OTY,csvLine) != None]   
                
                if len(csvLineNumbersWithOTY)==0:
                    logger.debug(f"No data for type: {OTY}?!")
                    continue
                                            
                logger.debug(f"csvLineNumbersWithOTY[0]:{csvLineNumbersWithOTY[0]}")
                descLine=csvLines[csvLineNumbersWithOTY[0]-4].strip()
                if re.search('^REM',descLine) != None:                
                    dataFramesDesc[OTY]=descLine
                else:
                    dataFramesDesc[OTY]=f"probably wrong estimated Desc: {descLine}"
                                
                #ncsvLineNumbersWithOTY=[idx for idx in range(len(csvLines)) if idx not in csvLineNumbersWithOTY]
                dfOTY=pd.read_csv(self.csvFile
                            ,encoding=self.encoding
                            ,sep=';'
                            ,decimal=','
                            ,header=None
                            ,index_col=False
                            ,names= ['OTY']+dfFELOTY['ANAME'].to_list()  
                            ,dtype=dtype
                            #,converters=converters
                            ,skiprows = lambda x: x not in  csvLineNumbersWithOTY
                            ,on_bad_lines='warn'
                            #,engine='c'
                            #,nrows=nrows
                )
                cols=dfOTY.columns.to_list()
                dfOTY['lineNumber']=csvLineNumbersWithOTY#[:nrows]
                dfOTY=dfOTY.filter(items=['lineNumber']+cols,axis=1)
                #dfs[OTY]=dfOTY
                
                for index,row in dfFELOTY.iterrows():
                    
                    match row['ATYPE']:
            
                        case 'C':
                            pass
            
                        case 'N':
            
                            match row['APRECISION']:
            
                                case 0:
                                    try:                                                
                                        dfOTY[row['ANAME']]=dfOTY[row['ANAME']].str.strip().astype(np.int64,errors='ignore')                                                
                                    except Exception as e:
                                        logger.info(f"{OTY}:")
                                        logStrFinal="Exception: Line: {:d}: {!s:s}: {:s}".format(sys.exc_info()[-1].tb_lineno,type(e),str(e))
                                        logger.error(logStrFinal)    
                                        
                                case _:
                                    dfOTY[row['ANAME']]=dfOTY[row['ANAME']].str.replace(',','.').astype(float)
                                    
                                    
                        case _:
                            pass
                                    
                dataFrames[OTY]=dfOTY  
                
                
            dataFrames['FEL']=dfFEL
            dataFramesDesc['FEL']='type FEL: Feldbeschreibungen (type definitions)'
            return dataFrames,dataFramesDesc
                
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise e
            
        finally:
            logger.debug(f"{logStr}_Done.")     
            
    def getHierarchicalLayernames(self,sep='#'):
        """
        :return: {originalLayername:(hierarchicalLayername,[IDPTop,IDPLev1,...,ID]) ...}              
        """
        
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug(f"{logStr}Start.") 
        
        try:
            dct={}
            df=self.dataFrames['PRO'].copy(deep=True)
            
            uniqueTITELIndicator=df.groupby(by='TITEL').count()['lineNumber'].max()
            if uniqueTITELIndicator > 1:
                logger.info("TITEL not unique!")
                            
            df['PARENTID_']=df['PARENTID'].apply(lambda x: re.sub('^0+','',x.replace('$','').strip())).values
            def f(x):
                
                try:
                    ret = int(x)
                except:
                    if x == '':
                        ret=0
                    else:
                        ret = -1
                
                return ret   
            df['PARENTID_']=df['PARENTID_'].apply(lambda x: f(x))
            
            def fParentID(parentID,parentIDs):
                #logger.debug(f"parentID: {parentID} parentIDs: {parentIDs} ...")
                if parentID in [0,-1]: # exit
                    return
                else: # recurse   
                    for index, row in df.iterrows():
                        if row['ID']==parentID:
                            #logger.debug(f"parentID: {parentID} gefunden.")
                            parentIDs.append(row['ID'])
                            fParentID(row['PARENTID_'],parentIDs)
                            break            


            for index, row in df.iterrows():
                parentIDs=[]
                parentIDsRev=[]
                #logger.debug(f"Suchen nach Hierarchie für: {row['TITEL']} ID: {row['ID']} PARENTID: {row['PARENTID_']}")
                
                fParentID(row['PARENTID_'],parentIDs=parentIDs)
                #logger.debug(f"x parentIDs: {parentIDs}")
                
                layerName=''
                
                if len(parentIDs) > 0:                                        
                    parentIDsRev=parentIDs[::-1]                                                                               
                    for parentID in parentIDsRev: 
                        layerNameParent=df[df['ID']==parentID]['TITEL'].iloc[0]
                        if layerName=='':
                            layerName=layerNameParent
                        else:
                            layerName=layerName+sep+layerNameParent
                    
                    layerName=layerName+sep+row['TITEL']
                    #logger.debug(f"Hierarchie für: {row['TITEL']}: {layerName}")
                else:
                    layerName=row['TITEL']
                #logger.debug(f"hierarchischer Name für: {row['TITEL']}: {layerName}")
                
                if row['TITEL'] not in dct.keys():
                    pass
                else:
                    logger.info(f"TITEL not unique: {row['TITEL']}: hierarchicalLayername is set to hierarchicalLayername of lineNumber: {row['lineNumber']}")
                
                parentIDsRev.append(row['ID'])
                dct[row['TITEL']]=(layerName,parentIDsRev)
                
            return dct
           
                
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise e
            
        finally:
            logger.debug(f"{logStr}_Done.")     