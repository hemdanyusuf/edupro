// Main JavaScript File for ISTEAPP

// DOM Elements
const announcementsContainer = document.getElementById('announcementsContainer');
const newsContainer = document.getElementById('newsContainer');
const menuContainer = document.getElementById('menuContainer');
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const navLinks = document.getElementById('navLinks');

// Modal Elements
const modal = document.getElementById('contentModal');
const modalTitle = document.getElementById('modalTitle');
const modalBody = document.getElementById('modalBody');
const modalClose = document.getElementById('modalClose');

if (mobileMenuToggle && navLinks) {
    // Mobile Menu Toggle
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.nav-menu')) {
            navLinks.classList.remove('active');
        }
    });
}

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const href = this.getAttribute('href');
        if (href === '#' || href === '' || href === '#top') {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            if (navLinks) navLinks.classList.remove('active');
            return;
        }
        const target = document.querySelector(href);
        if (target) {
            // Sticky header yüksekliğini al
            const header = document.querySelector('.header');
            const headerHeight = header ? header.offsetHeight : 0;
            const elementPosition = target.getBoundingClientRect().top + window.pageYOffset;
            const offsetPosition = elementPosition - headerHeight - 8; // 8px ekstra boşluk
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
            // Close mobile menu after clicking
            if (navLinks) navLinks.classList.remove('active');
        }
    });
});

// Modal functionality
function openModal(title, content) {
    modalTitle.textContent = title;
    modalBody.innerHTML = content;
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Modal event listeners
if (modalClose) {
    modalClose.addEventListener('click', closeModal);
}

if (modal) {
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
}

// ESC tuşu ile modal kapatma
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal && modal.style.display === 'block') {
        closeModal();
    }
});

