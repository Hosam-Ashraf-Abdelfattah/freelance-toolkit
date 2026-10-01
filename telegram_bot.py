"""
telegram_bot.py - Modular Version
Can run standalone OR be imported as a module
"""

import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import queue
import threading
from typing import Dict, List, Optional, Callable
from abc import ABC, abstractmethod


# Bot Configuration
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class MessageLogger:
    """Handles logging of all bot messages."""
    
    def __init__(self):
        """Initialize message logger."""
        self.message_queue = queue.Queue()
    
    def log(self, user_info: Dict, message_type: str, content: str):
        """Log a message to console and queue."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        username = user_info.get('username', 'Unknown')
        user_id = user_info.get('id', 'N/A')
        first_name = user_info.get('first_name', '')
        
        print("\n" + "="*70)
        print(f"⏰ TIME: {timestamp}")
        print(f"👤 USER: {first_name} (@{username}) [ID: {user_id}]")
        print(f"📝 TYPE: {message_type}")
        print(f"💬 MESSAGE: {content}")
        print("="*70)
        
        self.message_queue.put({
            'timestamp': timestamp,
            'user': username,
            'user_id': str(user_id),
            'first_name': first_name,
            'type': message_type,
            'text': content,
            'content': content
        })
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """Get recent messages from queue."""
        messages = []
        temp_queue = queue.Queue()
        
        while not self.message_queue.empty() and len(messages) < limit:
            msg = self.message_queue.get()
            messages.append(msg)
            temp_queue.put(msg)
        
        while not temp_queue.empty():
            self.message_queue.put(temp_queue.get())
        
        return messages[::-1]


class VoiceProcessor:
    """Handles voice message processing."""
    
    def __init__(self):
        """Initialize voice processor."""
        self.recognizer = sr.Recognizer()
    
    async def process_voice(self, voice_file, user_id: int) -> Optional[str]:
        """Process voice message and convert to text."""
        voice_path = f"voice_{user_id}.ogg"
        wav_path = f"voice_{user_id}.wav"
        
        try:
            await voice_file.download_to_drive(voice_path)
            audio = AudioSegment.from_ogg(voice_path)
            audio.export(wav_path, format="wav")
            
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
            
            return text
            
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"Voice processing error: {e}")
            return None
        finally:
            if os.path.exists(voice_path):
                os.remove(voice_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)
    
    @staticmethod
    def text_to_speech(text: str, user_id: int, language: str = 'en') -> str:
        """Convert text to speech file."""
        tts = gTTS(text=text, lang=language, slow=False)
        voice_file = f"response_voice_{user_id}.mp3"
        tts.save(voice_file)
        return voice_file


class KnowledgeBase:
    """Manages bot knowledge and FAQ responses."""
    
    def __init__(self, data: Optional[Dict[str, str]] = None):
        """Initialize knowledge base."""
        self.data = data or self._get_default_data()
    
    def _get_default_data(self) -> Dict[str, str]:
        """Get default knowledge base data."""
        return {
            "support": "Support is available 24/7 via email at support@company.com or call +1-555-0123",
            "hours": "We are open Monday-Friday 9AM-6PM EST, closed on weekends and holidays",
            "return_policy": "We offer a 30-day money-back guarantee. No questions asked!",
            "shipping": "Free shipping on orders over $50. Standard delivery takes 3-5 business days.",
            "contact": "Email: info@company.com | Phone: +1-555-0100 | Address: 123 Main St, City, State",
            "demo": "Book a free demo at https://company.com/demo or reply with your email",
            "features": "Our platform includes: Analytics Dashboard, API Access, Team Collaboration, Custom Reports, and 24/7 Support",
        }
    
    def search(self, query: str) -> List[tuple]:
        """Search knowledge base for matching topics."""
        query_lower = query.lower().strip()
        matches = []
        
        for key, value in self.data.items():
            if key in query_lower or query_lower in key:
                matches.append((key, value))
        
        return matches
    
    def get_all_topics(self) -> List[str]:
        """Get list of all available topics."""
        return list(self.data.keys())


class TelegramBot:
    """Main Telegram bot with clean API for external use."""
    
    def __init__(self, token: str = BOT_TOKEN, 
                 knowledge_base: Optional[KnowledgeBase] = None,
                 custom_message_handler: Optional[Callable] = None):
        """
        Initialize Telegram bot.
        
        Args:
            token: Bot token from BotFather
            knowledge_base: Optional KnowledgeBase instance
            custom_message_handler: Optional custom handler for messages
        """
        if not token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN is not set. Copy .env.example to .env "
                "and add your token from @BotFather."
            )
        self.token = token
        self.knowledge_base = knowledge_base or KnowledgeBase()
        self.logger = MessageLogger()
        self.voice_processor = VoiceProcessor()
        self.custom_message_handler = custom_message_handler
        
        self.app: Optional[Application] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
    
    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user_info = self._get_user_info(update)
        self.logger.log(user_info, "COMMAND", "/start")
        
        welcome_msg = (
            "👋 Welcome to our Customer Support Bot!\n\n"
            "💬 **How to use:**\n"
            "• Type keywords like: pricing, support, hours, shipping, etc.\n"
            "• Send a voice message and I'll convert it to text\n"
            "• Use /help to see available topics\n\n"
            "How can I help you today?"
        )
        
        await update.message.reply_text(welcome_msg)
    
    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        user_info = self._get_user_info(update)
        self.logger.log(user_info, "COMMAND", "/help")
        
        topics = "\n".join([f"• {topic}" for topic in self.knowledge_base.get_all_topics()])
        help_msg = (
            "📚 **Available Topics:**\n\n"
            f"{topics}\n\n"
            "Just type a keyword or ask your question!"
        )
        
        await update.message.reply_text(help_msg)
    
    async def _handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages."""
        user_info = self._get_user_info(update)
        user_message = update.message.text
        
        self.logger.log(user_info, "TEXT", user_message)
        
        # If custom handler is provided, use it
        if self.custom_message_handler:
            handled = await self.custom_message_handler(self, update, context)
            if handled:
                return
        
        # Default FAQ handling
        matches = self.knowledge_base.search(user_message)
        
        if matches:
            for topic, answer in matches:
                response = f"📋 **{topic.upper()}**\n\n{answer}"
                await update.message.reply_text(response)
        else:
            fallback_msg = (
                "🤔 I'm not sure about that. Try asking about:\n\n"
                + "\n".join([f"• {t}" for t in self.knowledge_base.get_all_topics()[:5]])
                + "\n\nOr use /help to see all topics."
            )
            await update.message.reply_text(fallback_msg)
    
    async def _handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages."""
        user_info = self._get_user_info(update)
        self.logger.log(user_info, "VOICE", "🎤 Voice message received")
        
        await update.message.reply_text("🎧 Processing your voice message...")
        
        voice = await update.message.voice.get_file()
        text = await self.voice_processor.process_voice(voice, update.effective_user.id)
        
        if text:
            self.logger.log(user_info, "VOICE_TRANSCRIBED", f"'{text}'")
            await update.message.reply_text(f"📝 You said: \"{text}\"")
            
            # Process as text
            update.message.text = text
            await self._handle_text(update, context)
        else:
            await update.message.reply_text("❌ Could not understand the audio. Please try again.")
    
    def _get_user_info(self, update: Update) -> Dict:
        """Extract user info from update."""
        return {
            'username': update.effective_user.username,
            'id': update.effective_user.id,
            'first_name': update.effective_user.first_name
        }
    
    def start_background(self):
        """Start bot in background thread."""
        print("\n" + "🤖"*35)
        print("   TELEGRAM CRM BOT - MONITORING ACTIVE")
        print("🤖"*35 + "\n")
        print("📊 All customer conversations will appear below")
        print("🔴 Bot running in background\n")
        print("="*70 + "\n")
        
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.app = Application.builder().token(self.token).build()
        
        # Register handlers
        self.app.add_handler(CommandHandler("start", self._start_command))
        self.app.add_handler(CommandHandler("help", self._help_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_text))
        self.app.add_handler(MessageHandler(filters.VOICE, self._handle_voice))
        
        # Start bot
        self.loop.run_until_complete(self.app.initialize())
        self.loop.run_until_complete(self.app.start())
        self.loop.run_until_complete(self.app.updater.start_polling())
        
        self.loop.run_forever()
    
    def stop(self):
        """Stop the bot gracefully."""
        if self.app and self.loop:
            asyncio.run_coroutine_threadsafe(self.app.updater.stop(), self.loop)
            asyncio.run_coroutine_threadsafe(self.app.stop(), self.loop)
            asyncio.run_coroutine_threadsafe(self.app.shutdown(), self.loop)
            self.loop.stop()
    
    # ============ PUBLIC API METHODS ============
    
    async def send_message(self, chat_id: int, message: str) -> bool:
        """Send text message to user."""
        if not self.app:
            print("❌ Bot is not running")
            return False
        
        try:
            await self.app.bot.send_message(chat_id=chat_id, text=message)
            self.logger.log({'username': 'API', 'id': 'SYSTEM', 'first_name': 'External'}, 
                           "SENT_MESSAGE", f"To {chat_id}: {message}")
            return True
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    async def send_voice(self, chat_id: int, text: str, language: str = 'en') -> bool:
        """Send voice message to user."""
        if not self.app:
            print("❌ Bot is not running")
            return False
        
        try:
            voice_file = self.voice_processor.text_to_speech(text, chat_id, language)
            
            with open(voice_file, 'rb') as voice:
                await self.app.bot.send_voice(chat_id=chat_id, voice=voice)
            
            os.remove(voice_file)
            
            self.logger.log({'username': 'API', 'id': 'SYSTEM', 'first_name': 'External'}, 
                           "SENT_VOICE", f"To {chat_id}: {text}")
            return True
        except Exception as e:
            print(f"❌ Error sending voice: {e}")
            return False
    
    def send_message_sync(self, chat_id: int, message: str) -> bool:
        """Synchronous wrapper for send_message."""
        if not self.loop:
            return False
        
        future = asyncio.run_coroutine_threadsafe(
            self.send_message(chat_id, message), self.loop
        )
        try:
            return future.result(timeout=10)
        except:
            return False
    
    def send_voice_sync(self, chat_id: int, text: str, language: str = 'en') -> bool:
        """Synchronous wrapper for send_voice."""
        if not self.loop:
            return False
        
        future = asyncio.run_coroutine_threadsafe(
            self.send_voice(chat_id, text, language), self.loop
        )
        try:
            return future.result(timeout=10)
        except:
            return False
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """Get recent messages from logger."""
        return self.logger.get_recent_messages(limit)


# ============ STANDALONE MODE ============

if __name__ == "__main__":
    bot = TelegramBot()
    
    try:
        bot.start_background()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        bot.stop()
        print("✅ Bot stopped")