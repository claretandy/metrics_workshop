# -*- coding: utf-8 -*-
import os
from glob import glob
#from operator import itemgetter
import subprocess
import constants as cnst
import labeller as lblr
#import itertools
import atlas_utils
import shutil
import scipy.stats as ss
from datetime import date
from datetime import datetime
#import pdb

'''
This script loops through all images created by the atlas plotting script, 
and writes them into a LaTex file for writing the atlas pdf.

By   : Andy Hartley
Email: andrew.hartley@metoffice.gov.uk
Date : 2nd May 2017
'''

def getIntroText(metric):
    
    intro_text = {'ENGLISH' : {
            'annualMax' : u'This metric shows the maximum daily value for each variable, for the period shown.',
            'annualMin' : u'This metric shows the minimum daily value for each variable, for the period shown.',
            'annualTotalRain' : u'This metric shows the total accumulated rainfall for the period shown.',
            'annualMean' : u'This metric shows the mean daily value for each variable, for the period shown.',
            'annualMeanRainyDay' : u'This metric shows the mean rainfall on the days that it rained during the period shown.',
            'monthlyClimatologicalMean' : u'This metric shows the climatology for each variable for each month within the period shown.',
            'annualRainyDays' : u'This metric shows the number of days for the selected period when rainfall was above a threshold of '+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$.',
            'annualRainyDaysPerc' : u'This metric shows the percentage of days for the selected period when rainfall was above a threshold of '+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$.',
            'annualHotDays' : u'This metric shows the number of daysfor the selected period with a Daily Maximum Temperature exceeding '+str(cnst.HOTDAYS_THRESHOLD)+lblr.DC+'.',
            'annualExtremeRain30' : u'This metric shows the number of days for the selected period when rainfall exceeds a threshold of 30mm day$^{-1}$',
            'annualExtremeRain50' : u'This metric shows the number of days for the selected period when rainfall exceeds a threshold of 50mm day$^{-1}$',
            'annualExtremeRain100' : u'This metric shows the number of days for the selected period when rainfall exceeds a threshold of 100mm day$^{-1}$',
            'annualStrongWindDays' : u'This metric shows the number of days for the selected period when daily mean wind speed exceeds a threshold of '+str(cnst.STRONGWIND_THRESHOLD)+'m s$^{-1}$',
            'wetSpell10' : u'This metric shows the number of periods with a wet spell longer than 10 days for the selected period.',
            'drySpell6' : u'This metric shows the number of periods with a dry spell longer than 6 days for the selected period.',
            'annualMaxRain5dSum' : u'Maximum Rainfall Total in a 5-day Period',
            'annualMaxRain3dSum' : u'Maximum Rainfall Total in a 3-day Period',
            'annualMaxRain2dSum' : u'Maximum Rainfall Total in a 2-day Period',
            'annualMaxRain5dMean' : u'Maximum Rainfall in a 5-day Period (Mean Daily Rate)',
            'annualMaxRain3dMean' : u'Maximum Rainfall in a 3-day Period (Mean Daily Rate)',
            'annualMaxRain2dMean' : u'Maximum Rainfall in a 2-day Period (Mean Daily Rate)',
            'SPIxMonthly' : u'The Standardised Precipitation Index (SPI) shown here is defined as the anomaly relative to the baseline period devided by the standard deviation of that baseline period. The Standardised Precipitation Index (SPI) is a metric which was developed primarily for defining and monitoring drought. It allows a user to determine the rarity of drought at a given time scale of interest. It can also be used to determine periods of anomalously wet events.',
            'SPIbiannual' : u'The Standardised Precipitation Index (SPI) shown here is defined as the anomaly relative to the baseline period devided by the standard deviation of that baseline period. In this case, a 2-year rolling window is used to compute the anomaly.',
            'onsetMarteau' : u'Local Agronomic Monsoon Onset Date (Marteau) is defined as the first rainy day (precipitation greater than 1 mm) of two consecutive rainy days (with total precipitation greater than 20 mm) and no 7-day dry spell with less than 5 mm of rainfall during the subsequent 20 days',
            'cdd' : u'Consecutive Dry Days',
            'pet' : u'Potential Evapo-Transpiration (Hargreaves equation based on daily Tmin, Tmax, Tmean and radiation)'
            },
            'FRANCAIS' : {
            'annualMax' : u'Cet indicateur illustre la valeur maximale journalière pour chaque variable, pour la période indiquée.',#'This shows the maximum daily value for each variable, for the period shown.',
            'annualMin' : u'Cet indicateur illustre la valeur minimale journalière pour chaque variable, pour la période indiquée.', #'This shows the minimum daily value for each variable, for the period shown.',
            'annualTotalRain' : u'Cet indicateur illustre la quantité totale de pluie tombée pendant la période indiquée.', #'This shows the total accumulated rainfall for the period shown.',
            'annualMean' : u'Cet indicateur illustre la valeur moyenne journalière pour chaque variable, pour la période indiquée.', #'This shows the mean daily value for each variable, for the period shown.',
            'annualMeanRainyDay' : u'Cet indicateur illustre la moyenne des précipitations pendant les jours pluvieux, pour la période indiquée.the period shown.', #'This shows the mean rainfall on the days that it rained with the period shown.',
            'monthlyClimatologicalMean' : u'Cet indicateur illustre la moyenne climatologique de chaque variable pour chaque mois, pour la période indiquée.', #'This shows the climatology for each variable for each month within the period shown.',
            'annualRainyDays' : u'Cet indicateur illustre le nombre de jours pour lesquels la pluviométrie est au-dessus du seuil de '+str(cnst.RAINYDAY_THRESHOLD)+' mm jour$^{-1}$, pendant la période indiquée.', # 'This shows the number of days in the period shown when rainfall was above a threshold of '+str(cnst.RAINYDAY_THRESHOLD)+'mm day$^{-1}$.', could also be: la pluviométrie depasse un seuil de
            'annualRainyDaysPerc' : u'Cet indicateur illustre le pourcentage de jours pour lesquels la pluviométrie est au-dessus du seuil de '+str(cnst.RAINYDAY_THRESHOLD)+'mm jour$^{-1}$, pendant la période indiquée.',
            'annualHotDays' : u'Cet indicateur illustre le nombre de jours pour lesquels la temperature maximale journalière est au-dessus du seuil de  '+str(cnst.HOTDAYS_THRESHOLD)+lblr.DC+', pendant la période indiquée.',
            'annualExtremeRain30' : u'Cet indicateur illustre le nombre de jours pour lesquels la pluviométrie est au-dessus du seuil de 30 mm jour$^{-1}$, pendant la période indiquée.',
            'annualExtremeRain50' : u'Cet indicateur illustre le nombre de jours pour lesquels la pluviométrie est au-dessus du seuil de 50 mm jour$^{-1}$, pendant la période indiquée.',
            'annualExtremeRain100' : u'Cet indicateur illustre le nombre de jours pour lesquels la pluviométrie est au-dessus du seuil de 100 mm jour$^{-1}$, pendant la période indiquée.',
            'annualStrongWindDays' : u'Cet indicateur illustre le nombre de jours pour lesquels la vitesse du vent est au-dessus du seuil de '+str(cnst.STRONGWIND_THRESHOLD)+'m s$^{-1}$',
            'wetSpell10' : u'Cet indicateur illustre le nombre de périodes pluvieuse d\'une durée plus longue que 10 jours, pendant la période indiquée.',
            'drySpell6' : u'Cet indicateur illustre le nombre de périodes sèche d\'une durée plus longue que 10 jours, pendant la période indiquée.',
            'annualMaxRain5dSum' : u'Cet indicateur illustre la pluviométrie maximale sur 5 jours.',
            'annualMaxRain3dSum' : u'Cet indicateur illustre la pluviométrie maximale sur 3 jours.',
            'annualMaxRain2dSum' : u'Cet indicateur illustre la pluviométrie maximale sur 2 jours.',
            'annualMaxRain5dMean' : u'Cet indicateur illustre les taux de précipitation maximal sur 5 jours (taux journalier moyen)',
            'annualMaxRain3dMean' : u'Cet indicateur illustre les taux de précipitation maximal sur 3 jours (taux journalier moyen)',
            'annualMaxRain2dMean' : u'Cet indicateur illustre les taux de précipitation maximal sur 2 jours (taux journalier moyen)',
            'SPIxMonthly' : u'L\'indice normalisé de précipitations ci-dessous est défini comme l\'anomalie par rapport à la période de référence divisée par l\'écart type pour cette même période. Cet indice normalisé de précipitations (SPI en anglais) est un indicateur qui a été développé principalement pour la caractérisation et la surveillance des sécheresses. Elle permet à un utilisateur de determiner la rareté de sécheresse à une échelle de temps donnée d\'intérêt. Elle peut aussi être utilisée pour identifier des périodes particulièrement humides.',
            'SPIbiannual' : u'L\'indice normalisé de précipitations ci-dessous est defini comme l\'anomalie par rapport à la période de référence diviser par l\'écart type pour cette même période. Une fenêtre glissante de 2 ans est utilisée pour calculer l\'anomalie.',
            'onsetMarteau' : u'La date de déclenchement de la mousson basé sur critères d\'agronomie locale (Marteau) est definie comme le premier jour de pluie (précipitation supérieure à 1 mm) de deux jours de pluie consecutifs (avec précipitation totale supérieure à 20 mm) et pas de période de secheresse (7 jours consecutifs avec moins de 5 mm de pluie) pendant les 20 jours successifs',
            'cdd' : u'Cet indicateur illustre le nombre de jours secs consécutifs pendant la période indiquée',
            'pet' : u'Cet indicateur illustre l\'évapotranspiration potentielle (équation de Hargreaves, basée sur les valeurs journalières de Tmin, Tmax, Tmean et flux solaire)'
            }
            }
    
    return(intro_text[cnst.LANGUAGE][metric])
    
