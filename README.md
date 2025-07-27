# 🧠 HyBe – HSBC's Smart Banking Assistant

HyBe is a Conversational AI system built for HSBC Hackathon 2026. It handles dynamic, multi-step banking interactions like loan applications, card blocking, and account queries — all in natural language.

---

## 🚀 Problem Statement: Conversational AI System

**Goal**: Build an intelligent assistant that can support goal-driven, real-time conversations for:

- 💸 Applying for loans  
- 💳 Blocking a lost or stolen card  
- 📄 Requesting account statements or transaction summaries  
- 🧾 Asking about balances, charges, or interest rates  

The assistant must:
- Support multi-turn interactions
- Understand interruptions and clarifications
- Fetch real-time data from backend or web sources
- Respond contextually and execute tasks live

---

## 🧠 Introducing: **HyBe**

HyBe (short for *Hyper Banking Entity*) is HSBC’s all-in-one smart banking assistant, capable of handling everything from balance queries to processing your entire loan application.

### 💡 Key Features

| Feature | Description |
|--------|-------------|
| 🔐 Guardrails | Refuses to answer non-HSBC or unrelated queries. |
| 🧑‍💼 Personalized | Knows the current logged-in user's details and context. |
| 💬 Multi-turn Flows | Tracks and adapts across user interactions. |
| 🌐 Fallback to Web | Dynamically scrapes HSBC public data when backend data is missing. |
| ⚡ Real-Time Execution | Integrates with backend services to perform actions like blocking cards. |

---

## 🗂️ Database Overview

### `User_Information`

| Column           | Type    | Description                       |
|------------------|---------|-----------------------------------|
| `id`             | Integer | Primary key                       |
| `name`           | String  | Full name of the user             |
| `email`          | String  | User's email address              |
| `account_number` | String  | Unique HSBC account number        |
| `loan_status`    | String  | Status of loan applications       |
| `cards`          | JSON    | List of user's debit/credit cards |

---

## 💬 Documented Conversation Flows

### 🦸 HSBC Hero Mode
- **Before login**: HyBe handles general questions using internal knowledge + web scraping if needed.
- **After login**: HyBe switches to a personalized mode using session-specific user data.

---

### 🏦 Loan Application Flow
1. HyBe initiates the process with: _“Sure, let’s apply for a loan. What type?”_
2. Collects required details step-by-step (type, amount, duration, income, etc.)
3. Confirms inputs and submits to backend.
4. Responds with real-time status and stores the result.

---

### 💳 Card Blocking Flow
- Detects intent: _“I lost my card”_
- Confirms: _“Would you like to block your debit card ending with 1234?”_
- Blocks via backend → confirms success

---

### 📄 Transaction Summary
- Responds to: _“Show my last 5 transactions”_
- Displays bullet-point summaries in chat
- Allows download of detailed PDF/CSV if needed

---

### 💰 Balance and Charges
- Direct Q&A on current balance, interest rates, fee breakdowns
- Context-aware follow-ups: _“Why was ₹500 charged?”_

---

## 🔮 Future Scope

### 🔧 Enhancements in Pipeline

- **🖼️ Image Uploads + OCR**  
  Upload ID proofs or utility bills → auto-fill loan/KYC forms via OCR.

- **🗣️ Voice Interaction**  
  Integrate Whisper or Web Speech API for real-time voice chat.

- **⚠️ Fraud Detection**  
  Analyze behavior and chat intent to detect suspicious activity.

- **🔔 Notification Support**  
  Push updates for application status, card actions, or new charges.

---

## 🛠️ Stack Used

- **Frontend**: HTML/CSS (Flask + Modal UI)  
- **Backend**: Flask (Python)  
- **Database**: SQLite (via SQLAlchemy)  
- **AI Model**: OpenAI GPT with domain-restricted prompt tuning  
- **APIs**: Mock services for account, loan, and card ops

---

## 👥 Team

- Vennela Vallabhaneni  

---

## 🔗 Demo Instructions

1. Clone the repo  
2. `pip install -r requirements.txt`  
3. Run with:  
   ```bash
   flask run
