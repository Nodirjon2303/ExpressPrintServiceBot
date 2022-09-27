from aiogram import types, Bot
from filters import IsPrivate
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMedia, CallbackQuery
from keyboards.inline.inline_btn_ru import guruhlar_ru, show_products_ru, savatcha_btn_ru
from keyboards.default.default_btn_ru import main_btn_ru
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
import sqlite3
from data.products import prices
from states.reg_state_ru import show_buy_ru


@dp.message_handler(IsPrivate(), text="Для детского сада",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    print("bogcha uchun guruhlar rus")
    global tr
    tr = 1
    await state.update_data(
        {"category": "bogcha"}
    )
    await message.answer("Детский сад", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"Выберите группу.", reply_markup=guruhlar_ru("bogcha"))
    await show_buy_ru.subcategory.set()


@dp.message_handler(IsPrivate(), text="Для школы",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    global tr
    tr = 1
    await state.update_data(
        {"category": "maktab"}
    )
    await message.answer("Школьный отдел", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"Выберите группу.", reply_markup=guruhlar_ru("maktab"))
    await show_buy_ru.subcategory.set()


@dp.callback_query_handler(text="back",  state=show_buy_ru.subcategory)
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Домашняя страница", reply_markup=main_btn_ru)
    await state.finish()


@dp.message_handler(IsPrivate(), text="/start",  state=show_buy_ru.subcategory)
async def bot_start(message: types.Message, state=FSMContext):
    await call.message.delete()
    await call.message.answer("Привет {message.from_user.full_name}. Мы рады видеть вас здесь.", reply_markup=main_btn_ru)
    await state.finish()

    
global tr
tr = 1


# @dp.callback_query_handler(text = "hammasi", state=show_buy_ru.subcategory)
# async def select_pro(call: CallbackQuery, state: FSMContext):
#     await state.update_data(
#         {"subcategory": "hammasi"}
#     )
#     data = await state.get_data()
#     category = data.get("category")
#     global tr
#     tr = 1

    
    
@dp.callback_query_handler(state=show_buy_ru.subcategory)
async def select_pro(call: CallbackQuery, state: FSMContext):
    subcategory = call.data
    await state.update_data(
        {"subcategory": subcategory}
    )
    data = await state.get_data()
    category = data.get("category")
    global tr
    tr = 1
    print(subcategory)
    print(tr)
    user_id = call.from_user.id
    
    if subcategory != "hammasi":
    
        len_pro = db.select_product_category(category, subcategory)
    else:
        len_pro = db.select_all_product()
        
    if len_pro:
        sevimlilar = db.select_sevimlilar(user_id, user_id)
        
        await call.message.delete()
        
        products = len_pro[tr-1]

        matn = f"id: {products[0]}\n"
        matn += f"<b>Name: {products[1]}</b>\n\n"
        matn += f"{products[2]}\n"
        # matn += f"Price: {products[3]} sum\n"
        # matn += f"Category: {products[4]}\n"
        # matn += f"Subcategory: {products[5]}\n"
        # matn += f"Date: {products[7]}\n"
        
        pro_count = db.select_sells_product(user_id, user_id)
        
        
        pro_dict = {}
        narx = 0
        
    
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                product = db.select_product(id, id)
                print(pro_dict)
                print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * product[3]
        
        try:
            await bot.send_animation(chat_id=call.message.chat.id, animation=products[6], caption=matn, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0], products[3], products[1], len(sevimlilar), narx))
            
        except :
            await bot.send_photo(call.message.chat.id, products[6], matn, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0], products[3], products[1], len(sevimlilar), narx))

        # await call.message.answer("ok")
        # await state.finish()
        await show_buy_ru.next.set()
    else:
        await call.answer("В этом разделе нет товаров")

@dp.message_handler(IsPrivate(), text="/start",  state=show_buy_ru.next)
async def bot_start(message: types.Message, state=FSMContext):
    await message.delete()
    await message.answer(f"Привет {message.from_user.full_name}. Мы рады видеть вас здесь.", reply_markup=main_btn_ru)
    await state.finish()