def monthLookUp(abrv):
    
    month_long_names = {'ENGLISH' : {
        'mjjas' : u'May to September',
        'amj'   : u'April, May and June',
        'jas'   : u'July, August and September',
        'ond'   : u'October, November and December',
        'mj'    : u'May and June',
        'jj'    : u'June and July',
        'ja'    : u'July and August',
        'as'    : u'August and September',
        'so'    : u'September and October',
        'ann'   : u'Annual',
        'may'   : u'May',
        'jun'   : u'June',
        'jul'   : u'July',
        'aug'   : u'August',
        'sep'   : u'September',
        'oct'   : u'October',
        'nov'   : u'November'
        },
        'FRANCAIS' : {
        'mjjas' : u'mai à septembre',
        'amj'   : u'avril, mai et juin',
        'jas'   : u'juillet, août et septembre',
        'ond'   : u'octobre, novembre and décembre',
        'mj'    : u'mai et juin',
        'jj'    : u'juin et juillet',
        'ja'    : u'juillet et août',
        'as'    : u'août et septembre',
        'so'    : u'septembre et octobre',
        'ann'   : u'Annuel',
        'may'   : u'mai',
        'jun'   : u'juin',
        'jul'   : u'juillet',
        'aug'   : u'août',
        'sep'   : u'septembre',
        'oct'   : u'octobre',
        'nov'   : u'novembre'
        }
        }
    
    return(month_long_names[cnst.LANGUAGE][abrv])
    
    
