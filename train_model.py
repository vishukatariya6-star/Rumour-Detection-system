import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from utils.text_utils import clean_text

# Create model folder if not exists
if not os.path.exists("model"):
    os.makedirs("model")

# Load dataset
fake = pd.read_csv("data/Fake.csv")
true = pd.read_csv("data/True.csv")

fake["label"] = 0
true["label"] = 1

df = pd.concat([fake, true])
df = df.sample(frac=1).reset_index(drop=True)

# Use title + text if available
if "title" in df.columns and "text" in df.columns:
    df["content"] = df["title"] + " " + df["text"]
elif "text" in df.columns:
    df["content"] = df["text"]

# Clean text
df["content"] = df["content"].apply(clean_text)

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    df["content"], df["label"], test_size=0.2, random_state=42
)

# TFIDF
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)

# Model
model = LogisticRegression(max_iter=200)
model.fit(X_train_vec, y_train)

# Save
pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(vectorizer, open("model/tfidf.pkl", "wb"))

print("Model trained and saved successfully.")
