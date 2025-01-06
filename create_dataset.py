import pandas as pd
import random

def generate_dataset():
    # Ham (normal) e-postalar için şablonlar
    ham_templates = [
        "Sayın {recipient}, {date} tarihli {event} hakkında bilgilendirme.",
        "{faculty} Fakültesi {date} tarihli ders programı güncellenmiştir.",
        "Değerli öğrencilerimiz, {location} {event} ertelenmiştir.",
        "{date} tarihli {committee} toplantısı {location} yapılacaktır.",
        "{faculty} bölümü {event} tarihi {date} olarak güncellenmiştir.",
        "Öğrenci kulübü {event} etkinliği {date} tarihinde {location} gerçekleşecektir.",
        "{recipient}, {course} dersi ödevini teslim aldım, teşekkürler.",
        "BAÜ {department} semineri {date} tarihinde {location} gerçekleşecektir.",
        "{date} tarihli {exam} sınavı {location} yapılacaktır.",
        "{scholarship} bursu başvuruları {date} tarihinde başlayacaktır."
    ]

    # Spam e-postalar için şablonlar
    spam_templates = [
        "DİKKAT! {amount} TL ödülünüzü almak için tıklayın!",
        "BAÜ öğrencilerine özel {discount} indirim fırsatı!",
        "Tebrikler! {prize} kazandınız, hemen tıklayın!",
        "ACIL! {document} için son {hours} saat!",
        "ÖNEMLİ: {account} hesabınız {action} gerekiyor!",
        "Öğrenci kredisi borcunuz siliniyor! Hemen başvurun!",
        "BAÜ öğrencilerine özel {product} kampanyası! {discount} indirim!",
        "Sınavsız {degree} fırsatı! Hemen başvurun!",
        "Günde {amount} TL kazanç! Öğrenciler için part-time iş!",
        "{service} hizmetinde büyük indirim! Kaçırmayın!"
    ]

    # Değişken havuzları
    variables = {
        'recipient': ['Öğrencilerimiz', 'Değerli öğrenciler', 'Sayın öğrencilerimiz', 'Sevgili öğrenciler'],
        'faculty': ['Mühendislik', 'Fen-Edebiyat', 'İİBF', 'Tıp', 'Eğitim', 'Mimarlık'],
        'department': ['Bilgisayar Mühendisliği', 'Makine Mühendisliği', 'Elektrik-Elektronik', 'İşletme', 'Matematik'],
        'location': ['A Blok', 'B Blok', 'C Blok', 'Kongre Merkezi', 'Merkez Kampüs', 'Çağış Kampüsü'],
        'event': ['oryantasyon', 'seminer', 'konferans', 'workshop', 'mezuniyet töreni', 'teknik gezi'],
        'date': [f'0{i}/0{j}/2024' if i < 10 and j < 10 else f'{i}/{j}/2024' for i in range(1,13) for j in range(1,29)],
        'committee': ['Fakülte Kurulu', 'Bölüm Kurulu', 'Öğrenci Temsilciliği', 'Senato', 'Yönetim Kurulu'],
        'course': ['Algoritma', 'Veri Yapıları', 'Programlama', 'Matematik', 'Fizik', 'Kimya'],
        'exam': ['Vize', 'Final', 'Bütünleme', 'Quiz', 'Ödev Sunumu'],
        'scholarship': ['Başarı Bursu', 'TÜBİTAK Bursu', 'Spor Bursu', 'Sanat Bursu', 'İhtiyaç Bursu'],
        'amount': [f'{i}000' for i in range(1,10)],
        'discount': [f'%{i*10}' for i in range(1,10)],
        'prize': ['Laptop', 'Tablet', 'Akıllı Telefon', 'Hediye Çeki', 'Burs'],
        'document': ['Burs Belgesi', 'Öğrenci Belgesi', 'Transkript', 'Diploma', 'Kimlik'],
        'hours': ['24', '48', '72'],
        'account': ['Öğrenci', 'E-posta', 'OBS', 'Kütüphane'],
        'action': ['güncelleme', 'doğrulama', 'aktivasyon', 'yenileme'],
        'product': ['Bilgisayar', 'Telefon', 'Tablet', 'Yazıcı'],
        'service': ['Yurt', 'Yemek', 'Ulaşım', 'Kırtasiye'],
        'degree': ['Yüksek Lisans', 'Doktora', 'Sertifika', 'Diploma']
    }

    # Veri seti oluşturma
    data = []
    
    # Ham e-postalar
    for _ in range(5000):
        template = random.choice(ham_templates)
        message = template
        
        # Şablondaki değişkenleri rastgele değerlerle değiştir
        for var in variables.keys():
            if '{' + var + '}' in message:
                message = message.replace('{' + var + '}', random.choice(variables[var]))
        
        data.append({'label': 'ham', 'text': message})

    # Spam e-postalar
    for _ in range(5000):
        template = random.choice(spam_templates)
        message = template
        
        # Şablondaki değişkenleri rastgele değerlerle değiştir
        for var in variables.keys():
            if '{' + var + '}' in message:
                message = message.replace('{' + var + '}', random.choice(variables[var]))
        
        data.append({'label': 'spam', 'text': message})

    # DataFrame oluştur ve karıştır
    df = pd.DataFrame(data)
    df = df.sample(frac=1).reset_index(drop=True)
    
    # CSV olarak kaydet
    df.to_csv('data/spam_dataset_tr_large.csv', index=False)
    print("Veri seti oluşturuldu ve kaydedildi!")

if __name__ == "__main__":
    generate_dataset() 