def getMetricNiceName(name, var):
    
    if name in ['annualMax', 'annualMin', 'annualMean', 'monthlyClimatologicalMean']:
        oname = lblr.METRICLONGNAME[cnst.LANGUAGE][name] + ' ' + cnst.VARNAMES[cnst.LANGUAGE][var].title()
    else:
        oname = lblr.METRICLONGNAME[cnst.LANGUAGE][name]
        
    return(oname)
    
def getNicePlotName(plot_name):
    
    nice_plot_name = {'ENGLISH' : {
            'allModelRank' : u'Model ranking scatterplots', 
            'mapPerc' : u'Maps of present climate and future ensemble spread (10th and 90th percentiles)',
            'nbModelHistogram' : u'\'Number of model\' histograms', 
            'MultiNbModelHistogram' : u'\'Number of model\' histograms for all scenarios', 
            'allModelBoxplot' : u'Boxplots', 
            'lineplot' : u'Spaghetti timeseries', 
            'allModelHisto' : u'\'All Model\' histograms',
            'allModelMonthClim' : u'Monthly climatological mean'
            },
            'FRANCAIS' : {
            'allModelRank' : u'Diagrammes de dispersion des modèles climatiques', # 'Model ranking scatterplots',
            'mapPerc' : u'Cartes du climat historique et de l\'écart de l\'ensemble (10e et 90e percentile)', # 'Maps of ensemble spread (10th and 90th percentiles)',
            'nbModelHistogram' : u'Histogrammes de \'nombre des modèles\'', # '\'Number of model\' histograms',
            'MultiNbModelHistogram' : u'Histogrammes de \'nombre des modèles\' par tous les scénarios', # '\'Number of model\' histograms for all scenarios',
            'allModelBoxplot' : u'Les tracés en boîte', # 'Boxplots',
            'lineplot' : u'Les séries chronologiques', # 'Spaghetti timeseries',
            'allModelHisto' : u'Histogrammes de \'tous les modèles\'', # '\'All Model\' histograms',
            'allModelMonthClim' : u'Les climatologies mensuelles moyennes' #'Monthly climatological mean'
            }
            }
    try:
        return(nice_plot_name[cnst.LANGUAGE][plot_name])
    except:
        return(plot_name)
#        sys.exit('Unable to find ' + plot_name + 'in the function \'getNicePlotName\'')

def getNicePlotType(plot_type):
    nice_plottype_name = {'ENGLISH' : {
            'rcp26PercentageAnomaly' : u'\% Change by Scenario',
            'rcp45PercentageAnomaly' : u'\% Change by Scenario',
            'rcp85PercentageAnomaly' : u'\% Change by Scenario',
            'rcp26Anomaly' : u'Absolute Change by Scenario',
            'rcp45Anomaly' : u'Absolute Change by Scenario',
            'rcp85Anomaly' : u'Absolute Change by Scenario',
            'rcp26' : u'Each Scenario', 
            'rcp45' : u'Each Scenario', 
            'rcp85' : u'Each Scenario', 
            'scenarios' : u'All scenarios', 
            'historical' : u'Each Scenario', 
            'percentageAnomaly' : u'Percentage Change',
            'anomaly' : u'Absolute Change',
            'allscen' : u'All scenarios for 1950-2100'
            },
            'FRANCAIS' : {
            'rcp26PercentageAnomaly' : u'Variation en pourcentage par scénario', #'\% Change by Scenario',
            'rcp45PercentageAnomaly' : u'Variation en pourcentage par scénario', #'\% Change by Scenario',
            'rcp85PercentageAnomaly' : u'Variation en pourcentage par scénario', #'\% Change by Scenario',
            'rcp26Anomaly' : u'Variation absolue par scénario', # 'Absolute Change by Scenario',
            'rcp45Anomaly' : u'Variation absolue par scénario', # 'Absolute Change by Scenario',
            'rcp85Anomaly' : u'Variation absolue par scénario', # 'Absolute Change by Scenario',
            'rcp26' : u'Chaque scénario', #'Each Scenario',
            'rcp45' : u'Chaque scénario', #'Each Scenario',
            'rcp85' : u'Chaque scénario', #'Each Scenario',
            'scenarios' : u'Tous les scénarios', # 'All scenarios', 
            'historical' : u'Chaque scénario', # 'Each Scenario', 
            'percentageAnomaly' : u'Variation en pourcentage', # 'Percentage Change',
            'anomaly' : u'Variation absolue', # 'Absolute Change',
            'allscen' : u'Tous les scénarios pour 1950-2100' # 'All scenarios for 1950-2100'
            }
            }
    try:
        return(nice_plottype_name[cnst.LANGUAGE][plot_type])
    except:
        return(plot_type)


