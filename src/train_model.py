import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from preprocess import clean_text, get_turkish_stopwords

def train_spam_model():
    # Veri setini yükleme
    df = pd.read_csv('../data/trspam.csv', names=['label', 'text'])
    
    # Veriyi temizleme
    df['text'] = df['text'].apply(clean_text)
    
    # Eğitim ve test verilerini ayırma
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], 
        df['label'], 
        test_size=0.2, 
        random_state=42
    )
    
    # Model pipeline oluşturma
    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            stop_words=get_turkish_stopwords(),
            max_features=5000,
            ngram_range=(1, 2)
        )),
        ('classifier', MultinomialNB())
    ])
    
    # Modeli eğitme
    model.fit(X_train, y_train)
    
    # Model performansını değerlendirme
    accuracy = model.score(X_test, y_test)
    print(f"Model doğruluk oranı: {accuracy:.2f}")
    
    # Modeli kaydetme
    joblib.dump(model, '../model/spam_model.pkl')
    
if __name__ == "__main__":
    train_spam_model() 