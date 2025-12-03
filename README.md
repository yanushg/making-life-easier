# assistant-gatekeeper

A personal AI assistant that sits between you and all the calls/chats you don’t want to handle yourself.

Typical use case: dealing with annoying service providers (cellphone company, utilities, etc.).  
The bot reads incoming messages, understands the context, and replies on your behalf using a pluggable AI engine.

---

## Features

- **Multi-channel support**
  - WhatsApp integration (via provider API such as Meta Cloud API / Twilio)
  - Web chat widget for browser-based conversations

- **AI-powered replies**
  - Central “AI client” interface: plug in OpenAI, local LLM, or any other 3rd-party model
  - Conversation-aware responses (keeps recent context)

- **Conversation orchestration**
  - Unified conversation model for all channels
  - Stores message history and metadata in a database
  - Can be extended to:
    - Ask user for approval before sending replies
    - Escalate to user when confidence is low

- **Configurable rules**
  - Define which types of conversations you don’t want to handle:
    - e.g. `cellphone_provider`, `utilities`, `spam`
  - Future: intent classification, automatic routing

---

## High-Level Architecture

1. **Channels**
   - Webhooks for WhatsApp
   - HTTP / WebSocket API for web chat

2. **Backend (Python)**
   - FastAPI application
   - Endpoints for:
     - `/webhook/whatsapp` – incoming WhatsApp messages
     - `/webchat` – web chat messages
     - `/user-settings` – user preferences & rules

3. **Conversation Engine**
   - Normalizes messages from all channels into one format
   - Loads recent conversation history from the database
   - Builds prompts and calls the selected AI engine
   - Chooses reply text and sends it back via the correct channel

4. **AI / ML Layer**
   - Abstract `AIClient` interface
   - Default implementation can use a hosted LLM (e.g. OpenAI)
   - Can be replaced with a custom or fine-tuned model

5. **Storage**
   - Relational DB (e.g. PostgreSQL) for:
     - Users
     - Conversations
     - Messages
     - Preferences / rules
   - Optional Redis for caching and queues

6. **Background Jobs**
   - Workers (Celery/RQ) for:
     - Long-running AI calls
     - External provider API calls
     - Scheduled follow-ups

---

## Tech Stack (planned)

- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL (via SQLAlchemy / SQLModel)
- **Cache / Queue:** Redis (optional)
- **Workers:** Celery or RQ (optional)
- **AI Engine:** pluggable (OpenAI, local LLM, etc.)

---

## Getting Started

> Note: Adjust commands once the actual code structure is ready.

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/assistant-gatekeeper.git
cd assistant-gatekeeper
2. Create and activate a virtual environment
bash
Copy code
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Environment configuration
Create a .env file (or use environment variables) with values like:

bash
Copy code
# Example only – adapt to your chosen providers
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/assistant_gatekeeper
WHATSAPP_API_TOKEN=your_whatsapp_token_here
WHATSAPP_PHONE_NUMBER_ID=1234567890
AI_PROVIDER=openai              # or "local", "custom"
OPENAI_API_KEY=your_openai_key
5. Run database migrations
bash
Copy code
alembic upgrade head
(If you don’t use Alembic yet, this section can be updated later.)

6. Run the development server
bash
Copy code
uvicorn app.main:app --reload
The API should now be available at: http://localhost:8000

Usage (conceptually)
Configure your WhatsApp provider to send webhooks to:

POST https://your-domain.com/webhook/whatsapp

Embed the web chat widget on your site to talk with the same backend.

The backend:

Receives messages from providers

Stores them as Message records in the database

Calls the AI client to generate a reply

Sends the reply back through WhatsApp or web chat

Future ideas:

Web UI to review and edit conversations

“Approval mode” where AI drafts a reply and waits for your OK

Per-provider profiles (e.g., special behavior for cellphone company vs bank)

Roadmap
 Basic FastAPI structure with WhatsApp webhook endpoint

 Conversation and message models + DB integration

 Simple AIClient with a dummy implementation

 Real AI integration (OpenAI or other)

 Web chat endpoint and simple frontend widget

 Settings for “what I don’t want to handle”

 Optional: admin dashboard for reviewing conversations

Contributing
Right now this is an early-stage personal project.
Guidelines (for future contributors):

Open an issue to discuss big changes

Write clear commit messages

Add tests when adding features or fixing bugs