def getFullCaption(metric, var, region, bc, seas, plotnm, plottype):
    
    # Plotnames: ['allModelRank', 'mapPerc', 'nbModelHistogram', 'MultiNbModelHistogram', 'allModelBoxplot', 'lineplot', 'allModelHisto']
    # Plottypes: ['rcp85PercentageAnomaly', 'rcp85Anomaly', 'rcp85', 'scenarios', 'historical', 'percentageAnomaly', 'anomaly', 'allscen']
    
    caption_template = {'ENGLISH' : {
            'allModelRank' : u'This scatterplot shows xxx_pt_short_xxx xxx_metric_xxx for the period xxx_periodstart_xxx to xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Each data point shows an individual model averaged over xxx_region_xxx, and ranked according to the magnitude of the value on the y-axis. The colour of the points refers to the values given on the y-axis. This particular plot shows xxx_pt_long_xxx.',# xxx_title_end_xxx.',
            'mapPerc' : u'These maps show the historical climatology (top) and the ensemble spread in xxx_pt_short_xxx xxx_metric_xxx for the period xxx_periodstart_xxx to xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx (middle and bottom). They show the 90th and 10th percentiles of the distribution across the model ensemble, computed separately at each grid point, for the xxx_region_xxx region. This particular plot shows xxx_pt_long_xxx.',# xxx_title_end_xxx.',
            'nbModelHistogram' : u'This histogram shows the number of models that agree on xxx_pt_short_xxx xxx_metric_xxx for the period xxx_periodstart_xxx to xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Each vertical bar shows the number of models that agree on the range of values shown on the x-axis for the xxx_region_xxx region. This particular plot shows xxx_pt_long_xxx.',# xxx_title_end_xxx.',
            'MultiNbModelHistogram' : u'These histograms shows the number of models that agree on xxx_pt_short_xxx xxx_metric_xxx for the period xxx_periodstart_xxx to xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Each vertical bar shows the number of models that agree on the range of values shown on the x-axis for the xxx_region_xxx region . This particular plot shows xxx_pt_long_xxx.',# xxx_title_end_xxx.',
            'allModelBoxplot' : u'This boxplot shows xxx_pt_short_xxx xxx_metric_xxx for the period xxx_periodstart_xxx to xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Each data point (horizontal red line) shows an individual model averaged over the xxx_region_xxx region, with the solid box representing the 25th to 75th percentile range, and the whiskers the 10th to 90th percentile range. This particular plot shows xxx_pt_long_xxx.',# xxx_title_end_xxx.',
            'lineplot' : u'This timeseries plot shows xxx_pt_short_xxx xxx_metric_xxx for the period xxx_periodstart_xxx to xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Each line represents an individual model averaged over the xxx_region_xxx of interest for each year in the timeseries. This particular plot shows xxx_pt_long_xxx xxx_title_end_xxx.', 
            'allModelHisto' : u'This histogram shows xxx_pt_short_xxx xxx_metric_xxx for the period xxx_periodstart_xxx to xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Each vertical bar shows an individual model averaged over the xxx_region_xxx region. This particular plot shows xxx_pt_long_xxx xxx_title_end_xxx.' ,
            'allModelMonthClim': u'This boxplot of the monthly climatology shows xxx_pt_short_xxx xxx_metric_xxx for the period xxx_periodstart_xxx to xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Each data point (horizontal red line) shows an individual model averaged over the xxx_region_xxx region, with the solid box representing the 25th to 75th percentile range, and the whiskers the 10th to 90th percentile range. This particular plot shows xxx_pt_long_xxx.'# xxx_title_end_xxx.',
    },
    'FRANCAIS' : {
    'allModelRank' : u'Ce diagramme de dispersion illustre xxx_pt_short_xxx xxx_metric_xxx entre xxx_periodstart_xxx et xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Chaque point indique la moyenne spatiale d\'un modèle sur xxx_region_xxx; les points sont organisés ("rank", sur l\'axe des abscisses) en fonction de la magnitude de leur valeur sur l\'axe des ordonnées. Ce diagramme montre xxx_pt_long_xxx.',# xxx_title_end_xxx.',
            'mapPerc' : u'Ces cartes illustrent l\'écart de l\'ensemble pour xxx_pt_short_xxx xxx_metric_xxx, pour la période entre xxx_periodstart_xxx et xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Elles indiquent les 90eme et 10eme pourcentiles de la distribution des modèles dans l\'ensemble, calculés séparément a chaque point de grille, sur la région xxx_region_xxx. Ce diagramme montre xxx_pt_long_xxx.',# xxx_title_end_xxx.',
            'nbModelHistogram' : u'Cet histogramme illustre le nombre de modèles en accord avec  xxx_pt_short_xxx xxx_metric_xxx pour la période entre xxx_periodstart_xxx et xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Chaque barre verticale indique le nombre de modèles en accord avec la gamme de valeur indiquée sur l\'axe des abscisses pour la région xxx_region_xxx. Ce diagramme montre xxx_pt_plot_xxx.',# xxx_title_end_xxx.',
            'MultiNbModelHistogram' : u'Ces histogrammes illustrent le nombre de modèles en accord avec xxx_pt_short_xxx xxx_metric_xxx pour la période entre xxx_periodstart_xxx et xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Chaque barre verticale indique le nombre de modèles en accord avec la gamme de valeur indiquée sur l\'axe des abscisses pour la région xxx_region_xxx. Ce diagramme montre xxx_pt_long_xxx.',# xxx_title_end_xxx.',
            'allModelBoxplot' : u'Ce tracé en boîte illustre xxx_pt_short_xxx xxx_metric_xxx pour la période entre xxx_periodstart_xxx et xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Chaque point (ligne rouge horizontale) indique la moyenne spatiale d\'un modèle sur la région xxx_region_xxx, la boîte indiquant l\'intervalle entre le 25eme et le 75eme pourcentile, et les moustaches l\'intervalle entre le 10eme et le 90eme pourcentile. Ce diagramme montre xxx_pt_long_xxx.',# xxx_title_end_xxx.',
            'lineplot' : u'Cette série chronologique illustre xxx_pt_short_xxx xxx_metric_xxx pour la période entre xxx_periodstart_xxx et xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Chaque ligne indique la moyenne spatiale d\'un modèle sur la région xxx_region_xxx étudiée, pour chaque année de la série chronologique. Ce diagramme montre xxx_pt_long_xxx xxx_title_end_xxx.', 
            'allModelHisto' :  'Cet histogramme illustre xxx_pt_short_xxx xxx_metric_xxx pour la période entre xxx_periodstart_xxx et xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Chaque barre verticale indique la moyenne spatiale d\'un modèle sur la région xxx_region_xxx. Ce diagramme montre xxx_pt_long_xxx xxx_title_end_xxx.'  ,
            'allModelMonthClim':  'Ce tracé en boîte de la climatologie mensuelle illustre xxx_pt_short_xxx xxx_metric_xxx pour la période entre xxx_periodstart_xxx et xxx_periodend_xxxxxx_wrt_xxxxxx_seasinfo_xxx. Chaque point (ligne rouge horizontale) indique la moyenne spatiale d\'un modèle sur la région xxx_region_xxx region, la boîte indiquant l\'intervalle entre le 25eme et le 75eme pourcentile, et les moustaches l\'intervalle entre le 10eme et le 90eme pourcentile. Ce diagramme montre xxx_pt_long_xxx.' 
    }
    }
    
    myCaption = caption_template[cnst.LANGUAGE][plotnm]
    
    # Now do some find and replacing to fill in the gaps in the caption 
    # Add plottype short
    # ['rcp85PercentageAnomaly', 'rcp85Anomaly', 'rcp85', 'scenarios', 'historical', 'percentageAnomaly', 'anomaly', 'allscen']
    pt_short = {'ENGLISH' : {
            'rcp26PercentageAnomaly' : u'the percentage change in', 
            'rcp45PercentageAnomaly' : u'the percentage change in', 
            'rcp85PercentageAnomaly' : u'the percentage change in', 
            'rcp26Anomaly' : u'the absolute change in', 
            'rcp45Anomaly' : u'the absolute change in', 
            'rcp85Anomaly' : u'the absolute change in', 
            'rcp26' : u'the future (RCP2.6) distribution of', 
            'rcp45' : u'the future (RCP4.5) distribution of', 
            'rcp85' : u'the future (RCP8.5) distribution of', 
            'scenarios' : u'historical model spread (for the '+str(cnst.HIST[0])+' - '+str(cnst.HIST[1])+' period) compared to all available future scenarios of', 
            'historical' : u'the historical distribution of', 
            'percentageAnomaly' : u'the percentage change (all available scenarios) in',  # not sure about the 'all available scenarios' bit
            'anomaly' : u'the absolute change (all available scenarios) of',
            'allscen' : u'all available scenarios of'
            },
            'FRANCAIS' : {
            'rcp26PercentageAnomaly' : u'le pourcentage de variation de', 
            'rcp45PercentageAnomaly' : u'le pourcentage de variation de', 
            'rcp85PercentageAnomaly' : u'le pourcentage de variation de', 
            'rcp26Anomaly' : u'la variation absolue de', 
            'rcp45Anomaly' : u'la variation absolue de', 
            'rcp85Anomaly' : u'la variation absolue de', 
            'rcp26' : u'la distribution future (RCP 2.6) de', 
            'rcp45' : u'la distribution future (RCP 4.5) de', 
            'rcp85' : u'la distribution future (RCP 8.5) de', 
            'scenarios' : u'l\'écart historique des modèles (pour la période de ' + str(cnst.HIST[0]) + ' à ' +str(cnst.HIST[1])+'), comparé à tous les scénarios futures disponibles de', 
            'historical' : u'la distribution historique de', 
            'percentageAnomaly' : u'le pourcentage de variation (tous les scénarios disponibles) de',  
            'anomaly' : u'la variation absolue (tous les scénarios disponibles) de',
            'allscen' : u'tous les scénarios disponibles de'
            }
            }
    try:
        pt_short_txt = pt_short[cnst.LANGUAGE][plottype]
    except:
        pt_short_txt = ''
    # TODO: Put in deFunction here
    myCaption = myCaption.replace('xxx_pt_short_xxx', pt_short_txt)
    
    # Fix metric name peculiarities
    if metric in ['annualMax', 'annualMin', 'annualMean', 'monthlyClimatologicalMean']:
        oname = lblr.METRICLONGNAME[cnst.LANGUAGE][metric] + ' ' + cnst.VARNAMES[cnst.LANGUAGE][var].title()
    else:
        oname = lblr.METRICLONGNAME[cnst.LANGUAGE][metric]

    myCaption = myCaption.replace('xxx_metric_xxx', oname.lower())
    
    # Add period start and end years
    if plottype == 'historical':
        periodstart = str(cnst.HIST[0])
        periodend = str(cnst.HIST[1])
    else:
        periodstart = str(cnst.FUTURE[0])
        periodend = str(cnst.FUTURE[1])
        
    myCaption = myCaption.replace('xxx_periodstart_xxx', periodstart)
    myCaption = myCaption.replace('xxx_periodend_xxx', periodend)
    
    # 'With regard to' Only for future periods ...
    if plottype == 'historical':
        wrt_txt = ''
    else:
        if cnst.LANGUAGE == 'ENGLISH':
            wrt_txt = ' (compared to a baseline period of '+str(cnst.HIST[0])+' - ' +str(cnst.HIST[1])+') '
        else:
            wrt_txt = ' (par rapport à la période de référence de ' +str(cnst.HIST[0]) + ' à ' + str(cnst.HIST[1])+') '
    myCaption = myCaption.replace('xxx_wrt_xxx', wrt_txt)
    
    # Add nice season name
    if seas == 'ann':
        myCaption = myCaption.replace('xxx_seasinfo_xxx', '')
    else:
        if cnst.LANGUAGE == 'ENGLISH':
            myCaption = myCaption.replace('xxx_seasinfo_xxx', ' for the '+monthLookUp(seas)+' season')
        else:
            myCaption = myCaption.replace('xxx_seasinfo_xxx',  'pour la saison ' +monthLookUp(seas))
    
    # Add region nice name
    myCaption = myCaption.replace('xxx_region_xxx', region[1])
    
    # Add plot type information
    pt_long_desc = {'ENGLISH' : {
            'rcp26PercentageAnomaly' : u'the percentage change for the RCP2.6 scenario',
            'rcp45PercentageAnomaly' : u'the percentage change for the RCP4.5 scenario',
            'rcp85PercentageAnomaly' : u'the percentage change for the RCP8.5 scenario',
            'rcp26Anomaly' : u'the absolute change for the RCP2.6 scenario',
            'rcp45Anomaly' : u'the absolute change for the RCP4.5 scenario',
            'rcp85Anomaly' : u'the absolute change for the RCP8.5 scenario',
            'rcp26' : u'future RCP2.6 scenario distribution',
            'rcp45' : u'future RCP4.5 scenario distribution',
            'rcp85' : u'future RCP8.5 scenario distribution',
            'scenarios' : u'all available scenarios',
            'historical' : u'the historical distribution',
            'percentageAnomaly' : u'the percentage change for all available scenarios',  # not sure about the 'all available scenarios' bit
            'anomaly' : u'the absolute change for all available scenarios',
            'allscen' : u'all available scenarios'
            },
            'FRANCAIS' : {
            'rcp26PercentageAnomaly' : u'le pourcentage de variation pour le scénario RCP2.6',
            'rcp45PercentageAnomaly' : u'le pourcentage de variation pour le scénario RCP4.5',
            'rcp85PercentageAnomaly' : u'le pourcentage de variation pour le scénario RCP8.5',
            'rcp26Anomaly' : u'la variation absolue pour le scénario RCP2.6',
            'rcp45Anomaly' : u'la variation absolue pour le scénario RCP4.5',
            'rcp85Anomaly' : u'la variation absolue pour le scénario RCP8.5',
            'rcp26' : u'future distribution pour le scénario RCP 2.6',
            'rcp45' : u'future distribution pour le scénario RCP 4.5',
            'rcp85' : u'future distribution pour le scénario RCP 8.5',
            'scenarios' : u'tous les scénarios disponibles',
            'historical' : u'la distribution historique',
            'percentageAnomaly' : u'le pourcentage de variation pour tous les scénarios disponibles',  # not sure about the 'all available scenarios' bit
            'anomaly' : u'le pourcentage de variation pour tous les scénarios disponibles',
            'allscen' : u'tous les scénarios disponibles'
            }
            }
    try:
        pt_long_txt = pt_long_desc[cnst.LANGUAGE][plottype]
    except:
        pt_long_txt = plottype
    myCaption = myCaption.replace('xxx_pt_long_xxx', pt_long_txt)
    
    # Repeat the metric name again at the end
    myCaption = myCaption.replace('xxx_title_end_xxx', oname.lower())
    
    return(myCaption)
    

