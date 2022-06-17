from telegram import InlineKeyboardMarkup
from telegram.ext import ContextTypes

from db_utils import get_notes
from markup import get_branch_markup, get_module_markup, get_scheme_markup, get_semester_markup, get_subject_markup

function_calls = {
    "scheme": {
        "next": get_branch_markup,
        "previous": get_scheme_markup,
        "previous_step": None
    },
    "branch": {
        "next": get_semester_markup,
        "previous": get_branch_markup,
        "previous_step": "scheme"
    },
    "semester": {
        "next": get_subject_markup,
        "previous": get_semester_markup,
        "previous_step": "branch"
    },
    "subject": {
        "next": get_module_markup,
        "previous": get_subject_markup,
        "previous_step": "semester"
    }
}

async def set_message_text(query: any, text: str, markup: InlineKeyboardMarkup) -> None:
    # CallbackQueries need to be answered, even if no notification to the user is needed
    await query.answer()
    await query.edit_message_text(
        text=text, reply_markup=markup
    )


async def get_document_url(chat_data: dict) -> str:
    note = get_notes(chat_data["subject"], chat_data["module"])
    return note[3]


async def move_forward(current: str, value: str, query: any, context: ContextTypes.DEFAULT_TYPE, **kwargs: any) -> None:
    text = "Choose :"
    context.chat_data[current] = value
    await set_message_text(query, text, await function_calls[current]["next"](**kwargs))


async def move_backward(current: str, query: any, context: ContextTypes.DEFAULT_TYPE, **kwargs: any) -> None:
    text = "Choose :"
    await set_message_text(query, text, await function_calls[current]["previous"](**kwargs))
    context.chat_data["current"] = function_calls[context.chat_data["current"]]["previous_step"]
