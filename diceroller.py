from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters, CallbackContext
from random import randint
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

ENTER_KEY = "ENTER"
BACKSPACE_KEY = "BACKSPACE"
RESET_KEY = "RESET"
PLUS_KEY = "PLUS"
MINUS_KEY = "MINUS"

NUMBERS = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
]

NUMBER_STATE = 0
SIDES_STATE = 1
MODIFIER_STATE = 2
DONE_STATE = 3

class DiceRollerBuilder:
    def __init__(self):
        self.number = ""
        self.sides = ""
        self.modifier = ""
        self.modifier_sign = "+"

        # NUMBER, SIDES, MODIFIER, DONE
        self.state = NUMBER_STATE

    def new_input(self, input: str):
        if input == RESET_KEY:
            self.__init__()
        elif self.state == NUMBER_STATE:
            if input in NUMBERS:
                self.number += input
            elif input == BACKSPACE_KEY:
                self.number = self.number[:-1]
            elif input == ENTER_KEY and self.number:
                self.state = SIDES_STATE
        elif self.state == SIDES_STATE:
            if input in NUMBERS:
                self.sides += input
            elif input == BACKSPACE_KEY:
                self.sides = self.sides[:-1]
            elif input == ENTER_KEY and self.sides:
                self.state = MODIFIER_STATE
        elif self.state == MODIFIER_STATE:
            if input in NUMBERS:
                self.modifier += input
            elif input == BACKSPACE_KEY:
                self.modifier = self.modifier[:-1]
            elif input == PLUS_KEY:
                self.modifier_sign = "+"
            elif input == MINUS_KEY:
                self.modifier_sign = "-"
            elif input == ENTER_KEY:
                self.state = DONE_STATE


    def reply_text(self):
        if self.state < DONE_STATE:
            number = self.print_number()
            sides = self.print_sides()
            modifier = self.print_modifier()
            if self.state == NUMBER_STATE:
                guide = "Dice number to roll:"
            elif self.state == SIDES_STATE:
                guide = "Enter side number:"
            elif self.state == MODIFIER_STATE:
                guide = "Enter your modifier:"
            else:
                guide = "Rolling..."
            return f"¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\n{guide}\n{number}{sides}{modifier}\n___________________________"
        else:
            # Time to roll baby!
            if self.modifier == "":
                modifier = 0
            elif self.modifier_sign == "-":
                modifier = -1 * int(self.modifier)
            else:
                modifier = int(self.modifier)
            number = int(self.number)
            sides = int(self.sides)
            roll = roll_dice(number, sides, modifier)
            return create_roll_response(roll)


    def print_number(self):
        if self.number:
            return self.number
        else:
            return "Roll my " + "🎲" * 3

    def print_sides(self):
        if self.state >= SIDES_STATE:
            return f"d{self.sides}"
        else:
            return ""

    def print_modifier(self):
        if self.state >= MODIFIER_STATE:
            return f"{self.modifier_sign}{self.modifier}"
        else:
            return ""


    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu


    def button_gen(self):
        if self.state == DONE_STATE:
            return None
        button_list = [
            InlineKeyboardButton("↻", callback_data=RESET_KEY),
            InlineKeyboardButton("←", callback_data=BACKSPACE_KEY),
            InlineKeyboardButton("↵", callback_data=ENTER_KEY),
            InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
            InlineKeyboardButton("4", callback_data='4'),
            InlineKeyboardButton("5", callback_data='5'),
            InlineKeyboardButton("6", callback_data='6'),
            InlineKeyboardButton("7", callback_data='7'),
            InlineKeyboardButton("8", callback_data='8'),
            InlineKeyboardButton("9", callback_data='9'),
            InlineKeyboardButton("+", callback_data=PLUS_KEY),
            InlineKeyboardButton("0", callback_data='0'),
            InlineKeyboardButton("-", callback_data=MINUS_KEY),
        ]
        reply_markup = InlineKeyboardMarkup(self.build_menu(button_list, n_cols=3))
        return reply_markup

def parse_command(arg):
    if "+" in arg:
        remainder, modifier = arg.split("+")
        no_of_dice, no_dice_sides = remainder.split("d")
    elif "-" in arg:
        remainder, modifier = arg.split("-")
        modifier = int(modifier)*-1
        no_of_dice, no_dice_sides = remainder.split("d")
    else:
        no_of_dice, no_dice_sides = arg.split("d")
        modifier = 0

    no_of_dice = int(no_of_dice)
    no_dice_sides = int(no_dice_sides)
    modifier = int(modifier)

    return no_of_dice, no_dice_sides, modifier

