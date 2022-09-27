from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, db, bot
import sqlite3



select_lang_ru = InlineKeyboardMarkup(
	inline_keyboard=[
	[
	
		InlineKeyboardButton(text="O'zbek 🇺🇿 ", callback_data="uzbek"),
		InlineKeyboardButton(text="Русский 🇷🇺 ", callback_data="russian"),
	],
])

def deleting_ru(id):
	pro_delete = InlineKeyboardMarkup(
		inline_keyboard=[
		[
			InlineKeyboardButton(text="📝 Edit ", callback_data=f"edit:{id}"),
			InlineKeyboardButton(text="❌ Delete ", callback_data=f"delete:{id}"),
			
		],
	])
	return pro_delete

def add_pocket_ru(id, sell_count, price, name, sevimlilar, narx):
	pro_savat = InlineKeyboardMarkup(
		inline_keyboard=[
      [
			InlineKeyboardButton(text=f"➕  {price} UZS {name} ➕", callback_data=f"pocket:{id}"),
          ],
		[
			InlineKeyboardButton(text=f"♥️  ({sevimlilar}) ", callback_data=f"collek:{id}"),
			InlineKeyboardButton(text=f"🛍 {narx} UZS  ({sell_count})", callback_data=f"payme"),
			
		],
 
	])
	return pro_savat


def savatcha_btn_ru():
	pro_savat = InlineKeyboardMarkup(
		inline_keyboard=[
		
  [
			InlineKeyboardButton(text="💳 Оплата", callback_data=f"payme_card_ru"),
			
		],
  [
			InlineKeyboardButton(text="♻️ Уменьшить количество продуктов", callback_data=f"change_sell_pro_ru"),
			
		],
   [
			InlineKeyboardButton(text="❌ Очистить корзину", callback_data=f"delete_sells_ru"),
			
		],
	])
	return pro_savat


def change_sells_pro_ru(user_id):
    products_btn = InlineKeyboardMarkup(row_width=3)
    
    
    pro_sells = db.select_sells_product(user_id, user_id)
    pro_dict = {}
    raqam = 0
    for i in pro_sells:
        if i[2] in pro_dict:
            pro_dict[i[2]] = pro_dict[i[2]] + 1
        else:
            pro_dict[i[2]] = 1
    for id in pro_dict:
        raqam += 1
        product = db.select_product(id, id)
        products_btn.insert(InlineKeyboardButton(text=f" ➖ ", callback_data=f"minus:{id}"))
        products_btn.insert(InlineKeyboardButton(text=f"  {product[1]} ", callback_data=f"soni:{id}"))
        products_btn.insert(InlineKeyboardButton(text=f" ➕ ", callback_data=f"pulus:{id}"))
    
    products_btn.insert(InlineKeyboardButton(text="🔙 Назад", callback_data="back_sell"))
    
    return products_btn






adding_pro_ru = InlineKeyboardMarkup(
	inline_keyboard=[
	[
	
		InlineKeyboardButton(text="✅ Да", callback_data="yes"),
		InlineKeyboardButton(text="❌ Нет", callback_data="no"),
	],
])



def guruhlar_ru(category):
    son1 = len(db.select_product_category(category, "bukletlar"))
    son2 = len(db.select_product_category(category, "materiallar"))
    son3 = len(db.select_product_category(category, "suratlar"))
    son4 = len(db.select_product_category(category, "lepbuklar"))
    son5 = len(db.select_product_category(category, "plakatlar"))
    son6 = len(db.select_product_category(category, "bezak"))
    son7 = len(db.select_product_category(category, "maska"))
    son8 = len(db.select_product_category(category, "maket"))
    son9 = len(db.select_product_category(category, "hujjatlar"))
    jami = son1 + son2 + son3 + son4 + son5 + son6 + son7 + son8 + son9
    guruhlar_btn = InlineKeyboardMarkup(
		inline_keyboard=[
		[	
			InlineKeyboardButton(text=f"Все ({jami})", callback_data=f"hammasi"),
		],
		[
			InlineKeyboardButton(text=f"Буклеты ({son1})", callback_data=f"bukletlar"),
			InlineKeyboardButton(text=f"Д. Материалы ({son2})", callback_data=f"materiallar"),
		],
		[
			InlineKeyboardButton(text=f"Картинки ({son3})", callback_data=f"suratlar"),
			InlineKeyboardButton(text=f"Лепбуки ({son4})", callback_data=f"lepbuklar"),
		],
  [
			InlineKeyboardButton(text=f"Плакаты ({son5})", callback_data=f"plakatlar"),
			InlineKeyboardButton(text=f"Украшение(оформление) ({son6})", callback_data=f"bezak"),
		],
  [
			InlineKeyboardButton(text=f"Маска ({son7})", callback_data=f"maska"),
			InlineKeyboardButton(text=f"Расклад и игры ({son8})", callback_data=f"maket"),
		],
   [
			InlineKeyboardButton(text=f"Документы ({son9})", callback_data=f"hujjatlar"),
		],
  [
			InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"back"),
	  
  ]
  
	])
    return guruhlar_btn





