
async def create_ad_message(data):
    title = data['title']
    description = data['description']
    image_id = data['image']
    price = data['price']
    ads_id = data["ads_id"]


    # Формируем текст сообщения
    message_text = (
        f"✨ *Объявление:* ✨\n"
        f"📦 *Название:* {title}\n"
        f"📝 *Описание:* {description}\n"
        f"💰 *Цена:* {price}₽\n"
        f"🆔 *ID:* {ads_id}\n"
    )

    return message_text, image_id
