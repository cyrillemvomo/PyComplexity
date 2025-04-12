function run_Shin_algo_improved(MainDirectoryPath, csvFilePath, fs, outputFolderPath)
    
    % run_Shin_algo_improved Runs the Shin_algo_improved function on provided data and saves the output as a CSV file.
    %
    % Inputs:
    %   - MainDirectoryPath: Path to the directory containing the function and its dependencies.
    %   - csvFilePath: Path to the CSV file containing acceleration data
    %   (required columns format: time in second, acc vert in m/s2, acc ml in m/s2, acc ap in m/s2.)
    %   - fs: Sampling frequency (in Hz).
    %   - outputFolderPath: Path to the folder where the output CSV file will be saved.
    %
    % Output:
    %   - None (CSV file with HSD output is saved in the specified folder).
    %
    % Example usage:
    %   MainDirectoryPath = '/path/to/main/directory';
    %   csvFilePath = '/path/to/csv/file.csv';
    %   fs = 128; % Sampling frequency
    %   plot_results = 0; % Optional, default is 0
    %   outputFolderPath = '/path/to/output/folder';
    %
    %   run_Shin_algo_improved(MainDirectoryPath, csvFilePath, fs, outputFolderPath);





    % Add the directory and its subdirectories to MATLAB's search path
    addpath(genpath(MainDirectoryPath));

    % Load the CSV file
    data = csvread(csvFilePath, 1, 0); % Skip header row if it exists

    % Extract relevant columns from the data
    imu_acc = data(:, 2:4); % Assuming the acceleration columns are 2nd (vertical), 3rd (ML), and 4th (AP)

    % Call the function
    HSD_Output = Shin_algo_improved(imu_acc, fs);

    % Extract the name of the initial CSV file (assuming it's the last part of the path)
    [~, csvFileName, ~] = fileparts(csvFilePath);

    % Define the file name for the output CSV file
    outputFileName = sprintf('%s.csv', csvFileName);

    % % Convert the struct to a table
    % HSD_Output_Table = struct2table(HSD_Output);
    % 
    % % Write the table to a CSV file
    % outputFilePath = fullfile(outputFolderPath, outputFileName);
    % writetable(HSD_Output_Table, outputFilePath);

    % Write the IC vector to a CSV file
    outputFilePath = fullfile(outputFolderPath, outputFileName);
    writematrix(HSD_Output, outputFilePath);
end
