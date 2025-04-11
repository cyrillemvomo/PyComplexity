__author__ = 'Cyrille Mvomo, https://github.com/cyrillemvomo'
__version__ = "1"
__license__ = "MIT"



class RawData:
  """
    Countain the raw gait data file and medical record (demographic and clinical)
  """
  def __init__(self, Gait_Data_Path, Medical_Record_Path):
    """Store raw data from the study
      
    Input(s)
    ----------
    Gait_Data_Path      :   String
                            Path of the folder containing gait data files (only .h5 files)
    Medical_Record_Path :   String
                            Path of the folder containing all demographic and clinical data for each participant (single excel or csv)
    Method(s)
    ----------
    RawData_Sourced     :   Binarized Dictionnary (all the data of the study)
    """
    
    ######### Declare variables #########
    self.Gait_Data_Path = Gait_Data_Path
    self.Medical_Record_Path = Medical_Record_Path

    ######### Convert a h5 file to a pandas df #########
  def RawData_Sourced(self, save= False):
    """
        To access and save the data sourced
    """
    ######### Make sure file path is provided or raise error #########
    try:
      # Importation
      import pandas as pd
      import pickle, gzip, h5py, os
      #In case an error occur
      if not self.Gait_Data_Path and not self.Medical_Record_Path:
          raise ValueError("Both Gait Data and Medical Record paths are missing.")
      elif not self.Gait_Data_Path:
          raise ValueError("Gait Data path not provided.")
      elif not self.Medical_Record_Path:
          raise ValueError("Medical Record path not provided.")
    except FileNotFoundError:
        print("Folder not found. Please provide a valid file path.")
    except ValueError as ve:
        print(ve)
    except ImportError:
      print("Error: One of the required library is not installed.")


    ######### MAIN VARIABLES #########
    TRASH_LIST= [] #for h5 files that doesn't contain raw data
    GAIT_FILE_NAME_LIST = []
    MEDICAL_FILE_NAME_LIST = []
    GAIT_LIST = []
    GAIT_DICTIONNARY = {}
    MEDICAL_DICTIONNARY= {}

    ######### GET GAIT DATA #########
    
    for filename in os.listdir(self.Gait_Data_Path):# Get files names
        if not filename.startswith('.') and os.path.isfile(os.path.join(self.Gait_Data_Path, filename)):
            file_name_without_extension = os.path.splitext(filename)[0]
            GAIT_FILE_NAME_LIST.append(file_name_without_extension)
    GAIT_FILE_NAME_LIST.sort()
    for h5file in GAIT_FILE_NAME_LIST: # Extract signal from H5 files
        DATA = f"{self.Gait_Data_Path}/" + h5file + f".h5"
        try:
            with h5py.File(DATA, 'r') as file:
                try:
                    sacrum_sensor_id = "3308"
                    TIME_S = ((file['Sensors'][sacrum_sensor_id]['Time'][:]) - (file['Sensors'][sacrum_sensor_id]['Time'][:])[0])/1e6 # timestamp converted to seconds
                    ACC_VERTICAL_MS2 = file['Sensors'][sacrum_sensor_id]["Accelerometer"][:][:, 0] # m/s2
                    ACC_ML_MS2 = file['Sensors'][sacrum_sensor_id]["Accelerometer"][:][:, 1] # m/s2
                    ACC_AP_MS2 = file['Sensors'][sacrum_sensor_id]["Accelerometer"][:][:, 2] # m/s2
                    GYR_VERTICAL_DEGS = file['Sensors'][sacrum_sensor_id]["Gyroscope"][:][:, 0] * 57.2958 # rad/s converted to degree/s
                    GYR_ML_DEGS = file['Sensors'][sacrum_sensor_id]["Gyroscope"][:][:, 1] * 57.2958 # rad/s converted to degree/s
                    GYR_AP_DEGS = file['Sensors'][sacrum_sensor_id]["Gyroscope"][:][:, 2] * 57.2958 # rad/s converted to degree/s
                except Exception as e:
                    sacrum_sensor_id = 'XI-003308' # one participant with weird id
                    TIME_S = ((file['Sensors'][sacrum_sensor_id]['Time'][:]) - (file['Sensors'][sacrum_sensor_id]['Time'][:])[0])/1e6 # timestamp converted to seconds
                    ACC_VERTICAL_MS2 = file['Sensors'][sacrum_sensor_id]["Accelerometer"][:][:, 0] # m/s2
                    ACC_ML_MS2 = file['Sensors'][sacrum_sensor_id]["Accelerometer"][:][:, 1] # m/s2
                    ACC_AP_MS2 = file['Sensors'][sacrum_sensor_id]["Accelerometer"][:][:, 2] # m/s2
                    GYR_VERTICAL_DEGS = file['Sensors'][sacrum_sensor_id]["Gyroscope"][:][:, 0] * 57.2958 # rad/s converted to degree/s
                    GYR_ML_DEGS = file['Sensors'][sacrum_sensor_id]["Gyroscope"][:][:, 1] * 57.2958 # rad/s converted to degree/s
                    GYR_AP_DEGS = file['Sensors'][sacrum_sensor_id]["Gyroscope"][:][:, 2] * 57.2958 # rad/s converted to degree/s
        except Exception as e: # avoid error
            TRASH_LIST.append(h5file)
            continue
        GAIT_LIST.append(pd.DataFrame({
                    'TIME_S' : TIME_S,
                    'ACC_VERTICAL_MS2': ACC_VERTICAL_MS2, 
                    'ACC_ML_MS2': ACC_ML_MS2,
                    'ACC_AP_MS2': ACC_AP_MS2,
                    'GYR_VERTICAL_DEGS': GYR_VERTICAL_DEGS, 
                    'GYR_ML_DEGS': GYR_ML_DEGS,
                    'GYR_AP_DEGS': GYR_AP_DEGS,}))
    GAIT_FILE_NAME_LIST = [element for element in GAIT_FILE_NAME_LIST if element not in TRASH_LIST]
  
    for label, df in zip(GAIT_FILE_NAME_LIST, GAIT_LIST): #Create the dictionnary
        GAIT_DICTIONNARY[label] = df



    ######### GET MEDICAL DATA #########
        
    for filename in os.listdir(self.Medical_Record_Path):
        if not filename.startswith('.') and not filename.startswith('~') and os.path.isfile(os.path.join(self.Medical_Record_Path, filename)):
            file_name_without_extension = os.path.splitext(filename)[0]
            MEDICAL_FILE_NAME_LIST.append(file_name_without_extension)
    MEDICAL_FILE_NAME_LIST.sort()
    MEDICAL_LIST = [pd.read_excel(f'{self.Medical_Record_Path}/{MEDICAL_FILE_NAME_LIST[0]}.xlsx', sheet_name='Clean')]
    MEDICAL_LIST[0] = MEDICAL_LIST[0].sort_values(by= ["ID"])
    for label, df in zip(MEDICAL_FILE_NAME_LIST, MEDICAL_LIST):
        MEDICAL_DICTIONNARY[label] = df
    MEDICAL_DICTIONNARY["Medical_Record"] = MEDICAL_DICTIONNARY.pop(MEDICAL_FILE_NAME_LIST[0]) # rename original medical data file

    ######### GET FINAL SOURCED DATA #########

    RawData_Sourced = MEDICAL_DICTIONNARY
    RawData_Sourced.update(GAIT_DICTIONNARY) # combine the two dictionnaries 
    
    if save:
        with open("RawData_Sourced.bin", "wb") as f: # Binarize the data and save it to the .bin file
            pickle.dump(RawData_Sourced, f)
        return RawData_Sourced
    else:
        return RawData_Sourced

