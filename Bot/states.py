from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateProduct(StatesGroup):
	title = State()
	description = State()
	price = State()
	images = State()


class RegisterState(StatesGroup):
	username = State()
	password = State()

