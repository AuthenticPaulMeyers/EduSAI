from openai import OpenAI
import os
import time
import random
from dotenv import load_dotenv

load_dotenv(override=True)

def create_chat(prompt, conversation_history):
    """A chat completion with retry/backoff handling for rate limits."""
    api_key = os.getenv("API_KEY") or os.getenv("OPENROUTER_API_KEY")
    max_retries = int(os.getenv("CHAT_MAX_RETRIES", "4"))
    backoff_base = float(os.getenv("CHAT_BACKOFF_BASE", "1.5"))

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # Add user message to the conversation history
    conversation_history.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    )

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            completion = client.chat.completions.create(
                model="kwaipilot/kat-coder-pro:free",
                messages=conversation_history,
                temperature=0.7,
                stream=True
            )

            # Collect streamed chunks safely
            full_response = ""
            for chunk in completion:
                try:
                    # chunks may be dict-like or object-like depending on SDK
                    choice = None
                    if isinstance(chunk, dict):
                        choice = chunk.get("choices", [None])[0]
                        delta = choice.get("delta") if choice else None
                        content = delta.get("content") if isinstance(delta, dict) else None
                    else:
                        choice = getattr(chunk, "choices", [None])[0]
                        delta = getattr(choice, "delta", None)
                        content = getattr(delta, "content", None)

                    if content:
                        full_response += content
                except Exception:
                    # Ignore malformed chunk and continue
                    continue

            # Add AI response to the conversation history
            conversation_history.append({"role": "assistant", "content": full_response})

            return full_response

        except Exception as e:
            err_text = str(e).lower()
            # simple heuristics to detect rate limit / 429
            is_rate_limit = (
                "429" in err_text
                or "rate" in err_text and "limit" in err_text
                or "rate-limited" in err_text
                or "rate_limited" in err_text
            )

            if is_rate_limit and attempt < max_retries:
                sleep_seconds = (backoff_base ** attempt) + random.uniform(0, 1)
                print(f"Rate limited (attempt {attempt}/{max_retries}). Backing off {sleep_seconds:.1f}s and retrying...")
                time.sleep(sleep_seconds)
                continue

            # If not a rate-limit, or we've exhausted retries, log and return friendly message
            print(f"An unexpected error occurred (attempt {attempt}): {e}")
            if is_rate_limit:
                return (
                    "The model is temporarily rate-limited upstream. "
                    "Please try again shortly, or configure your own provider key."
                )
            return "An unexpected error occurred. Please try again."
