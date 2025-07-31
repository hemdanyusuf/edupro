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
- **Flask**: Python web framework
- **BeautifulSoup4**: HTML/XML parsing için
- **Playwright**: JavaScript destekli web scraping
- **Flask-CORS**: Cross-Origin Resource Sharing desteği

### Frontend
- **HTML5 & CSS3**: Modern web standartları
- **JavaScript (ES6+)**: Dinamik içerik yönetimi
- **Font Awesome**: İkon kütüphanesi
- **Google Fonts**: Inter font ailesi

## 📦 Kurulum

### Gereksinimler
- Python 3.8+
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
playwright install chromium
```

5. **Uygulamayı başlatın**
```bash
python app.py
```

Uygulama varsayılan olarak `http://localhost:5000` adresinde çalışacaktır.

## 📁 Proje Yapısı

```
edupro/
├── app.py                  # Ana Flask uygulaması
├── requirements.txt        # Python bağımlılıkları
├── README.md              # Proje dokümantasyonu
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

## 📝 Notlar

- Scraping işlemleri üniversite web sitesinin yapısına bağlıdır. Site değişikliklerinde `scrapers.py` dosyasının güncellenmesi gerekebilir.
- Yemek menüsü için Playwright kullanılmaktadır çünkü içerik JavaScript ile yüklenmektedir.
- Veriler 5 dakikada bir otomatik olarak yenilenir.

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