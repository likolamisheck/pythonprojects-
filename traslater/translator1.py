import nest_asyncio
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction
from deep_translator import GoogleTranslator
from PIL import Image
import easyocr
from io import BytesIO
import logging
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

TOKEN = "7114344377:AAFT2T87oUsLTk0-6cQPXVXBEMvRWSWuiqU"

# Define states for the conversation handler
WAITING_START = 0
LANGUAGE = 1
SELECT_LANGUAGE = 2
UPLOAD_PHOTO = 3
SESSION_CONTROL = 4

class TranslatorBot:
    def __init__(self):
        """Initialize the bot with necessary handlers"""
        self.application = Application.builder().token(TOKEN).build()
        
        # Initialize multiple readers for different language groups
        self.readers = {
            'latin': easyocr.Reader(['en', 'fr', 'es', 'pt', 'it']),
            'cyrillic': easyocr.Reader(['en', 'ru']),
            'arabic': easyocr.Reader(['en', 'ar']),
            'japanese': easyocr.Reader(['en', 'ja']),
            'korean': easyocr.Reader(['en', 'ko']),
            'chinese': easyocr.Reader(['en', 'ch_sim'])
        }
        
        self.translator = GoogleTranslator(target='en')
        self.setup_handlers()

    def setup_handlers(self):
        """Set up command and message handlers"""
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                WAITING_START: [
                    CallbackQueryHandler(self.start_session, pattern='^start_session$')
                ],
                LANGUAGE: [
                    CallbackQueryHandler(self.language_selection)
                ],
                UPLOAD_PHOTO: [
                    MessageHandler(filters.PHOTO, self.handle_image),
                    CallbackQueryHandler(self.end_session, pattern='^end_session$')
                ],
                SESSION_CONTROL: [
                    CallbackQueryHandler(self.handle_session_control)
                ]
            },
            fallbacks=[CommandHandler("start", self.start)]
        )
        
        self.application.add_handler(conversation_handler)

    async def start(self, update: Update, context):
        """Handle the /start command"""
        keyboard = [[InlineKeyboardButton("Start Session", callback_data='start_session')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "👋 Welcome to the OCR Translation Bot!\nClick 'Start Session' to begin:",
            reply_markup=reply_markup
        )
        
        return WAITING_START

    async def start_session(self, update: Update, context):
        """Handle session start"""
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("English", callback_data='en')],
            [InlineKeyboardButton("French", callback_data='fr')],
            [InlineKeyboardButton("Spanish", callback_data='es')],
            [InlineKeyboardButton("German", callback_data='de')],
            [InlineKeyboardButton("Arabic", callback_data='ar')],
            [InlineKeyboardButton("Russian", callback_data='ru')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Please select your target language for translation:",
            reply_markup=reply_markup
        )
        
        return LANGUAGE

    async def language_selection(self, update: Update, context):
        """Handle the selected language"""
        query = update.callback_query
        language = query.data
        context.user_data['target_language'] = language

        await query.answer()
        
        # Create upload photo button
        upload_keyboard = [[KeyboardButton("📸 Upload Photo")]]
        reply_markup = ReplyKeyboardMarkup(upload_keyboard, resize_keyboard=True)
        
        await query.edit_message_text(
            f"🔄 Target language: {language}\n\nPlease upload a photo with text to translate:"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Use the button below or simply send a photo:",
            reply_markup=reply_markup
        )

        return UPLOAD_PHOTO

    async def handle_image(self, update: Update, context):
        """Handle incoming images"""
        try:
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=ChatAction.TYPING
            )

            # Process image (keeping your existing image processing logic)
            photo = await update.message.photo[-1].get_file()
            photo_bytes = await photo.download_as_bytearray()

            temp_image_path = 'temp_image.jpg'
            with open(temp_image_path, 'wb') as f:
                f.write(photo_bytes)

            best_result = []
            best_confidence = 0
            
            for reader_name, reader in self.readers.items():
                try:
                    results = reader.readtext(temp_image_path)
                    if results:
                        confidence = sum(result[2] for result in results) / len(results)
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_result = results
                except Exception as e:
                    logger.error(f"Error with {reader_name} reader: {str(e)}")
                    continue

            try:
                os.remove(temp_image_path)
            except:
                pass

            if not best_result:
                keyboard = [
                    [InlineKeyboardButton("Continue Session", callback_data='continue')],
                    [InlineKeyboardButton("End Session", callback_data='end_session')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    "❌ I couldn't detect any text in this image. Please try again.",
                    reply_markup=reply_markup
                )
                return SESSION_CONTROL

            detected_text = ' '.join([result[1] for result in best_result])
            target_language = context.user_data.get('target_language', 'en')
            
            try:
                translated_text = GoogleTranslator(source='auto', target=target_language).translate(detected_text)
                
                response = (
                    f"📝 Detected Text:\n{detected_text}\n\n"
                    f"🔄 {target_language.upper()} Translation:\n{translated_text}"
                )

                # Add session control buttons
                keyboard = [
                    [InlineKeyboardButton("Continue Session", callback_data='continue')],
                    [InlineKeyboardButton("End Session", callback_data='end_session')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                if len(response) > 4000:
                    chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
                    for chunk in chunks[:-1]:
                        await update.message.reply_text(chunk)
                    await update.message.reply_text(chunks[-1], reply_markup=reply_markup)
                else:
                    await update.message.reply_text(response, reply_markup=reply_markup)

                return SESSION_CONTROL

            except Exception as e:
                logger.error(f"Translation error: {str(e)}")
                keyboard = [
                    [InlineKeyboardButton("Continue Session", callback_data='continue')],
                    [InlineKeyboardButton("End Session", callback_data='end_session')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    "⚠️ Translation error. Please try again.",
                    reply_markup=reply_markup
                )
                return SESSION_CONTROL

        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            keyboard = [
                [InlineKeyboardButton("Continue Session", callback_data='continue')],
                [InlineKeyboardButton("End Session", callback_data='end_session')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "⚠️ Processing error. Please try again.",
                reply_markup=reply_markup
            )
            return SESSION_CONTROL

    async def handle_session_control(self, update: Update, context):
        """Handle session control (continue or end)"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'continue':
            keyboard = [[KeyboardButton("📸 Upload Photo")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
            await query.edit_message_text(
                "Please upload another photo to translate:"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Use the button below or simply send a photo:",
                reply_markup=reply_markup
            )
            return UPLOAD_PHOTO
            
        elif query.data == 'end_session':
            return await self.end_session(update, context)

    async def end_session(self, update: Update, context):
        """End the current session"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [[InlineKeyboardButton("Start New Session", callback_data='start_session')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Session ended. Thank you for using OCR Translation Bot!",
            reply_markup=reply_markup
        )
        return WAITING_START

    async def run(self):
        """Run the bot"""
        await self.application.run_polling()

def main():
    """Main function to run the bot"""
    bot = TranslatorBot()
    
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(bot.run())
    else:
        loop.run_until_complete(bot.run())

if __name__ == "__main__":
    main()