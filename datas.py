import numpy as np
import pandas as pd
class DataProcessor:
    def __init__(self, data):
        self.data = data

    def normalize(self):
        """Normalize the data to have mean 0 and standard deviation 1."""
        mean = np.mean(self.data)
        std = np.std(self.data)
        self.data = (self.data - mean) / std
        return self.data

    def to_dataframe(self):
        """Convert the data to a pandas DataFrame."""
        df = pd.DataFrame(self.data, columns=['Value'])
        return df
if __name__ == "__main__":
    sample_data = np.array([10, 20, 30, 40, 50])
    processor = DataProcessor(sample_data)
    
    normalized_data = processor.normalize()
    print("Normalized Data:")
    print(normalized_data)
    
    df = processor.to_dataframe()
    print("\nDataFrame:")
    print(df)