#def getShortCaption(metric, bc, seas, plotnm):
#    
#    if cnst.LANGUAGE == 'ENGLISH':
#        mycaption = 'As above, but for ' + monthLookUp(seas) + ' in the 2050s ('+str(cnst.FUTURE[0])+'-'+str(cnst.FUTURE[1])+') compared to historical ('+str(cnst.HIST[0])+'-'+str(cnst.HIST[1])+'). The bias corrected dataset used was ' + bc.replace("_", "\_") + '.'
#    else:
#        mycaption = 'As above, but for ' + monthLookUp(seas) + ' in the 2050s ('+str(cnst.FUTURE[0])+'-'+str(cnst.FUTURE[1])+') compared to historical ('+str(cnst.HIST[0])+'-'+str(cnst.HIST[1])+'). The bias corrected dataset used was ' + bc.replace("_", "\_") + '.'
#        
#    return(mycaption)


def isExcluded(metric, var, bc_res, seas, reg, pn, pt):
    # Checks if the plot that is about to be written to the atlas has been flagged to be excluded
    # NB: nothing to do for bc_res at the moment 

    for exc in cnst.PLOTS_TOEXCLUDE:

        if exc[0] == metric:

            if (var in exc[1]) or ('all' in exc[1]):
                if (seas in exc[2]) or ('all' in exc[2]):
                    if (reg in exc[3]) or ('all' in exc[3]):
                        if (pn in exc[4]) or ('all' in exc[4]):
                            if (pt in exc[5]) or ('all' in exc[5]):
                                return True
    
    # If it doesn't get to the end of the tree, then we return false
    return False

