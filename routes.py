import os
from datetime import datetime
from flask import render_template, request, jsonify, session
from app import app, db
from models import User, Message, KeywordDetection, BotActivity
from bots import BotManager
from keywords import keyword_analyzer
import uuid
import logging

# Initialize bot manager
bot_manager = BotManager()

@app.route('/')
def index():
    """Main chat interface"""
    # Generate session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    # Get or create user
    user = User.query.filter_by(session_id=session['session_id']).first()
    if not user:
        # Create anonymous user
        username = f"user_{session['session_id'][:8]}"
        user = User(
            username=username,
            session_id=session['session_id']
        )
        db.session.add(user)
        db.session.commit()
    
    # Update last active
    user.last_active = datetime.utcnow()
    db.session.commit()
    
    # Get available bots
    bots = bot_manager.get_all_bot_names()
    
    return render_template('index.html', user=user, bots=bots)

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    # Get statistics
    total_users = User.query.count()
    total_messages = Message.query.count()
    total_keywords = KeywordDetection.query.count()
    
    # Users by skill level
    skill_distribution = db.session.query(
        User.skill_level, 
        db.func.count(User.id)
    ).group_by(User.skill_level).all()
    
    # Top scoring users
    top_users = User.query.filter(User.total_score > 0)\
                         .order_by(User.total_score.desc())\
                         .limit(10).all()
    
    # Recent activity
    recent_messages = db.session.query(Message, User)\
                               .join(User)\
                               .order_by(Message.timestamp.desc())\
                               .limit(50).all()
    
    # Keyword statistics
    keyword_stats = db.session.query(
        KeywordDetection.category,
        db.func.count(KeywordDetection.id).label('count'),
        db.func.sum(KeywordDetection.points).label('total_points')
    ).group_by(KeywordDetection.category)\
     .order_by(db.func.sum(KeywordDetection.points).desc()).all()
    
    return render_template('dashboard.html',
                         total_users=total_users,
                         total_messages=total_messages,
                         total_keywords=total_keywords,
                         skill_distribution=skill_distribution,
                         top_users=top_users,
                         recent_messages=recent_messages,
                         keyword_stats=keyword_stats)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """Handle user message and bot response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        bot_name = data.get('bot', 'SecurityExpert')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get user
        user = User.query.filter_by(session_id=session['session_id']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Analyze message for keywords
        score_added, detected_keywords = keyword_analyzer.analyze_message(user_message)
        
        # Save user message
        user_msg = Message(
            user_id=user.id,
            bot_name=bot_name,
            content=user_message,
            is_user_message=True,
            score_added=score_added
        )
        db.session.add(user_msg)
        db.session.flush()  # Get message ID
        
        # Save detected keywords
        for kw_data in detected_keywords:
            if kw_data['keyword'] != 'context_bonus':  # Skip context bonus for individual tracking
                keyword_detection = KeywordDetection(
                    user_id=user.id,
                    message_id=user_msg.id,
                    keyword=kw_data['keyword'],
                    category=kw_data['category'],
                    points=kw_data['points']
                )
                db.session.add(keyword_detection)
        
        # Update user score and skill level
        user.total_score += score_added
        user.update_skill_level()
        user.last_active = datetime.utcnow()
        
        # Generate bot response
        bot_response = bot_manager.get_bot_response(bot_name, user_message, user.total_score)
        
        # Save bot message
        bot_msg = Message(
            user_id=user.id,
            bot_name=bot_name,
            content=bot_response,
            is_user_message=False,
            score_added=0
        )
        db.session.add(bot_msg)
        
        # Log bot activity
        bot_activity = BotActivity(
            bot_name=bot_name,
            action='responded_to_message',
            target_user_id=user.id,
            details=f"User score: {user.total_score}, Keywords detected: {len(detected_keywords)}"
        )
        db.session.add(bot_activity)
        
        db.session.commit()
        
        response_data = {
            'user_message': user_message,
            'bot_response': bot_response,
            'bot_name': bot_name,
            'score_added': score_added,
            'total_score': user.total_score,
            'skill_level': user.skill_level,
            'detected_keywords': detected_keywords
        }
        
        # Log for monitoring
        logging.info(f"User {user.username} - Score: {user.total_score} - Keywords: {len(detected_keywords)}")
        
        return jsonify(response_data)
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in send_message: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/chat_history')
def get_chat_history():
    """Get chat history for current user"""
    try:
        user = User.query.filter_by(session_id=session['session_id']).first()
        if not user:
            return jsonify({'messages': []})
        
        messages = Message.query.filter_by(user_id=user.id)\
                              .order_by(Message.timestamp.asc())\
                              .limit(100).all()
        
        chat_history = []
        for msg in messages:
            chat_history.append({
                'content': msg.content,
                'is_user_message': msg.is_user_message,
                'bot_name': msg.bot_name,
                'timestamp': msg.timestamp.strftime('%H:%M:%S'),
                'score_added': msg.score_added
            })
        
        return jsonify({
            'messages': chat_history,
            'user_score': user.total_score,
            'skill_level': user.skill_level
        })
        
    except Exception as e:
        logging.error(f"Error in get_chat_history: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/dashboard_data')
def get_dashboard_data():
    """Get dashboard data for charts"""
    try:
        # Skill level distribution
        skill_data = db.session.query(
            User.skill_level, 
            db.func.count(User.id).label('count')
        ).group_by(User.skill_level).all()
        
        skill_distribution = {
            'labels': [item[0] for item in skill_data],
            'data': [item[1] for item in skill_data]
        }
        
        # Keyword category distribution
        keyword_data = db.session.query(
            KeywordDetection.category,
            db.func.count(KeywordDetection.id).label('count')
        ).group_by(KeywordDetection.category).all()
        
        keyword_distribution = {
            'labels': [item[0] for item in keyword_data],
            'data': [item[1] for item in keyword_data]
        }
        
        # Activity over time (last 7 days)
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        daily_activity = db.session.query(
            db.func.date(Message.timestamp).label('date'),
            db.func.count(Message.id).label('message_count')
        ).filter(Message.timestamp >= week_ago)\
         .group_by(db.func.date(Message.timestamp))\
         .order_by('date').all()
        
        activity_chart = {
            'labels': [item[0].strftime('%Y-%m-%d') for item in daily_activity],
            'data': [item[1] for item in daily_activity]
        }
        
        return jsonify({
            'skill_distribution': skill_distribution,
            'keyword_distribution': keyword_distribution,
            'activity_chart': activity_chart
        })
        
    except Exception as e:
        logging.error(f"Error in get_dashboard_data: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html'), 500
