"""AI Agent module - handles online and offline AI responses."""
import json
from openai import OpenAI
from config import OPENAI_MODEL, JARVIS_PREFIX

client = OpenAI()

SYSTEM_PROMPT = """Sen Jarvis AI Assistant'sın. Türkçe konuşan, yardımsever, profesyonel bir yapay zeka asistanısın.
Kullanıcının sorularına detaylı ve doğru yanıtlar ver.
Web araması, kod çalıştırma, çeviri ve dosya analizi yapabilirsin.
Yanıtlarını Telegram formatında ver (bold için *text*, italic için _text_)."""

JARVIS_SYSTEM_PROMPT = """Sen Jarvis'sin - Tony Stark'ın kişisel yapay zeka asistanı.
Kullanıcıya her zaman "Efendim" diye hitap et.
Profesyonel, kibar, zeki ve biraz espritüel ol.
İngilizce teknoloji terimlerini kullanabilirsin ama ana dilin Türkçe.
Her yanıtın başında veya uygun yerlerde "Efendim" kullan.
Yanıtlarını Telegram formatında ver (bold için *text*, italic için _text_)."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Web'de arama yapar ve sonuçları döndürür",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Arama sorgusu"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_python_code",
            "description": "Python kodu çalıştırır ve çıktısını döndürür",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Çalıştırılacak Python kodu"
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "translate_text",
            "description": "Metni belirtilen dile çevirir",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Çevrilecek metin"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "Hedef dil (örn: en, tr, de, fr)"
                    }
                },
                "required": ["text", "target_language"]
            }
        }
    }
]


def get_ai_response(messages: list, jarvis_mode: bool = False, tools_enabled: bool = True) -> str:
    """Get response from OpenAI API (online mode)."""
    system_msg = JARVIS_SYSTEM_PROMPT if jarvis_mode else SYSTEM_PROMPT
    full_messages = [{"role": "system", "content": system_msg}] + messages

    try:
        kwargs = {
            "model": OPENAI_MODEL,
            "messages": full_messages,
            "max_tokens": 2000,
            "temperature": 0.7,
        }
        if tools_enabled:
            kwargs["tools"] = TOOLS
            kwargs["tool_choice"] = "auto"

        response = client.chat.completions.create(**kwargs)
        message = response.choices[0].message

        # Handle tool calls
        if message.tool_calls:
            tool_results = []
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                result = execute_tool(func_name, func_args)
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # Add assistant message with tool calls and tool results
            full_messages.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in message.tool_calls
                ]
            })
            full_messages.extend(tool_results)

            # Get final response
            final_response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=full_messages,
                max_tokens=2000,
                temperature=0.7,
            )
            return final_response.choices[0].message.content or "Yanıt oluşturulamadı."

        return message.content or "Yanıt oluşturulamadı."

    except Exception as e:
        return f"⚠️ AI hatası: {str(e)}"


def execute_tool(func_name: str, func_args: dict) -> str:
    """Execute a tool function and return result."""
    if func_name == "web_search":
        return web_search(func_args.get("query", ""))
    elif func_name == "run_python_code":
        return run_python_code(func_args.get("code", ""))
    elif func_name == "translate_text":
        return translate_text(func_args.get("text", ""), func_args.get("target_language", "en"))
    return "Bilinmeyen araç."


def web_search(query: str) -> str:
    """Perform web search using DuckDuckGo."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if results:
                output = ""
                for i, r in enumerate(results, 1):
                    output += f"{i}. {r['title']}\n{r['body']}\n{r['href']}\n\n"
                return output
            return "Sonuç bulunamadı."
    except Exception as e:
        return f"Arama hatası: {str(e)}"


def run_python_code(code: str) -> str:
    """Execute Python code safely."""
    import subprocess
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout
        if result.stderr:
            output += f"\nHata: {result.stderr}"
        return output if output else "Kod çalıştırıldı, çıktı yok."
    except subprocess.TimeoutExpired:
        return "Zaman aşımı: Kod 10 saniye içinde tamamlanamadı."
    except Exception as e:
        return f"Kod çalıştırma hatası: {str(e)}"


def translate_text(text: str, target_language: str) -> str:
    """Translate text using AI."""
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": f"Translate the following text to {target_language}. Only return the translation, nothing else."},
                {"role": "user", "content": text}
            ],
            max_tokens=1000,
        )
        return response.choices[0].message.content or "Çeviri yapılamadı."
    except Exception as e:
        return f"Çeviri hatası: {str(e)}"