def makeTitlePage(season, texdir):
    # Makes a title page specific to the region, season and language 
    # This page sits behind the default cover page, but in front of the TOC
    
    if cnst.LANGUAGE == 'ENGLISH':
        ifile = os.getcwd() + os.sep + '0_titlepage_ENGLISH.tex'
        ofile = texdir + '/0_titlepage_ENGLISH.tex'
        details = u'For '+cnst.REGIONS[1]+' in '+ monthLookUp(season) +' (English version)'
    else:
        ifile = os.getcwd() + os.sep + '0_titlepage_FRANCAIS.tex'
        ofile = texdir + '/0_titlepage_FRANCAIS.tex'
        details = u'Pour '+cnst.REGIONS[1]+' en '+ monthLookUp(season) +' (version française)'
        
    with open(ifile) as fin, open(ofile,"w") as fout:
        for line in fin:
            if line.strip() == 'insert_details':
                fout.write(line.strip().replace('insert_details',details.encode('utf-8')))
            elif 'insert_version_number' in line.strip():
                fout.write(line.strip().replace('insert_version_number', cnst.VERSION))
            elif 'insert_date' == line.strip():
                fout.write(line.strip().replace('insert_date',datetime.strftime(date.today(), '%-d %B %Y')))
            else:
                fout.write(line+'\r\n')                
        
                
    return(ofile)

