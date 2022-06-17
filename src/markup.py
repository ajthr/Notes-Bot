from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from constants import (
    schemes,
    branches,
    semesters,
    modules,
    go_back
)

from db_utils import get_subjects

async def get_scheme_markup() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=scheme["text"], callback_data=scheme["callback_data"])] for scheme in schemes]
    return InlineKeyboardMarkup(keyboard)


async def get_branch_markup() -> InlineKeyboardMarkup:
    branches.append(go_back)
    keyboard = [[InlineKeyboardButton(text=branch["text"], callback_data=branch["callback_data"])] for branch in branches]
    branches.pop()

    return InlineKeyboardMarkup(keyboard)


async def get_semester_markup() -> InlineKeyboardMarkup:
    keyboard = []
    for semester in semesters:
        sem_list = []
        for sem in semester:
            sem_list.append(InlineKeyboardButton(text=sem["text"], callback_data=sem["callback_data"]))
        keyboard.append(sem_list)

    go_back_markup = [InlineKeyboardButton(text=go_back["text"], callback_data=go_back["callback_data"])]
    keyboard.append(go_back_markup)

    return InlineKeyboardMarkup(keyboard)


async def get_subject_markup(scheme: str, branch: str, semester: str) -> InlineKeyboardMarkup:
    subjects = get_subjects(scheme=scheme, branch=branch, semester=semester)
    keyboard = [[InlineKeyboardButton(text=subject[0] + " - " + subject[1], callback_data="subject_" + subject[0].lower())] for subject in subjects]
    go_back_markup = [InlineKeyboardButton(text=go_back["text"], callback_data=go_back["callback_data"])]
    keyboard.append(go_back_markup)

    return InlineKeyboardMarkup(keyboard)


async def get_module_markup() -> InlineKeyboardMarkup:
    modules.append(go_back)
    keyboard = [[InlineKeyboardButton(text=module["text"], callback_data=module["callback_data"])] for module in modules]
    modules.pop()

    return InlineKeyboardMarkup(keyboard)
