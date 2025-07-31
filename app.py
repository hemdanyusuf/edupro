from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from isteapp.scraping import ISTEScraper
import os
import openai

app = Flask(__name__, template_folder='isteapp/templates', static_folder='isteapp/static')
CORS(app)

# Scraper instance
scraper = ISTEScraper()

# Ana sayfa route'u
@app.route('/')
def index():
    return render_template('index.html')

# Duyurular API endpoint'i
@app.route('/api/duyurular')
def get_duyurular():
    try:
        duyurular = scraper.get_duyurular()
        return jsonify({'success': True, 'data': duyurular})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Haberler API endpoint'i
@app.route('/api/haberler')
def get_haberler():
    try:
        haberler = scraper.get_haberler()
        return jsonify({'success': True, 'data': haberler})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Yemek menüsü API endpoint'i
@app.route('/api/yemek-menusu')
def get_yemek_menusu():
    try:
        tarih = request.args.get('tarih')
        yemekler = scraper.get_yemek_menusu(tarih)
        return jsonify({'success': True, 'data': yemekler})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/haftalik-yemek-menusu')
def get_haftalik_yemek_menusu():
    try:
        yemekler = scraper.get_haftalik_yemek_menusu()
        return jsonify({'success': True, 'data': yemekler})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Duyuru içeriği API endpoint'i
@app.route('/api/duyuru-icerik')
def get_duyuru_icerik():
    try:
        link = request.args.get('link')
        if not link:
            return jsonify({'success': False, 'error': 'Link parametresi gerekli'})
        
        icerik = scraper.get_duyuru_icerik(link)
        return jsonify(icerik)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Haber içeriği API endpoint'i
