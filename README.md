# 🧠 Aklımda hatırlatıcı uygulaması

KPSS, YKS, ilaç takibi ve günlük işler için basit bir hatırlatıcı deneyimi.

## Yerelde çalıştırma

1. Bağımlılıkları kurun:

   ```bash
   pip install -r requirements.txt
   ```

2. Uygulamayı başlatın:

   ```bash
   streamlit run streamlit_app.py
   ```

## Streamlit Cloud üzerinde yayınlama

1. **Kodu GitHub'a gönderin.** Depoyu kendi GitHub hesabınıza alın ve değişikliklerinizi push edin.
2. **[Streamlit Cloud](https://streamlit.io/cloud) hesabı açın** ve "New app" butonuna tıklayın.
3. **Depoyu ve dalı seçin.** `streamlit_app.py` dosyasının yer aldığı dalı ve dosya yolunu belirtin.
4. **Gizli anahtarları ekleyin (isteğe bağlı).** Uygulamanız API anahtarları kullanıyorsa "Secrets" bölümünden tanımlayın.
5. **Deploy butonuna basın.** Uygulama birkaç dakika içinde `https://<proje-adı>.streamlit.app` adresinde yayınlanır.

Güncelleme yaptığınızda depoya push etmeniz yeterlidir; Streamlit Cloud otomatik olarak yeniden deploy eder.
