import logging
import os
import sys

import pandas as pd
import geopandas
import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import matplotlib

from matplotlib import cm
from matplotlib.colors import ListedColormap
import matplotlib.font_manager as font_manager
import matplotlib.patheffects as path_effects

import contextily as cx

import matplotlib.patches as mpatches

logger = logging.getLogger('PT3S')  

def cmpTIMEs( df=pd.DataFrame() # a V3sErg=dx.MxAdd(mx) df i.e. v3sKNOT=V3sErg['V3_KNOT']
             ,col='KNOT~*~*~*~PH'
             ,timeLstA=[]
             ,timeLstB=[]             
             ,newColNamesBase=[]):

    """
    compares the value of col between 2 TIMEs (B-A) and creates new cols    
    """

    pass
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

    try:
        for timeA,timeB,newColNameBase in zip(timeLstA,timeLstB,newColNamesBase):

             ergCol_timeA=('TIME'
            ,col
            ,pd.Timestamp(timeA.strftime('%Y-%m-%d %X.%f'))
            ,pd.Timestamp(timeA.strftime('%Y-%m-%d %X.%f'))
            )

             ergCol_timeB=('TIME'
            ,col
            ,pd.Timestamp(timeB.strftime('%Y-%m-%d %X.%f'))
            ,pd.Timestamp(timeB.strftime('%Y-%m-%d %X.%f'))
            )

             if ergCol_timeA not in df.columns:               
                logger.warning("{:s}col: {:s} nicht vorhanden.".format(logStr,col)) 
                continue
             if ergCol_timeB not in df.columns:
                logger.warning("{:s}col: {:s} nicht vorhanden.".format(logStr,col)) 
                continue
             
             df[newColNameBase+'_DIF']=df.apply(lambda row: row[ergCol_timeB]-row[ergCol_timeA] ,axis=1)    
             df[newColNameBase+'_DIFAbs']=df.apply(lambda row: math.fabs(row[newColNameBase+'_DIF']) ,axis=1)    
         
         
    except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise e         
    finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