@app.route('/api/haber-icerik')
def get_haber_icerik():
    try:
        link = request.args.get('link')
        if not link:
            return jsonify({'success': False, 'error': 'Link parametresi gerekli'})
        
        icerik = scraper.get_haber_icerik(link)
        return jsonify(icerik)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    try:
        user_message = request.json.get('message', '')
        if not user_message:
            return jsonify({'reply': 'Lütfen bir soru yazın.'})
        
        # RAG: Güncel verileri çek
        duyurular = scraper.get_duyurular()
        haberler = scraper.get_haberler()
        yemekler = scraper.get_haftalik_yemek_menusu()  # Haftalık menü kullan
        
        # Duyurular için detaylı içerik çek (ilk 3 duyuru)
        duyuru_detaylari = []
        for duyuru in duyurular[:3]:  # İlk 3 duyuru
            try:
                if duyuru['link'] != '#':
                    icerik = scraper.get_duyuru_icerik(duyuru['link'])
                    if icerik['success']:
                        # İçeriği kısalt (ilk 800 karakter - daha detaylı)
                        kisa_icerik = icerik['content'][:800] + "..." if len(icerik['content']) > 800 else icerik['content']
                        duyuru_detaylari.append({
                            'baslik': duyuru['baslik'],
                            'tarih': duyuru['tarih'],
                            'aciklama': duyuru['aciklama'],
                            'icerik': kisa_icerik
                        })
                    else:
                        duyuru_detaylari.append({
                            'baslik': duyuru['baslik'],
                            'tarih': duyuru['tarih'],
                            'aciklama': duyuru['aciklama'],
                            'icerik': duyuru['aciklama']
                        })
                else:
                    duyuru_detaylari.append({
                        'baslik': duyuru['baslik'],
                        'tarih': duyuru['tarih'],
                        'aciklama': duyuru['aciklama'],
                        'icerik': duyuru['aciklama']
                    })
            except Exception as e:
                print(f"Duyuru içerik çekme hatası: {e}")
                duyuru_detaylari.append({
                    'baslik': duyuru['baslik'],
                    'tarih': duyuru['tarih'],
                    'aciklama': duyuru['aciklama'],
                    'icerik': duyuru['aciklama']
                })
        
        # Haberler için detaylı içerik çek (ilk 2 haber)
        haber_detaylari = []
        for haber in haberler[:2]:  # İlk 2 haber
            try:
                if haber['link'] != '#':
                    icerik = scraper.get_haber_icerik(haber['link'])
                    if icerik['success']:
                        # İçeriği kısalt (ilk 800 karakter - daha detaylı)
                        kisa_icerik = icerik['content'][:800] + "..." if len(icerik['content']) > 800 else icerik['content']
                        haber_detaylari.append({
                            'baslik': haber['baslik'],
                            'tarih': haber['tarih'],
                            'aciklama': haber['aciklama'],
                            'icerik': kisa_icerik
                        })
                    else:
                        haber_detaylari.append({
                            'baslik': haber['baslik'],
                            'tarih': haber['tarih'],
                            'aciklama': haber['aciklama'],
                            'icerik': haber['aciklama']
                        })
                else:
                    haber_detaylari.append({
                        'baslik': haber['baslik'],
                        'tarih': haber['tarih'],
                        'aciklama': haber['aciklama'],
                        'icerik': haber['aciklama']
                    })
            except Exception as e:
                print(f"Haber içerik çekme hatası: {e}")
                haber_detaylari.append({
                    'baslik': haber['baslik'],
                    'tarih': haber['tarih'],
                    'aciklama': haber['aciklama'],
                    'icerik': haber['aciklama']
                })
        
        # Promptu hazırla (detaylı içeriklerle)
        duyuru_str = '\n\n'.join([
            f"DUYURU {i+1}:\nBaşlık: {d['baslik']}\nTarih: {d['tarih']}\nAçıklama: {d['aciklama']}\nDetaylı İçerik: {d['icerik']}"
            for i, d in enumerate(duyuru_detaylari)
        ])
        
        haber_str = '\n\n'.join([
            f"HABER {i+1}:\nBaşlık: {h['baslik']}\nTarih: {h['tarih']}\nAçıklama: {h['aciklama']}\nDetaylı İçerik: {h['icerik']}"
            for i, h in enumerate(haber_detaylari)
        ])
        
        yemek_str = '\n'.join([f"{y['gun']} {y['ogun']}: {', '.join(y['yemekler'])}" for y in yemekler])
        
        rag_context = f"""GÜNCEL DUYURULAR:
{duyuru_str}

SON HABERLER:
{haber_str}

HAFTALIK YEMEK MENÜSÜ:
{yemek_str}

ÖNEMLİ: Yukarıdaki duyuru ve haber içeriklerini dikkatlice oku. Kullanıcı bu içerikler hakkında soru sorduğunda, içerikteki bilgileri kullanarak detaylı cevap ver. İçerikte bulunan tarihler, isimler, yerler, sayılar ve diğer önemli bilgileri belirt."""
        
        # Context uzunluğunu kontrol et
        print(f"[LOG] Context uzunluğu: {len(rag_context)} karakter")
        
        # OpenAI API anahtarı
        OPENAI_API_KEY=sk-xxxxxxx
        
        # Mesajları hazırla
        messages = [
            {"role": "system", "content": """Sen İskenderun Teknik Üniversitesi öğrenci portalı için Türkçe konuşan bir yardımcı botsun. 
            
Görevlerin:
1. Duyurular hakkında detaylı bilgi ver - içeriklerini açıkla
2. Haberler hakkında detaylı bilgi ver - içeriklerini açıkla
3. Yemek menüsü hakkında bilgi ver (bugün, yarın, bu hafta)
4. Kullanıcının sorularına nazik ve yardımcı bir şekilde cevap ver

Kurallar:
- Sadece duyurular, haberler ve yemek menüsü hakkında bilgi ver
- Bilmediğin veya alakasız sorulara 'Bu konuda yardımcı olamam.' de
- Duyuru ve haber içeriklerini detaylı şekilde açıkla
- Tarih bilgilerini belirt
- Kısa ve öz cevaplar ver
- Kullanıcı \"detay ver\" dediğinde içerik kısmından bilgi ver
- Kullanıcı \"hakkında bilgi ver\" dediğinde hem açıklama hem içerik kısmından bilgi ver
- Kullanıcı içerikten spesifik bir şey sorduğunda (örnek: \"ilk haberin içeriğinde ne yazıyor\", \"duyuruda hangi tarihler var\", \"ilk haberin içeriğinde geçen kurum adı nedir\") o spesifik bilgiyi içerikten bulup cevapla
- İçerikteki önemli detayları (tarihler, isimler, yerler, sayılar) belirt
- Kullanıcının sorduğu spesifik bilgiyi içerikten bulup cevapla
- Yemek menüsü sorularında (\"yarın ne var\", \"pazartesi ne var\", \"bu hafta ne var\") haftalık menüden ilgili günün bilgisini ver
- Gün isimleri ve tarihleri eşleştirerek doğru menüyü bul
- Duyuru içeriği hakkında sorulan her soruya cevap ver - içerikteki bilgileri kullan
- "Duyuru içeriği hakkında" veya "duyuru içeriğinde" gibi ifadeler geçen sorulara mutlaka cevap ver
- İçerikte bulunan bilgileri kullanarak kullanıcının sorularını yanıtla
"""},
            {"role": "system", "content": rag_context},
            {"role": "user", "content": user_message}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=800,
            temperature=0.3,
        )
        reply = response.choices[0].message['content'].strip()
        print(f"[LOG] Chatbot yanıtı: {reply}")
        return jsonify({'reply': reply})
    except Exception as e:
        print(f"Chatbot hatası: {e}")
        return jsonify({'reply': f'Bir hata oluştu: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 