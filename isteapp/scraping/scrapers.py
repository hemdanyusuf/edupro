import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import asyncio
from playwright.async_api import async_playwright

class ISTEScraper:
    """İSTE web sitesinden veri çeken scraper sınıfı"""
    
    def __init__(self):
        self.base_url = "https://iste.edu.tr"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_duyurular(self):
        print("[LOG] get_duyurular fonksiyonu çağrıldı.")
        """Öğrenci duyurularını çeker (güncel HTML yapısına göre)"""
        try:
            url = f"{self.base_url}/duyuru-merkezi/ogrenci"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            duyurular = []
            articles = soup.select('article.border')
            for article in articles[:7]:
                date_elem = article.select_one('.date')
                link_elem = article.select_one('a[href]')
                title_elem = article.select_one('h3')
                desc_elem = article.select_one('p')
                if link_elem and title_elem:
                    duyurular.append({
                        'baslik': title_elem.get_text(strip=True),
                        'tarih': date_elem.get_text(strip=True) if date_elem else '',
                        'aciklama': desc_elem.get_text(strip=True) if desc_elem else '',
                        'link': link_elem['href'] if link_elem['href'].startswith('http') else self.base_url + link_elem['href']
                    })
            if not duyurular:
                duyurular = [{
                    'baslik': 'Duyuru bulunamadı',
                    'tarih': '',
                    'aciklama': '',
                    'link': '#'
                }]
            print(f"[LOG] get_duyurular sonucu: {duyurular}")
            return duyurular
        except Exception as e:
            print(f"Duyuru çekme hatası: {str(e)}")
            return [{
                'baslik': 'Duyurular yüklenemedi',
                'tarih': '',
                'aciklama': '',
                'link': '#'
            }]

    def get_haberler(self):
        print("[LOG] get_haberler fonksiyonu çağrıldı.")
        """Haber merkezinden haberleri çeker (güncel HTML yapısına göre)"""
        try:
            url = f"{self.base_url}/haber-merkezi"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            haberler = []
            articles = soup.select('article.border')
            for article in articles[:7]:
                date_elem = article.select_one('.date')
                link_elem = article.select_one('a[href]')
                title_elem = article.select_one('h3')
                desc_elem = article.select_one('p')
                img_elem = article.select_one('img')
                haber = {
                    'baslik': title_elem.get_text(strip=True) if title_elem else '',
                    'tarih': date_elem.get_text(strip=True) if date_elem else '',
                    'aciklama': desc_elem.get_text(strip=True) if desc_elem else '',
                    'link': link_elem['href'] if link_elem and link_elem['href'].startswith('http') else (self.base_url + link_elem['href'] if link_elem else '#'),
                }
                if img_elem and img_elem.get('src'):
                    haber['gorsel'] = img_elem['src'] if img_elem['src'].startswith('http') else self.base_url + img_elem['src']
                haberler.append(haber)
            if not haberler:
                haberler = [{
                    'baslik': 'Haber bulunamadı',
                    'tarih': '',
                    'aciklama': '',
                    'link': '#',
                    'gorsel': ''
                }]
            print(f"[LOG] get_haberler sonucu: {haberler}")
            return haberler
        except Exception as e:
            print(f"Haber çekme hatası: {str(e)}")
            return [{
                'baslik': 'Haberler yüklenemedi',
                'tarih': '',
                'aciklama': '',
                'link': '#',
                'gorsel': ''
            }]
    
    def get_haber_icerik(self, link):
        """Belirli bir haberin içeriğini çeker"""
        print(f"[LOG] get_haber_icerik çağrıldı. Link: {link}")
        try:
            response = requests.get(link, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # İSTE web sitesi için özel CSS seçiciler - daha geniş kapsamlı
            content_selectors = [
                'main',           # Main elementi (en genel)
                'main .content',  # Ana içerik alanı
                'main article',   # Article elementi
                'main .container', # Container içeriği
                '.content',       # Genel içerik
                '.article-content', # Makale içeriği
                '.post-content',  # Post içeriği
                'article',        # Article elementi
                '.entry-content', # Entry içeriği
                '.post-body',     # Post body
                '.container',     # Container
                '.main-content'   # Main content
            ]
            
            content_elem = None
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    print(f"[LOG] İçerik elementi bulundu: {selector}")
                    break
            
            if content_elem:
                # HTML içeriğini temizle (script, style, nav, header, footer taglerini kaldır)
                for unwanted in content_elem(["script", "style", "nav", "header", "footer", ".nav", ".header", ".footer", ".breadcrumb", ".sidebar"]):
                    unwanted.decompose()
                
                # Metin içeriğini al
                content = content_elem.get_text(separator='\n', strip=True)
                # HTML içeriğini al
                clean_html = str(content_elem)
                
                print(f"[LOG] İçerik başarıyla çekildi. Uzunluk: {len(content)} karakter")
                return {
                    'success': True,
                    'content': content,
                    'html_content': clean_html
                }
            else:
                print("[LOG] İçerik elementi bulunamadı, body kullanılıyor")
                # Sayfa içeriğinin tamamını al
                body = soup.find('body')
                if body:
                    # Gereksiz elementleri kaldır
                    for unwanted in body(["script", "style", "nav", "header", "footer", ".nav", ".header", ".footer", ".breadcrumb", ".sidebar"]):
                        unwanted.decompose()
                    
                    content = body.get_text(separator='\n', strip=True)
                    clean_html = str(body)
                    print(f"[LOG] Body içeriği çekildi. Uzunluk: {len(content)} karakter")
                    return {
                        'success': True,
                        'content': content,
                        'html_content': clean_html
                    }
                else:
                    print("[LOG] Body elementi de bulunamadı")
                    return {
                        'success': False,
                        'error': 'İçerik bulunamadı'
                    }
        except Exception as e:
            print(f"[LOG] get_haber_icerik hatası: {str(e)}")
            return {
                'success': False,
                'error': f'İçerik çekme hatası: {str(e)}'
            }

    def get_duyuru_icerik(self, link):
        """Belirli bir duyurunun içeriğini çeker"""
        print(f"[LOG] get_duyuru_icerik çağrıldı. Link: {link}")
        try:
            response = requests.get(link, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # İSTE web sitesi için özel CSS seçiciler - daha geniş kapsamlı
            content_selectors = [
                'main',           # Main elementi (en genel)
                'main .content',  # Ana içerik alanı
                'main article',   # Article elementi
                'main .container', # Container içeriği
                '.content',       # Genel içerik
                '.article-content', # Makale içeriği
                '.post-content',  # Post içeriği
                'article',        # Article elementi
                '.entry-content', # Entry içeriği
                '.post-body',     # Post body
                '.container',     # Container
                '.main-content'   # Main content
            ]
            
            content_elem = None
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    print(f"[LOG] İçerik elementi bulundu: {selector}")
                    break
            
            if content_elem:
                # HTML içeriğini temizle (script, style, nav, header, footer taglerini kaldır)
                for unwanted in content_elem(["script", "style", "nav", "header", "footer", ".nav", ".header", ".footer", ".breadcrumb", ".sidebar"]):
                    unwanted.decompose()
                
                # Metin içeriğini al
                content = content_elem.get_text(separator='\n', strip=True)
                # HTML içeriğini al
                clean_html = str(content_elem)
                
                print(f"[LOG] İçerik başarıyla çekildi. Uzunluk: {len(content)} karakter")
                return {
                    'success': True,
                    'content': content,
                    'html_content': clean_html
                }
            else:
                print("[LOG] İçerik elementi bulunamadı, body kullanılıyor")
                # Sayfa içeriğinin tamamını al
                body = soup.find('body')
                if body:
                    # Gereksiz elementleri kaldır
                    for unwanted in body(["script", "style", "nav", "header", "footer", ".nav", ".header", ".footer", ".breadcrumb", ".sidebar"]):
                        unwanted.decompose()
                    
                    content = body.get_text(separator='\n', strip=True)
                    clean_html = str(body)
                    print(f"[LOG] Body içeriği çekildi. Uzunluk: {len(content)} karakter")
                    return {
                        'success': True,
                        'content': content,
                        'html_content': clean_html
                    }
                else:
                    print("[LOG] Body elementi de bulunamadı")
                    return {
                        'success': False,
                        'error': 'İçerik bulunamadı'
                    }
        except Exception as e:
            print(f"[LOG] get_duyuru_icerik hatası: {str(e)}")
            return {
                'success': False,
                'error': f'İçerik çekme hatası: {str(e)}'
            }

    async def get_yemek_menusu_async(self, tarih=None):
        """Playwright ile yemek menüsünü DOM'dan çeker. Tarih verilirse o güne tıklar."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto("https://yemekhane.iste.edu.tr/", wait_until='networkidle', timeout=30000)
                await page.wait_for_timeout(2000)
                # Eğer tarih verilmişse, ajandadan o güne tıkla
                if tarih:
                    try:
                        dt = datetime.strptime(tarih, '%Y-%m-%d')
                        year = dt.year
                        month = dt.month
                        day = dt.day
                        # Ajanda gününü bul ve tıkla
                        await page.evaluate(f'''
                            var days = document.querySelectorAll('[data-year][data-month][data-day]');
                            days.forEach(function(el) {{
                                if (el.getAttribute('data-year') == '{year}' && el.getAttribute('data-month').padStart(2, '0') == '{month:02d}' && el.getAttribute('data-day').padStart(2, '0') == '{day:02d}') {{
                                    el.click();
                                }}
                            }});
                        ''')
                        await page.wait_for_timeout(1500)
                    except Exception:
                        pass
                # Menü başlık ve içeriklerini çek
                menu_data = []
                try:
                    tarih_label = await page.locator('#tarih').inner_text()
                except Exception:
                    tarih_label = ''
                for menu_no in [1, 2]:
                    try:
                        ogun = await page.locator(f'#menu{menu_no}_head').inner_text()
                    except Exception:
                        ogun = ''
                    yemekler = []
                    for i in range(1, 8):
                        try:
                            yemek = await page.locator(f'#menu{menu_no}_{i}').inner_text()
                        except Exception:
                            yemek = ''
                        if yemek.strip():
                            yemekler.append(yemek.strip())
                    if ogun and yemekler:
                        menu_data.append({
                            'gun': tarih_label,
                            'ogun': ogun,
                            'yemekler': yemekler
                        })
                if not menu_data:
                    menu_data = [{
                        'gun': tarih_label or (tarih if tarih else datetime.now().strftime('%d-%m-%Y')),
                        'ogun': 'MENÜ',
                        'yemekler': ['Menü bulunamadı']
                    }]
                return menu_data
            except Exception as e:
                print(f"Yemek menüsü çekme hatası: {str(e)}")
                return [{
                    'gun': tarih if tarih else datetime.now().strftime('%d-%m-%Y'),
                    'ogun': 'MENÜ',
                    'yemekler': ['Menü yüklenemedi']
                }]
            finally:
                await browser.close()

    def get_yemek_menusu(self, tarih=None):
        print(f"[LOG] get_yemek_menusu fonksiyonu çağrıldı. Tarih: {tarih}")
        result = asyncio.run(self.get_yemek_menusu_async(tarih))
        print(f"[LOG] get_yemek_menusu sonucu: {result}")
        return result

    def get_haftalik_yemek_menusu(self):
        """Haftalık yemek menüsünü çeker"""
        print("[LOG] get_haftalik_yemek_menusu fonksiyonu çağrıldı")
        try:
            # Bu haftanın tarihlerini hesapla (Pazartesi'den başlayarak)
            today = datetime.now()
            monday = today - timedelta(days=today.weekday())  # Bu haftanın pazartesi
            week_dates = []
            for i in range(7):  # 7 gün
                week_date = monday + timedelta(days=i)
                week_dates.append(week_date.strftime('%Y-%m-%d'))
            
            # Her gün için menüyü çek
            haftalik_menu = []
            for date_str in week_dates:
                try:
                    gun_menu = self.get_yemek_menusu(date_str)
                    if gun_menu:
                        haftalik_menu.extend(gun_menu)
                except Exception as e:
                    print(f"[LOG] {date_str} tarihi için menü çekme hatası: {e}")
                    # Hata durumunda boş menü ekle
                    haftalik_menu.append({
                        'gun': datetime.strptime(date_str, '%Y-%m-%d').strftime('%d-%m-%Y'),
                        'ogun': 'MENÜ',
                        'yemekler': ['Menü bulunamadı']
                    })
            
            print(f"[LOG] get_haftalik_yemek_menusu sonucu: {len(haftalik_menu)} gün")
            return haftalik_menu
        except Exception as e:
            print(f"[LOG] get_haftalik_yemek_menusu hatası: {e}")
            return [] 