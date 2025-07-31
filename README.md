# ISTEAPP - İskenderun Teknik Üniversitesi Öğrenci Portalı

Modern ve kullanıcı dostu bir öğrenci portalı uygulaması. İskenderun Teknik Üniversitesi öğrencileri için geliştirilmiş, duyurular, haberler ve yemek menüsü gibi güncel bilgilere hızlı erişim sağlayan web uygulaması.

## 🚀 Özellikler

- **Hızlı Erişim Butonları**: OBS, E-posta ve UBOM sistemlerine tek tıkla erişim
- **Güncel Duyurular**: Öğrenci duyurularının otomatik olarak çekilmesi ve gösterilmesi
- **Son Haberler**: Üniversite haberlerinin anlık takibi
- **Yemek Menüsü**: Günlük yemek listesinin görüntülenmesi
- **Responsive Tasarım**: Tüm cihazlarda mükemmel görünüm
- **Modern Animasyonlar**: CSS animasyonları ile zenginleştirilmiş kullanıcı deneyimi

## 🛠️ Teknolojiler

### Backend
- **Flask 2.3.3**: Python web framework (Python 3.11 uyumlu)
- **BeautifulSoup4**: HTML/XML parsing için
- **Playwright**: JavaScript destekli web scraping
- **Flask-CORS**: Cross-Origin Resource Sharing desteği
- **Gunicorn**: Production WSGI server

### Frontend
- **HTML5 & CSS3**: Modern web standartları
- **JavaScript (ES6+)**: Dinamik içerik yönetimi
- **Font Awesome**: İkon kütüphanesi
- **Google Fonts**: Inter font ailesi

## 📦 Kurulum

### Gereksinimler
- **Python 3.11.7** (greenlet uyumluluğu için)
- pip (Python paket yöneticisi)

### Adımlar

1. **Projeyi klonlayın**
```bash
git clone https://github.com/yourusername/isteapp.git
cd isteapp
```

2. **Sanal ortam oluşturun** (önerilen)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

4. **Playwright tarayıcılarını yükleyin**
```bash
playwright install
```

5. **Uygulamayı başlatın**
```bash
python app.py
```

Uygulama varsayılan olarak `http://localhost:5000` adresinde çalışacaktır.

## 🚀 Deployment Seçenekleri

### 1. Render (Önerilen)
Render platformunda otomatik deployment için:

1. GitHub repository'nizi Render'a bağlayın
2. `render.yaml` dosyası otomatik olarak kullanılacaktır
3. Environment variables'ları Render dashboard'unda ayarlayın

### 2. Heroku
```bash
# Heroku CLI ile
heroku create your-app-name
git push heroku main
```

### 3. Docker ile Deployment
```bash
# Docker image oluştur
docker build -t isteapp .

# Container çalıştır
docker run -p 5000:5000 isteapp
```

### 4. VPS/Server Deployment
```bash
# Setup script çalıştır
chmod +x setup.sh
./setup.sh

# Gunicorn ile production'da çalıştır
gunicorn --bind 0.0.0.0:5000 app:app
```

## 📁 Proje Yapısı

```
edupro/
├── app.py                  # Ana Flask uygulaması
├── requirements.txt        # Python bağımlılıkları
├── runtime.txt            # Python versiyonu (3.11.7)
├── Procfile              # Heroku deployment
├── render.yaml           # Render deployment
├── Dockerfile            # Docker deployment
├── setup.sh              # Deployment setup script
├── .gitignore            # Git ignore patterns
├── .dockerignore         # Docker ignore patterns
├── README.md             # Proje dokümantasyonu
└── isteapp/
    ├── scraping/
    │   ├── __init__.py
    │   └── scrapers.py    # Web scraping sınıfları
    ├── static/
    │   ├── css/
    │   │   ├── style.css      # Ana stil dosyası
    │   │   └── animations.css # Animasyon stilleri
    │   ├── js/
    │   │   └── main.js        # Frontend JavaScript
    │   └── images/
    │       └── iste-logo.png  # Üniversite logosu
    └── templates/
        └── index.html         # Ana sayfa template'i
```

## 🔧 API Endpoints

- `GET /` - Ana sayfa
- `GET /api/duyurular` - Öğrenci duyurularını getirir
- `GET /api/haberler` - Son haberleri getirir
- `GET /api/yemek-menusu` - Günlük yemek menüsünü getirir
- `GET /api/haftalik-yemek-menusu` - Haftalık yemek menüsünü getirir
- `POST /api/chatbot` - AI chatbot endpoint'i

## 🎨 Özelleştirme

### Renk Teması
CSS değişkenlerini `style.css` dosyasında düzenleyerek renk temasını değiştirebilirsiniz:

```css
:root {
    --primary-red: #DC143C;
    --primary-dark-red: #B91C3C;
    --secondary-white: #FFFFFF;
    /* ... */
}
```

### Logo Değiştirme
`isteapp/static/images/iste-logo.png` dosyasını kendi logonuzla değiştirin.

## 🔧 Environment Variables

Production deployment için gerekli environment variables:

```bash
FLASK_ENV=production
FLASK_DEBUG=0
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Production Deployment

### Gunicorn ile çalıştırma
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Nginx konfigürasyonu örneği
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/isteapp/static;
    }
}
```

## ⚠️ Önemli Notlar

### Python Versiyonu
- **Python 3.11.7** kullanılmaktadır
- Python 3.13'te greenlet modülü derleme sorunları yaşanabilir
- `runtime.txt` dosyası Python versiyonunu belirtir

### Dependencies
- Flask 2.3.3 kullanılmaktadır (3.0.0 yerine)
- Tüm dependencies Python 3.11 ile uyumludur
- Playwright browser'ları deployment sırasında otomatik yüklenir

### Scraping İşlemleri
- Scraping işlemleri üniversite web sitesinin yapısına bağlıdır
- Site değişikliklerinde `scrapers.py` dosyasının güncellenmesi gerekebilir
- Yemek menüsü için Playwright kullanılmaktadır (JavaScript içerik)
- Veriler 5 dakikada bir otomatik olarak yenilenir

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👨‍💻 Geliştirici

ISTEAPP - İskenderun Teknik Üniversitesi öğrencileri için geliştirilmiştir.

---

**Not**: Bu uygulama resmi bir İSTE uygulaması değildir. Öğrenci projesi olarak geliştirilmiştir. 