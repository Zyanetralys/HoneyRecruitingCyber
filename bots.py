import random
import re
from datetime import datetime

class CybersecurityBot:
    """Base class for all bots"""
    
    def __init__(self, name, personality_type):
        self.name = name
        self.personality_type = personality_type
        self.conversation_history = []
    
    def generate_response(self, user_message, user_score=0):
        """Generate response based on bot personality"""
        return "I'm not sure how to respond to that."
    
    def analyze_user_level(self, score):
        """Analyze user technical level based on score"""
        if score >= 151:
            return "advanced"
        elif score >= 51:
            return "intermediate"
        else:
            return "beginner"

class ExpertBot(CybersecurityBot):
    """Advanced cybersecurity expert bot"""
    
    def __init__(self):
        super().__init__("SecurityExpert", "expert")
        self.responses = {
            "greeting": [
                "Hello! I specialize in advanced cybersecurity implementations. What security challenges are you working on?",
                "Greetings! I've been analyzing some interesting attack vectors lately. What brings you here?",
                "Hi there! Always good to meet someone interested in security. What's your current project?"
            ],
            "advanced": [
                "That's an interesting approach. Have you considered the implications for your threat model?",
                "Good point. In my experience with enterprise security, I've seen similar patterns in APT campaigns.",
                "I agree. That technique is particularly effective against zero-day exploits in the wild.",
                "Exactly! That's why we implement defense in depth strategies in critical infrastructure."
            ],
            "intermediate": [
                "That's a solid foundation. You might want to explore more advanced persistence techniques.",
                "Good thinking! Have you looked into how this applies to red team operations?",
                "Interesting perspective. This could be enhanced with some threat intelligence integration."
            ],
            "beginner": [
                "That's a great question! Security is all about understanding the threat landscape first.",
                "Good to see you're interested in learning! Start with understanding common attack vectors.",
                "Welcome to cybersecurity! The fundamentals are crucial - focus on the CIA triad first."
            ],
            "technical": [
                "In my penetration testing experience, I've found that enumeration is key to successful exploitation.",
                "When I analyze malware samples, I always start with behavioral analysis before diving into static analysis.",
                "OWASP Top 10 vulnerabilities are still prevalent, but the real threats are in custom applications.",
                "Advanced persistent threats require sophisticated detection capabilities and threat hunting skills."
            ]
        }
    
    def generate_response(self, user_message, user_score=0):
        user_level = self.analyze_user_level(user_score)
        message_lower = user_message.lower()
        
        # Detect technical keywords to provide advanced responses
        advanced_keywords = ['exploit', 'vulnerability', 'malware', 'pentest', 'apt', 'threat hunting']
        if any(keyword in message_lower for keyword in advanced_keywords):
            return random.choice(self.responses["technical"])
        
        # Respond based on user level
        if "hello" in message_lower or "hi" in message_lower:
            return random.choice(self.responses["greeting"])
        
        return random.choice(self.responses[user_level])

class CasualBot(CybersecurityBot):
    """IT professional who occasionally mentions security"""
    
    def __init__(self):
        super().__init__("TechGuru", "casual")
        self.responses = {
            "greeting": [
                "Hey! I work in IT infrastructure. Always interesting to chat with fellow tech people.",
                "Hi there! Just finished setting up some new servers. What are you working on?",
                "Hello! I manage our company's tech stack. Love discussing technology trends."
            ],
            "security_casual": [
                "Yeah, security is important. We had to update our firewall rules last week.",
                "True, we always make sure to patch our systems regularly. Can't be too careful these days.",
                "Security audits are such a pain, but necessary. Our compliance team is always on us about it.",
                "We use some basic monitoring tools. Nothing too fancy, but it catches the obvious stuff."
            ],
            "tech_general": [
                "I've been working with cloud infrastructure lately. AWS and Azure mostly.",
                "Our network setup is pretty standard. Nothing too exciting, but it works.",
                "We're migrating to containerized applications. Docker has been a game changer.",
                "Database performance optimization keeps me busy. PostgreSQL is solid though."
            ],
            "casual": [
                "That's cool! I'm always learning something new in this field.",
                "Interesting stuff! Technology changes so fast these days.",
                "Nice! I love seeing how different people approach tech problems."
            ]
        }
    
    def generate_response(self, user_message, user_score=0):
        message_lower = user_message.lower()
        
        # Security-related casual responses
        security_keywords = ['security', 'firewall', 'patch', 'vulnerability', 'attack']
        if any(keyword in message_lower for keyword in security_keywords):
            return random.choice(self.responses["security_casual"])
        
        # Tech-related responses
        tech_keywords = ['server', 'network', 'database', 'cloud', 'infrastructure']
        if any(keyword in message_lower for keyword in tech_keywords):
            return random.choice(self.responses["tech_general"])
        
        if "hello" in message_lower or "hi" in message_lower:
            return random.choice(self.responses["greeting"])
        
        return random.choice(self.responses["casual"])

