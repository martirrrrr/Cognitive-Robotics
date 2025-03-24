import pandas as pd
import os

# Load csv
file_path = "./Test/User_Folder/User_2.csv"
df = pd.read_csv(file_path, skiprows=1)

print(df.columns.tolist())


# Folders
output_dir = "./Test/User_Folder/EEG_Slices"
os.makedirs(output_dir, exist_ok=True)

# frequency (256 Hz per EEG)
sampling_rate = 256  # 256 sample per sec

# Find total duration
start_time = df["Timestamp"].iloc[0]  # 1st timestamp
end_time = df["Timestamp"].iloc[-1]   # last timestamp
total_duration = end_time - start_time  # time in sec

# Scan each 10s
segment_duration = 10  # Block length
slice_duration = 3     # Time slice
slice_offset = 2       # Offset 

segment_samples = segment_duration * sampling_rate  # Samples per 10s
slice_samples = slice_duration * sampling_rate      # Samples per 3s
slice_start = slice_offset * sampling_rate         # Offset in samples

# Iteration
num_segments = int(total_duration // segment_duration)

for i in range(num_segments):
    start_idx = i * segment_samples
    end_idx = start_idx + segment_samples

    # Check block size
    if end_idx > len(df):
        break

    # Select segments from dataframe tuples
    segment_df = df.iloc[start_idx:end_idx]

    # Extract slices
    slice_df = segment_df.iloc[slice_start:slice_start + slice_samples]

    # Save csv autoincrement
    output_file = os.path.join(output_dir, f"EEG_Slice_{i+1}.csv")
    slice_df.to_csv(output_file, index=False)

    print(f"Created: {output_file}")

print("All slices succesfully created! 🎉")
