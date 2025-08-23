import re
from typing import Dict, List, Tuple

class KeywordAnalyzer:
    """Analyzes messages for cybersecurity keywords and assigns scores"""
    
    def __init__(self):
        self.keywords = {
            'advanced_security': {
                'keywords': [
                    'penetration testing', 'pentest', 'exploit', 'vulnerability assessment',
                    'threat hunting', 'malware analysis', 'reverse engineering',
                    'forensics', 'incident response', 'apt', 'advanced persistent threat',
                    'zero-day', 'buffer overflow', 'sql injection', 'xss', 'csrf',
                    'privilege escalation', 'lateral movement', 'persistence',
                    'command and control', 'c2', 'backdoor', 'rootkit', 'botnet'
                ],
                'points': 15,
                'category': 'Advanced Security'
            },
            'security_tools': {
                'keywords': [
                    'nmap', 'metasploit', 'burp suite', 'wireshark', 'nessus',
                    'openvas', 'kali linux', 'parrot os', 'john the ripper',
                    'hashcat', 'aircrack', 'hydra', 'sqlmap', 'nikto',
                    'beef', 'ettercap', 'tcpdump', 'volatility', 'autopsy'
                ],
                'points': 12,
                'category': 'Security Tools'
            },
            'security_concepts': {
                'keywords': [
                    'firewall', 'ids', 'ips', 'siem', 'endpoint protection',
                    'antivirus', 'encryption', 'decryption', 'hash', 'digital signature',
                    'certificate', 'pki', 'authentication', 'authorization',
                    'access control', 'multi-factor authentication', 'mfa',
                    'vpn', 'ssl', 'tls', 'https'
                ],
                'points': 8,
                'category': 'Security Concepts'
            },
            'attack_types': {
                'keywords': [
                    'phishing', 'social engineering', 'ransomware', 'trojan',
                    'virus', 'worm', 'spyware', 'adware', 'keylogger',
                    'denial of service', 'dos', 'ddos', 'man in the middle', 'mitm',
                    'eavesdropping', 'spoofing', 'brute force', 'dictionary attack'
                ],
                'points': 10,
                'category': 'Attack Types'
            },
            'compliance_frameworks': {
                'keywords': [
                    'owasp', 'nist', 'iso 27001', 'pci dss', 'hipaa', 'gdpr',
                    'sox', 'compliance', 'audit', 'risk assessment',
                    'vulnerability management', 'security policy'
                ],
                'points': 6,
                'category': 'Compliance & Frameworks'
            },
            'network_security': {
                'keywords': [
                    'network security', 'perimeter defense', 'dmz',
                    'network segmentation', 'vlan', 'nat', 'proxy',
                    'load balancer', 'waf', 'web application firewall',
                    'network monitoring', 'packet analysis'
                ],
                'points': 7,
                'category': 'Network Security'
            }
        }
        
        # Compile regex patterns for better performance
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for all keywords"""
        self.patterns = {}
        for category, data in self.keywords.items():
            patterns = []
            for keyword in data['keywords']:
                # Create pattern that matches whole words
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                patterns.append((pattern, keyword))
            self.patterns[category] = patterns
    
    def analyze_message(self, message: str) -> Tuple[int, List[Dict]]:
        """
        Analyze message for cybersecurity keywords
        Returns: (total_score, list of detected keywords with details)
        """
        message_lower = message.lower()
        total_score = 0
        detected_keywords = []
        
        for category, data in self.keywords.items():
            category_points = data['points']
            category_name = data['category']
            
            for pattern, original_keyword in self.patterns[category]:
                matches = re.findall(pattern, message_lower)
                if matches:
                    # Score each occurrence but with diminishing returns
                    occurrences = len(matches)
                    # First occurrence gets full points, subsequent ones get 50%
                    keyword_score = category_points + (occurrences - 1) * (category_points // 2)
                    total_score += keyword_score
                    
                    detected_keywords.append({
                        'keyword': original_keyword,
                        'category': category_name,
                        'points': keyword_score,
                        'occurrences': occurrences
                    })
        
        # Bonus for context (multiple categories in one message)
        unique_categories = set(kw['category'] for kw in detected_keywords)
        if len(unique_categories) > 1:
            context_bonus = len(unique_categories) * 3
            total_score += context_bonus
            detected_keywords.append({
                'keyword': 'context_bonus',
                'category': 'Context Bonus',
                'points': context_bonus,
                'occurrences': len(unique_categories)
            })
        
        return total_score, detected_keywords
    
    def get_keyword_categories(self) -> List[str]:
        """Get all keyword categories"""
        return [data['category'] for data in self.keywords.values()]
    
    def get_keywords_by_category(self, category: str) -> List[str]:
        """Get all keywords for a specific category"""
        for cat_data in self.keywords.values():
            if cat_data['category'] == category:
                return cat_data['keywords']
        return []
    
    def get_all_keywords(self) -> List[str]:
        """Get all keywords across all categories"""
        all_keywords = []
        for data in self.keywords.values():
            all_keywords.extend(data['keywords'])
        return all_keywords

# Global instance
keyword_analyzer = KeywordAnalyzer()
