# 🤖 Jarvis AI Assistant - Telegram Bot

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)

**Profesyonel, çift modlu (Online/Offline) yapay zeka destekli Telegram asistanı**

</div>

---

## ✨ Özellikler

### 🎩 Jarvis Modu
- Tony Stark'ın Jarvis'i gibi profesyonel ve kibar üslup
- "Efendim" hitabı ile kişiselleştirilmiş deneyim
- `/jarvis` komutu ile anında aktif/pasif

### 🔄 Çift Çalışma Modu
| Özellik | 🟢 Online | 🔴 Offline |
|---------|-----------|------------|
| AI Model | GPT-4.1-nano | Kural Tabanlı |
| Web Arama | ✅ | ❌ |
| Kod Çalıştırma | ✅ | ✅ |
| Çeviri | ✅ | ❌ |
| Temel Sohbet | ✅ | ✅ |
| Hesaplama | ✅ | ✅ |

### 🛠️ Araçlar & Eklentiler
- 🔍 **Web Araması** - DuckDuckGo entegrasyonu
- 💻 **Kod Çalıştırma** - Python kodu çalıştırma
- 🌐 **Çeviri** - Çoklu dil desteği
- 📄 **Dosya Analizi** - TXT, PDF, DOCX dosya okuma
- 🧮 **Hesap Makinesi** - Matematiksel işlemler
- 📱 **QR Kod** - QR kod oluşturma
- 🌤️ **Hava Durumu** - Anlık hava bilgisi
- 📰 **Haberler** - Son dakika haberleri

### 🎨 Arayüz
- Inline keyboard butonları ile kolay navigasyon
- Güzel formatlı mesajlar (bold, italic, emoji)
- Menü sistemi ile kullanıcı dostu deneyim
- Durum göstergeleri (🟢 Online, 🔴 Offline)

---

## 📋 Komutlar

| Komut | Açıklama |
|-------|----------|
| `/start` | Botu başlat, ana menüyü göster |
| `/help` | Tüm komutları listele |
| `/jarvis` | Jarvis modunu aç/kapat |
| `/clear` | Konuşma geçmişini temizle |
| `/search [sorgu]` | Web araması yap |
| `/code [kod]` | Python kodu çalıştır |
| `/translate [dil] [metin]` | Metin çevir |
| `/mode [online/offline]` | Mod değiştir |
| `/settings` | Ayarlar menüsü |
| `/stats` | Kullanım istatistikleri |
| `/calc [ifade]` | Hesap makinesi |
| `/qr [metin]` | QR kod oluştur |
| `/weather [şehir]` | Hava durumu |
| `/news` | Son haberler |

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.9+
- Telegram Bot Token ([BotFather](https://t.me/BotFather))
- OpenAI API Key (online mod için)

### Hızlı Kurulum

```bash
# Repoyu klonla
git clone https://github.com/redcs-cyber/jarvis-telegram-bot.git
cd jarvis-telegram-bot

# Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyasını yapılandır
cp .env.example .env
# .env dosyasını düzenleyin ve token'larınızı ekleyin

# Botu başlat
python3 main.py
```

### Docker ile Kurulum

```bash
docker build -t jarvis-bot .
docker run -d --env-file .env --name jarvis jarvis-bot
```

### Arka Planda Çalıştırma

```bash
nohup python3 main.py > bot.log 2>&1 &
```

---

## 📁 Proje Yapısı

```
jarvis-telegram-bot/
├── main.py                 # Ana uygulama
├── config.py               # Yapılandırma ayarları
├── requirements.txt        # Python bağımlılıkları
├── Dockerfile              # Docker desteği
├── .env.example            # Ortam değişkenleri örneği
├── .gitignore              # Git ignore kuralları
├── README.md               # Bu dosya
├── handlers/
│   ├── __init__.py
│   └── command_handlers.py # Komut ve mesaj işleyicileri
├── utils/
│   ├── __init__.py
│   ├── ai_agent.py         # Online AI motoru
│   ├── offline_engine.py   # Offline kural tabanlı motor
│   └── tools.py            # Yardımcı araçlar
└── models/
    ├── __init__.py
    └── session.py           # Oturum yönetimi
```

---

## 📄 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

<div align="center">
Made with ❤️ by redcs-cyber
</div>
