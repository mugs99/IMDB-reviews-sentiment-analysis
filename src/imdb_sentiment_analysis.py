import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

def load_data():
    df = pd.read_csv('/content/IMDB Dataset.csv')
    return df

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    text = ' '.join(words)

    return text

def preprocess_data(df):
    df['review'] = df['review'].apply(preprocess_text)
    return df

def train_model(df):
    X = df['review']
    y = df['sentiment']

    # Vectorize text data
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Naive Bayes classifier
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Evaluate the model
    evaluate_model(model,X_val,y_val)

    return model

def evaluate_model(model, X_val, y_val):
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)
    print(f"Validation Accuracy: {accuracy}")

def main():
    df = load_data()

    # Preprocess the data
    df = preprocess_data(df)

    # Train the model
    model = train_model(df)

if __name__ == '__main__':
    main()
