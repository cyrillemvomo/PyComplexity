function run_zjilsV3(MainDirectoryPath, csvFilePath, fs, outputFolderPath, LBh, HSsamp)

    % run_zjilsV3 Runs the zjilsV3 function on provided data and saves the output as a CSV file.
    %
    % Inputs:
    %   - MainDirectoryPath: Path to the directory containing the function and its dependencies.
    %   - csvFilePath: Path to the CSV file containing acceleration data
    %   (required columns format: time in second, acc vert in m/s2, acc ml in m/s2, acc ap in m/s2. Only vertical used)
    %   - HeightcsvFilePath: Path to the CSV file containing the participant height
    %   - HeelStrikescsvFilePath: Path to the CSV file containing the participant detected Heel strikes
    %   - fs: Sampling frequency (in Hz).
    %   - outputFolderPath: Path to the folder where the output CSV file will be saved.
    %
    % Output:
    %   - None (CSV file with HSD output is saved in the specified folder).
    %
    % Example usage:
    %   MainDirectoryPath = '/path/to/main/directory';
    %   csvFilePath = '/path/to/csv/file.csv';
    %   HeightcsvFilePath = '/path/to/csv/file.csv';
    %   HeelStrikescsvFilePath = '/path/to/csv/file.csv';
    %   fs = 128; % Sampling frequency
    %   outputFolderPath = '/path/to/output/folder';
    %
    %   run_zjilsV3(MainDirectoryPath, csvFilePath, HeightcsvFilePath, HeelStrikescsvFilePath, fs, outputFolderPath);





    % Add the directory and its subdirectories to MATLAB's search path
    addpath(genpath(MainDirectoryPath));

    % Load the CSV files
    data = csvread(csvFilePath, 1, 0); % Skip header row if it exists
    height_data = csvread(HeightcsvFilePath, 1, 0); % Skip header row if it exists
    heelstrikes_data = csvread(HeelStrikescsvFilePath, 1, 0); % Skip header row if it exists

    % Extract relevant columns from the data
    imu_acc = data(:, 2); % Assuming the acceleration columns is 2nd (vertical)
    height = height_data(1, 1); % Assuming the height is the first value of the first column
    heel_strikes = heelstrikes_data(:, 2); % Assuming the frames of detected events are in the second column

    % Call the function
    SLE_Output = zjilsV3(LB_vacc_high = imu_acc, fs = fs, HSsamp = heel_strikes, LBh = height); %SLE mean step length estimation

    % Extract the name of the initial CSV file (assuming it's the last part of the path)
    [~, csvFileName, ~] = fileparts(csvFilePath);

    % Define the file name for the output CSV file
    outputFileName = sprintf('%s.csv', csvFileName);

    % % Convert the struct to a table
    % SLE_Output_Table = struct2table(SLE_Output);
    % 
    % % Write the table to a CSV file
    % outputFilePath = fullfile(outputFolderPath, outputFileName);
    % writetable(SLE_Output_Table, outputFilePath);

    % Write the IC vector to a CSV file
    outputFilePath = fullfile(outputFolderPath, outputFileName);
    writematrix(SLE_Output, outputFilePath);
end