class NormalBot(CybersecurityBot):
    """Regular IT user discussing general technology"""
    
    def __init__(self):
        super().__init__("DevFriend", "normal")
        self.responses = {
            "greeting": [
                "Hi! I'm a developer working on web applications. Nice to meet you!",
                "Hello! I code mostly in Python and JavaScript. What about you?",
                "Hey there! Always good to meet other people in tech."
            ],
            "programming": [
                "I've been learning React lately. The component lifecycle is interesting.",
                "Python is my go-to language. So versatile for different projects.",
                "I'm working on a REST API right now. JSON handling can be tricky sometimes.",
                "Version control with Git has made my life so much easier."
            ],
            "general": [
                "That sounds interesting! I'm always curious about new technologies.",
                "Cool! I love how diverse the tech field is.",
                "Nice! There's always something new to learn in this industry."
            ]
        }
    
    def generate_response(self, user_message, user_score=0):
        message_lower = user_message.lower()
        
        programming_keywords = ['code', 'programming', 'python', 'javascript', 'api', 'development']
        if any(keyword in message_lower for keyword in programming_keywords):
            return random.choice(self.responses["programming"])
        
        if "hello" in message_lower or "hi" in message_lower:
            return random.choice(self.responses["greeting"])
        
        return random.choice(self.responses["general"])

class NoviceBot(CybersecurityBot):
    """Beginner asking basic security questions"""
    
    def __init__(self):
        super().__init__("NewbieTech", "novice")
        self.responses = {
            "greeting": [
                "Hi! I'm pretty new to tech stuff. Still learning the basics!",
                "Hello! I'm trying to understand more about computer security. It's confusing!",
                "Hey! I keep hearing about cybersecurity everywhere. What's it all about?"
            ],
            "questions": [
                "What's the difference between a virus and malware anyway?",
                "Is it true that hackers can just take over your computer remotely?",
                "I heard about something called phishing. How does that work exactly?",
                "Should I be worried about using public WiFi? Everyone says it's dangerous.",
                "What's a firewall supposed to do? I see it mentioned everywhere.",
                "How do people actually become hackers? Is it really that easy?",
                "I don't understand what encryption means. Can you explain it simply?"
            ],
            "confused": [
                "That sounds really complicated! Is there a simpler way to think about it?",
                "Wow, I had no idea it was so complex. Where should someone like me start?",
                "I'm getting lost with all these technical terms. Is there a beginner's guide somewhere?"
            ]
        }
    
    def generate_response(self, user_message, user_score=0):
        message_lower = user_message.lower()
        
        if "hello" in message_lower or "hi" in message_lower:
            return random.choice(self.responses["greeting"])
        
        # Ask questions about security if user mentions technical terms
        security_keywords = ['security', 'hack', 'attack', 'malware', 'virus']
        if any(keyword in message_lower for keyword in security_keywords):
            return random.choice(self.responses["questions"])
        
        # Show confusion for complex topics
        complex_keywords = ['vulnerability', 'exploit', 'penetration', 'forensics']
        if any(keyword in message_lower for keyword in complex_keywords):
            return random.choice(self.responses["confused"])
        
        return random.choice(self.responses["questions"])

class BotManager:
    """Manages all bots and their interactions"""
    
    def __init__(self):
        self.bots = {
            'SecurityExpert': ExpertBot(),
            'TechGuru': CasualBot(),
            'DevFriend': NormalBot(),
            'NewbieTech': NoviceBot()
        }
    
    def get_bot_response(self, bot_name, user_message, user_score=0):
        """Get response from specific bot"""
        if bot_name in self.bots:
            return self.bots[bot_name].generate_response(user_message, user_score)
        return "Bot not available."
    
    def get_random_bot(self):
        """Get a random bot for conversation"""
        return random.choice(list(self.bots.keys()))
    
    def get_all_bot_names(self):
        """Get list of all available bots"""
        return list(self.bots.keys())
