from asammdf import MDF
import pandas as pd
import numpy as np

class MF4Processor:
    def __init__(self, mf4_file_path):
        self.mf4_file_path = mf4_file_path
        self.mdf = None
        self.data_groups = None
        self.load_mf4_file()

    def load_mf4_file(self):
        try:
            self.mdf = MDF(self.mf4_file_path)
            self.data_groups = self.mdf.groups
        except Exception as e:
            raise ValueError(f"Error loading MF4 file: {e}")

    def save_channel_names_to_txt(self, output_txt_path):
        try:
            all_channels = []
            for group in self.data_groups:
                all_channels.extend([channel.name for channel in group.channels])
            with open(output_txt_path, 'w') as file:
                for channel_name in all_channels:
                    file.write(f"{channel_name}\n")
        except Exception as e:
            raise RuntimeError(f"Failed to save channel names: {e}")

    def get_signal_as_numpy(self, channel_name):
        try:
            for idx, group in enumerate(self.data_groups):
                if channel_name in [channel.name for channel in group.channels]:
                    signal_data = self.mdf.get(channel_name, group=idx)
                    samples = np.nan_to_num(np.array(signal_data.samples, dtype=float), nan=0)
                    if isinstance(samples[0], np.void):
                        samples = np.array([list(sample[0]) for sample in samples])
                    return samples
            raise ValueError(f"Channel '{channel_name}' not found.")
        except Exception as e:
            raise RuntimeError(f"Error retrieving signal: {e}")

    def convert_channel_to_csv(self, channel_name, output_csv_path=None):
        try:
            samples = self.get_signal_as_numpy(channel_name)
            if samples.ndim == 1:
                df = pd.DataFrame(samples, columns=["Signal_1"])
            elif samples.ndim == 2:
                df = pd.DataFrame(samples, columns=[f"Signal_{i+1}" for i in range(samples.shape[1])])
            else:
                raise ValueError("Unexpected data format.")
            if not output_csv_path:
                output_csv_path = f"{channel_name}.csv"
            df.to_csv(output_csv_path, index=False)
        except Exception as e:
            raise RuntimeError(f"Error converting channel to CSV: {e}")
