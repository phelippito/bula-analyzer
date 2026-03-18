import anthropic
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"Chave encontrada: {api_key[:15]}...")

client = anthropic.Anthropic(api_key=api_key)

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Olá! Responda apenas: API Funcionando!"}
    ]
)

print(message.content[0].text)