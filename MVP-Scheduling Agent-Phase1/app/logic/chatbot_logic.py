def get_bot_response(user_message: str) -> str:
    msg = user_message.strip().lower()

    if "hi" in msg or "hello" in msg:
        return "Hello! 👋 Welcome to SunnyBot.\nChoose: 1) Courses, 2) Pricing, 3) Schedule a demo."
    elif msg == "1":
        return "We offer AI, ML, and Python courses.\nReply a) AI or b) Python."
    elif msg == "a":
        return "Our AI course covers GenAI, Agents, and RAG.\nReply 'syllabus' for details or 'fees' for pricing."
    elif msg == "syllabus":
         return (
        "🧠 *AI Course Syllabus*\n\n"
        "📘 *Module 1: Generative AI Fundamentals*\n"
        "• Introduction to LLMs (GPT, Claude, Gemini, etc.)\n"
        "• Prompt engineering and chain-of-thought basics\n"
        "• Building text, image, and code generation apps\n\n"
        "🤖 *Module 2: Agentic AI Systems*\n"
        "• Understanding autonomous and tool-using agents\n"
        "• Building multi-agent workflows using LangChain/LangGraph\n"
        "• Real-world use cases: YouTube → Blog, Data Summarizers, Task Automators\n\n"
        "📚 *Module 3: RAG (Retrieval-Augmented Generation)*\n"
        "• How RAG improves LLM accuracy\n"
        "• Vector databases (FAISS, Chroma)\n"
        "• Building context-aware chatbots with private data\n\n"
        "🧩 *Module 4: Project & Deployment*\n"
        "• End-to-end project implementation\n"
        "• Connecting APIs and hosting your AI apps\n"
        "• Integration with frontend or WhatsApp bots\n\n"
        "Reply 'fees' to know about the course pricing 💰"
    )
    elif msg == "fees":
         return (
        "💰 *Course Fees Details*\n\n"
        "The complete *AI Mastery Program* (covering GenAI, Agents, and RAG) is available in two options:\n\n"
        "🎓 *Basic Plan* – ₹4,999\n"
        "• Access to recorded sessions\n"
        "• 3 mini-projects\n"
        "• Lifetime access to materials\n\n"
        "🚀 *Pro Plan* – ₹8,999\n"
        "• Live mentor-led sessions\n"
        "• 5+ real-world projects (YouTube → Blog, Chatbot, RAG App, etc.)\n"
        "• 1:1 project guidance & resume support\n"
        "• Certificate of completion\n\n"
        "Flexible EMI and group discounts available 🎯\n\n"
        "Reply 'enroll' to get registration details or 'syllabus' to review the course modules again."
    )
    elif msg == "yes":
        return "Pricing:\nAI: ₹25,000\nML: ₹20,000\nPython: ₹15,000"
    elif msg == "no":
        return "You can schedule a demo by replying with your preferred date and time."
    elif msg == "enroll":
        return "Need help with enrollment? Just reply 'support' and our team will assist you 🤝"
    elif msg == "support":
        return "Thanks for contacting us! Our team will reach out to you within next 24 hours 🤝"
    else:
        return "Sorry, I didn’t understand. Please reply with a valid option."