def show_products_ru(jami, tr, call_1, call_2, sell_count, buy_id, price, name, sevimlilar, narx):
	# print(call_1)
	birinchi_rasmni_korish = InlineKeyboardMarkup(
		inline_keyboard=[
		[
			InlineKeyboardButton(text="⬅️", callback_data=f"{call_1}"),
			InlineKeyboardButton(text=f"{tr} / {jami}", callback_data="place"),
			InlineKeyboardButton(text="➡️", callback_data=f"{call_2}"),
		],
		[
			InlineKeyboardButton(text=f"➕  {price} UZS {name}  ➕", callback_data=f"pocket:{buy_id}"),
		],
  [
			InlineKeyboardButton(text=f"♥️  ({sevimlilar}) ", callback_data=f"collec:{buy_id}"),
			InlineKeyboardButton(text=f"🛍 {narx} UZS  ({sell_count})", callback_data=f"payme"),
		],
  [
			InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_gr"),
		],
	])
	return birinchi_rasmni_korish



def change_product_ru(tr,jami):
	# print(call_2)

	change_photo_btn = InlineKeyboardMarkup(
		inline_keyboard=[
		[
		InlineKeyboardButton(text="⬅️", callback_data=f"oldingi"),
		InlineKeyboardButton(text=f"{tr} / {jami}", callback_data="place"),
		InlineKeyboardButton(text="➡️", callback_data=f"keyingi"),
	],
		[
			InlineKeyboardButton(text="🗑 В корзину", callback_data=f"add_product"),
		],
	])

	return change_photo_btn




def build_keyboard_ru(product):
    keys = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Покупка", callback_data=f"product:{product}"),
        ],
    ])
    return keys