def pNFD_FW(                   
                 ax=None
                ,axTitle=None
                
                ,gdf_ROHR=geopandas.GeoDataFrame()      
                ,gdf_FWVB=geopandas.GeoDataFrame()         
                ,gdf_KNOT=geopandas.GeoDataFrame()                                 
             
                # Layout ROHR
            
                # Sachdatum
                ,attr_colors_ROHR_Sach = 'DI' 
                ,attr_colors_ROHR_Sach_zOrder = 3
                ,colors_ROHR_Sach = ['lightgray', 'dimgray']                
                ,norm_min_ROHR_Sach = None 
                ,norm_max_ROHR_Sach = None

                ,attr_lws_ROHR_Sach='DI'                     
                ,attr_colors_ROHR_Sach_patches_fmt="DN (Innen) {:4.0f}"
                ,attr_colors_ROHR_Sach_patchValues=None
                
                # Breitenfaktor (fuer Sach- und Ergebnisdaten)
                ,fac_lws_ROHR=5. 

                # Ergebnis: Farbe
                ,attr_colors_ROHR_Erg='QMAVAbs'#None 
                ,attr_colors_ROHR_Erg_zOrder = 4 
                ,colors_ROHR_Erg = ['darkgreen','magenta']
                ,norm_min_ROHR_Erg = None 
                ,norm_max_ROHR_Erg = None            
                ,attr_colors_ROHR_Erg_patches_fmt="Q (abs.) {:4.0f} t/h"
                ,attr_colors_ROHR_Erg_patchValues=None
                
                                
                ,query_ROHR_Erg=None #'{:s} > 1.'.format(attr_colors_ROHR_Erg)
                # wenn angegeben, werden nur Ergebnisse von Rohren geplottet die dem query entsprechen
                                
                # Ergebnis: Breite: Standard: so wie die Sachdaten (diese werden dann komplett ueberzeichnet) ...
                ,lws_ROHR_Erg_Sach=True
                # andernfalls richtet sich die Breite nach dem Ergebnisattribut; es ergeben sich _dann in absteigender Richtung duennere oder dickere Breiten als bei den Sachdaten 
                # _Bsp. Sach DI und Erg QAbs: der max. DN und der max. Fluss werden mitderselben Breite gezeichnet; darunter ergeben sich unterschiedliche Breiten; DN i.d.R. breiter als Fluss
                ,fac_lws_ROHR_Erg=None # nur wirksam bei lws_ROHR_Erg_Sach=False; dann Standard fac_lws_ROHR  
            

                # Layout FWVB
            
                # Sachdatum
                ,attr_colors_FWVB_Sach='W0'
                ,attr_colors_FWVB_Sach_zOrder = 1
                ,attr_colors_FWVB_Sach_patches_fmt="W {:4.0f} kW"        
                ,attr_colors_FWVB_Sach_patchValues=None
                ,colors_FWVB_Sach = ['oldlace', 'orange'] 
                ,norm_min_FWVB_Sach = None 
                ,norm_max_FWVB_Sach = None            
            
                ,attr_ms_FWVB_Sach='W0' 
                ,fac_ms_FWVB=None # fac_ms_KNOT oder 8000.  wenn beides undefiniert

                # Ergebnis: Farbe
                ,attr_colors_FWVB_Erg='QM'#None 
                ,attr_colors_FWVB_Erg_zOrder = 2
                ,attr_colors_FWVB_Erg_patches_fmt="dp {:4.1f} bar"     
                ,attr_colors_FWVB_Erg_patchValues = None
                ,attr_colors_FWVB_ErgNeg_patches_fmt="dp -{:4.1f} bar"                     
                ,colors_FWVB_Erg = ['aquamarine','teal'] 
                ,norm_min_FWVB_Erg = None 
                ,norm_max_FWVB_Erg = None         
                
                # Ergebnis: Groesse: Standard: -1
                ,ms_FWVB_Erg=-1
                # -2: konst. Groesse 
                # -1: Groesse so wie die Sachdaten (diese werden dann komplett ueberzeichnet) 
                #       sind die Sachdaten nicht angefordert dasselbe Ergebnis wie ms_FWVB_Erg=0
                #  0: Groesse nach Ergebnisdaten (bei dp als Erg und W0 als Sach fuehrt dies zu vielen Überzeichnungen)
                # >0: Prozent (1=100%): Groesse nach Ergebnisdaten, aber nur max. ms_FWVB_Erg-Prozent der Sachdatengroesse 
                #               dies führt bei ]0;1[ dazu, dass die Sachdatenannotation immer sichtbar bleibt

                ,colors_FWVB_ErgNeg = ['lightskyblue','royalblue'] # ['aquamarine','skyblue']
                # wenn nicht None, dann werden negative Werte mit dieser Farbe gezeichnet; beide Farbskalen (die dann pos. und diese neg.) werden voll ausgenutzt
                # die Groesse erstreckt sich ueber den gesamten Wertebereich d.h. z.B. -.25 ist so gross wie +.25                

            
                # Layout NODES (KNOTen)
                ,attr_colors_KNOT_Erg=None 
                ,attr_colors_KNOT_Erg_patches_fmt="pDiff +{:4.2f} bar"        
                ,attr_colors_KNOT_ErgNeg_patches_fmt="pDiff -{:4.2f} bar"  
                ,attr_colors_KNOT_Erg_patchValues=None                         
                ,colors_KNOT_Erg = ['yellow','red']
                ,marker_KNOT_Erg='.'
                ,norm_min_KNOT_Erg = None 
                ,norm_max_KNOT_Erg = None  
                
                ,size_min_KNOT_Erg=None      
                ,size_max_KNOT_Erg=None  
                
                ,attr_colors_KNOT_Erg_zOrder=5

                ,colors_KNOT_ErgNeg = ['yellowgreen','sienna']
                # wenn nicht None, dann werden negative Werte mit dieser Farbe gezeichnet
                # norm_max_KNOT_Erg nicht vorgegeben:
                #   beide Farbskalen (die pos. und diese neg.) werden voll ausgenutzt
                #   die Groesse erstreckt sich ueber den Absolutwert d.h. z.B. -.25 ist so gross wie +.25 

                ,fac_ms_KNOT = None  # fac_ms_FWVB oder 8000.  wenn beides undefiniert

                # Layout Karte
                ,MapOn=False
                ,LabelsOnTop = False                               
                ,Map_resolution = 15

                ):
        """
        Plots data from GeoDataFrames with extensive customization options.
        
        Parameters:
            - ax (matplotlib.axes.Axes, optional): The axis on which to plot. Default is None.
            - axTitle (str, optional): Title for the axis. Default is None.
            - gdf_ROHR (geopandas.GeoDataFrame, optional): GeoDataFrame for ROHR data. Default is an empty GeoDataFrame.
            - gdf_FWVB (geopandas.GeoDataFrame, optional): GeoDataFrame for FWVB data. Default is an empty GeoDataFrame.
            - gdf_KNOT (geopandas.GeoDataFrame, optional): GeoDataFrame for KNOT data. Default is an empty GeoDataFrame.
        
        Sach (Static Data) Parameters:
            - attr_colors_ROHR_Sach (str, optional): Attribute for ROHR Sach colors. Default is 'DI'.
            - attr_colors_FWVB_Sach (str, optional): Attribute for FWVB Sach colors. Default is 'W0'.
            - attr_colors_ROHR_Sach_zOrder (int, optional): Z-order for ROHR Sach colors. Default is 3.
            - attr_colors_FWVB_Sach_zOrder (int, optional): Z-order for FWVB Sach colors. Default is 1.
            - colors_ROHR_Sach (list, optional): Colors for ROHR Sach. Default is ['lightgray', 'dimgray'].
            - colors_FWVB_Sach (list, optional): Colors for FWVB Sach. Default is ['oldlace', 'orange'].
            - norm_min_ROHR_Sach (float, optional): Minimum normalization value for ROHR Sach. Default is None.
            - norm_min_FWVB_Sach (float, optional): Minimum normalization value for FWVB Sach. Default is None.
            - norm_max_ROHR_Sach (float, optional): Maximum normalization value for ROHR Sach. Default is None.
            - norm_max_FWVB_Sach (float, optional): Maximum normalization value for FWVB Sach. Default is None.
            - attr_lws_ROHR_Sach (str, optional): Attribute for ROHR Sach line widths. Default is 'DI'.
            - attr_ms_FWVB_Sach (str, optional): Attribute for FWVB Sach marker sizes. Default is 'W0'.
            - attr_colors_ROHR_Sach_patches_fmt (str, optional): Format for ROHR Sach patches. Default is "DN (Innen) {:4.0f}".
            - attr_colors_FWVB_Sach_patches_fmt (str, optional): Format for FWVB Sach patches. Default is "W {:4.0f} kW".
            - attr_colors_ROHR_Sach_patchValues (list, optional): Values for ROHR Sach patches. Default is None.
            - attr_colors_FWVB_Sach_patchValues (list, optional): Values for FWVB Sach patches. Default is None.
            - fac_lws_ROHR (float, optional): Factor for ROHR line widths. Default is 5.0.
            - fac_ms_FWVB (float, optional): Factor for FWVB marker sizes. Default is None.
        
        Erg (Result Data) Parameters:
            - attr_colors_ROHR_Erg (str, optional): Attribute for ROHR Erg colors. Default is 'QMAVAbs'.
            - attr_colors_FWVB_Erg (str, optional): Attribute for FWVB Erg colors. Default is 'QM'.
            - attr_colors_ROHR_Erg_zOrder (int, optional): Z-order for ROHR Erg colors. Default is 4.
            - attr_colors_FWVB_Erg_zOrder (int, optional): Z-order for FWVB Erg colors. Default is 2.
            - colors_ROHR_Erg (list, optional): Colors for ROHR Erg. Default is ['darkgreen', 'magenta'].
            - colors_FWVB_Erg (list, optional): Colors for FWVB Erg. Default is ['aquamarine', 'teal'].
            - norm_min_ROHR_Erg (float, optional): Minimum normalization value for ROHR Erg. Default is None.
            - norm_min_FWVB_Erg (float, optional): Minimum normalization value for FWVB Erg. Default is None.
            - norm_max_ROHR_Erg (float, optional): Maximum normalization value for ROHR Erg. Default is None.
            - norm_max_FWVB_Erg (float, optional): Maximum normalization value for FWVB Erg. Default is None.
            - attr_colors_ROHR_Erg_patches_fmt (str, optional): Format for ROHR Erg patches. Default is "Q (abs.) {:4.0f} t/h".
            - attr_colors_FWVB_Erg_patches_fmt (str, optional): Format for FWVB Erg patches. Default is "dp {:4.1f} bar".
            - attr_colors_ROHR_Erg_patchValues (list, optional): Values for ROHR Erg patches. Default is None.
            - attr_colors_FWVB_Erg_patchValues (list, optional): Values for FWVB Erg patches. Default is None.
            - query_ROHR_Erg (str, optional): Query for ROHR Erg. Default is None.
            - lws_ROHR_Erg_Sach (bool, optional): Line width for ROHR Erg Sach. Default is True.
            - ms_FWVB_Erg (int, optional): Marker size for FWVB Erg. Default is -1.
            - fac_lws_ROHR_Erg (float, optional): Factor for ROHR Erg line widths. Default is None.
            - colors_FWVB_ErgNeg (list, optional): Colors for FWVB Erg negative values. Default is ['lightskyblue', 'royalblue'].
        
        Unique Parameters for KNOT and Map:
            - attr_colors_KNOT_Erg (str, optional): Attribute for KNOT Erg colors. Default is None.
            - attr_colors_KNOT_Erg_patches_fmt (str, optional): Format for KNOT Erg patches. Default is "pDiff +{:4.2f} bar".
            - attr_colors_KNOT_ErgNeg_patches_fmt (str, optional): Format for KNOT Erg negative patches. Default is "pDiff -{:4.2f} bar".
            - attr_colors_KNOT_Erg_patchValues (list, optional): Values for KNOT Erg patches. Default is None.
            - colors_KNOT_Erg (list, optional): Colors for KNOT Erg. Default is ['yellow', 'red'].
            - marker_KNOT_Erg (str, optional): Marker for KNOT Erg. Default is '.'.
            - norm_min_KNOT_Erg (float, optional): Minimum normalization value for KNOT Erg. Default is None.
            - norm_max_KNOT_Erg (float, optional): Maximum normalization value for KNOT Erg. Default is None.
            - size_min_KNOT_Erg (float, optional): Minimum size for KNOT Erg. Default is None.
            - size_max_KNOT_Erg (float, optional): Maximum size for KNOT Erg. Default is None.
            - attr_colors_KNOT_Erg_zOrder (int, optional): Z-order for KNOT Erg colors. Default is 5.
            - colors_KNOT_ErgNeg (list, optional): Colors for KNOT Erg negative values. Default is ['yellowgreen', 'sienna'].
            - fac_ms_KNOT (float, optional): Factor for KNOT marker sizes. Default is None.
            - MapOn (bool, optional): Whether to add a basemap. Default is False.
            - LabelsOnTop (bool, optional): Whether to place labels on top of the basemap. Default is False.
            - Map_resolution (int, optional): Resolution for the basemap. Default is 15.
        
        Returns:
            tuple: A tuple containing patches for ROHR Sach, ROHR Erg, FWVB Sach, FWVB Erg, and KNOT Erg.
        """
   
        logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 

        try:
            
            attr_colors_ROHR_Sach_patches=None
            attr_colors_ROHR_Erg_patches=None
            attr_colors_FWVB_Sach_patches=None
            attr_colors_FWVB_Erg_patches=None
            attr_colors_KNOT_Erg_patches=None
           
            if ax == None:
                ax = plt.gca()

            ### ROHRe ###
        
            attr_colors_ROHR_Sach_patches=[]
            attr_colors_ROHR_Erg_patches=[]       
            if not gdf_ROHR.empty:        
        
        
                # Erstellen der Colormap 
                cmap_ROHR = matplotlib.colors.LinearSegmentedColormap.from_list('cmap_ROHR', colors_ROHR_Sach, N = 256)        
            
                # Normierung fuer Colormap
                if norm_min_ROHR_Sach == None:            
                    norm_min_ROHR_Sach=gdf_ROHR[attr_colors_ROHR_Sach].min()
                if norm_max_ROHR_Sach == None:
                    norm_max_ROHR_Sach=gdf_ROHR[attr_colors_ROHR_Sach].max()
                    
                norm_diff_ROHR_Sach=norm_max_ROHR_Sach-norm_min_ROHR_Sach
                
                if norm_diff_ROHR_Sach < 0.01:
                    norm_min_ROHR_Sach=0.99*norm_max_ROHR_Sach
                    norm_diff_ROHR_Sach=norm_max_ROHR_Sach-norm_min_ROHR_Sach
                                
                logger.debug("{0:s}norm_min_ROHR_Sach: {1:10.2f} norm_max_ROHR_Sach: {2:10.2f}".format(logStr,norm_min_ROHR_Sach,norm_max_ROHR_Sach)) 
                                
                norm_ROHR_color = plt.Normalize(vmin=norm_min_ROHR_Sach, vmax=norm_max_ROHR_Sach) 
                                
                #logger.debug("{0:s}norm_ROHR_color(gdf_ROHR[attr_lws_ROHR_Sach]) * fac_lws_ROHR: {1:s}".format(logStr,str(norm_ROHR_color(gdf_ROHR[attr_lws_ROHR_Sach]) * fac_lws_ROHR))) 
                
                # Plotten ROHRe
                logger.debug(f"{logStr} Plotten ROHRe: gdf_ROHR.shape[0]: {gdf_ROHR.shape[0]}")

                for index,row in (gdf_ROHR.iterrows()):
                    pass
                    #logger.debug(f"{logStr} fuer Plot vorgesehen: ROHR mit NAME_i {row['NAME_i']} NAME_k {row['NAME_k']} tk {row['tk']}")

                gdf_ROHR.plot(ax = ax
                             ,zorder = attr_colors_ROHR_Sach_zOrder
                             ,linewidth = norm_ROHR_color(gdf_ROHR[attr_lws_ROHR_Sach].astype(float)) * fac_lws_ROHR
                             # wg. astype: ufunc 'isnan' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''
                             ,color = cmap_ROHR(norm_ROHR_color(gdf_ROHR[attr_colors_ROHR_Sach].astype(float)))
                             ,path_effects=[path_effects.Stroke(capstyle="round")]
                             )
            
                if attr_colors_ROHR_Sach_patchValues == None:
                     attr_colors_ROHR_Sach_patchValues=np.arange(norm_min_ROHR_Sach,norm_max_ROHR_Sach+1,norm_diff_ROHR_Sach/4)                 
                attr_colors_ROHR_Sach_patches = [ mpatches.Patch(color=cmap_ROHR(norm_ROHR_color(value)), label=attr_colors_ROHR_Sach_patches_fmt.format(value) ) 
                                                 for value in attr_colors_ROHR_Sach_patchValues]        
            
                    
                if attr_colors_ROHR_Erg != None:
                    
                    # Erstellen der Colormap 
                    cmap_ROHRErg = matplotlib.colors.LinearSegmentedColormap.from_list('cmap_ROHRErg', colors_ROHR_Erg, N = 256)     
                
                    # Normierung fuer Colormap
                    if norm_min_ROHR_Erg == None:            
                        norm_min_ROHR_Erg=gdf_ROHR[attr_colors_ROHR_Erg].min()    
                    if norm_max_ROHR_Erg == None:            
                        norm_max_ROHR_Erg=gdf_ROHR[attr_colors_ROHR_Erg].max()
                    norm_ROHRErg_color = plt.Normalize(vmin=norm_min_ROHR_Erg, vmax=norm_max_ROHR_Erg)       
                    norm_diff_ROHR_Erg=norm_max_ROHR_Erg-norm_min_ROHR_Erg
                
                    # Breite
                    if lws_ROHR_Erg_Sach:            
                        attr_lws_ROHR_Erg=attr_colors_ROHR_Sach
                        norm_ROHR_lws_Erg=norm_ROHR_color
                        fac_lws_ROHR_Erg=fac_lws_ROHR
                    else:
                        attr_lws_ROHR_Erg=attr_colors_ROHR_Erg
                        norm_ROHR_lws_Erg=norm_ROHRErg_color
                        
                        if fac_lws_ROHR_Erg == None:
                            fac_lws_ROHR_Erg=fac_lws_ROHR
                    
                    if query_ROHR_Erg != None:
                        df=gdf_ROHR.query(query_ROHR_Erg)
                    else:
                        df=gdf_ROHR
                    # große ueber kleine zeichnen
                    df=df.sort_values(by=[attr_colors_ROHR_Erg],ascending=True)
            
                    df.plot(ax = ax
                             ,zorder = attr_colors_ROHR_Erg_zOrder
                             ,linewidth = norm_ROHR_lws_Erg(df[attr_lws_ROHR_Erg]) * fac_lws_ROHR_Erg
                             ,color = cmap_ROHRErg(norm_ROHRErg_color(df[attr_colors_ROHR_Erg]))
                             ,path_effects=[path_effects.Stroke(capstyle="round")]
                             )       
                    
                    
                    # Legendeneinräge
                                 
                    if attr_colors_ROHR_Erg_patchValues == None:
                         attr_colors_ROHR_Erg_patchValues=np.arange(norm_min_ROHR_Erg,norm_max_ROHR_Erg+1,norm_diff_ROHR_Erg/4)                 
                    attr_colors_ROHR_Erg_patches = [ mpatches.Patch(color=cmap_ROHRErg(norm_ROHRErg_color(value)), label=attr_colors_ROHR_Erg_patches_fmt.format(value) ) 
                                                     for value in attr_colors_ROHR_Erg_patchValues]                                                                                                                                 
                                                                                                                              
            
            ### FWVBe ###
            attr_colors_FWVB_Sach_patches=[]
            attr_colors_FWVB_Erg_patches=[]       
            if not gdf_FWVB.empty:

                # Groessenfaktor
                if fac_ms_FWVB == None:
                    if fac_ms_KNOT != None:
                        fac_ms_FWVB=fac_ms_KNOT
                    else:
                        fac_ms_FWVB=8000.
                        
                        
                logger.debug("{0:s}fac_ms_FWVB: {1:10.2f}".format(logStr,fac_ms_FWVB)) 

                #attr_colors_FWVB_Sach_patches=[]
                if attr_colors_FWVB_Sach != None:

                    # Erstellen der Colormap
                    cmap_FWVB = matplotlib.colors.LinearSegmentedColormap.from_list('cmap_FWVB', colors_FWVB_Sach, N = 256)        

                    # Normierung fuer Colormap
                    if norm_min_FWVB_Sach == None:            
                        norm_min_FWVB_Sach=gdf_FWVB[attr_colors_FWVB_Sach].min()
                    if norm_max_FWVB_Sach == None:
                        norm_max_FWVB_Sach=gdf_FWVB[attr_colors_FWVB_Sach].max()
                        
                    #norm_FWVB_color = plt.Normalize(vmin=norm_min_FWVB_Sach, vmax=norm_max_FWVB_Sach)
                    # Werte außerhalb vmin, vmax erhalten ohne clip Werte < 0 > 1 und damit (bei Wert <= 0) keine Darstellung wenn die Normierung auch fuer die Groesse verwendet wird
                    norm_diff_FWVB_Sach=norm_max_FWVB_Sach-norm_min_FWVB_Sach
                    
                    if norm_diff_FWVB_Sach < 0.01:
                        norm_min_FWVB_Sach=0.99*norm_max_FWVB_Sach
                        norm_diff_FWVB_Sach=norm_max_FWVB_Sach-norm_min_FWVB_Sach      
                        
                        
                    logger.debug("{0:s}norm_min_FWVB_Sach: {1:10.2f} norm_max_FWVB_Sach: {2:10.2f}".format(logStr,norm_min_FWVB_Sach,norm_max_FWVB_Sach)) 
                    norm_FWVB_color = plt.Normalize(vmin=norm_min_FWVB_Sach, vmax=norm_max_FWVB_Sach)                    
                    
                    logger.debug("{0:s}ms_min_FWVB_Sach: {1:10.2f} ms_max_FWVB_Sach: {2:10.2f}".format(logStr
                                                                                                         ,norm_FWVB_color(gdf_FWVB[attr_ms_FWVB_Sach].min())
                                                                                                         ,norm_FWVB_color(gdf_FWVB[attr_ms_FWVB_Sach].max())
                                 )) 
                
                    # Plotten FWVB
                    gdf_FWVB.plot(ax = ax
                                ,zorder = attr_colors_FWVB_Sach_zOrder 
                                ,marker = '.'
                                ,markersize = norm_FWVB_color(gdf_FWVB[attr_ms_FWVB_Sach]) * fac_ms_FWVB                       
                                ,color = cmap_FWVB(norm_FWVB_color(gdf_FWVB[attr_colors_FWVB_Sach]))
                                )
                            
                    if attr_colors_FWVB_Sach_patchValues == None:
                         attr_colors_FWVB_Sach_patchValues=np.arange(norm_min_FWVB_Sach,norm_max_FWVB_Sach+1,norm_diff_FWVB_Sach/4)    
                         
                    attr_colors_FWVB_Sach_patches = [ mpatches.Patch(color=cmap_FWVB(norm_FWVB_color(value)), label=attr_colors_FWVB_Sach_patches_fmt.format(value) ) 
                                                     for value in attr_colors_FWVB_Sach_patchValues]                                                                                                                                 
                                                                                                                               
                #attr_colors_FWVB_Erg_patches=[]
                if attr_colors_FWVB_Erg != None:
                    
                    logger.debug("{0:s}attr_colors_FWVB_Erg: {1:s}".format(logStr,str(attr_colors_FWVB_Erg))) 

                    minValue=gdf_FWVB[attr_colors_FWVB_Erg].astype(float).min()
                
                    # Erstellen der Colormaps 
                    cmap_FWVBErg = matplotlib.colors.LinearSegmentedColormap.from_list('cmap_FWVBErg', colors_FWVB_Erg, N = 256)     

                    if colors_FWVB_ErgNeg != None and minValue <0:                    
                        cmap_FWVBErgNeg = matplotlib.colors.LinearSegmentedColormap.from_list('cmap_FWVBErgNeg', colors_FWVB_ErgNeg, N = 256)  
            
                    # Normierung fuer (1) Colormap und Groesse
                    if norm_min_FWVB_Erg == None:    
                         if colors_FWVB_ErgNeg != None and minValue <0:
                            norm_min_FWVB_Erg=0.
                         else:
                            norm_min_FWVB_Erg=gdf_FWVB[attr_colors_FWVB_Erg].astype(float).min()    
                    if norm_max_FWVB_Erg == None:            
                        if colors_FWVB_ErgNeg != None and minValue <0:
                            norm_max_FWVB_Erg=max(gdf_FWVB[attr_colors_FWVB_Erg].astype(float).max(),-gdf_FWVB[attr_colors_FWVB_Erg].astype(float).min())
                        else:
                            norm_max_FWVB_Erg=gdf_FWVB[attr_colors_FWVB_Erg].astype(float).max()
                    norm_FWVBErg_color = plt.Normalize(vmin=norm_min_FWVB_Erg, vmax=norm_max_FWVB_Erg)    
                    norm_diff_FWVB_Erg=norm_max_FWVB_Erg-norm_min_FWVB_Erg
                
                    # Groesse
                    if ms_FWVB_Erg == -2:                           
                        markersizes=1. * fac_ms_FWVB                       
                    elif ms_FWVB_Erg == -1:   
                        if attr_colors_FWVB_Sach != None:
                            markersizes=norm_FWVB_color(gdf_FWVB[attr_colors_FWVB_Sach]) * fac_ms_FWVB       
                        else:
                            # Sachdaten nicht definiert
                            try:
                                markersizes=norm_FWVBErg_color(gdf_FWVB[attr_colors_FWVB_Erg].astype(float)) * fac_ms_FWVB           
                            except ValueError:
                                logger.debug("{0:s}ms_FWVB_Erg: {1:d} und attr_colors_FWVB_Sach nicht definiert; Verhalten wie bei -2 ...".format(logStr,ms_FWVB_Erg)) 
                                markersizes=1. * fac_ms_FWVB   
                                pass
                                
                            
                    elif ms_FWVB_Erg == 0:                         
                        markersizes=norm_FWVBErg_color(gdf_FWVB[attr_colors_FWVB_Erg].astype(float)) * fac_ms_FWVB           

                    else:
                        if attr_colors_FWVB_Sach != None:
                            markersizesSach=norm_FWVB_color(gdf_FWVB[attr_colors_FWVB_Sach]) * fac_ms_FWVB                
                        else:
                            markersizesSach=norm_FWVBErg_color(gdf_FWVB[attr_colors_FWVB_Erg].astype(float)) * fac_ms_FWVB          
                        markersizesErg=norm_FWVBErg_color(gdf_FWVB[attr_colors_FWVB_Erg].astype(float)) * fac_ms_FWVB           
                        markersizes=[min(ms_FWVB_Erg*msSach,msErg) for (msSach,msErg) in zip(markersizesSach,markersizesErg)]
                      
                    #if isinstance(markersizes,list):    
                    #    logger.debug("{0:s}markersizes: min {1:10.2f} max {2:10.2f} ".format(logStr,min(markersizes),max(markersizes))) 
                    #else:
                    #    logger.debug("{0:s}markersizes: {1:10.2f}  ".format(logStr,markersizes)) 

                    # Plotten FWVB

                    if colors_FWVB_ErgNeg != None and minValue <0:
                        # Farbnormierungen
                        norm_FWVBErg_color=plt.Normalize(vmin=norm_min_FWVB_Erg, vmax=gdf_FWVB[attr_colors_FWVB_Erg].astype(float).max())  
                        norm_FWVBErgNeg_color=plt.Normalize(vmin=norm_min_FWVB_Erg, vmax=-gdf_FWVB[attr_colors_FWVB_Erg].astype(float).min())  

                        norm_FWVBErg_size=plt.Normalize(vmin=0., vmax=max(gdf_FWVB[attr_colors_FWVB_Erg].astype(float).max(),-gdf_FWVB[attr_colors_FWVB_Erg].astype(float).min()))  

                        gdf=gdf_FWVB[gdf_FWVB[attr_colors_FWVB_Erg].astype(float)>=0]
                        if not gdf.empty:
                            gdf.plot(ax = ax
                                        ,zorder = attr_colors_FWVB_Erg_zOrder  
                                        ,marker = '.'                           
                                        ,markersize = norm_FWVBErg_size(gdf[attr_colors_FWVB_Erg].astype(float)) * fac_ms_FWVB   
                                        ,color = cmap_FWVBErg(norm_FWVBErg_color(gdf[attr_colors_FWVB_Erg].astype(float))) 
                                        )  
                            
                        colors=cmap_FWVBErg(np.arange(cmap_FWVBErg.N))
                        attr_colors_FWVB_Erg_patches = [ mpatches.Patch(color=colors[i], label=attr_colors_FWVB_Erg_patches_fmt.format(value) ) for (i,value) in zip([0
                                                                                                                  ,cmap_FWVBErg.N-1],[gdf[attr_colors_FWVB_Erg].min(),                                                                                                                    
                                                                                                                                   gdf[attr_colors_FWVB_Erg].max()])
                                                                                                                                   ]        
                        attr_colors_FWVB_Erg_patches[0].set_label("{:s} ({:7.6f})".format(attr_colors_FWVB_Erg_patches[0].get_label(),gdf_FWVB[gdf_FWVB[attr_colors_FWVB_Erg].astype(float)>0][attr_colors_FWVB_Erg].min()))                            
                                                    
                    
                        gdf=gdf_FWVB[gdf_FWVB[attr_colors_FWVB_Erg].astype(float)<0]
                        if not gdf.empty:
                            gdf.plot(ax = ax
                                        ,zorder = 2 
                                        ,marker = '.'                           
                                        ,markersize = norm_FWVBErg_size(gdf[attr_colors_FWVB_Erg].astype(float).apply(lambda x: math.fabs(x))) * fac_ms_FWVB   
                                        ,color = cmap_FWVBErgNeg(norm_FWVBErgNeg_color(gdf[attr_colors_FWVB_Erg].astype(float).apply(lambda x: math.fabs(x)))) 
                                        )  
                            
                            
                            colors=cmap_FWVBErgNeg(np.arange(cmap_FWVBErgNeg.N))
                            attr_colors_FWVB_Erg_patches=attr_colors_FWVB_Erg_patches + [ mpatches.Patch(color=colors[i], label=attr_colors_FWVB_ErgNeg_patches_fmt.format(value) ) for (i,value) in zip([0
                                                                                                                      ,cmap_FWVBErgNeg.N-1],[-gdf[attr_colors_FWVB_Erg].max(),                                                                                                                    
                                                                                                                                       -gdf[attr_colors_FWVB_Erg].min()])
                                                                                                                                       ]        
                            attr_colors_FWVB_Erg_patches[2].set_label("{:s} ({:7.6f})".format(attr_colors_FWVB_Erg_patches[2].get_label(),gdf_FWVB[gdf_FWVB[attr_colors_FWVB_Erg].astype(float)<0][attr_colors_FWVB_Erg].max()))                            
                            
                            
                            
                            
                            
                    else:
                        
                        try:
                            colors=cmap_FWVBErg(norm_FWVBErg_color(gdf_FWVB[attr_colors_FWVB_Erg].astype(float)))
                            pass
                        except ValueError:
                            colors=cmap_FWVBErg(.666)

                        gdf_FWVB.plot(ax = ax
                                    ,zorder = attr_colors_FWVB_Erg_zOrder
                                    ,marker = '.'                           
                                    ,markersize = markersizes          
                                    ,color = colors#cmap_FWVBErg(norm_FWVBErg_color(gdf_FWVB[attr_colors_FWVB_Erg].astype(float))) 
                                    )    

                        if attr_colors_FWVB_Erg_patchValues == None:
                            attr_colors_FWVB_Erg_patchValues=np.arange(norm_min_FWVB_Erg,norm_max_FWVB_Erg+1,norm_diff_FWVB_Erg/4)                                                                                 
                        attr_colors_FWVB_Erg_patches = [ mpatches.Patch(color=cmap_FWVBErg(norm_FWVBErg_color(value)), label=attr_colors_FWVB_Erg_patches_fmt.format(value) ) for value in attr_colors_FWVB_Erg_patchValues]
                                                                                                                                                                                                                                                  

        
            ### KNOTen ###

            attr_colors_KNOT_Sach_patches=[]
            attr_colors_KNOT_Erg_patches=[]   
            attr_colors_KNOT_Erg_patchesNeg=[]                      
            if not gdf_KNOT.empty and attr_colors_KNOT_Erg != None:

                ##minValue=gdf_KNOT[attr_colors_KNOT_Erg].astype(float).min()
                
                # Erstellen der Colormaps 
                cmap_KNOTErg = matplotlib.colors.LinearSegmentedColormap.from_list('cmap_KNOTErg', colors_KNOT_Erg, N = 256)     
                minValue=gdf_KNOT[attr_colors_KNOT_Erg].astype(float).min()
                if colors_KNOT_ErgNeg != None and minValue <0:                    
                    cmap_KNOTErgNeg = matplotlib.colors.LinearSegmentedColormap.from_list('cmap_KNOTErgNeg', colors_KNOT_ErgNeg, N = 256)                      
                # Funktionsweise Farbskalen nach Normierung: Werte ]0,1[ erhalten die Randfarben 0,1
            
                # Normierungen fuer Groesse und Farbe                
                if norm_min_KNOT_Erg == None:       
                    if colors_KNOT_ErgNeg != None and minValue <0:
                        norm_min_KNOT_Erg=0.
                    else:
                        norm_min_KNOT_Erg=gdf_KNOT[attr_colors_KNOT_Erg].astype(float).min()    
                if norm_max_KNOT_Erg == None:
                    if colors_KNOT_ErgNeg != None and minValue <0:
                        norm_max_KNOT_Erg=max(gdf_KNOT[attr_colors_KNOT_Erg].astype(float).max(),-gdf_KNOT[attr_colors_KNOT_Erg].astype(float).min())                        
                        norm_KNOTErg_color=plt.Normalize(vmin=norm_min_KNOT_Erg, vmax=gdf_KNOT[attr_colors_KNOT_Erg].astype(float).max())  
                        norm_KNOTErgNeg_color=plt.Normalize(vmin=norm_min_KNOT_Erg, vmax=-gdf_KNOT[attr_colors_KNOT_Erg].astype(float).min())  
                    else:
                        norm_max_KNOT_Erg=gdf_KNOT[attr_colors_KNOT_Erg].astype(float).max()                    
                else:                    
                    # Farbnormierungen
                    norm_KNOTErg_color=plt.Normalize(vmin=norm_min_KNOT_Erg, vmax=norm_max_KNOT_Erg)  
                    norm_KNOTErgNeg_color=plt.Normalize(vmin=norm_min_KNOT_Erg, vmax=norm_max_KNOT_Erg)                      
                norm_KNOTErg_Size = plt.Normalize(vmin=norm_min_KNOT_Erg, vmax=norm_max_KNOT_Erg)  
                # Werte ]vmin,vmax[ erhalten Werte ]0,1[ entsprechend der Normierung [0,1] mit [vmin,vmax]
                logger.debug("{:s}norm_KNOTErg_Size: norm_min_KNOT_Erg={:15.6f} norm_max_KNOT_Erg={:15.6f} .".format(logStr,norm_min_KNOT_Erg,norm_max_KNOT_Erg)) 

                # Groesse
                if fac_ms_KNOT == None:
                    if fac_ms_FWVB != None:
                        fac_ms_KNOT=fac_ms_FWVB
                    else:
                        fac_ms_KNOT=8000.                

                if colors_KNOT_ErgNeg != None and minValue <0:                    

                    gdf=gdf_KNOT[gdf_KNOT[attr_colors_KNOT_Erg].astype(float)>=0]
                    if not gdf.empty:
                        gdf.plot(ax = ax
                                    ,zorder = attr_colors_KNOT_Erg_zOrder 
                                    ,marker = '.'                           
                                    ,markersize = norm_KNOTErg_Size(gdf[attr_colors_KNOT_Erg].astype(float)) * fac_ms_KNOT   
                                    ,color = cmap_KNOTErg(norm_KNOTErg_color(gdf[attr_colors_KNOT_Erg].astype(float))) 
                                    )  
                        
                        colors=cmap_KNOTErg(np.arange(cmap_KNOTErg.N))
                        attr_colors_KNOT_Erg_patches = [ mpatches.Patch(color=colors[i], label=attr_colors_KNOT_Erg_patches_fmt.format(value) ) for (i,value) in zip([0
                                                                                                                 ,cmap_KNOTErg.N-1],[gdf[attr_colors_KNOT_Erg].min(),                                                                                                                    
                                                                                                                                  gdf[attr_colors_KNOT_Erg].max()])
                                                                                                                                  ]        
                        attr_colors_KNOT_Erg_patches[0].set_label("{:s} ({:7.6f})".format(attr_colors_KNOT_Erg_patches[0].get_label(),gdf_KNOT[gdf_KNOT[attr_colors_KNOT_Erg].astype(float)>0][attr_colors_KNOT_Erg].min()))
                            
                    
                    gdf=gdf_KNOT[gdf_KNOT[attr_colors_KNOT_Erg].astype(float)<0]
                    if not gdf.empty:
                        gdf.plot(ax = ax
                                    ,zorder = 2 
                                    ,marker = '.'                           
                                    ,markersize = norm_KNOTErg_Size(gdf[attr_colors_KNOT_Erg].astype(float).apply(lambda x: math.fabs(x))) * fac_ms_KNOT   
                                    ,color = cmap_KNOTErgNeg(norm_KNOTErgNeg_color(gdf[attr_colors_KNOT_Erg].astype(float).apply(lambda x: math.fabs(x)))) 
                                    )  

                        colors=cmap_KNOTErgNeg(np.arange(cmap_KNOTErgNeg.N))
                        attr_colors_KNOT_Erg_patchesNeg = [ mpatches.Patch(color=colors[i], label=attr_colors_KNOT_ErgNeg_patches_fmt.format(value) ) for (i,value) in zip([0
                                                                                                                 ,cmap_KNOTErgNeg.N-1],[-gdf[attr_colors_KNOT_Erg].max(),                                                                                                                    
                                                                                                                                  -gdf[attr_colors_KNOT_Erg].min()])
                                                                                                                                  ]     
                                                                                                                                        
                        attr_colors_KNOT_Erg_patchesNeg[0].set_label("{:s} ({:7.6f})".format(attr_colors_KNOT_Erg_patchesNeg[0].get_label(),gdf_KNOT[gdf_KNOT[attr_colors_KNOT_Erg].astype(float)<0][attr_colors_KNOT_Erg].max()))                                                                                                                                    
                        
                    attr_colors_KNOT_Erg_patches=attr_colors_KNOT_Erg_patches+attr_colors_KNOT_Erg_patchesNeg
                        
                    
                        
                        
                else:
                    
                    msFactor=norm_KNOTErg_Size(gdf_KNOT[attr_colors_KNOT_Erg].astype(float))   
                                        
                    if size_min_KNOT_Erg!= None and size_min_KNOT_Erg>0 and size_min_KNOT_Erg<1:   
                        if size_max_KNOT_Erg==None or size_max_KNOT_Erg>size_min_KNOT_Erg:
                            for idx,(index,row) in enumerate(gdf_KNOT.iterrows()):
                                if msFactor[idx] < size_min_KNOT_Erg:
                                        msFactor[idx]=size_min_KNOT_Erg                                         
                    if size_max_KNOT_Erg!= None and size_max_KNOT_Erg>0 and size_max_KNOT_Erg<1:
                        if size_min_KNOT_Erg==None or size_min_KNOT_Erg<size_max_KNOT_Erg:
                            for idx,(index,row) in enumerate(gdf_KNOT.iterrows()):
                                if msFactor[idx] > size_max_KNOT_Erg:
                                        msFactor[idx]=size_max_KNOT_Erg      
                                        
                    logger.debug(f"{logStr}min. ms Factor: {msFactor[np.logical_not(np.isnan(msFactor))].min()} * fac_ms_KNOT max. ms Factor: {msFactor[np.logical_not(np.isnan(msFactor))].max()} * fac_ms_KNOT")
                    
                    gdf_KNOT.plot(ax = ax
                                ,zorder = attr_colors_KNOT_Erg_zOrder 
                                ,marker = marker_KNOT_Erg                        
                                ,markersize = msFactor * fac_ms_KNOT      
                                ,color = cmap_KNOTErg(norm_KNOTErg_Size(gdf_KNOT[attr_colors_KNOT_Erg].astype(float))) 
                                )   
                    
                    # Legendeneinräge                                                     
                    if attr_colors_KNOT_Erg_patchValues == None:
                         norm_diff_KNOT_Erg=norm_max_KNOT_Erg-norm_min_KNOT_Erg
                         attr_colors_KNOT_Erg_patchValues=np.arange(norm_min_KNOT_Erg,norm_max_KNOT_Erg+1,norm_diff_KNOT_Erg/4)                 
                    attr_colors_KNOT_Erg_patches = [mpatches.Patch(
                                                     color=cmap_KNOTErg(norm_KNOTErg_Size(value))
                                                    ,label=attr_colors_KNOT_Erg_patches_fmt.format(value)
                                                    ) 
                                                    for value in attr_colors_KNOT_Erg_patchValues
                                                    ]
                    #attr_colors_KNOT_Erg_patches[-1].set_label("{:s} (max.: {:4.2f})".format(
                    #      attr_colors_KNOT_Erg_patches[-1].get_label()
                    #     ,gdf_KNOT[attr_colors_KNOT_Erg].max()
                    #    )
                    #    )
                        
                    



        
        
            if MapOn:
                if LabelsOnTop:
                    cx.add_basemap(ax, crs=gdf_ROHR.crs.to_string(), source = cx.providers.CartoDB.PositronNoLabels, zoom = Map_resolution)
                    cx.add_basemap(ax, crs=gdf_ROHR.crs.to_string(), source = cx.providers.CartoDB.PositronOnlyLabels, zoom = Map_resolution)
                else:
                    cx.add_basemap(ax, crs=gdf_ROHR.crs.to_string(), source = cx.providers.CartoDB.Positron, zoom = Map_resolution)

            ax.axis('off')

            if axTitle != None:
                ax.set_title(axTitle)


            #ax.legend(handles=attr_colors_ROHR_Sach_patches
            #          ,loc='upper left'
            #          ,facecolor='white', framealpha=.01)


        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise e        
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
            return attr_colors_ROHR_Sach_patches,attr_colors_ROHR_Erg_patches,attr_colors_FWVB_Sach_patches,attr_colors_FWVB_Erg_patches,attr_colors_KNOT_Erg_patches