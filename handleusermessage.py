# Yu-Gi-Fly Bot Telegram Bot
# Copyright (C) 2023 Alexelgt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from time import sleep

from telegram import Update

from yugiflybot import supportmethods as support

from yugiflybot.regex import FLY_GROUPS_REGEX, cards_info, animations_info, photos_info

combo_ids = {
    "2-3": "CgACAgQAAx0CR9kKNwACqthgq3YLNSvV7OJUd8lr12juMfimaQACMwIAAr4GpFKVUzYwrKpIhh8E",
    "4": "CgACAgQAAx0CR9kKNwACqvdgq4Xx6S6OBsWLSbphnB_Oo0QrYAACRgIAAvLplVJvgGqtC__wcR8E",
    "5-": "CgACAgQAAx0CR9kKNwACqypgq5ARtetfmZaE420gVc1G-agpEQACxQoAAnd-YFHaxO04cWwkrB8E"
}


async def update_info(update: Update, context):
    print(update)


# ==== Cards ==== #
async def check_cards_text(update: Update, context):
    _, text, _ = support.extract_update_info(update)

    combo_points = 0

    try:
        fly_groups_points = len(FLY_GROUPS_REGEX.findall(text))

        combo_points += fly_groups_points

        for card_value in cards_info.values():
            if bool(card_value["regex"].search(text)):
                if combo_points < 10:
                    await support.send_sticker_message(update, context, card_value["sticker_id"], replyToMessage=True)
                    sleep(1.25)

                combo_points += 1

        if fly_groups_points > 0:
            output_text = f"Detectados {fly_groups_points} grupos fly"
            await support.send_text_message(update, context, output_text, None, replyToMessage=True)
            sleep(1.25)

        if combo_points in range(2, 4):
            output_text = f"💥 <b>¡Combo x{combo_points}!</b>\n\nNo está mal, fly, pero puedes hacerlo mejor."
            await support.send_animation_message(update, context, combo_ids["2-3"], output_text, None, replyToMessage=True)
        elif combo_points == 4:
            output_text = f"💥 <b>¡Combo x{combo_points}!</b>\n\nTu nivel de fly es increíble."
            await support.send_animation_message(update, context, combo_ids["4"], output_text, None, replyToMessage=True)
        elif combo_points >= 5:
            output_text = f"💥 <b>¡Combo x{combo_points}!</b>\n\n¡No puede ser! Has encontrado la última carta y liberado a Flyxodia."
            await support.send_animation_message(update, context, combo_ids["5-"], output_text, None, replyToMessage=True)

    except:
        pass

    await check_animations_photos_text(update, context)
# == Cards == #


# ==== Animations and photos ==== #
async def check_animations_photos_text(update: Update, context):
    _, text, _ = support.extract_update_info(update)

    try:
        for animation_value in animations_info.values():
            if bool(animation_value["regex"].search(text)):
                await support.send_animation_message(update, context, animation_value["animation_id"], None, None, replyToMessage=True)
                sleep(1.25)

        for photo_value in photos_info.values():
            if bool(photo_value["regex"].search(text)):
                await support.send_photo_message(update, context, photo_value["photo_name"], photo_value["output_text"], None, deleteMessage=False, replyToMessage=False, delete_reply_after=None)
                sleep(1.25)
    except:
        pass
# == Animations and photos == #
