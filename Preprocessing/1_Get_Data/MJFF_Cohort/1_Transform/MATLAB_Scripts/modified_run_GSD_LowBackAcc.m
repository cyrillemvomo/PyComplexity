function run_GSD_LowBackAcc(MainDirectoryPath, csvFilePath, fs, plot_results, outputFolderPath)

    % Add the directory and its subdirectories to MATLAB's search path
    addpath(genpath(MainDirectoryPath));

    % Load the CSV file
    data = csvread(csvFilePath, 1, 0); % Skip header row if it exists

    % Extract relevant columns from the data and drop nan
    imu_acc = gpuArray(data(:, 2:4)); % Convert to GPU array
    imu_acc(isnan(imu_acc)) = 0; % Replace NaN values with 0

    % Set whether to plot the results
    if nargin < 4
        plot_results = 0; % Default value
    end

    try
        % Call the function
        GSD_Output = GSD_LowBackAcc(imu_acc, fs, plot_results);

        % Convert the struct to a table
        GSD_Output_Table = struct2table(GSD_Output);

        % Extract the name of the initial CSV file
        [~, csvFileName, ~] = fileparts(csvFilePath);

        % Define the file name for the output CSV file
        outputFileName = sprintf('%s.csv', csvFileName);

        % Define the output file path
        outputFilePath = fullfile(outputFolderPath, outputFileName);
        
        % Only write the table to CSV if it is not empty
        if ~isempty(GSD_Output_Table)
            writetable(GSD_Output_Table, outputFilePath);
        else
            fprintf('GSD_Output_Table is empty, CSV not written.\n');
        end

    catch ME
        % Display error message for debugging
        fprintf('An error occurred: %s\n', ME.message);

        % Create an empty table in case of error
        GSD_Output_Table = table();

        % Since the table is empty, no CSV will be written
        fprintf('GSD_Output failed, so no CSV file was created.\n');
    end
end
