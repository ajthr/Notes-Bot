#!/usr/bin/env python
import os

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from db_utils import connect_db
from utils import move_backward, move_forward, get_document_url
from markup import get_scheme_markup


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query.data != "go_back":
        code_list = str(query.data).split("_")
        context.chat_data["current"] = code_list[0]
        if code_list[0] == "scheme":
            await move_forward(current=context.chat_data["current"], value=code_list[1], query=query, context=context)

        elif code_list[0] == "branch":
            await move_forward(current=context.chat_data["current"], value=code_list[1], query=query, context=context)

        elif code_list[0] == "semester":
            config = {
                "scheme": context.chat_data["scheme"],
                "branch": context.chat_data["branch"],
                "semester": code_list[1],
            }
            await move_forward(current=context.chat_data["current"], value=code_list[1], query=query, context=context, **config)

        elif code_list[0] == "subject":
            await move_forward(current=context.chat_data["current"], value=code_list[1], query=query, context=context)

        elif code_list[0] == "module":
            context.chat_data["module"] = code_list[1]
            url = await get_document_url(context.chat_data)

            await query.delete_message()
            await context.bot.send_document(context._chat_id, url)

            # clear chat context after use
            context.chat_data.clear()
            await query.answer("Done!")

        else:
            await query.answer("Wrong Input!")
    else:
        if context.chat_data["current"] != "subject":
            await move_backward(current=context.chat_data["current"], query=query, context=context)
        else:
            config = {
                "scheme": context.chat_data["scheme"],
                "branch": context.chat_data["branch"],
                "semester": context.chat_data["semester"]
            }
            await move_backward(current=context.chat_data["current"], query=query, context=context, **config)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Choose :", reply_markup=await get_scheme_markup())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start to use this bot.")


def main() -> None:
    # Create the Application
    application = Application.builder().token(os.environ.get("BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(callback))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    cursor = connect_db()
    if cursor is not None:
        main()
    else:
        print("Cannot connect to database!")
        exit(0)
