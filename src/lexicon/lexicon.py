class Lexicon:
    COMMANDS = {
        "/start": "Запуск бота",
    }

    LEXICON = {
        "kb_name": {
            "settings_menu": "🏠Меню настроек",
            "back": "⬅️Назад",
            "subscribe": "Подписаться",
            "check_subscription": "✅Готово",
            "boost_check": "Прима {} узнать подробнее",
            "boost_settings": "⚙️Перейти к настройками",
            "boost_settings_one": "Прима {} настроить",
            "register": "✅Зарегистрировался? Продолжим?",
            "continue": "✅Продолжить",
            "personal": "👥Персонал настроить",
            "boost": "🚀Буст {} настроить",
            "company": "🏢Компания настроить",
        },
        "description": (
            "Прима Буст - счастье посуточника поможет заметно сократить время в работе,"
            " сделать твой бизнес прибыльней, а тебя счастливей жми СТАРТ…."
        ),
        "send": {
            "start_subscription": (
                "Я Прима Ассист.\n"
                "Помогу Вам подробно познакомиться с Прима Бустами, которые помогают в  работе посуточнику.\n\n"
                "Но для начала подпишитесь на наш официальный канал."
            ),
            "subscription_fail": "Вы не подписались на канал.",
            "boost_main_menu": "Узнай подробно о действии бустов",
            "boost_info_one": "Буст {boost_name}\n<a href=\"{video_link}\">Ссылка на видео</a>",
            "boost_settings": "Меню настройки бустов",
            "register": "Сперва зарегистрируй личный кабинет на сайте Прима Буст.\n\n{link}",
            "end_instruction": "Настроил? Продолжим?",
            "company": "Отлично.\nДавай настроим компанию, сейчас пришлю инструкцию.",
            "personal": "Давай настроим персонал.",
            "boost": "Пришло время для настройки буста.\nСейчас пришлю инструкции для {}.",
            "end_boost": "Отлично! Настройка буста {} завершена. Для настройки других бустов перейдите в главное меню.",
            "is_end_boost": (
                "✅Вижу, что вы уже прошли настройку одного из бустов✅\n\n"
                "Этап настройки компании и персонала для всех бустов одинаковый.\n"
                "Если вы еще не зарегистрировали личный кабинет на сайте Прима Буст, то зарегистрируйте его по ссылке ниже👇\n"
                "{link}\n\n"
                "Меню для настройки {boost_name}."
            )
        },
        "errors": {
            "video_not_found": "Извините, пока нет описания буста {}.\nВ скором времени добавим.",
            "instruction_not_ready": "Извините, пока нет инструкции  для {}.\nВ скором времени добавим.",
        },
    }

    def __init__(self) -> None:
        self._lexicon = self.LEXICON
        self.description: str = self._lexicon["description"]

        self.cmd: LexiconCmdMsg = LexiconCmdMsg(self.COMMANDS)
        self.send: LexiconMsgSend = LexiconMsgSend(self._lexicon)
        self.kb_name: LexiconMsgKbName = LexiconMsgKbName(self._lexicon)
        self.back_to: LexiconBackToMsg = LexiconBackToMsg(self._lexicon)
        self.errors: LexiconErrorsMsg = LexiconErrorsMsg(self._lexicon)


class LexiconBackToMsg:
    def __init__(self, lexicon: dict) -> None:
        pass


class LexiconErrorsMsg:
    def __init__(self, lexicon: dict) -> None:
        self._lexicon = lexicon["errors"]

        self.video_not_found = self._lexicon["video_not_found"]
        self.instruction_not_ready = self._lexicon["instruction_not_ready"]


class LexiconCmdMsg:
    def __init__(self, commands: dict) -> None:
        self._commands = commands
        self.start = "/start"


class LexiconMsgSend:
    def __init__(self, lexicon: dict) -> None:
        self._lexicon = lexicon["send"]
        self.start_subscription = self._lexicon["start_subscription"]
        self.subscription_fail = self._lexicon["subscription_fail"]

        self.boost_main_menu = self._lexicon["boost_main_menu"]
        self.boost_info_one = self._lexicon["boost_info_one"]

        self.boost_settings = self._lexicon["boost_settings"]

        self.register = self._lexicon["register"]
        self.company = self._lexicon["company"]
        self.personal = self._lexicon["personal"]
        self.boost = self._lexicon["boost"]
        self.end_boost = self._lexicon["end_boost"]

        self.is_end_boost = self._lexicon["is_end_boost"]


class LexiconMsgKbName:
    def __init__(self, lexicon: dict) -> None:
        self._lexicon = lexicon["kb_name"]

        self.settings_menu = self._lexicon["settings_menu"]

        self.back = self._lexicon["back"]
        self.continue_btn = self._lexicon["continue"]

        self.subscribe = self._lexicon["subscribe"]
        self.check_subscription = self._lexicon["check_subscription"]

        self.boost_check = self._lexicon["boost_check"]
        self.boost_settings = self._lexicon["boost_settings"]

        self.boost_settings_one = self._lexicon["boost_settings_one"]

        self.register = self._lexicon["register"]

        self.personal = self._lexicon["personal"]
        self.boost = self._lexicon["boost"]
        self.company = self._lexicon["company"]