def runAtlas(season):
    version = cnst.VERSION
    texdir = cnst.METRIC_ATLASDIR + os.sep + season + '_atlas'
    imgdir = cnst.METRIC_PLOTDIR 
    coverpage = 'AMMA2050_atlas_coverpage_v'+cnst.VERSION+'.pdf' if os.path.isfile(os.getcwd + os.sep + 'AMMA2050_atlas_coverpage_v'+cnst.VERSION+'.pdf') else 'AMMA2050_atlas_coverpage_v1.0.pdf'

    if os.path.isdir(texdir):
        shutil.rmtree(texdir, ignore_errors=True)

    try:
        os.makedirs(texdir)
    except:
        print texdir + ' could not be created, so using the existing directory'


    # Copy the coverpage and intro section from the scripts folder into the atlas output folder
    if cnst.LANGUAGE == 'ENGLISH':
        shutil.copyfile(os.getcwd() + os.sep + '1introduction_ENGLISH.tex', texdir + os.sep + '1_introduction.tex')
    else:
        shutil.copyfile(os.getcwd() + os.sep + '1introduction_FRANCAIS.tex', texdir + os.sep + '1_introduction.tex')
        
    shutil.copyfile(os.getcwd() + os.sep + coverpage, texdir + os.sep + coverpage)
    shutil.copyfile(os.getcwd() + os.sep + 'atlas_template.tex',   texdir + os.sep + 'atlas_template.tex')
    
    titlepage_fname = makeTitlePage(season, texdir)

    plot_sections = []
#    last_plot_name = []
#    last_metric = []
    section_counter = 2 # Starts at 2 because 1 is the Introduction
    
    # Metric-specific options are set in constants.py
    for row in cnst.METRICS_TORUN:
        
        metric = row[0]
        variable = row[1] # NB: Could be multiple
        if metric in cnst.CONSTANT_PERIOD_METRIC:
            seas = row[2][0]
        else: seas = season

        for var in variable:
            # Create a new section for this metric
            section_fname = texdir + '/' + str(section_counter) + "_" + metric + "_" + var + ".tex"
            print section_fname
            if os.path.isfile(section_fname):
                os.remove(section_fname)
                    
            fmetric = open(section_fname, "w+")
            fmetric.write('\section{'+getMetricNiceName(metric, var).encode('utf-8')+'} \label{sec:'+metric+'}\r\n')
            fmetric.write('\r\n')
            
            # Write some introductory text
            fmetric.write(getIntroText(metric).encode('utf-8') + '\r\n')
            fmetric.write('\r\n')
        
            for bc_res in cnst.BC_RES:
                reg = cnst.ATLAS_REGION[0]

                imgfiles = sorted(glob(imgdir + os.sep + bc_res + os.sep + metric + os.sep + metric + '_' + var + '_' + bc_res + '_' + seas +'_'+reg+ '*.png'))
                imgdata = [atlas_utils.split_imgname(imgfile) for imgfile in imgfiles]
                
                plotnames = list(set([id['plotname'] for id in imgdata]))
                plottypes = list(set([id['plottype'] for id in imgdata]))
                
                print imgfiles
                print plotnames
                print plottypes
                
                # Plotnames: ['allModelRank', 'mapPerc', 'nbModelHistogram', 'MultiNbModelHistogram', 'allModelBoxplot', 'lineplot', 'allModelHisto']
                # Plottypes: ['rcp85PercentageAnomaly', 'rcp85Anomaly', 'rcp85', 'scenarios', 'historical', 'percentageAnomaly', 'anomaly', 'allscen']

                # Loop through all plotnames associated with this metric-var combination
                for pn in plotnames:
                    print pn
                    
                    # Make sub section
                    # Create a subsection for this plot name
