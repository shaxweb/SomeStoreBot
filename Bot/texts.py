def start(user):
	return f"Hello, {user.full_name}"


def create_product(type, cur_image=None):
	if type == "title":
		return "📝 <b>Ónim atın jazıń:</b>"
	elif type == "description":
		return "📝 <b>Ónimdi táriyipleń:</b>"
	elif type == "price":
		return "📝 <b>Ónimniń bahasın jazıń:</b>"
	elif type == "images":
		return f"🖼️ <b>Ónimniń súwretin jiberiń <i>[{cur_image}/4]</i></b>"


def not_registered():
	return "Register error"


def unknown():
	return "Unknown Command"