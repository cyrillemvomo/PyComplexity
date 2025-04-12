% Define the path to the directory containing the function file
functionFolderPath = '/Users/cyrilleetude/Documents/GitHub/A_Principal_Component_Model_Provides_Gait_Features_for_Tracking_Symptoms_Severity_and_Neural_Progres/MJFF_Cohort/2_Transform/0_Detect_Gait_Sequences/MATLAB_Scripts';

% Add the folder to the MATLAB path
addpath(functionFolderPath);

% Define the path to the directory containing the CSV files
%csvFolder = '/Volumes/Active/Datasets/A_Principal_Component_Model_Provides_Gait_Features_for_Tracking_Symptoms_Severity_and_Neural_Progres/MJFF_Cohort/RawData_Sourced/HomeDay1';
csvFolder = '/Volumes/Active/Datasets/A_Principal_Component_Model_Provides_Gait_Features_for_Tracking_Symptoms_Severity_and_Neural_Progres/MJFF_Cohort/RawData_Sourced/HomeDay2';%CHANGE HERE

% Get a list of all CSV files in the folder
csvFiles = dir(fullfile(csvFolder, '*.csv'));

% Start a parallel pool with the default number of workers
%parpool('local');

% Loop through each CSV file
for i = 1:length(csvFiles)
    try
        % Get the path to the current CSV file
        csvFilePath = fullfile(csvFolder, csvFiles(i).name);

        % Skip files that start with '.' or end with '~'
        [~, fileName, ext] = fileparts(csvFilePath);
        if startsWith(fileName, '.') || endsWith(fileName, '~')
            continue; % Skip this file
        end

        % Define other parameters (sampling frequency, plot_results, outputFolderPath)
        MainDirectoryPath = '/Users/cyrilleetude/Documents/GitHub/A_Principal_Component_Model_Provides_Gait_Features_for_Tracking_Symptoms_Severity_and_Neural_Progres/MJFF_Cohort/2_Transform/0_Detect_Gait_Sequences/MATLAB_Scripts/Mobilise-D-TVS-Recommended-Algorithms-master';
        fs = 50; % Sampling frequency
        plot_results = 0; % Optional, default is 0
        %outputFolderPath = '/Users/cyrilleetude/Documents/GitHub/A_Principal_Component_Model_Provides_Gait_Features_for_Tracking_Symptoms_Severity_and_Neural_Progres/MJFF_Cohort/2_Transform/0_Detect_Gait_Sequences/Day1';
        outputFolderPath = '/Users/cyrilleetude/Documents/GitHub/A_Principal_Component_Model_Provides_Gait_Features_for_Tracking_Symptoms_Severity_and_Neural_Progres/MJFF_Cohort/2_Transform/0_Detect_Gait_Sequences/Day2';%CHANGE HERE

        disp(['Processing CSV file: ', csvFilePath]); % Debug print to check which file is being processed

        % Run the GSD algorithm on the current CSV file
        run_GSD_LowBackAcc(MainDirectoryPath, csvFilePath, fs, plot_results, outputFolderPath);
    catch ex
        disp(['Error processing CSV file: ', csvFilePath]); % Debug print to check which file caused the error
        disp(getReport(ex)); % Display the error message
    end
end