def roll_dice(no_of_dice, no_dice_sides, modifier):
    # Limit number of dice roll to something sane
    no_of_dice = min(20, no_of_dice)
    no_dice_sides = min(10000, no_dice_sides)
    rolls = [randint(1, no_dice_sides) for _ in range(no_of_dice)]

    if modifier > 0:
        modifier_text = f"+{modifier}"
    elif modifier < 0:
        modifier_text = f"{modifier}"
    else:
        modifier_text = ""

    value = {
        'parameters': f"{no_of_dice}d{no_dice_sides}{modifier_text}",
        'rolls': rolls,
        'modifier': modifier_text,
        'sum': sum(rolls) + modifier
    }

    return value


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def unknown(update: Update, _context: CallbackContext):
    update.message.reply_text("Sorry, I didn't understand that command.")


def create_roll_response(roll):
    """Craft a message to the user after rolling the dice"""
    list_rolls = " + ".join([str(i) for i in roll.get('rolls')])
    parameters = roll['parameters']
    modifier = roll['modifier']
    sums = str(roll.get("sum"))
    return f"Parameters: {parameters}\nRoll: ({list_rolls}) {modifier} \nYour final roll is: 🎲 {sums} 🎲 "


def roll_command(update: Update, context: CallbackContext):
#   update.message.reply_text(args)
    args = context.args
    if len(args) == 0:
        builder = DiceRollerBuilder()
        context.chat_data["builder"] = builder
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=builder.reply_text(),
                                 reply_markup=builder.button_gen())

    for arg in args:
        try:
            no_of_dice, no_dice_sides, modifier = parse_command(arg)
        except ValueError as err:
            update.message.reply_markdown(f"‼️ Your input '{arg}' was invalid: {err}‼️\n\n💣 Roll dice in the format '1d20+5' for example; no spaces 💣 ")
            continue

        roll = roll_dice(no_of_dice, no_dice_sides, modifier)
        update.message.reply_markdown(create_roll_response(roll))


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def callback(update: Update, context: CallbackContext):
    bot = context.bot
    DDR = update.callback_query
    try:
        builder = context.chat_data['builder']
    except KeyError:
        builder = DiceRollerBuilder()
        context.chat_data['builder'] = builder
    builder.new_input(DDR.data)

    reply_text = builder.reply_text()

    if reply_text != DDR.message.text:
        bot.edit_message_text(chat_id = DDR.message.chat.id,
                              message_id = DDR.message.message_id,
                              reply_markup = builder.button_gen(),
                              text = reply_text)
    else:
        bot.answer_callback_query(callback_query_id = DDR.id,
                                  text = "That did not work. Try again.",
                                  show_alert = True)



def make_bot(token):
    #bot = telegram.Bot(token=token)
    #print(bot.get_me())
    updater = Updater(token=token, use_context=True)

    ##For quicker access to the Dispatcher used by your Updater, you can introduce it locally:
    dispatcher = updater.dispatcher

    ##This is a good time to set up the logging module, so you will know when (and why) things don't work as expected:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

#    testing ...
#    echo_handler = MessageHandler(Filters.text, echo)
#    dispatcher.add_handler(echo_handler)

    roll_handler = CommandHandler("roll", roll_command)
    dispatcher.add_handler(roll_handler)

    callback_handler = CallbackQueryHandler(callback)
    dispatcher.add_handler(callback_handler)

    # this must be last
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    return updater


def start_bot(bot):
    # this will start your bot
    print("Starting bot. Press CTRL+C to stop it.")
    bot.start_polling()
    bot.idle()
    print("Stopping bot")
    bot.stop()


def test_parse_command():
    assert parse_command("2d20+9") == (2, 20, 9)
    assert parse_command("1d20") == (1, 20, 0)


def get_token():
    """
    - TELEGRAM_TOKEN
    - TELEGRAM_TOKEN_FILE
    - `.telegram-token`
    """
    token = os.getenv("TELEGRAM_TOKEN")
    if token:
        return token

    token_file = os.getenv("TELEGRAM_TOKEN_FILE", ".telegram-token"):
    with open(token_file, 'r') as file:
        return file.read().strip()


if __name__ == "__main__":
    token = get_token()
    bot = make_bot(token)
    start_bot(bot)

# TO DO:
#    Advantage
#    Disadvantage
#    Bold important text
#    Don't put telegram token in my code!!!
#    Limit dice number
#    Oh no vanity feature if natural 1
