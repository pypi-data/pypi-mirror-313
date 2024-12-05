import pandas as pd
from stat_df import statistics  # Adjust the import based on your structure
import random

# Set a seed for reproducibility
random.seed(42)

# Generate dummy data
data = {
    "Strings": [f"Item {i}" for i in range(1, 21)],  # 20 string entries
    "Floats": [
        round(random.uniform(1.0, 100.0), 2) for _ in range(20)
    ],  # 20 float entries
}

# Create the DataFrame
dummy_df = pd.DataFrame(data)

# Display the DataFrame
print(dummy_df)

statistics.show_stats(dummy_df)
