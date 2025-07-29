from aiogram.types import *
import requests, sql


def register(data):
	sql.register(data.id, data.full_name, data.username)


per_page = 5

def get_pagination_buttons(data, type, data_id: None, page: int):
	keyboard = InlineKeyboardMarkup(row_width=5)

	if page > 0:
		keyboard.add(InlineKeyboardButton(text="Back ⬅️", callback_data=f"msg_page:{type}:{page-1}:{data_id}"))
	
	if (page + 1) * per_page < len(data):
		keyboard.add(InlineKeyboardButton(text="➡️ Next", callback_data=f"msg_page:{type}:{page+1}:{data_id}"))
	
	return keyboard


async def send_paginated_data(bot, chat_id, message_id, data, data_id, type, page: int):
	page = int(page)
	
	start = page * per_page
	end = start + per_page
	page_data = "\n".join(data[start:end]) or "❌"
	
	text = f"📜 Page {page+1}/{(len(data) - 1) // per_page + 1}\n\n{page_data}"
	keyboard = get_pagination_buttons(data, type, data_id, page)
	
	if message_id:
		await bot.edit_message_text(chat_id=chat_id, text=text, message_id=message_id, reply_markup=keyboard)
	else:
		await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


def count_mismatches(s1, s2):
    length = max(len(s1), len(s2))
    mismatches = 0
    for i in range(length):
        c1 = s1[i] if i < len(s1) else ''
        c2 = s2[i] if i < len(s2) else ''
        if c1 != c2:
            mismatches += 1
    return mismatches


async def ping_to_backend():
	url = "https://somestorebackend.onrender.com/ping/"
	response = requests.get(url)
	return response.json()


async def publish_product(images_path, data):
	if data.get("title") and data.get("description") and data.get("price") and images_path:
		url = "https://somestorebackend.onrender.com/create_product/"
		files = []
		for image in images_path:
			files.append(("images", (image, open(image, "rb"), "image/jpeg")))
		
		print(files)
		response = requests.post(url, data=data, files=files)
		return response.json()


async def check_user(user_id):
	user = sql.get_data(user_id)["user"]
	if user:
		backend_username = user[4]
		backend_password = user[5]
		if backend_username:
			return True
		return False
	return False

