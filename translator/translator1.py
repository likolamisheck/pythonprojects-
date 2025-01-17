import nest_asyncio
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
LANGUAGE = 1
SELECT_LANGUAGE = 2

class TranslatorBot:
    def __init__(self):
        """Initialize the bot with necessary handlers"""
        self.application = Application.builder().token(TOKEN).build()
        
        # Initialize multiple readers for different language groups
        self.readers = {
            'latin': easyocr.Reader(['en', 'fr', 'es', 'pt', 'it']),  # Latin script languages
            'cyrillic': easyocr.Reader(['en', 'ru']),  # Russian
            'arabic': easyocr.Reader(['en', 'ar']),    # Arabic
            'japanese': easyocr.Reader(['en', 'ja']),  # Japanese
            'korean': easyocr.Reader(['en', 'ko']),    # Korean
            'chinese': easyocr.Reader(['en', 'ch_sim'])  # Simplified Chinese
        }
        
        self.translator = GoogleTranslator(target='en')
        self.setup_handlers()

    def setup_handlers(self):
        """Set up command and message handlers"""
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                LANGUAGE: [CallbackQueryHandler(self.language_selection)],
                SELECT_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_selected_language)]
            },
            fallbacks=[]
        )
        
        self.application.add_handler(conversation_handler)
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_image))

    async def start(self, update: Update, context):
        """Handle the /start command"""
        # Ask the user to select the target language for translation
        keyboard = [
            [InlineKeyboardButton("English", callback_data='en')],
            [InlineKeyboardButton("French", callback_data='fr')],
            [InlineKeyboardButton("Spanish", callback_data='es')],
            [InlineKeyboardButton("German", callback_data='de')],
            [InlineKeyboardButton("Arabic", callback_data='ar')],
            [InlineKeyboardButton("Russian", callback_data='ru')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Welcome to LIGAPHU TranslatOR  Please select your target language for translation:",
            reply_markup=reply_markup
        )
        
        return LANGUAGE

    async def language_selection(self, update: Update, context):
        """Handle the selected language"""
        query = update.callback_query
        language = query.data
        
        # Store the selected language in the context
        context.user_data['target_language'] = language

        await query.answer()
        await query.edit_message_text(
            text=f"You have selected {language} as your target language. NOW UPLOAD A PHOTO FROM YOUR PHONE THROUGH THE CAMERA ROLL"
        )

        # Proceed to handle image translations
        return SELECT_LANGUAGE

    async def handle_selected_language(self, update: Update, context):
        """Handle the user's selected language"""
        user_message = update.message.text
        context.user_data['target_language'] = user_message
        
        await update.message.reply_text(
            f"You have selected {user_message} as your target language. NOW UPLOAD A PHOTO FROM YOUR PHONE THROUGH THE CAMERA ROLL"
        )

        return ConversationHandler.END

    async def handle_image(self, update: Update, context):
        """Handle incoming images"""
        try:
            # Show "processing" status
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id,
                action=ChatAction.TYPING
            )

            # Get the largest version of the photo
            photo = await update.message.photo[-1].get_file()
            photo_bytes = await photo.download_as_bytearray()

            # Save bytes to a temporary file
            temp_image_path = 'temp_image.jpg'
            with open(temp_image_path, 'wb') as f:
                f.write(photo_bytes)

            # Try each reader and collect results
            best_result = []
            best_confidence = 0
            
            for reader_name, reader in self.readers.items():
                try:
                    results = reader.readtext(temp_image_path)
                    if results:
                        # Calculate average confidence
                        confidence = sum(result[2] for result in results) / len(results)
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_result = results
                except Exception as e:
                    logger.error(f"Error with {reader_name} reader: {str(e)}")
                    continue

            # Clean up temporary file
            try:
                os.remove(temp_image_path)
            except:
                pass

            if not best_result:
                await update.message.reply_text(
                    "I couldn't detect any text in this image. "
                    "Please make sure the text is clear and try again."
                )
                return

            # Extract text from results
            detected_text = ' '.join([result[1] for result in best_result])

            target_language = context.user_data.get('target_language', 'en')
            
            try:
                # Translate text
                translated_text = GoogleTranslator(source='auto', target=target_language).translate(detected_text)

                # Format response
                response = (
                    f"Detected Text:\n{detected_text}\n\n"
                    f"{target_language.upper()} Translation:\n{translated_text}"
                )

                # Split response if it's too long
                if len(response) > 4000:
                    chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
                    for chunk in chunks:
                        await update.message.reply_text(chunk)
                else:
                    await update.message.reply_text(response)

            except Exception as e:
                logger.error(f"Translation error: {str(e)}")
                await update.message.reply_text(
                    "I had trouble translating the text. "
                    "Please try again with a clearer image."
                )

        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            await update.message.reply_text(
                " An error occurred while processing your image. "
                "Please try again later."
            )

    async def run(self):
        """Run the bot"""
        await self.application.run_polling()

def main():
    """Main function to run the bot"""
    bot = TranslatorBot()
    
    # Run the bot with proper asyncio handling
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(bot.run())
    else:
        loop.run_until_complete(bot.run())

if __name__ == "__main__":
    main()