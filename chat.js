// Chat functionality for the cybersecurity honeypot
class ChatInterface {
    constructor() {
        this.messageForm = document.getElementById('messageForm');
        this.messageInput = document.getElementById('messageInput');
        this.chatMessages = document.getElementById('chatMessages');
        this.sendButton = document.getElementById('sendButton');
        this.botSelect = document.getElementById('botSelect');
        this.userScore = document.getElementById('userScore');
        this.userTotalScore = document.getElementById('userTotalScore');
        this.userSkillLevel = document.getElementById('userSkillLevel');
        this.recentKeywords = document.getElementById('recentKeywords');
        
        this.isTyping = false;
        this.keywordHistory = new Set();
        
        this.initializeEventListeners();
        this.loadChatHistory();
        
        // Auto-focus on message input
        this.messageInput.focus();
    }
    
    initializeEventListeners() {
        this.messageForm.addEventListener('submit', (e) => this.handleSendMessage(e));
        
        // Enter key to send (but allow Shift+Enter for new lines)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSendMessage(e);
            }
        });
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });
    }
    
    async handleSendMessage(e) {
        e.preventDefault();
        
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;
        
        const selectedBot = this.botSelect.value;
        
        // Disable input during processing
        this.setInputState(false);
        
        // Add user message to chat immediately
        this.addMessage(message, true, selectedBot);
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        
        // Show typing indicator
        this.showTypingIndicator(selectedBot);
        
        try {
            const response = await fetch('/api/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    bot: selectedBot
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            setTimeout(() => {
                this.addMessage(data.bot_response, false, data.bot_name);
                this.updateUserStats(data);
                this.showScorePopup(data.score_added, data.detected_keywords);
                this.updateKeywordHistory(data.detected_keywords);
            }, 500); // Small delay for realism
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, there was an error processing your message. Please try again.', false, 'System', true);
        }
        
        // Re-enable input
        this.setInputState(true);
        this.messageInput.focus();
    }
    
    addMessage(content, isUser, botName, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${isUser ? 'user' : 'bot'}`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit'
        });
        
        if (isUser) {
            messageDiv.innerHTML = `
                <div class="message-bubble ${isError ? 'bg-danger' : ''}">
                    <div class="message-content">${this.escapeHtml(content)}</div>
                    <div class="message-meta">You • ${timeString}</div>
                </div>
            `;
        } else {
            const botIcon = this.getBotIcon(botName);
            messageDiv.innerHTML = `
                <div class="d-flex align-items-start gap-2">
                    <div class="bot-avatar bg-secondary d-flex align-items-center justify-content-center">
                        <i class="${botIcon}"></i>
                    </div>
                    <div class="message-bubble ${isError ? 'bg-danger' : ''}">
                        <div class="message-content">${this.escapeHtml(content)}</div>
                        <div class="message-meta">${botName} • ${timeString}</div>
                    </div>
                </div>
            `;
        }
        
        // Clear initial message if this is the first real message
        const initialMessage = this.chatMessages.querySelector('.text-center.text-muted');
        if (initialMessage) {
            initialMessage.remove();
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator(botName) {
        this.isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator-container';
        typingDiv.innerHTML = `
            <div class="d-flex align-items-start gap-2">
                <div class="bot-avatar bg-secondary d-flex align-items-center justify-content-center">
                    <i class="${this.getBotIcon(botName)}"></i>
                </div>
                <div class="typing-indicator">
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        const typingIndicator = this.chatMessages.querySelector('.typing-indicator-container');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    getBotIcon(botName) {
        const icons = {
            'SecurityExpert': 'fas fa-shield-alt text-primary',
            'TechGuru': 'fas fa-server text-info',
            'DevFriend': 'fas fa-code text-success',
            'NewbieTech': 'fas fa-question-circle text-warning',
            'System': 'fas fa-cog text-danger'
        };
        return icons[botName] || 'fas fa-robot text-secondary';
    }
    
    updateUserStats(data) {
        if (this.userScore) {
            this.userScore.textContent = `Score: ${data.total_score}`;
        }
        if (this.userTotalScore) {
            this.userTotalScore.textContent = data.total_score;
        }
        if (this.userSkillLevel) {
            this.userSkillLevel.textContent = data.skill_level;
            
            // Update skill level color
            this.userSkillLevel.className = 'fs-6 fw-bold';
            if (data.skill_level === 'Avanzado') {
                this.userSkillLevel.className += ' text-success';
            } else if (data.skill_level === 'Intermedio') {
                this.userSkillLevel.className += ' text-warning';
            } else {
                this.userSkillLevel.className += ' text-info';
            }
        }
    }
    
    showScorePopup(scoreAdded, detectedKeywords) {
        if (scoreAdded > 0) {
            const popup = document.createElement('div');
            popup.className = 'score-popup alert alert-success alert-dismissible fade show';
            popup.innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="fas fa-plus-circle me-2"></i>
                    <div>
                        <strong>+${scoreAdded} points!</strong>
                        <div class="small">Keywords detected: ${detectedKeywords.length}</div>
                    </div>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
            
            document.body.appendChild(popup);
            
            // Auto-remove after 3 seconds
            setTimeout(() => {
                if (popup.parentNode) {
                    popup.remove();
                }
            }, 3000);
        }
    }
    
    updateKeywordHistory(detectedKeywords) {
        detectedKeywords.forEach(kw => {
            if (kw.keyword !== 'context_bonus') {
                this.keywordHistory.add(kw.keyword);
            }
        });
        
        this.renderRecentKeywords();
    }
    
    renderRecentKeywords() {
        if (!this.recentKeywords) return;
        
        const keywords = Array.from(this.keywordHistory).slice(-10); // Last 10 keywords
        
        if (keywords.length === 0) {
            this.recentKeywords.innerHTML = '<span class="badge bg-secondary">No topics yet</span>';
            return;
        }
        
        this.recentKeywords.innerHTML = keywords
            .map(keyword => `<span class="badge bg-primary keyword-badge">${this.escapeHtml(keyword)}</span>`)
            .join('');
    }
    
    async loadChatHistory() {
        try {
            const response = await fetch('/api/chat_history');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Update user stats
            if (data.user_score !== undefined) {
                this.updateUserStats({
                    total_score: data.user_score,
                    skill_level: data.skill_level
                });
            }
            
            // Load messages
            if (data.messages && data.messages.length > 0) {
                // Clear initial message
                const initialMessage = this.chatMessages.querySelector('.text-center.text-muted');
                if (initialMessage) {
                    initialMessage.remove();
                }
                
                data.messages.forEach(msg => {
                    this.addMessageFromHistory(msg);
                });
            }
            
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }
    
    addMessageFromHistory(msg) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${msg.is_user_message ? 'user' : 'bot'}`;
        
        if (msg.is_user_message) {
            messageDiv.innerHTML = `
                <div class="message-bubble">
                    <div class="message-content">${this.escapeHtml(msg.content)}</div>
                    <div class="message-meta">You • ${msg.timestamp}${msg.score_added > 0 ? ` • +${msg.score_added} pts` : ''}</div>
                </div>
            `;
        } else {
            const botIcon = this.getBotIcon(msg.bot_name);
            messageDiv.innerHTML = `
                <div class="d-flex align-items-start gap-2">
                    <div class="bot-avatar bg-secondary d-flex align-items-center justify-content-center">
                        <i class="${botIcon}"></i>
                    </div>
                    <div class="message-bubble">
                        <div class="message-content">${this.escapeHtml(msg.content)}</div>
                        <div class="message-meta">${msg.bot_name} • ${msg.timestamp}</div>
                    </div>
                </div>
            `;
        }
        
        this.chatMessages.appendChild(messageDiv);
    }
    
    setInputState(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        this.botSelect.disabled = !enabled;
        
        if (enabled) {
            this.sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        } else {
            this.sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, (m) => map[m]);
    }
}

// Initialize chat interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatInterface();
});

// Add some visual enhancements
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling to chat
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.style.scrollBehavior = 'smooth';
    }
    
    // Add focus states
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('focus', () => {
            messageInput.parentElement.classList.add('border-primary');
        });
        
        messageInput.addEventListener('blur', () => {
            messageInput.parentElement.classList.remove('border-primary');
        });
    }
});

