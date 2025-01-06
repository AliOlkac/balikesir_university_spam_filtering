import re
import string
from typing import List

def clean_text(text: str) -> str:
    """Metin temizleme işlemi"""
    # Küçük harfe çevirme
    text = text.lower()
    
    # Noktalama işaretlerini kaldırma
    text = ''.join([char for char in text if char not in string.punctuation])
    
    # Sayıları kaldırma
    text = re.sub(r'\d+', '', text)
    
    # Fazla boşlukları temizleme
    text = ' '.join(text.split())
    
    return text

def get_turkish_stopwords() -> List[str]:
    """Türkçe stop words listesi"""
    return [
        'acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 
        'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 
        'en', 'gibi', 'hem', 'hep', 'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 
        'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nerde',
        'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 
        'tüm', 've', 'veya', 'ya', 'yani'
    ] 