def show_like_products_ru(jami, tr, sell_count, buy_id, price, name,  narx):
	# print(call_1)
	birinchi_rasmni_korish = InlineKeyboardMarkup(
		inline_keyboard=[
		[
			InlineKeyboardButton(text="⬅️", callback_data=f"prev"),
			InlineKeyboardButton(text=f"{tr} / {jami}", callback_data="place"),
			InlineKeyboardButton(text="➡️", callback_data=f"next"),
		],
		[
			InlineKeyboardButton(text=f"➕  {price} UZS {name}  ➕", callback_data=f"pocket:{buy_id}"),
		],
  [
			InlineKeyboardButton(text=f"💔 / ❌", callback_data=f"delete:{buy_id}"),
			InlineKeyboardButton(text=f"🛍 {narx} UZS  ({sellfrom aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, db, bot
import sqlite3



select_lang_ru = InlineKeyboardMarkup(
	inline_keyboard=[
	[
	
		InlineKeyboardButton(text="O'zbek 🇺🇿 ", callback_data="uzbek"),
		InlineKeyboardButton(text="Русский 🇷🇺 ", callback_data="russian"),
	],
])

def deleting_ru(id):
	pro_delete = InlineKeyboardMarkup(
		inline_keyboard=[
		[
			InlineKeyboardButton(text="📝 Edit ", callback_data=f"edit:{id}"),
			InlineKeyboardButton(text="❌ Delete ", callback_data=f"delete:{id}"),
			
		],
	])
	return pro_delete

def add_pocket_ru(id, sell_count, price, name, sevimlilar, narx):
	pro_savat = InlineKeyboardMarkup(
		inline_keyboard=[
      [
			InlineKeyboardButton(text=f"➕  {price} UZS {name} ➕", callback_data=f"pocket:{id}"),
          ],
		[
			InlineKeyboardButton(text=f"♥️  ({sevimlilar}) ", callback_data=f"collek:{id}"),
			InlineKeyboardButton(text=f"🛍 {narx} UZS  ({sell_count})", callback_data=f"payme"),
			
		],
 
	])
	return pro_savat


def savatcha_btn_ru():
	pro_savat = InlineKeyboardMarkup(
		inline_keyboard=[
		
  [
			InlineKeyboardButton(text="💳 Оплата", callback_data=f"payme_card_ru"),
			
		],
  [
			InlineKeyboardButton(text="♻️ Уменьшить количество продуктов", callback_data=f"change_sell_pro_ru"),
			
		],
   [
			InlineKeyboardButton(text="❌ Очистить корзину", callback_data=f"delete_sells_ru"),
			
		],
	])
	return pro_savat


def change_sells_pro_ru(user_id):
    products_btn = InlineKeyboardMarkup(row_width=3)
    
    
    pro_sells = db.select_sells_product(user_id, user_id)
    pro_dict = {}
    raqam = 0
    for i in pro_sells:
        if i[2] in pro_dict:
            pro_dict[i[2]] = pro_dict[i[2]] + 1
        else:
            pro_dict[i[2]] = 1
    for id in pro_dict:
        raqam += 1
        product = db.select_product(id, id)
        products_btn.insert(InlineKeyboardButton(text=f" ➖ ", callback_data=f"minus:{id}"))
        products_btn.insert(InlineKeyboardButton(text=f"  {product[1]} ", callback_data=f"soni:{id}"))
        products_btn.insert(InlineKeyboardButton(text=f" ➕ ", callback_data=f"pulus:{id}"))
    
    products_btn.insert(InlineKeyboardButton(text="🔙 Назад", callback_data="back_sell"))
    
    return products_btn






adding_pro_ru = InlineKeyboardMarkup(
	inline_keyboard=[
	[
	
		InlineKeyboardButton(text="✅ Да", callback_data="yes"),
		InlineKeyboardButton(text="❌ Нет", callback_data="no"),
	],
])



def guruhlar_ru(category):
    son1 = len(db.select_product_category(category, "bukletlar"))
    son2 = len(db.select_product_category(category, "materiallar"))
    son3 = len(db.select_product_category(category, "suratlar"))
    son4 = len(db.select_product_category(category, "lepbuklar"))
    son5 = len(db.select_product_category(category, "plakatlar"))
    son6 = len(db.select_product_category(category, "bezak"))
    son7 = len(db.select_product_category(category, "maska"))
    son8 = len(db.select_product_category(category, "maket"))
    son9 = len(db.select_product_category(category, "hujjatlar"))
    jami = son1 + son2 + son3 + son4 + son5 + son6 + son7 + son8 + son9
    guruhlar_btn = InlineKeyboardMarkup(
		inline_keyboard=[
		[	
			InlineKeyboardButton(text=f"Все ({jami})", callback_data=f"hammasi"),
		],
		[
			InlineKeyboardButton(text=f"Буклеты ({son1})", callback_data=f"bukletlar"),
			InlineKeyboardButton(text=f"Д. Материалы ({son2})", callback_data=f"materiallar"),
		],
		[
			InlineKeyboardButton(text=f"Картинки ({son3})", callback_data=f"suratlar"),
			InlineKeyboardButton(text=f"Лепбуки ({son4})", callback_data=f"lepbuklar"),
		],
  [
			InlineKeyboardButton(text=f"Плакаты ({son5})", callback_data=f"plakatlar"),
			InlineKeyboardButton(text=f"Украшение(оформление) ({son6})", callback_data=f"bezak"),
		],
  [
			InlineKeyboardButton(text=f"Маска ({son7})", callback_data=f"maska"),
			InlineKeyboardButton(text=f"Расклад и игры ({son8})", callback_data=f"maket"),
		],
   [
			InlineKeyboardButton(text=f"Документы ({son9})", callback_data=f"hujjatlar"),
		],
  [
			InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"back"),
	  
  ]
  
	])
    return guruhlar_btn





def show_products_ru(jami, tr, call_1, call_2, sell_count, buy_id, price, name, sevimlilar, narx):
	# print(call_1)
	birinchi_rasmni_korish = InlineKeyboardMarkup(
		inline_keyboard=[
		[
			InlineKeyboardButton(text="⬅️", callback_data=f"{call_1}"),
			InlineKeyboardButton(text=f"{tr} / {jami}", callback_data="place"),
			InlineKeyboardButton(text="➡️", callback_data=f"{call_2}"),
		],
		[
			InlineKeyboardButton(text=f"➕  {price} UZS {name}  ➕", callback_data=f"pocket:{buy_id}"),
		],
  [
			InlineKeyboardButton(text=f"♥️  ({sevimlilar}) ", callback_data=f"collec:{buy_id}"),
			InlineKeyboardButton(text=f"🛍 {narx} UZS  ({sell_count})", callback_data=f"payme"),
		],
  [
			InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_gr"),
		],
	])
	return birinchi_rasmni_korish



def change_product_ru(tr,jami):
	# print(call_2)

	change_photo_btn = InlineKeyboardMarkup(
		inline_keyboard=[
		[
		InlineKeyboardButton(text="⬅️", callback_data=f"oldingi"),
		InlineKeyboardButton(text=f"{tr} / {jami}", callback_data="place"),
		InlineKeyboardButton(text="➡️", callback_data=f"keyingi"),
	],
		[
			InlineKeyboardButton(text="🗑 В корзину", callback_data=f"add_product"),
		],
	])

	return change_photo_btn




def build_keyboard_ru(product):
    keys = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Покупка", callback_data=f"product:{product}"),
        ],
    ])
    return keys









def show_like_products_ru(jami, tr, sell_count, buy_id, price, name,  narx):
	# print(call_1)
	birinchi_rasmni_korish = InlineKeyboardMarkup(
		inline_keyboard=[
		[
			InlineKeyboardButton(text="⬅️", callback_data=f"prev"),
			InlineKeyboardButton(text=f"{tr} / {jami}", callback_data="place"),
			InlineKeyboardButton(text="➡️", callback_data=f"next"),
		],
		[
			InlineKeyboardButton(text=f"➕  {price} UZS {name}  ➕", callback_data=f"pocket:{buy_id}"),
		],
  [
			InlineKeyboardButton(text=f"💔 / ❌", callback_data=f"delete:{buy_id}"),
			InlineKeyboardButton(text=f"🛍 {narx} UZS  ({sell_count})", callback_data=f"payme"),
		],
  [
			InlineKeyboardButton(text="🔙 Назад", callback_data=f"back_gr"),
		],
	])
	return birinchi_rasmni_korish


