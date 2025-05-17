async def create_ad_message(data):
    title = data['title'].replace('_', '\\_').replace('*', '\\*')
    description = data['description'].replace('_', '\\_').replace('*', '\\*')
    image_id = data['image']
    price = data['price']
    user_tag = data["user_tag"].replace('_', '\\_').replace('*', '\\*')
    ads_id = data["ads_id"]

    # Формируем текст сообщения
    message_text = (
        f"\t\t\t\t*{title}*\n\n"
        f"\t\t\t\t{description}\n\n"
        f"💰 *Цена:* {price}₽\n"
        f"🤝 *Продавец:* @{user_tag}\n"
        f"🆔 *ID:* {ads_id}\n"
    )

    return message_text, image_id


def start_message(name, tgk_address):
    tgk_address = tgk_address.replace('_', '\\_').replace('*', '\\*')
    message_text = (
        f"*Здравствуйте, {name}! Мы рады приветствовать вас!* 🎉\n\n"
        "*Что мы предлагаем?*\n"
        "В нашем сервисе вы можете _размещать_ и _просматривать_ объявления о продаже различных электронных "
        "товаров. 📱💻\n\n"
        "*Где найти объявления?*\n"
        f"Все объявления публикуются в нашем телеграмм-канале @{tgk_address}. 📢\n\n"
        "*Как создать объявление?*\n"
        "Публикация объявлений происходит _в боте_! Если вы хотите создать свое объявление или узнать больше о наших "
        "_возможностях_, просто введите команду: /help 🤔"
    )

    return message_text


def help_message():
    message_text = (
        "*Добро пожаловать в раздел помощи!* 🤗\n\n"
        "*Доступные команды:*\n\n"
        "/add\\_ad - _С помощью этой команды вы можете создать новое объявление. Просто запустите команду, "
        "и откроется форма для заполнения всех необходимых данных о вашем товаре._ 📦✨\n\n"
        "/my\\_ads - _Эта команда позволяет вам просмотреть все ваши объявления. Вы также можете удалить "
        "ненужные или проданные товары, чтобы поддерживать порядок в своем списке._ 🗑️📝"
    )

    return message_text