// İçerik yükleme fonksiyonu
async function loadContent(link, title, type) {
    console.log(`[LOG] loadContent çağrıldı. Link: ${link}, Title: ${title}, Type: ${type}`);
    openModal(title, '<div class="loading"><i class="fas fa-spinner fa-spin"></i><span>İçerik yükleniyor...</span></div>');
    
    try {
        const endpoint = type === 'duyuru' ? '/api/duyuru-icerik' : '/api/haber-icerik';
        console.log(`[LOG] Endpoint: ${endpoint}`);
        const response = await fetch(`${endpoint}?link=${encodeURIComponent(link)}`);
        const data = await response.json();
        console.log(`[LOG] API Response:`, data);
        
        if (data.success) {
            // HTML içeriğini güvenli şekilde render et
            const content = data.html_content || data.content;
            console.log(`[LOG] Content type: ${data.html_content ? 'HTML' : 'Text'}, Length: ${content ? content.length : 0}`);
            
            // İçeriği güvenli şekilde render et
            if (data.html_content) {
                // HTML içeriği varsa, sadece içerik kısmını al
                let cleanContent = content;
                
                // Gereksiz elementleri temizle
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = content;
                
                // Navigation, header, footer gibi elementleri kaldır
                const elementsToRemove = tempDiv.querySelectorAll('nav, header, footer, .nav, .header, .footer, .breadcrumb, .sidebar');
                elementsToRemove.forEach(el => el.remove());
                
                // Sadece ana içerik kısmını al
                const mainContent = tempDiv.querySelector('main, .content, .article-content, .post-content') || tempDiv;
                
                modalBody.innerHTML = `
                    <div class="content-text">
                        ${mainContent.innerHTML}
                    </div>
                    <div class="content-footer">
                        <a href="${link}" target="_blank" class="btn btn-primary">
                            <i class="fas fa-external-link-alt"></i> Orijinal Sayfayı Aç
                        </a>
                    </div>
                `;
            } else {
                // Sadece metin içeriği varsa
                modalBody.innerHTML = `
                    <div class="content-text">
                        <p>${content.replace(/\n/g, '</p><p>')}</p>
                    </div>
                    <div class="content-footer">
                        <a href="${link}" target="_blank" class="btn btn-primary">
                            <i class="fas fa-external-link-alt"></i> Orijinal Sayfayı Aç
                        </a>
                    </div>
                `;
            }
            console.log(`[LOG] İçerik başarıyla yüklendi`);
        } else {
            console.log(`[LOG] API Error: ${data.error}`);
            modalBody.innerHTML = `
                <div class="error-message">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>${data.error || 'İçerik yüklenemedi'}</p>
                    <a href="${link}" target="_blank" class="btn btn-primary">
                        <i class="fas fa-external-link-alt"></i> Orijinal Sayfayı Aç
                    </a>
                </div>
            `;
        }
    } catch (error) {
        console.error('[LOG] İçerik yükleme hatası:', error);
        modalBody.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>İçerik yüklenirken bir hata oluştu.</p>
                <a href="${link}" target="_blank" class="btn btn-primary">
                    <i class="fas fa-external-link-alt"></i> Orijinal Sayfayı Aç
                </a>
            </div>
        `;
    }
}

// Fetch and display announcements
async function loadAnnouncements() {
    try {
        const response = await fetch('/api/duyurular');
        const data = await response.json();
        
        if (data.success && data.data.length > 0) {
            const allDuyurular = data.data;
            const firstDuyurular = allDuyurular.slice(0, 3);
            const restDuyurular = allDuyurular.slice(3);
            let html = firstDuyurular.map(duyuru => `
                <div class="announcement-item animate-fade-in">
                    <a href="#" onclick="loadContent('${duyuru.link}', '${duyuru.baslik.replace(/'/g, "\\'")}', 'duyuru'); return false;">
                        <h4>${duyuru.baslik}</h4>
                    </a>
                    <div class="item-meta">
                        <span><i class="fas fa-calendar-alt"></i> ${duyuru.tarih}</span>
                    </div>
                </div>
            `).join('');
            if (restDuyurular.length > 0) {
                html += `<div id="moreAnnouncementsContainer">
                    <button id="showMoreAnnouncements" class="see-all">Devamını Gör <i class="fas fa-chevron-down"></i></button>
                    <div id="moreAnnouncements" style="display:none;">` + restDuyurular.map(duyuru => `
                        <div class="announcement-item animate-fade-in">
                            <a href="#" onclick="loadContent('${duyuru.link}', '${duyuru.baslik.replace(/'/g, "\\'")}', 'duyuru'); return false;">
                                <h4>${duyuru.baslik}</h4>
                            </a>
                            <div class="item-meta">
                                <span><i class="fas fa-calendar-alt"></i> ${duyuru.tarih}</span>
                            </div>
                        </div>
                    `).join('') + `</div>
                </div>`;
            }
            announcementsContainer.innerHTML = html;
            const showMoreBtn = document.getElementById('showMoreAnnouncements');
            if (showMoreBtn) {
                showMoreBtn.addEventListener('click', function() {
                    const moreDiv = document.getElementById('moreAnnouncements');
                    if (moreDiv.style.display === 'none') {
                        moreDiv.style.display = 'block';
                        showMoreBtn.innerHTML = 'Daha Az Göster <i class="fas fa-chevron-up"></i>';
                    } else {
                        moreDiv.style.display = 'none';
                        showMoreBtn.innerHTML = 'Devamını Gör <i class="fas fa-chevron-down"></i>';
                    }
                });
            }
        } else {
            announcementsContainer.innerHTML = `
                <div class="no-data">
                    <i class="fas fa-info-circle"></i>
                    <p>Henüz duyuru bulunmamaktadır.</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Duyurular yüklenemedi:', error);
        announcementsContainer.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Duyurular yüklenirken bir hata oluştu.</p>
            </div>
        `;
    }
}

// Fetch and display news
async function loadNews() {
    try {
        const response = await fetch('/api/haberler');
        const data = await response.json();
        
        if (data.success && data.data.length > 0) {
            const allNews = data.data;
            const firstNews = allNews.slice(0, 2);
            const restNews = allNews.slice(2);
            let html = firstNews.map(haber => `
                <div class="news-item animate-fade-in">
                    <a href="#" onclick="loadContent('${haber.link}', '${haber.baslik.replace(/'/g, "\\'")}', 'haber'); return false;">
                        <h4>${haber.baslik}</h4>
                        ${haber.aciklama ? `<p>${haber.aciklama}</p>` : ''}
                    </a>
                    <div class="item-meta">
                        <span><i class="fas fa-calendar-alt"></i> ${haber.tarih}</span>
                    </div>
                </div>
            `).join('');
            if (restNews.length > 0) {
                html += `<div id="moreNewsContainer">
                    <button id="showMoreNews" class="see-all">Devamını Gör <i class="fas fa-chevron-down"></i></button>
                    <div id="moreNews" style="display:none;">` + restNews.map(haber => `
                        <div class="news-item animate-fade-in">
                            <a href="#" onclick="loadContent('${haber.link}', '${haber.baslik.replace(/'/g, "\\'")}', 'haber'); return false;">
                                <h4>${haber.baslik}</h4>
                                ${haber.aciklama ? `<p>${haber.aciklama}</p>` : ''}
                            </a>
                            <div class="item-meta">
                                <span><i class="fas fa-calendar-alt"></i> ${haber.tarih}</span>
                            </div>
                        </div>
                    `).join('') + `</div>
                </div>`;
            }
            newsContainer.innerHTML = html;
            const showMoreBtn = document.getElementById('showMoreNews');
            if (showMoreBtn) {
                showMoreBtn.addEventListener('click', function() {
                    const moreDiv = document.getElementById('moreNews');
                    if (moreDiv.style.display === 'none') {
                        moreDiv.style.display = 'block';
                        showMoreBtn.innerHTML = 'Daha Az Göster <i class="fas fa-chevron-up"></i>';
                    } else {
                        moreDiv.style.display = 'none';
                        showMoreBtn.innerHTML = 'Devamını Gör <i class="fas fa-chevron-down"></i>';
                    }
                });
            }
        } else {
            newsContainer.innerHTML = `
                <div class="no-data">
                    <i class="fas fa-info-circle"></i>
                    <p>Henüz haber bulunmamaktadır.</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Haberler yüklenemedi:', error);
        newsContainer.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Haberler yüklenirken bir hata oluştu.</p>
            </div>
        `;
    }
}

// Fetch and display food menu
async function loadFoodMenu(dateStr) {
    try {
        let url = '/api/yemek-menusu';
        if (dateStr) {
            url += '?tarih=' + encodeURIComponent(dateStr);
        }
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success && data.data.length > 0) {
            menuContainer.innerHTML = `
                <div class="menu-grid">
                    ${data.data.map(menu => `
                        <div class="menu-day animate-fade-in">
                            <h4><i class="fas fa-calendar-day"></i> ${menu.gun}</h4>
                            <h5>${menu.ogun}</h5>
                            <ul class="menu-items">
                                ${menu.yemekler.map(yemek => `<li>${yemek}</li>`).join('')}
                            </ul>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            menuContainer.innerHTML = `
                <div class="no-data">
                    <i class="fas fa-info-circle"></i>
                    <p>Yemek menüsü henüz yayınlanmamıştır.</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Yemek menüsü yüklenemedi:', error);
        menuContainer.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Yemek menüsü yüklenirken bir hata oluştu.</p>
            </div>
        `;
    }
}

// Fetch and display weekly food menu
async function loadWeeklyFoodMenu() {
    try {
        const response = await fetch('/api/haftalik-yemek-menusu');
        const data = await response.json();
        
        if (data.success && data.data.length > 0) {
            menuContainer.innerHTML = `
                <div class="weekly-menu-grid">
                    ${data.data.map(menu => `
                        <div class="weekly-menu-day animate-fade-in">
                            <h4><i class="fas fa-calendar-day"></i> ${menu.gun}</h4>
                            <h5>${menu.ogun}</h5>
                            <ul class="weekly-menu-items">
                                ${menu.yemekler.map(yemek => `<li>${yemek}</li>`).join('')}
                            </ul>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            menuContainer.innerHTML = `
                <div class="no-data">
                    <i class="fas fa-info-circle"></i>
                    <p>Haftalık yemek menüsü henüz yayınlanmamıştır.</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Haftalık yemek menüsü yüklenemedi:', error);
        menuContainer.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Haftalık yemek menüsü yüklenirken bir hata oluştu.</p>
            </div>
        `;
    }
}

// Menu toggle functionality
function setupMenuToggle() {
    const gunlukBtn = document.getElementById('gunlukMenuBtn');
    const haftalikBtn = document.getElementById('haftalikMenuBtn');
    
    gunlukBtn.addEventListener('click', () => {
        gunlukBtn.classList.add('active');
        haftalikBtn.classList.remove('active');
        loadFoodMenu();
    });
    
    haftalikBtn.addEventListener('click', () => {
        haftalikBtn.classList.add('active');
        gunlukBtn.classList.remove('active');
        loadWeeklyFoodMenu();
    });
}

// Scroll reveal animation
function revealOnScroll() {
    const reveals = document.querySelectorAll('.reveal');
    
    reveals.forEach(element => {
        const windowHeight = window.innerHeight;
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < windowHeight - elementVisible) {
            element.classList.add('active');
        }
    });
}

// Add scroll event listener for reveal animation
window.addEventListener('scroll', revealOnScroll);

// Intersection Observer for lazy loading
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all content sections
document.querySelectorAll('.content-section').forEach(section => {
    observer.observe(section);
});

// Auto-refresh data every 5 minutes
setInterval(() => {
    loadAnnouncements();
    loadNews();
    loadFoodMenu();
}, 5 * 60 * 1000);

// Error and no-data styles
const style = document.createElement('style');
style.textContent = `
    .error-message, .no-data {
        text-align: center;
        padding: 3rem;
        color: var(--text-gray);
    }
    
    .error-message i, .no-data i {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .error-message {
        color: #dc3545;
    }
    
    .no-data {
        color: #6c757d;
    }
`;
document.head.appendChild(style);

// Ajanda tıklama desteği
function setupCalendarMenu() {
    // Ajanda günlerine tıklama desteği
    const calendar = document.querySelector('.responsive-calendar .days');
    if (!calendar) return;
    calendar.addEventListener('click', function(e) {
        const day = e.target.closest('[data-year][data-month][data-day]');
        if (day) {
            const year = day.getAttribute('data-year');
            const month = day.getAttribute('data-month').padStart(2, '0');
            const date = day.getAttribute('data-day').padStart(2, '0');
            const tarih = `${year}-${month}-${date}`;
            loadFoodMenu(tarih);
            // Seçili günü vurgula
            calendar.querySelectorAll('.selected').forEach(el => el.classList.remove('selected'));
            day.classList.add('selected');
        }
    });
}

function observeCalendarDays() {
    const calendar = document.querySelector('.responsive-calendar .days');
    if (!calendar) return;
    const observer = new MutationObserver(() => {
        setupCalendarMenu();
    });
    observer.observe(calendar, { childList: true, subtree: true });
}

// === Chatbot Balloon Logic ===
const chatbotBalloon = document.getElementById('chatbotBalloon');
const chatbotOpenBtn = document.getElementById('chatbotOpenBtn');
const chatbotCloseBtn = document.getElementById('chatbotCloseBtn');
const chatbotNavBtn = document.getElementById('chatbotNavBtn');
const chatbotForm = document.getElementById('chatbotForm');
const chatbotInput = document.getElementById('chatbotInput');
const chatbotMessages = document.getElementById('chatbotMessages');

// Örnek sorular kutusu
let chatbotSamplesDiv = null;
function showChatbotSamples() {
    if (!chatbotSamplesDiv) {
        chatbotSamplesDiv = document.createElement('div');
        chatbotSamplesDiv.id = 'chatbotSamplesBox';
        chatbotSamplesDiv.innerHTML = `
            <ul class='chatbot-sample-questions'>
                <li>Duyurular neler?</li>
                <li>Haberler neler?</li>
                <li>Bugün yemekte ne var?</li>
            </ul>
        `;
    }
    // inputun hemen üstüne ekle
    const form = document.getElementById('chatbotForm');
    if (form && chatbotSamplesDiv.parentNode !== chatbotBalloon) {
        chatbotBalloon.appendChild(chatbotSamplesDiv); // fallback
    }
    if (form && chatbotSamplesDiv.parentNode !== form.parentNode) {
        form.parentNode.insertBefore(chatbotSamplesDiv, form);
    }
    chatbotSamplesDiv.style.display = 'block';
    setTimeout(() => {
        document.querySelectorAll('.chatbot-sample-questions li').forEach(li => {
            li.style.cursor = 'pointer';
            li.onclick = function() {
                chatbotInput.value = this.textContent;
                chatbotForm.dispatchEvent(new Event('submit'));
            };
        });
    }, 100);
}
function hideChatbotSamples() {
    if (chatbotSamplesDiv) chatbotSamplesDiv.style.display = 'none';
}

function showChatbotWelcome() {
    chatbotMessages.innerHTML = '';
    appendMessage('bot', `Merhaba! Size nasıl yardımcı olabilirim?`);
    showChatbotSamples();
}

// Chatbot açıldığında örnek soruları göster
function openChatbot() {
    chatbotBalloon.classList.add('active');
    chatbotOpenBtn.style.display = 'none';
    chatbotInput.focus();
    showChatbotWelcome();
}
function closeChatbot() {
    chatbotBalloon.classList.remove('active');
    chatbotOpenBtn.style.display = 'flex';
}
chatbotOpenBtn.addEventListener('click', openChatbot);
if (chatbotCloseBtn) chatbotCloseBtn.addEventListener('click', closeChatbot);
if (chatbotNavBtn) chatbotNavBtn.addEventListener('click', function(e) {
    e.preventDefault();
    openChatbot();
});

// Mesajı ekrana yazdır
function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chatbot-message ' + (role === 'user' ? 'user' : 'bot');
    msgDiv.innerHTML = `<div class="bubble">${text}</div>`;
    chatbotMessages.appendChild(msgDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

// Mesaj gönderme
if (chatbotForm) {
    chatbotForm.addEventListener('submit', async function(e) {
        hideChatbotSamples();
        e.preventDefault();
        const userMsg = chatbotInput.value.trim();
        if (!userMsg) return;
        appendMessage('user', userMsg);
        chatbotInput.value = '';
        appendMessage('bot', '<i class="fas fa-spinner fa-spin"></i>');
        try {
            const res = await fetch('/api/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg })
            });
            const data = await res.json();
            // Son bot mesajını (spinner) sil
            const lastBotMsg = chatbotMessages.querySelector('.chatbot-message.bot:last-child');
            if (lastBotMsg) lastBotMsg.remove();
            if (data && data.reply) {
                appendMessage('bot', data.reply);
            } else {
                appendMessage('bot', 'Bir hata oluştu. Lütfen tekrar deneyin.');
            }
        } catch (err) {
            const lastBotMsg = chatbotMessages.querySelector('.chatbot-message.bot:last-child');
            if (lastBotMsg) lastBotMsg.remove();
            appendMessage('bot', 'Bir hata oluştu. Lütfen tekrar deneyin.');
        }
    });
}

// Initialize - Load all data when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadAnnouncements();
    loadNews();
    loadFoodMenu();
    setupCalendarMenu();
    observeCalendarDays();
    setupMenuToggle(); // Call setupMenuToggle here
    
    // Add loading animation to quick access buttons
    document.querySelectorAll('.quick-btn').forEach((btn, index) => {
        btn.style.animationDelay = `${0.1 * index}s`;
        btn.classList.add('animate-fade-in');
    });
    
    // Add hover sound effect (optional)
    const quickBtns = document.querySelectorAll('.quick-btn');
    quickBtns.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.transform = 'scale(1.05)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'scale(1)';
        });
    });
});

// Service Worker Registration (for PWA support)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').then(registration => {
            console.log('ServiceWorker registration successful');
        }).catch(err => {
            console.log('ServiceWorker registration failed: ', err);
        });
    });
} 