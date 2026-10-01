"""
unified_pricing_bot.py
Combines telegram_bot and calculate_project_pricing using composition
"""

import asyncio
import re
import statistics
from datetime import datetime
import signal
import sys
import threading
import os
from gtts import gTTS

# Import our modular components
from telegram_bot import TelegramBot, KnowledgeBase
from calculate_project_pricing import FreelancePriceScraper


class PricingRequestDetector:
    """Detects if a message is a pricing request."""
    
    KEYWORDS = [
        'price', 'pricing', 'cost', 'quote',
        'how much', 'what is the', "what's the",
        'estimate', 'budget', 'rate'
    ]
    
    @classmethod
    def is_pricing_request(cls, text: str) -> bool:
        """Check if message is asking for pricing."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in cls.KEYWORDS)


class ProjectTitleExtractor:
    """Extracts project titles from user messages."""
    
    REMOVE_PHRASES = [
        'what is the price of', 'what is the cost of', "what's the price of",
        'how much for', 'how much does', 'how much is',
        'price of', 'pricing for', 'quote for', 'cost of',
        'i need', 'i want', 'looking for', 'give me',
        'can you', 'could you', 'please', 'tell me',
    ]
    
    @classmethod
    def extract(cls, message: str) -> str:
        """Extract project title from user message."""
        message = message.lower()
        
        for phrase in cls.REMOVE_PHRASES:
            message = message.replace(phrase, '')
        
        message = message.strip()
        message = re.sub(r'\s+', ' ', message)
        message = re.sub(r'^(a|an|the)\s+', '', message)
        message = re.sub(r'[?!.]+$', '', message)
        
        return message.strip() if message else None


class PricingResponseFormatter:
    """Formats pricing results for Telegram."""
    
    @staticmethod
    def format_text(results, exchange_rate, project_title):
        """Format pricing results as text message."""
        lines = []
        lines.append("💰 " + "="*45)
        lines.append(f"PRICING ANALYSIS: {project_title}")
        lines.append("="*48)
        lines.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"💱 1 USD = {exchange_rate:.2f} EGP")
        lines.append("")
        
        # Platform results
        for result in results:
            if 'error' in result:
                lines.append(f"❌ {result['platform']}: Error")
                continue
            
            lines.append(f"🔹 {result['platform']}")
            
            if result.get('hourly_rates') and len(result['hourly_rates']) > 0:
                avg_usd = result['hourly_avg']
                avg_egp = avg_usd * exchange_rate
                min_usd = min(result['hourly_rates'])
                max_usd = max(result['hourly_rates'])
                
                lines.append(f"   ⏰ Hourly:")
                lines.append(f"      ${avg_usd:.0f}/hr (EGP {avg_egp:.0f}/hr) avg")
                lines.append(f"      ${min_usd:.0f}-${max_usd:.0f}/hr range")
            
            if result.get('fixed_prices') and len(result['fixed_prices']) > 0:
                avg_usd = result['fixed_avg']
                avg_egp = avg_usd * exchange_rate
                min_usd = min(result['fixed_prices'])
                max_usd = max(result['fixed_prices'])
                
                lines.append(f"   💵 Fixed:")
                lines.append(f"      ${avg_usd:.0f} (EGP {avg_egp:.0f}) avg")
                lines.append(f"      ${min_usd:.0f}-${max_usd:.0f} range")
            
            lines.append("")
        
        # Summary
        all_hourly, all_fixed = PricingResponseFormatter._collect_prices(results)
        
        lines.append("="*48)
        lines.append("📊 OVERALL SUMMARY")
        lines.append("")
        
        if all_hourly:
            avg_usd = statistics.mean(all_hourly)
            med_usd = statistics.median(all_hourly)
            lines.append(f"⏰ Hourly ({len(all_hourly)} samples):")
            lines.append(f"   Avg: ${avg_usd:.0f}/hr (EGP {avg_usd*exchange_rate:.0f}/hr)")
            lines.append(f"   Med: ${med_usd:.0f}/hr (EGP {med_usd*exchange_rate:.0f}/hr)")
            lines.append("")
        
        if all_fixed:
            avg_usd = statistics.mean(all_fixed)
            med_usd = statistics.median(all_fixed)
            lines.append(f"💵 Fixed ({len(all_fixed)} samples):")
            lines.append(f"   Avg: ${avg_usd:.0f} (EGP {avg_usd*exchange_rate:.0f})")
            lines.append(f"   Med: ${med_usd:.0f} (EGP {med_usd*exchange_rate:.0f})")
            lines.append("")
        
        if not all_hourly and not all_fixed:
            lines.append("⚠️  No pricing data found")
        
        lines.append("="*48)
        return "\n".join(lines)
    
    @staticmethod
    def format_voice(results, exchange_rate, project_title):
        """Format pricing results as voice script."""
        all_hourly, all_fixed = PricingResponseFormatter._collect_prices(results)
        
        script = f"Here is the pricing summary for {project_title}. "
        
        if all_hourly:
            avg = statistics.mean(all_hourly)
            script += f"The average hourly rate is {avg:.0f} dollars per hour. "
        
        if all_fixed:
            avg = statistics.mean(all_fixed)
            script += f"The average fixed price is {avg:.0f} dollars. "
        
        if not all_hourly and not all_fixed:
            script += "Unfortunately, no pricing data was found for this project type."
        
        return script
    
    @staticmethod
    def _collect_prices(results):
        """Collect all prices from results."""
        all_hourly = []
        all_fixed = []
        
        for result in results:
            if 'error' not in result:
                all_hourly.extend(result.get('hourly_rates', []))
                all_fixed.extend(result.get('fixed_prices', []))
        
        return all_hourly, all_fixed


class UnifiedPricingBot:
    """Main application that combines bot and pricing scraper."""
    
    def __init__(self):
        """Initialize the unified bot."""
        print("\n" + "🤖"*35)
        print("   UNIFIED TELEGRAM BOT - FAQ + PRICING")
        print("🤖"*35 + "\n")
        
        # Initialize components
        self.scraper = None
        self.bot = TelegramBot(custom_message_handler=self._custom_message_handler)
        
        # Setup signal handler
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        """Handle shutdown gracefully."""
        print("\n\n🛑 Shutting down...")
        if self.scraper:
            self.scraper.close()
        self.bot.stop()
        sys.exit(0)
    
    async def _custom_message_handler(self, bot_instance, update, context):
        """Custom message handler for pricing requests."""
        user_message = update.message.text
        
        # Check if it's a pricing request
        if PricingRequestDetector.is_pricing_request(user_message):
            project_title = ProjectTitleExtractor.extract(user_message)
            
            if project_title and len(project_title) > 2:
                print(f"\n💰 PRICING REQUEST: {project_title}")
                await self._handle_pricing_request(update, project_title)
                return True  # Handled
            else:
                await update.message.reply_text(
                    "❓ Please be more specific!\n\n"
                    "Example: 'Price of Python web scraping'"
                )
                return True  # Handled
        
        return False  # Not handled, use default FAQ
    
    async def _handle_pricing_request(self, update, project_title):
        """Handle pricing request asynchronously."""
        chat_id = update.effective_user.id
        
        try:
            await update.message.reply_text(
                f"🔍 Searching prices for: {project_title}\n\n⏳ This will take 30-60 seconds..."
            )
            
            # Initialize scraper if needed
            if self.scraper is None:
                self.scraper = FreelancePriceScraper(headless=True)
            
            # Search in background thread
            loop = asyncio.get_event_loop()
            results, exchange_rate = await loop.run_in_executor(
                None, 
                self._search_pricing, 
                project_title
            )
            
            # Format and send text response
            text_response = PricingResponseFormatter.format_text(
                results, exchange_rate, project_title
            )
            await update.message.reply_text(text_response)
            
            # Format and send voice response
            voice_script = PricingResponseFormatter.format_voice(
                results, exchange_rate, project_title
            )
            
            # Generate voice file
            tts = gTTS(text=voice_script, lang='en', slow=False)
            voice_file = f"response_voice_{chat_id}.mp3"
            tts.save(voice_file)
            
            with open(voice_file, 'rb') as voice:
                await update.message.reply_voice(voice=voice)
            
            os.remove(voice_file)
            
            print(f"✅ Pricing sent to chat_id: {chat_id}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            await update.message.reply_text("❌ Sorry, an error occurred. Please try again.")
    
    def _search_pricing(self, project_title):
        """Search pricing (blocking function for executor)."""
        results = self.scraper.search_all(project_title, show_egp=False)
        exchange_rate = self.scraper.get_usd_to_egp_rate()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pricing_{timestamp}.json"
        self.scraper.save_to_json(results, exchange_rate, filename)
        
        return results, exchange_rate
    
    def run(self):
        """Run the unified bot."""
        print("📊 Handles both FAQ and pricing requests")
        print("🔴 Press Ctrl+C to stop\n")
        print("="*70 + "\n")
        print("✅ Bot is ready! Send messages to test.\n")
        
        try:
            self.bot.start_background()
        except KeyboardInterrupt:
            self._signal_handler(signal.SIGINT, None)


# ============ MAIN EXECUTION ============

if __name__ == "__main__":
    app = UnifiedPricingBot()
    app.run()