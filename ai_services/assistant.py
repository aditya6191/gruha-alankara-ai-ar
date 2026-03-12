"""
LangChain Assistant ("Buddy") for Gruha Alankara.
Handles conversational interactions for automated furniture booking.
"""

from langchain_core.messages import SystemMessage, HumanMessage

class BuddyAgent:
    def __init__(self):
        # We simulate the LangChain LLM setup here
        print("[Buddy] Initializing Language Model parameters...")
        self.memory = [
            SystemMessage(content="You are Buddy, a helpful AI interior design assistant for Gruha Alankara. You speak English, Hindi, and Telugu.")
        ]
        
    def respond_to(self, user_input, lang='en'):
        """
        Processes standard natural language input via LangChain memory patterns.
        """
        self.memory.append(HumanMessage(content=user_input))
        
        from ai_services.cache import AgentCache
        cache = AgentCache()
        
        cache_key = f"{user_input}_{lang}"
        cached_result = cache.get_cached_response(cache_key, lang)
        if cached_result:
            print("[Buddy] Returning cached response.")
            return cached_result
            
        # Simulated intelligent reasoning parsing
        response_text = ""
        user_lower = user_input.lower()
        
        if 'book' in user_lower or 'buy' in user_lower:
             if lang == 'te':
                 response_text = "మీ ఫర్నిచర్‌ని బుక్ చేస్తున్నాను. (Booking your furniture)"
             elif lang == 'hi':
                 response_text = "मैं आपका फर्नीचर बुक कर रहा हूँ। (Booking your furniture)"
             else:
                 response_text = "I'm initiating the booking process for your furniture now."
        else:
             if lang == 'te':
                  response_text = "నేను మీకు ఎలా సహాయపడగలను? (How can I help you?)"
             elif lang == 'hi':
                  response_text = "मैं आपकी कैसे मदद कर सकता हूँ? (How can I help you?)"
             else:
                  response_text = "How can I help you design your perfect room today?"
                  
        return response_text

if __name__ == '__main__':
    agent = BuddyAgent()
    print("Agent says:", agent.respond_to("I want to book the sofa", 'en'))
    print("Agent says (Hindi):", agent.respond_to("book", 'hi'))
