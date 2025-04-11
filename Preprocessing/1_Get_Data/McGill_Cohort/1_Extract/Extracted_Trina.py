__author__ = 'Cyrille Mvomo, https://github.com/cyrillemvomo'
__version__ = "1"
__license__ = "MIT"



class Extracted_Data_Trina:
  """
    Countain the  gait data file and medical record (demographic and clinical) extracted
  """
  def __init__(self, Source_Folder_Path, Gait_Data_Path, Medical_Record_Path):
    """Store raw data from the study : "Cerebral Metabolic Changes Related to Freezing of Gait in Parkinson Disease"
      
    Input(s)
    ----------
    Source_Folder_Path      :   String
                            Path of the source folder containing sourced gait and medical data files (py file: Sourced.py)
    Gait_Data_Path          :   String
                            Path of the source folder containing sourced gait data files
    Medical_Record_Path     :   String
                            Path of the source folder containing sourced medical data files
    Method(s)
    ----------
    RawData_Extracted     :   Binarized Dictionnary (all the data of the study to be used)
    """
    
    ######### Declare variables #########
    self.Source_Folder_Path = Source_Folder_Path
    self.Gait_Data_Path = Gait_Data_Path
    self.Medical_Record_Path = Medical_Record_Path

    ######### Convert a h5 file to a pandas df #########
  def RawData_Extracted(self, save_data=False):
    """
        To access the data extracted
    """
    ######### Make sure file path is provided or raise error #########
    try:
      # Importation
      import sys, pickle
      import pandas as pd
      import numpy as np
      sys.path.append(self.Source_Folder_Path)
      from Sourced_Trina import RawData
      #In case an error occur
      if not self.Gait_Data_Path and not self.Medical_Record_Path and not self.Source_Folder_Path:
          raise ValueError("Both Gait Data, Source folder and Medical Record paths are missing.")
      elif not self.Gait_Data_Path:
          raise ValueError("Gait Data path not provided.")
      elif not self.Medical_Record_Path:
          raise ValueError("Medical Record path not provided.")
      elif not self.Source_Folder_Path:
          raise ValueError("Source Folder path not provided.")
    except FileNotFoundError:
        print("Folder not found. Please provide a valid file path.")
    except ValueError as ve:
        print(ve)
    except ImportError:
      print("Error: One of the required library is not installed.")


    ######### MAIN VARIABLES #########
    SOURCED_DATA = RawData(Gait_Data_Path = self.Gait_Data_Path, Medical_Record_Path = self.Medical_Record_Path).RawData_Sourced() # Read sourced data
    GAIT_LIST_SOURCED = []
    GAIT_DICTIONNARY_SOURCED = {}
    ID_LIST = np.array(list(SOURCED_DATA.keys()))[1:]
    GAIT_LIST_SOURCED = [SOURCED_DATA[ID].iloc[:, :] for ID in ID_LIST]

    ######### STORE EXTRACTED GAIT DATA #########
    for label, df in zip(ID_LIST, GAIT_LIST_SOURCED):
      GAIT_DICTIONNARY_SOURCED[label] = df

    ######### STORE EXTRACTED MEDICAL DATA #########
    MEDICAL_DATA = pd.DataFrame({
                                'ID' : SOURCED_DATA['Medical_Record']['Subject ID'].values,
                                'SEX' : SOURCED_DATA['Medical_Record']['Sex'].values,
                                'AGE_Y' : SOURCED_DATA['Medical_Record']['Age (at first assessment)'].values,
                                'HEIGHT_M' : SOURCED_DATA['Medical_Record']['Height (cm)'].values/1e2,
                                'DISEASE_DURATION' : SOURCED_DATA['Medical_Record']['Disease Duration'].values,
                                'MDS_UPDRS_III_ON' : SOURCED_DATA['Medical_Record']['UPDRS Motor Score ON (total/rigidity/bradykinesia/pigd/tremor)'].values,
                                'MDS_UPDRS_III_OFF' : SOURCED_DATA['Medical_Record']['UPDRS Motor Score ON (total/rigidity/bradykinesia/pigd/tremor)'].values,
                                'H&Y' : SOURCED_DATA['Medical_Record']['Hoehn & Yahr scale'].values,                            
                                'COGNITIVE_HEALTH' : SOURCED_DATA['Medical_Record']['MOCA'].values,
                                'HADS_A' : SOURCED_DATA['Medical_Record']['HADS-A'].values,
                                'HADS_D' : SOURCED_DATA['Medical_Record']['HADS-D'].values,
                                'HANDEDNESS_R_1' : np.where((SOURCED_DATA['Medical_Record']['Handedness (Edinborough)'].values.__contains__("R") == True), 1, 0),
                                'BALANCE_IMPAIRMENT' : SOURCED_DATA['Medical_Record']['Previous Falls'].values,
                                'FOG_STATUT' : SOURCED_DATA['Medical_Record']['Group (1=FOG+, 2= FOG-, 3= Control'].values,
                                'PIGD_BURDEN' : SOURCED_DATA['Medical_Record']['pigd ON'].values,
                                'TREMOR_BURDEN' : SOURCED_DATA['Medical_Record']['tremor ON'].values,
                                'FOG_STATUT' : SOURCED_DATA['Medical_Record']['Group (1=FOG+, 2= FOG-, 3= Control'].values,
                                'LEDD' : SOURCED_DATA['Medical_Record']['Dopa Equivalent'].values,
                                'DOSE_STRAIGHT' : SOURCED_DATA['Medical_Record']['Dose for straight (mCi)'].values,
                                'DOSE_STEERING' : SOURCED_DATA['Medical_Record']['Dose for steering (mCi)'].values,
                                'UPTAKE_TIME_STRAIGHT' : SOURCED_DATA['Medical_Record']['uptake time straight'].values,
                                'UPTAKE_TIME_STEERING' : SOURCED_DATA['Medical_Record']['uptake time steering'].values,
                                'DAYS_BETWEEN_STEERING_AND_STRAIGHT' : SOURCED_DATA['Medical_Record']['Days between Gait tasks'].values
                                }).sort_values(by='ID').set_index("ID")
    MEDICAL_DATA = MEDICAL_DATA[MEDICAL_DATA.index.isin(ID_LIST)]
    MEDICAL_DATA_SOURCED = {'Medical_Record': MEDICAL_DATA}

    ######### GET FINAL EXTRACTED DATA #########

    EXTRACTED_DATA = MEDICAL_DATA_SOURCED
    EXTRACTED_DATA.update(GAIT_DICTIONNARY_SOURCED)
    
    if save_data:
      with open("RawData_Extracted.bin", "wb") as f: # Binarize the data and save it to the .bin file
          pickle.dump(EXTRACTED_DATA, f)
    
    return EXTRACTED_DATA

