import os
import json
import openai
from flask import session

openai.api_key = os.getenv("OPENAI_API_KEY")
KNOWLEDGE_BASE_PATH = "hsbc_loan_knowledge.json"

# === 1. Extract keywords using LLM ===
def extract_keywords(question):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract 3–5 keywords for searching HSBC banking info."},
                {"role": "user", "content": question}
            ]
        )
        content = response.choices[0].message.content.strip()
        print("🔍 LLM raw keywords:", content)
        return [kw.strip().lower() for kw in content.split(',') if kw.strip()]
    except Exception as e:
        print("❌ Keyword extraction error:", e)
        return [question.lower()]

# === 2. Search local JSON knowledge base ===
def search_knowledge_base(keywords):
    try:
        with open(KNOWLEDGE_BASE_PATH, "r") as file:
            data = json.load(file)
    except Exception as e:
        print("❌ Error loading knowledge base:", e)
        return []

    results = []
    for kw in keywords:
        for faq in data.get("faqs", []):
            if kw in faq.get("question", "").lower():
                results.append(f"• ❓ {faq['question']}\n  💬 {faq['answer']}")
        for loan in data.get("loan_types", []):
            if kw in loan.get("type", "").lower() or kw in loan.get("description", "").lower():
                results.append(f"• 💼 {loan['type']}:\n  {loan['description']}")
        for news in data.get("latest_news", []):
            if kw in news.get("headline", "").lower() or kw in news.get("summary", "").lower():
                results.append(f"• 📰 {news['headline']}:\n  {news['summary']}")
    return results

# === 3. Fallback LLM-generated answer ===
def generate_llm_response(user_message):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant trained on HSBC banking products like loans, cards, accounts, etc. "
                        "Answer concisely using bullet points only. "
                        "Do not say 'contact HSBC', 'visit the website', or refer the user to any external source."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )
        content = response.choices[0].message.content.strip()
        print("🧠 LLM fallback response:", content)
        return content
    except Exception as e:
        print("❌ LLM fallback error:", e)
        return "• Sorry, I couldn't generate an answer right now."

# === 4. Chatbot entry point ===
def get_hsbc_response(user_message, user=None):
    print("User message:", user_message)

    keywords = extract_keywords(user_message)
    print("xtracted keywords:", keywords)

    kb_results = search_knowledge_base(keywords)
    print("Knowledge base results:", kb_results)

    if kb_results:
        return "\n\n".join(kb_results)

    return generate_llm_response(user_message)
