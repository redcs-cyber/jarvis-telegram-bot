"""Utility tools for the bot - QR code, calculator, URL shortener, etc."""
import subprocess
import qrcode
from io import BytesIO


def generate_qr_code(text: str) -> BytesIO:
    """Generate QR code image from text."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def calculate(expression: str) -> str:
    """Safe calculator."""
    try:
        # Only allow safe characters
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "⚠️ Geçersiz ifade. Sadece sayılar ve +, -, *, /, (, ) kullanın."
        result = eval(expression)
        return f"🧮 {expression} = {result}"
    except ZeroDivisionError:
        return "⚠️ Sıfıra bölme hatası!"
    except Exception as e:
        return f"⚠️ Hesaplama hatası: {str(e)}"


def run_code(code: str) -> str:
    """Run Python code and return output."""
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True, text=True, timeout=10
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += f"\n⚠️ Hata:\n{result.stderr}"
        return output if output.strip() else "✅ Kod çalıştırıldı, çıktı yok."
    except subprocess.TimeoutExpired:
        return "⏱️ Zaman aşımı: Kod 10 saniye içinde tamamlanamadı."
    except Exception as e:
        return f"⚠️ Hata: {str(e)}"


def get_system_stats() -> dict:
    """Get basic system statistics."""
    import platform
    import os
    return {
        "os": platform.system(),
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
