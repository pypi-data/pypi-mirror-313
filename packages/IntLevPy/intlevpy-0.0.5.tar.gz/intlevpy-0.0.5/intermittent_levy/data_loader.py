# data_loader.py

import os
import numpy as np

def load_eye_tracking_data(folder_path, file_pattern='Waldo_Ruj35.txt', remove_first_n_points=250):
    """
    Load and preprocess eye-tracking data from multiple .txt files in a folder.

    Parameters:
        folder_path (str): Path to the folder containing the .txt files.
        file_pattern (str): File pattern to match specific files (default: 'Waldo_Ruj35.txt').
        remove_first_n_points (int): Number of initial points to remove from each file.

    Returns:
        dict: A dictionary containing lists of cleaned data for time (T), x-coordinates (X),
              y-coordinates (Y), and saccades (saccade).
    """
    # Get list of files matching the pattern
    files = [file for file in os.listdir(folder_path) if file.endswith(file_pattern)]
    if not files:
        raise FileNotFoundError(f"No files found matching the pattern '{file_pattern}' in '{folder_path}'.")

    # Initialize lists to store data
    T, X, Y, saccade = [], [], [], []

    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            # Load data
            data = np.loadtxt(file_path)
            if data.shape[0] > data.shape[1]:
                data = data.T  # Transpose if rows > columns

            # Extract columns
            T_i = data[0]
            X_i = data[1]
            Y_i = data[2]
            saccade_i = data[3]

            # Remove initial points
            T_i = T_i[remove_first_n_points:]
            X_i = X_i[remove_first_n_points:]
            Y_i = Y_i[remove_first_n_points:]
            saccade_i = saccade_i[remove_first_n_points:]

            # Append cleaned data
            T.append(T_i)
            X.append(X_i)
            Y.append(Y_i)
            saccade.append(saccade_i)

        except Exception as e:
            print(f"Error loading {file}: {e}")

    return {
        "T": T,
        "X": X,
        "Y": Y,
        "saccade": saccade
    }
