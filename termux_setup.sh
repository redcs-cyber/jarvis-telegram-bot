#!/bin/bash
# ╔══════════════════════════════════════════╗
# ║  🤖 JARVIS AI ASSISTANT                 ║
# ║  Termux Otomatik Kurulum Scripti        ║
# ║  Sınırsız & 7/24 Çalışma               ║
# ╚══════════════════════════════════════════╝

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  🤖 JARVIS AI ASSISTANT KURULUMU        ║"
echo "║  Termux için Otomatik Kurulum           ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Renk tanımları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonksiyonlar
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}
print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}
print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}
print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# 1. Termux paketlerini güncelle
print_info "Paketler güncelleniyor..."
pkg update -y && pkg upgrade -y
print_status "Paketler güncellendi"

# 2. Gerekli paketleri yükle
print_info "Gerekli paketler yükleniyor..."
pkg install -y python git termux-services cronie termux-api
print_status "Paketler yüklendi"

# 3. Python pip güncelle
print_info "Pip güncelleniyor..."
pip install --upgrade pip
print_status "Pip güncellendi"

# 4. Projeyi klonla
print_info "Proje indiriliyor..."
cd ~
if [ -d "jarvis-telegram-bot" ]; then
    rm -rf jarvis-telegram-bot
fi
git clone https://github.com/redcs-cyber/jarvis-telegram-bot.git
cd jarvis-telegram-bot
print_status "Proje indirildi"

# 5. Python bağımlılıklarını yükle
print_info "Python bağımlılıkları yükleniyor..."
pip install python-telegram-bot==21.3 openai python-dotenv duckduckgo-search qrcode Pillow requests
print_status "Bağımlılıklar yüklendi"

# 6. .env dosyasını oluştur
print_info ".env dosyası oluşturuluyor..."
if [ ! -f .env ]; then
    echo "TELEGRAM_BOT_TOKEN=8631747699:AAENsrI9RNevTktESgHpCP-H-NmV-Xl-HHU" > .env
    echo "OPENAI_API_KEY=" >> .env
    echo "OPENAI_MODEL=gpt-4.1-nano" >> .env
fi
print_status ".env dosyası hazır"

# 7. Termux:Boot için otomatik başlatma ayarla
print_info "Otomatik başlatma ayarlanıyor..."
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-jarvis.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd ~/jarvis-telegram-bot
python main.py &
EOF
chmod +x ~/.termux/boot/start-jarvis.sh
print_status "Otomatik başlatma ayarlandı"

# 8. Sınırsız çalışma için wake-lock scripti
print_info "Sınırsız çalışma scripti oluşturuluyor..."
cat > ~/jarvis-telegram-bot/start.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🤖 Jarvis AI Assistant başlatılıyor..."
termux-wake-lock
cd ~/jarvis-telegram-bot

# Eğer zaten çalışıyorsa durdur
pkill -f "python main.py" 2>/dev/null
sleep 2

# Botu başlat
python main.py &
BOT_PID=$!
echo "✅ Bot başlatıldı! PID: $BOT_PID"
echo "📱 Telegram'da /start yazarak kullanabilirsiniz"
echo ""
echo "Durdurmak için: ./stop.sh"
echo "Logları görmek için: cat bot.log"
EOF
chmod +x ~/jarvis-telegram-bot/start.sh

# 9. Durdurma scripti
cat > ~/jarvis-telegram-bot/stop.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🛑 Jarvis durduruluyor..."
pkill -f "python main.py"
termux-wake-unlock
echo "✅ Bot durduruldu"
EOF
chmod +x ~/jarvis-telegram-bot/stop.sh

# 10. Watchdog scripti (bot çökerse otomatik yeniden başlat)
cat > ~/jarvis-telegram-bot/watchdog.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
while true; do
    if ! pgrep -f "python main.py" > /dev/null; then
        echo "$(date): Bot çökmüş, yeniden başlatılıyor..." >> ~/jarvis-telegram-bot/watchdog.log
        cd ~/jarvis-telegram-bot
        python main.py &
    fi
    sleep 30
done
EOF
chmod +x ~/jarvis-telegram-bot/watchdog.sh

# 11. Tam başlatma scripti (watchdog ile)
cat > ~/jarvis-telegram-bot/start-forever.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "╔══════════════════════════════════════════╗"
echo "║  🤖 JARVIS - SINIRSIZ MOD              ║"
echo "╚══════════════════════════════════════════╝"
echo ""
termux-wake-lock

cd ~/jarvis-telegram-bot

# Önceki süreçleri temizle
pkill -f "python main.py" 2>/dev/null
pkill -f "watchdog.sh" 2>/dev/null
sleep 2

# Botu başlat
python main.py &
echo "✅ Bot başlatıldı!"

# Watchdog başlat
./watchdog.sh &
echo "✅ Watchdog aktif (otomatik yeniden başlatma)"
echo ""
echo "📱 Telegram'da /start yazarak kullanın"
echo "🔒 Telefon kilitliyken de çalışmaya devam eder"
echo ""
echo "Durdurmak için: ./stop-forever.sh"
EOF
chmod +x ~/jarvis-telegram-bot/start-forever.sh

# 12. Tam durdurma scripti
cat > ~/jarvis-telegram-bot/stop-forever.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "🛑 Tüm süreçler durduruluyor..."
pkill -f "python main.py"
pkill -f "watchdog.sh"
termux-wake-unlock
echo "✅ Tamamı durduruldu"
EOF
chmod +x ~/jarvis-telegram-bot/stop-forever.sh

print_status "Tüm scriptler oluşturuldu"

# 13. Termux bildirim ayarı
print_info "Termux bildirim ayarlanıyor..."
mkdir -p ~/.termux
echo "wake-lock = true" >> ~/.termux/termux.properties 2>/dev/null
print_status "Bildirim ayarlandı"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  ✅ KURULUM TAMAMLANDI!                 ║"
echo "╠══════════════════════════════════════════╣"
echo "║                                          ║"
echo "║  Başlatma Komutları:                     ║"
echo "║                                          ║"
echo "║  Normal başlatma:                        ║"
echo "║  cd ~/jarvis-telegram-bot && ./start.sh  ║"
echo "║                                          ║"
echo "║  Sınırsız mod (önerilen):                ║"
echo "║  cd ~/jarvis-telegram-bot                ║"
echo "║  ./start-forever.sh                      ║"
echo "║                                          ║"
echo "║  Durdurma:                               ║"
echo "║  ./stop-forever.sh                       ║"
echo "║                                          ║"
echo "╚══════════════════════════════════════════╝"
echo ""
print_warning "ÖNEMLİ: Termux:Boot uygulamasını da yükleyin!"
print_warning "Bu sayede telefon yeniden başlatıldığında bot otomatik açılır."
print_info "Google Play: Termux:Boot"
echo ""

# Botu başlat
print_info "Bot şimdi başlatılıyor..."
termux-wake-lock 2>/dev/null
python main.py &
print_status "🤖 Jarvis aktif! Telegram'da /start yazın."