#                    if last_plot_name != pn or last_metric != metric:
                    fmetric.write('\subsection{'+getNicePlotName(pn).encode('utf-8')+'}\r\n')
                    fmetric.write('\r\n')
                    
                    # Order plot types correctly
                    plottypes_ordered = ['historical', 'rcp26', 'rcp45', 'rcp85', 'scenarios', 'allscen', 'rcp26Anomaly', 'rcp45Anomaly', 'rcp85Anomaly', 'anomaly', 'rcp26PercentageAnomaly', 'rcp45PercentageAnomaly', 'rcp85PercentageAnomaly', 'percentageAnomaly']
                    ptoi = [plottypes_ordered.index(pt) for pt in plottypes]
                    pt_i = [int(oi) for oi in ss.rankdata(ptoi)]
                    plottypes_neworder = [y for x,y in sorted(zip(pt_i,plottypes))]
                    
                    for pt in plottypes_neworder:
                        print pt
                        this_file = imgdir + os.sep + bc_res + os.sep + metric + os.sep + '_'.join([metric, var, bc_res, seas, reg, pn, pt]) + ".png"
                        if os.path.isfile(this_file) and not isExcluded(metric, var, bc_res, seas, reg, pn, pt):

                            # Create a subsection for this plot name
#                            fmetric.write('\subsubsection{'+getNicePlotType(pt)+'}\r\n')
#                            fmetric.write('\r\n')
                            
                            # Write the image into the tex file for this section
                            fmetric.write('\\begin{figure}[!htb]\r\n')
                            fmetric.write('\\begin{center}\r\n')
                            fmetric.write('\\includegraphics[width=\\textwidth]{'+this_file+'}\r\n')
                            fmetric.write('\\end{center}\r\n')
                            
    #                        if last_plot_name == pn:
    #                            fmetric.write('\\caption{'+getShortCaption(metric, bc_res, seas, pt)+'}\r\n')
    #                        else:
    #                            fmetric.write('\\caption{'+getFullCaption(metric, bc_res, seas, pt)+'}\r\n')
                            fmetric.write('\\caption{'+getFullCaption(metric, var, cnst.ATLAS_REGION[1], bc_res, seas, pn, pt).encode('utf-8')+'}\r\n')
    
                            fmetric.write('\\label{fig:'+os.path.basename(this_file).rstrip(".png")+'}\r\n')
                            fmetric.write('\\end{figure}\r\n')
                            fmetric.write('\r\n')
                    
                    # New page 
                    fmetric.write('\clearpage\r\n')
                    fmetric.write('\r\n')

            fmetric.close()
            plot_sections.append(texdir + "/" + str(section_counter) + "_" + metric + "_" + var)
            
#            print(section_counter)
            section_counter += 1
            
    # At the end, write the section names into atlas.tex
    # writeTex("atlas_"+version+".tex")
    # print(plot_sections)

    with open(texdir + "/atlas_template.tex", "r") as fin, open(texdir + "/atlas_"+cnst.ATLAS_REGION[0] +'_' + seas + '_v' +version+cnst.LANGUAGE[:2]+".tex","w") as fout:
        for line in fin:
            # print(line.encode("utf-8"))
            if line.strip() == '%InsertHere':
                for pltsec in plot_sections:
#                    print('\input{'+pltsec+'}')
                    fout.write('\input{'+pltsec+'}\r\n')
                # fout.write('%InsertHere\r\n')
            elif 'coverpage' in line.strip():
                fout.write(line.strip().replace('coverpage', texdir + os.sep + 'AMMA2050_atlas_coverpage_v1.0.pdf'))
            elif 'titlepage' in line.strip():
                fout.write(line.strip().replace('0titlepage', titlepage_fname))
            elif '1introduction' in line.strip():
                fout.write(line.strip().replace('1introduction', texdir + os.sep + '1_introduction'))
            else:
                fout.write(line+'\r\n')

    # Compile TWICE in latex
    subprocess.call(["pdflatex", "-output-directory", texdir, "-interaction", "batchmode", texdir + os.sep + "atlas_"+cnst.ATLAS_REGION[0] +'_' + seas + '_' +version+cnst.LANGUAGE[:2]+".tex"])
    subprocess.call(["pdflatex", "-output-directory", texdir, "-interaction", "batchmode", texdir + os.sep + "atlas_"+cnst.ATLAS_REGION[0] +'_' + seas + '_' +version+cnst.LANGUAGE[:2]+".tex"])
   # pdb.set_trace()
    afile = texdir + os.sep + "atlas_"+cnst.ATLAS_REGION[0] +'_' + seas + '_v' +version+cnst.LANGUAGE[:2]+".pdf"
    if os.path.isfile(afile):
        print('File successfully created: ' + afile)
    else:
        print('File NOT created: ' + afile )
    
