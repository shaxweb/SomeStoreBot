from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
from states import *

import buttons as btn
import config as conf
import funcs as fnc
import texts as txt
import json, time, sql, os

bot = Bot(conf.token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(state="*", text="Cancel")
async def cmd_cancel_state(message: Message, state: FSMContext):
	await state.finish()
	await message.answer("✔️", reply_markup=btn.start)


@dp.message_handler(commands="start")
async def cmd_start(message: Message):
	user = message.from_user
	fnc.register(user)
	await message.answer(txt.start(user), reply_markup=btn.start)
	await message.answer("ping: /ping")


@dp.message_handler(commands="ping")
async def ping(message: Message):
	sended_message = await message.answer("⌛")
	data = await fnc.ping_to_backend()
	await bot.edit_message_text(chat_id=message.from_id, message_id=sended_message.message_id, text=f"{data['message']}")


@dp.message_handler(text="Create Product")
async def create_product_view(message: Message):
	if not await fnc.check_user(message.from_id):
		await message.answer(txt.create_product("title"))
		await CreateProduct.title.set()
		await fnc.ping_to_backend()
	else:
		await message.reply(txt.not_registered())
		await RegisterState.username.set()


@dp.message_handler(state=CreateProduct, content_types=["text", "photo"])
async def create_product(message: Message, state: FSMContext):
	cur_state = await state.get_state()
	if cur_state == CreateProduct.title.state:
		await state.update_data(title=message.text)
		await message.answer(txt.create_product("description"))
		await CreateProduct.description.set()
		
	elif cur_state == CreateProduct.description.state:
		await state.update_data(description=message.text)
		await message.reply(txt.create_product("price"))
		await CreateProduct.price.set()
		
	elif cur_state == CreateProduct.price.state:
		if not message.text.isdigit():
			await message.answer("<b>UNCORRECT DATAS</b> (<i>Only numbers</i>)")
			return
			
		await state.update_data(price=message.text)
		await message.reply(txt.create_product("images", 1))
		await CreateProduct.images.set()
		
	elif cur_state == CreateProduct.images.state:
		photo = message.photo[-1]
		file_info = await bot.get_file(photo.file_id)
		file_path = file_info.file_path
		local_filename = f"product_image_{photo.file_id}.jpg"
		await bot.download_file(file_path, destination=local_filename)
		data = await state.get_data()
		images_list = data.get("images_list")
		if images_list:
			images_list.append(local_filename)
		else:
			images_list = [local_filename]
		await state.update_data(images_list=images_list)
		
		if len(images_list) >= 4:
			wait_message = await message.reply("⌛")
			data = await state.get_data()
			title, description, price = data.get("title"), data.get("description"), data.get("price")
			response = await fnc.publish_product(images_list, {"title": title, "description": description, "price": price, "author": 1, "category": 1})
			print(response)
			await bot.edit_message_text(chat_id=message.from_id, message_id=wait_message.message_id, text=response["message"])
			await state.finish()
			for image in images_list:
				os.remove(image)
		else:
			await message.reply(txt.create_product("images", len(images_list)+1))


@dp.message_handler(state=RegisterState)
async def register_user_view(message: Message, state: FSMContext):
	cur_state = await state.get_state()
	text = message.text
	
	if cur_state == RegisterState.username.state:
		await state.update_data(username=text)
		await message.reply("Enter the password")
		await RegisterState.password.set()
	elif cur_state == RegisterState.password.state:
		data = await state.get_data()
		username = data.get("username")
		password = text
	
	await state.finish()


@dp.message_handler()
async def cmd_unknown(message: Message):
	await message.reply(txt.unknown())

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)