import numpy as np
import pandas as pd
import os

def f():
    path = os.path.join("Data", "participant_ratings.csv")
    df = pd.read_csv(path)
    df= df.loc[df["Participant_id"] == 23]
    df = df.sort_values('Arousal')
    df = df.sort_values('Valence')
    print(df.iloc[0])
    print(df.iloc[-1])


f()