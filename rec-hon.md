# Cybersecurity Honeypot Recruitment System

## Overview

This is a cybersecurity recruitment honeypot system designed to simulate a technical forum environment where users interact with AI bots. The system evaluates users' cybersecurity knowledge through natural conversation, keyword detection, and scoring mechanisms. It serves as a controlled environment for assessing technical skills while maintaining detailed analytics on user interactions and knowledge levels.

The application creates an engaging chat interface where users can discuss cybersecurity topics with different AI personalities, each designed to evaluate different skill levels and provide appropriate responses based on detected expertise.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Flask with Jinja2 templates
- **UI Framework**: Bootstrap 5 with dark theme
- **JavaScript**: Vanilla JS with async/await for API communication
- **Real-time Updates**: AJAX-based chat interface with auto-refresh dashboard
- **Responsive Design**: Mobile-friendly layout with collapsible navigation

The frontend provides two main interfaces:
1. Chat interface for user-bot interactions
2. Analytics dashboard for monitoring user activity and system metrics

### Backend Architecture
- **Framework**: Flask web framework
- **Database ORM**: SQLAlchemy with declarative base
- **Session Management**: Flask sessions with UUID-based session IDs
- **Logging**: Python logging module configured for debugging
- **Middleware**: ProxyFix for proper handling of proxy headers

**Core Components**:
- **Bot Management System**: Modular bot classes with different personalities (Expert, Intermediate, Beginner)
- **Keyword Analysis Engine**: Real-time analysis of user messages for cybersecurity terms
- **Scoring System**: Dynamic scoring based on detected keywords and user interactions
- **User Profiling**: Automatic skill level classification based on accumulated scores

**API Design**:
- RESTful endpoints for chat functionality
- Real-time data endpoints for dashboard updates
- Session-based user tracking without requiring authentication

### Data Storage Solutions
- **Primary Database**: PostgreSQL with SQLAlchemy ORM
- **Connection Pooling**: Configured with pool recycling and pre-ping health checks
- **Database Models**:
  - User: Session-based user profiles with scoring and skill levels
  - Message: Complete conversation history with metadata
  - KeywordDetection: Detailed tracking of detected cybersecurity terms
  - BotActivity: Bot interaction logging and analytics

**Data Relationships**:
- One-to-many relationships between users and messages/keywords
- Cascade deletion for maintaining data integrity
- Automatic timestamp tracking for all interactions

### Security and Session Management
- **Session Security**: Environment-variable based secret keys
- **Anonymous Users**: UUID-based session tracking without requiring registration
- **Data Isolation**: Session-based data segregation
- **Input Validation**: Server-side validation for all user inputs

### Bot Intelligence System
**Multi-tier Bot Architecture**:
- **ExpertBot**: Advanced cybersecurity discussions and complex scenarios
- **Personality-based Responses**: Dynamic response generation based on user skill level
- **Context Awareness**: Conversation history tracking for coherent interactions
- **Adaptive Behavior**: Responses adjust based on detected user expertise level

**Keyword Analysis Engine**:
- **Real-time Processing**: Immediate analysis of user messages
- **Hierarchical Scoring**: Different point values for various cybersecurity domains
- **Category Classification**: Advanced Security, Security Tools, Security Concepts, Attack Types
- **Progressive Difficulty**: Content complexity adapts to user's demonstrated knowledge

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web framework for route handling and templating
- **SQLAlchemy**: Database ORM and connection management
- **PostgreSQL**: Primary database system (configurable via DATABASE_URL)
- **Werkzeug**: WSGI utilities and proxy handling

### Frontend Dependencies
- **Bootstrap 5**: UI framework with dark theme support
- **Font Awesome**: Icon library for enhanced user interface
- **Chart.js**: Data visualization for analytics dashboard

### Development and Deployment
- **Python Logging**: Built-in logging for debugging and monitoring
- **Environment Variables**: Configuration management for database URLs and secrets
- **UUID**: Session identifier generation
- **Regular Expressions**: Keyword pattern matching and text analysis

### Optional Integrations
The system is designed to be self-contained but can be extended with:
- External threat intelligence APIs
- Additional database backends through SQLAlchemy
- Third-party authentication providers
- Real-time notification systems
- Advanced analytics platforms

The architecture emphasizes modularity and extensibility, allowing for easy addition of new bot personalities, keyword categories, and analysis features without disrupting the core system functionality.