@dp.callback_query_handler(text="back_gr",  state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    
    data = await state.get_data()
    category = data.get("category")
    
    await call.message.answer(f" Выберите нужную группу.", reply_markup=guruhlar_ru(category))
    await show_buy_ru.subcategory.set()
    # await call.message.answer("Bosh sahifa", reply_markup=main_btn_ru)
    # await state.finish()



@dp.callback_query_handler(text="next", state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    # await call.message.delete()
    
    print(call.message.reply_markup.inline_keyboard[1][0]['text'])
    print(call.message.reply_markup.inline_keyboard[1][0]['callback_data'])

    data = await state.get_data()
    category = data.get("category")
    subcategory = data.get("subcategory")
    user_id = call.from_user.id

    global tr
    tr += 1
    
    if subcategory != "hammasi":
    
        len_pro = db.select_product_category(category, subcategory)
    else:
        len_pro = db.select_all_product()
    
    if len(len_pro) >= tr:

        print("trtrtr--", tr-1)

        products = len_pro[tr-1]

        matn = f"id: {products[0]}\n"
        matn += f"<b>Name: {products[1]}</b>\n\n"
        matn += f"{products[2]}\n"
        # matn += f"Price: {products[3]} sum\n"
        # matn += f"Category: {products[4]}\n"
        # matn += f"Subcategory: {products[5]}\n"
        # matn += f"Date: {products[7]}\n"
        
        sevimlilar = db.select_sevimlilar(user_id, user_id)
        pro_count = db.select_sells_product(user_id, user_id)
        
        pro_dict = {}
        narx = 0
        
    
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                product = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * product[3]
        
        pro_count = db.select_sells_product(user_id, user_id)
        
        await bot.edit_message_media(media=InputMedia(type='photo', media=products[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0], products[3], products[1], len(sevimlilar), narx))	

        # await bot.send_photo(call.message.chat.id, products[6], matn, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", products[0]))
    else:
        await call.answer("Это конечный продукт")

        tr -= 1

    await show_buy_ru.next.set()



@dp.callback_query_handler(text="prev", state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    # await call.message.delete()

    data = await state.get_data()
    category = data.get("category")
    subcategory = data.get("subcategory")
    user_id = call.from_user.id

    global tr
    tr -= 1
    
    if subcategory != "hammasi":
    
        len_pro = db.select_product_category(category, subcategory)
    else:
        len_pro = db.select_all_product()
    
    if 0 < tr:

        print("trtrtr--", tr-1)

        products = len_pro[tr-1]

        matn = f"id: {products[0]}\n"
        matn += f"<b>Name: {products[1]}</b>\n\n"
        matn += f"{products[2]}\n"
        # matn += f"Price: {products[3]} sum\n"
        # matn += f"Category: {products[4]}\n"
        # matn += f"Subcategory: {products[5]}\n"
        # matn += f"Date: {products[7]}\n"

        pro_count = db.select_sells_product(user_id, user_id)

        sevimlilar = db.select_sevimlilar(user_id, user_id)
        # pro_count = db.select_sells_product(user_id, user_id)
        
        pro_dict = {}
        narx = 0
        
    
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                product = db.select_product(id, id)
                print(pro_dict)
                print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * product[3]
        
        await bot.edit_message_media(media=InputMedia(type='photo', media=products[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0], products[3], products[1], len(sevimlilar), narx))	
        # await bot.send_photo(call.message.chat.id, products[6], matn, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", products[0]))
    else:
        await call.answer("Это первый продукт")

        tr += 1

    await show_buy_ru.next.set()
    
    


@dp.callback_query_handler(text="place", state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):

    await call.answer(f"Mahsulotlar soni")
    await show_buy_ru.next.set()



@dp.callback_query_handler(text="payme", state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    await call.message.answer("Товары в вашей корзине", reply_markup=main_btn_ru)
    user_id = call.from_user.id
    
    name = db.select_user(user_id, user_id)[1]
    
    pro_sells = db.select_sells_product(user_id, user_id)
        
    pro_dict = {}
    pro_text =     ""
    raqam = 0
    narx = 0
    
 
    if pro_sells:
        yetkazish = 8999

        for i in pro_sells:
            if i[2] in pro_dict:
                pro_dict[i[2]] = pro_dict[i[2]] + 1
            else:
                pro_dict[i[2]] = 1
            
        for id in pro_dict:
            raqam += 1
            
            product = db.select_product(id, id)
            print(pro_dict)
            print(product)
            
            pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
            narx += pro_dict[id] * product[3]
            
        pro_text += f"\n\nДоставка: {yetkazish} UZS \n"
            
        matn = f"{name} список продуктов, которые вы выбрали \n\n"
        matn += pro_text
        
        matn += f"\n Общий: {narx+yetkazish} UZS"
        
        await call.message.answer(matn, reply_markup=savatcha_btn_ru())


    else:
        matn = "У вас еще нет заказов!\n"
        await call.message.answer(matn, reply_markup=main_btn_ru)
        
    
   




@dp.callback_query_handler( state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    pro_id = call.data[7:]
    if call.data[0:7]=="pocket:":
        db.add_sell_product(call.from_user.id, pro_id)
    # db.add_sell_product(call.from_user.id, pro_id)
        
        await call.answer(f"#id:{pro_id} 🛍 добавлено в корзину")
    elif call.data[0:7]=="collec:":
        # print("################################",id)
        try:
            db.add_sevimlilar(call.from_user.id, pro_id)
            # await call.message.answer(f"✅ #id{id} \nMahsulot ♥️ sevimlilarga qo'shildi")
            await call.answer(f"#id:{pro_id} ♥️ добавлено в избранное")
        except :
            await call.answer(f"#id:{pro_id} ♥️ доступно в избранном")
        
    print(tr)
    
    user_id = call.from_user.id
    
    data = await state.get_data()
    category = data.get("category")
    subcategory = data.get("subcategory")

    if subcategory != "hammasi":
    
        len_pro = db.select_product_category(category, subcategory)
    else:
        len_pro = db.select_all_product()
    

    products = len_pro[tr-1]

    matn = f"id: {products[0]}\n"
    matn += f"<b>Name: {products[1]}</b>\n\n"
    matn += f"{products[2]}\n"
    # matn += f"Price: {products[3]} UZS\n"
    # matn += f"Category: {products[4]}\n"
    # matn += f"Subcategory: {products[5]}\n"
    # matn += f"Date: {products[7]}\n"
    
    # pro_count = db.select_sells_product(user_id, user_id)

    sevimlilar = db.select_sevimlilar(user_id, user_id)
    pro_count = db.select_sells_product(user_id, user_id)
    
    pro_dict = {}
    narx = 0
    

    if pro_count:
        for i in pro_count:
            if i[2] in pro_dict:
                pro_dict[i[2]] = pro_dict[i[2]] + 1
            else:
                pro_dict[i[2]] = 1
            
        for id in pro_dict:
            # raqam += 1
            
            product = db.select_product(id, id)
            print(pro_dict)
            print(product)
            
            # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
            narx += pro_dict[id] * product[3]
    
    prices.clear()

    await bot.edit_message_media(media=InputMedia(type='photo', media=producfrom aiogram import types, Bot
from filters import IsPrivate
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMedia, CallbackQuery
from keyboards.inline.inline_btn_ru import guruhlar_ru, show_products_ru, savatcha_btn_ru
from keyboards.default.default_btn_ru import main_btn_ru
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
import sqlite3
from data.products import prices
from states.reg_state_ru import show_buy_ru


@dp.message_handler(IsPrivate(), text="Для детского сада",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    print("bogcha uchun guruhlar rus")
    global tr
    tr = 1
    await state.update_data(
        {"category": "bogcha"}
    )
    await message.answer("Детский сад", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"Выберите группу.", reply_markup=guruhlar_ru("bogcha"))
    await show_buy_ru.subcategory.set()


@dp.message_handler(IsPrivate(), text="Для школы",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    global tr
    tr = 1
    await state.update_data(
        {"category": "maktab"}
    )
    await message.answer("Школьный отдел", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"Выберите группу.", reply_markup=guruhlar_ru("maktab"))
    await show_buy_ru.subcategory.set()


@dp.callback_query_handler(text="back",  state=show_buy_ru.subcategory)
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Домашняя страница", reply_markup=main_btn_ru)
    await state.finish()


@dp.message_handler(IsPrivate(), text="/start",  state=show_buy_ru.subcategory)
async def bot_start(message: types.Message, state=FSMContext):
    await call.message.delete()
    await call.message.answer("Привет {message.from_user.full_name}. Мы рады видеть вас здесь.", reply_markup=main_btn_ru)
    await state.finish()

    
global tr
tr = 1


# @dp.callback_query_handler(text = "hammasi", state=show_buy_ru.subcategory)
# async def select_pro(call: CallbackQuery, state: FSMContext):
#     await state.update_data(
#         {"subcategory": "hammasi"}
#     )
#     data = await state.get_data()
#     category = data.get("category")
#     global tr
#     tr = 1

    
    
@dp.callback_query_handler(state=show_buy_ru.subcategory)
async def select_pro(call: CallbackQuery, state: FSMContext):
    subcategory = call.data
    await state.update_data(
        {"subcategory": subcategory}
    )
    data = await state.get_data()
    category = data.get("category")
    global tr
    tr = 1
    print(subcategory)
    print(tr)
    user_id = call.from_user.id
    
    if subcategory != "hammasi":
    
        len_pro = db.select_product_category(category, subcategory)
    else:
        len_pro = db.select_all_product()
        
    if len_pro:
        sevimlilar = db.select_sevimlilar(user_id, user_id)
        
        await call.message.delete()
        
        products = len_pro[tr-1]

        matn = f"id: {products[0]}\n"
        matn += f"<b>Name: {products[1]}</b>\n\n"
        matn += f"{products[2]}\n"
        # matn += f"Price: {products[3]} sum\n"
        # matn += f"Category: {products[4]}\n"
        # matn += f"Subcategory: {products[5]}\n"
        # matn += f"Date: {products[7]}\n"
        
        pro_count = db.select_sells_product(user_id, user_id)
        
        
        pro_dict = {}
        narx = 0
        
    
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                product = db.select_product(id, id)
                print(pro_dict)
                print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * product[3]
        
        try:
            await bot.send_animation(chat_id=call.message.chat.id, animation=products[6], caption=matn, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0], products[3], products[1], len(sevimlilar), narx))
            
        except :
            await bot.send_photo(call.message.chat.id, products[6], matn, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0], products[3], products[1], len(sevimlilar), narx))

        # await call.message.answer("ok")
        # await state.finish()
        await show_buy_ru.next.set()
    else:
        await call.answer("В этом разделе нет товаров")

@dp.message_handler(IsPrivate(), text="/start",  state=show_buy_ru.next)
async def bot_start(message: types.Message, state=FSMContext):
    await message.delete()
    await message.answer(f"Привет {message.from_user.full_name}. Мы рады видеть вас здесь.", reply_markup=main_btn_ru)
    await state.finish()


@dp.callback_query_handler(text="back_gr",  state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    
    data = await state.get_data()
    category = data.get("category")
    
    await call.message.answer(f" Выберите нужную группу.", reply_markup=guruhlar_ru(category))
    await show_buy_ru.subcategory.set()
    # await call.message.answer("Bosh sahifa", reply_markup=main_btn_ru)
    # await state.finish()



@dp.callback_query_handler(text="next", state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    # await call.message.delete()
    
    print(call.message.reply_markup.inline_keyboard[1][0]['text'])
    print(call.message.reply_markup.inline_keyboard[1][0]['callback_data'])

    data = await state.get_data()
    category = data.get("category")
    subcategory = data.get("subcategory")
    user_id = call.from_user.id

    global tr
    tr += 1
    
    if subcategory != "hammasi":
    
        len_pro = db.select_product_category(category, subcategory)
    else:
        len_pro = db.select_all_product()
    
    if len(len_pro) >= tr:

        print("trtrtr--", tr-1)

        products = len_pro[tr-1]

        matn = f"id: {products[0]}\n"
        matn += f"<b>Name: {products[1]}</b>\n\n"
        matn += f"{products[2]}\n"
        # matn += f"Price: {products[3]} sum\n"
        # matn += f"Category: {products[4]}\n"
        # matn += f"Subcategory: {products[5]}\n"
        # matn += f"Date: {products[7]}\n"
        
        sevimlilar = db.select_sevimlilar(user_id, user_id)
        pro_count = db.select_sells_product(user_id, user_id)
        
        pro_dict = {}
        narx = 0
        
    
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                product = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * product[3]
        
        pro_count = db.select_sells_product(user_id, user_id)
        
        await bot.edit_message_media(media=InputMedia(type='photo', media=products[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0], products[3], products[1], len(sevimlilar), narx))	

        # await bot.send_photo(call.message.chat.id, products[6], matn, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", products[0]))
    else:
        await call.answer("Это конечный продукт")

        tr -= 1

    await show_buy_ru.next.set()



@dp.callback_query_handler(text="prev", state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    # await call.message.delete()

    data = await state.get_data()
    category = data.get("category")
    subcategory = data.get("subcategory")
    user_id = call.from_user.id

    global tr
    tr -= 1
    
    if subcategory != "hammasi":
    
        len_pro = db.select_product_category(category, subcategory)
    else:
        len_pro = db.select_all_product()
    
    if 0 < tr:

        print("trtrtr--", tr-1)

        products = len_pro[tr-1]

        matn = f"id: {products[0]}\n"
        matn += f"<b>Name: {products[1]}</b>\n\n"
        matn += f"{products[2]}\n"
        # matn += f"Price: {products[3]} sum\n"
        # matn += f"Category: {products[4]}\n"
        # matn += f"Subcategory: {products[5]}\n"
        # matn += f"Date: {products[7]}\n"

        pro_count = db.select_sells_product(user_id, user_id)

        sevimlilar = db.select_sevimlilar(user_id, user_id)
        # pro_count = db.select_sells_product(user_id, user_id)
        
        pro_dict = {}
        narx = 0
        
    
        if pro_count:
            for i in pro_count:
                if i[2] in pro_dict:
                    pro_dict[i[2]] = pro_dict[i[2]] + 1
                else:
                    pro_dict[i[2]] = 1
                
            for id in pro_dict:
                # raqam += 1
                
                product = db.select_product(id, id)
                print(pro_dict)
                print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * product[3]
        
        await bot.edit_message_media(media=InputMedia(type='photo', media=products[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0], products[3], products[1], len(sevimlilar), narx))	
        # await bot.send_photo(call.message.chat.id, products[6], matn, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", products[0]))
    else:
        await call.answer("Это первый продукт")

        tr += 1

    await show_buy_ru.next.set()
    
    


@dp.callback_query_handler(text="place", state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):

    await call.answer(f"Mahsulotlar soni")
    await show_buy_ru.next.set()



@dp.callback_query_handler(text="payme", state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    await call.message.answer("Товары в вашей корзине", reply_markup=main_btn_ru)
    user_id = call.from_user.id
    
    name = db.select_user(user_id, user_id)[1]
    
    pro_sells = db.select_sells_product(user_id, user_id)
        
    pro_dict = {}
    pro_text =     ""
    raqam = 0
    narx = 0
    
 
    if pro_sells:
        yetkazish = 8999

        for i in pro_sells:
            if i[2] in pro_dict:
                pro_dict[i[2]] = pro_dict[i[2]] + 1
            else:
                pro_dict[i[2]] = 1
            
        for id in pro_dict:
            raqam += 1
            
            product = db.select_product(id, id)
            print(pro_dict)
            print(product)
            
            pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
            narx += pro_dict[id] * product[3]
            
        pro_text += f"\n\nДоставка: {yetkazish} UZS \n"
            
        matn = f"{name} список продуктов, которые вы выбрали \n\n"
        matn += pro_text
        
        matn += f"\n Общий: {narx+yetkazish} UZS"
        
        await call.message.answer(matn, reply_markup=savatcha_btn_ru())


    else:
        matn = "У вас еще нет заказов!\n"
        await call.message.answer(matn, reply_markup=main_btn_ru)
        
    
   




@dp.callback_query_handler( state=show_buy_ru.next)
async def select_pro(call: CallbackQuery, state: FSMContext):
    pro_id = call.data[7:]
    if call.data[0:7]=="pocket:":
        db.add_sell_product(call.from_user.id, pro_id)
    # db.add_sell_product(call.from_user.id, pro_id)
        
        await call.answer(f"#id:{pro_id} 🛍 добавлено в корзину")
    elif call.data[0:7]=="collec:":
        # print("################################",id)
        try:
            db.add_sevimlilar(call.from_user.id, pro_id)
            # await call.message.answer(f"✅ #id{id} \nMahsulot ♥️ sevimlilarga qo'shildi")
            await call.answer(f"#id:{pro_id} ♥️ добавлено в избранное")
        except :
            await call.answer(f"#id:{pro_id} ♥️ доступно в избранном")
        
    print(tr)
    
    user_id = call.from_user.id
    
    data = await state.get_data()
    category = data.get("category")
    subcategory = data.get("subcategory")

    if subcategory != "hammasi":
    
        len_pro = db.select_product_category(category, subcategory)
    else:
        len_pro = db.select_all_product()
    

    products = len_pro[tr-1]

    matn = f"id: {products[0]}\n"
    matn += f"<b>Name: {products[1]}</b>\n\n"
    matn += f"{products[2]}\n"
    # matn += f"Price: {products[3]} UZS\n"
    # matn += f"Category: {products[4]}\n"
    # matn += f"Subcategory: {products[5]}\n"
    # matn += f"Date: {products[7]}\n"
    
    # pro_count = db.select_sells_product(user_id, user_id)

    sevimlilar = db.select_sevimlilar(user_id, user_id)
    pro_count = db.select_sells_product(user_id, user_id)
    
    pro_dict = {}
    narx = 0
    

    if pro_count:
        for i in pro_count:
            if i[2] in pro_dict:
                pro_dict[i[2]] = pro_dict[i[2]] + 1
            else:
                pro_dict[i[2]] = 1
            
        for id in pro_dict:
            # raqam += 1
            
            product = db.select_product(id, id)
            print(pro_dict)
            print(product)
            
            # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
            narx += pro_dict[id] * product[3]
    
    prices.clear()

    await bot.edit_message_media(media=InputMedia(type='photo', media=products[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_products_ru(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0], products[3], products[1], len(sevimlilar), narx))	
 
    await call.answer(f"#id:{call.data} добавлено в корзину")
    await show_buy_ru.next.set()
    