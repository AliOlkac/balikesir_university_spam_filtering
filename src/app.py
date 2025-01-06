import streamlit as st
import joblib
from preprocess import clean_text
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

def load_model():
    return joblib.load('model/spam_model.pkl')

def is_valid_email(email):
    """E-posta adresinin geçerli olup olmadığını kontrol eder"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def send_email(sender_email, sender_password, receiver_email, subject, body):
    """E-posta gönderme fonksiyonu"""
    try:
        # E-posta mesajını oluştur
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Mesaj gövdesini ekle
        message.attach(MIMEText(body, "plain"))

        # SMTP sunucusuna bağlan
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True, "E-posta başarıyla gönderildi!"
    except Exception as e:
        return False, f"Hata oluştu: {str(e)}"

def predict_spam(text, model):
    cleaned_text = clean_text(text)
    prediction = model.predict([cleaned_text])[0]
    proba = model.predict_proba([cleaned_text])[0]
    return prediction, proba

def main():
    st.set_page_config(
        page_title="Balıkesir Üniversitesi E-posta Sistemi",
        page_icon="📧",
        layout="wide"
    )
    
    st.title("📧 BAUN E-posta Sistemi")
    
    # Sidebar'da e-posta ayarları
    with st.sidebar:
        st.header("E-posta Ayarları")
        sender_email = st.text_input("Gönderen E-posta", key="sender_email")
        sender_password = st.text_input("E-posta Şifresi", type="password", key="sender_password")
        st.info("Not: Gmail kullanıyorsanız, 'Uygulama Şifresi' oluşturmanız gerekir.")
        
        if not sender_email or not sender_password:
            st.warning("E-posta göndermek için lütfen giriş bilgilerinizi doldurun.")
    
    # Ana bölüm
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Yeni E-posta")
        
        # E-posta formu
        receiver_email = st.text_input("Alıcı E-posta")
        subject = st.text_input("Konu")
        email_body = st.text_area("İçerik", height=200)
        
        # Model yükleme
        model = load_model()
        
        if st.button("Gönder", type="primary"):
            if not (sender_email and sender_password):
                st.error("Lütfen önce giriş bilgilerinizi doldurun!")
            elif not receiver_email:
                st.error("Lütfen alıcı e-posta adresini girin!")
            elif not is_valid_email(receiver_email):
                st.error("Geçersiz alıcı e-posta adresi!")
            elif not subject or not email_body:
                st.error("Lütfen konu ve içerik alanlarını doldurun!")
            else:
                # Spam kontrolü
                prediction, proba = predict_spam(email_body, model)
                spam_probability = proba[1] if prediction == "spam" else proba[0]
                
                if spam_probability > 0.7:
                    st.error("⚠️ Bu e-posta spam olarak tespit edildi! Göndermek istediğinizden emin misiniz?")
                    if st.button("Yine de Gönder"):
                        success, message = send_email(sender_email, sender_password, receiver_email, subject, email_body)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    success, message = send_email(sender_email, sender_password, receiver_email, subject, email_body)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
    with col2:
        st.subheader("Spam Analizi")
        if email_body:
            prediction, proba = predict_spam(email_body, model)
            spam_probability = proba[1] if prediction == "spam" else proba[0]
            
            # Spam olasılığı göstergesi
            st.metric(
                label="Spam Olasılığı",
                value=f"%{spam_probability*100:.1f}"
            )
            
            # İlerleme çubuğu
            st.progress(spam_probability)
            
            # Risk seviyesi
            if spam_probability > 0.7:
                st.error("🚨 Yüksek Risk!")
            elif spam_probability > 0.4:
                st.warning("⚠️ Orta Risk")
            else:
                st.success("✅ Düşük Risk")
            
            # Detaylı analiz
            st.markdown("### Analiz Detayları")
            st.write(f"Sınıflandırma: {'SPAM' if prediction == 'spam' else 'Normal'}")
            
            # Metin uzunluğu analizi
            word_count = len(email_body.split())
            st.write(f"Kelime Sayısı: {word_count}")
            if word_count < 10:
                st.info("ℹ️ Çok kısa metinler şüpheli olabilir.")
            
            # Büyük harf kullanımı analizi
            caps_ratio = sum(1 for c in email_body if c.isupper()) / len(email_body)
            if caps_ratio > 0.3:
                st.warning("⚠️ Aşırı büyük harf kullanımı tespit edildi.")

if __name__ == "__main__":
    main() 