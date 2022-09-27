from aiogram import types , Bot
from keyboards.default.default_btn_ru import main_btn_ru, maktab_ichi_ru, user_settings_ru, phone_num_ru, regions_btn_ru, back_btn_ru, bogcha_ichi_ru
from keyboards.inline.inline_btn_ru import select_lang_ru, add_pocket_ru, savatcha_btn_ru, show_like_products_ru, guruhlar_ru
from keyboards.default.default_btn import user_settings
from filters import IsPrivate
from states.reg_state_ru import update_user_ru
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery, InputMedia

from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
import sqlite3



@dp.message_handler(IsPrivate(), text="🔙 Назад")
async def bot_start(message: types.Message):
    await message.reply("Главная страница", reply_markup=main_btn_ru)
    


# @dp.message_handler(IsPrivate(), text="Для детского сада",  state=None)
# async def bot_start(message: types.Message, state=FSMContext):
#     print("bogcha ichi rus")
#     await message.reply("Выберите группу", reply_markup=guruhlar_ru("bogcha"))
    

# @dp.message_handler(IsPrivate(), text="Для школы",  state=None)
# async def bot_start(message: types.Message, state=FSMContext):
#     await message.reply("Выберите группу", reply_markup=guruhlar_ru("maktab"))
    
    
    
    
@dp.message_handler(IsPrivate(), text="⚙️ Настройки",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.reply("Информацию о каком разделе вы хотите отредактировать?", reply_markup=user_settings_ru)
    
    
    
@dp.message_handler(IsPrivate(), text="Язык 🇺🇿 / 🇷🇺",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.answer(f" O'zingizga qulay tilni tanlang 🇺🇿 / 🇷🇺  \n    ------------------------------------------  \n Выберите предпочитаемый язык 🇷🇺 / 🇺🇿 ", reply_markup=select_lang_ru)
    await state.set_state("change_lang_ru")

@dp.callback_query_handler( state="change_lang_ru")
async def select_lang_ru_func(call: CallbackQuery, state:FSMContext):
    print(call.data)
    try:
        if call.data=="uzbek":
            lang = 'uzbek'
            db.update_user_lan(lang, call.from_user.id)
            await call.message.answer("⚙️ Sozlamalar", reply_markup=user_settings)
        else:
            lang = 'russian'
            db.update_user_lan(lang, call.from_user.id)
            await call.message.answer("⚙️ Настройки", reply_markup=user_settings_ru)

    except Exception as err:
        print("tilni o'zgartirishda xatolik", err)
    await call.message.delete()
    await state.finish()
    
    
    
@dp.message_handler(IsPrivate(), text="👤 Личная информация",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.answer("Имя Введите вашу фамилию (введите только буквы). \n \n <i><b>Например: </b> Джалолиддин Маматмусаев </i>", reply_markup=ReplyKeyboardRemove())
    await update_user_ru.name.set()

        
@dp.message_handler(IsPrivate(), state=update_user_ru.name)
async def user_name(message: types.Message, state:FSMContext):
   
    name = message.text
    c=0
    for i in name:
        if i.isnumeric():
            c+=1
        
        
    if not c:
        await state.update_data(
			{"name":name}
		)
        # print("ismda faqat harflar")
        await message.answer("Введите свой номер телефона полностью: \n \n <i><b>Например:</b> +998912345678 </i>", reply_markup=phone_num_ru)
        await update_user_ru.phone.set()
    else:
        await message.answer("Ваше имя должно содержать только буквы!")
        await update_user_ru.name.set()



@dp.message_handler(IsPrivate(),  state=update_user_ru.phone, content_types=["contact","text"])
async def user_name(message: types.Message, state:FSMContext):
    phone = message
    
    if phone.text:
        if phone.text[:4] == '+998' and  len(phone.text)==13:
            await state.update_data(
            	{"phone": phone.text}
            )
            await message.answer("Выберите адрес.", reply_markup=regions_btn_ru)
            await update_user_ru.adress.set()
        else:
            await message.answer("❌ Вы ввели неверный формат!, \nВведите еще раз!")
            
            await message.answer("Или отправить через кнопку ниже! 👇🏻", reply_markup=phone_num_ru)
            await update_user_ru.phone.set()
    
    elif phone.contact:
        await state.update_data(
        	{"phone": phone.contact.phone_number}
        )
        await message.answer("Выберите адрес.", reply_markup=regions_btn_ru)
        await update_user_ru.adress.set()
    else:
        await message.answer("❌ Вы ввели неверный формат!, \nВведите еще раз!")
            
        await message.answer("Или отправить через кнопку ниже! 👇🏻", reply_markup=phone_num_ru)
        await update_user_ru.phone.set()



@dp.message_handler(IsPrivate(), state=update_user_ru.adress)
async def user_name(message: types.Message, state:FSMContext):
    adress = message.text
    await state.update_data(
        {"adress":adress}
    )
    id = message.from_user.id
    
    data = await state.get_data()
    name = data.get("name")
   
    phone = data.get("phone")
    adress = data.get("adress")
    try:
        db.update_user_info(name, phone, adress, id)
    except Exception as err:
        print("yangilashda xatolik>>>>>", err)
        
        
    await message.answer("⚙️ Настройки", reply_markup=user_settings_ru)
    await state.finish()
    
        
        

## maxsulotni izlash ###
@dp.message_handler(text="🔎 Поиск товара", state=None)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Пожалуйста, отправьте идентификатор продукта, который вы ищете:", reply_markup=back_btn_ru)
    await state.set_state("find-pro_ru")

    
# @dp.callback_query_handler( state="find-pro")
# async def select_pro(call: CallbackQuery, state:FSMContext):
#     await call.message.delete()
#     db.delete_product(call.data, call.data)
#     await call.message.answer(f"#id : {call.data}  -  maxsulot o'chirildi ✅")
#     await call.message.answer("Bosh sahifa", reply_markup=admin_main_btn_ru)
#     await state.finish()


@dp.message_handler(text="🔙 Назад",state="find-pro_ru")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Домашняя страница", reply_markup=main_btn_ru)
    await state.finish()
    


@dp.callback_query_handler(text="payme",state="find-pro_ru")
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
            # print(pro_dict)
            # print(product)
            
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
    
    


@dp.callback_query_handler(state="find-pro_ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    # print(call.data)
    id = call.data[7:]
    if call.data[0:7]=="pocket:":
        db.add_sell_product(call.from_user.id, id)
        await call.answer(f"#id:{id} 🛍 добавлено в корзину")
        await call.message.answer(f"✅ #id{id} \nТовар 🛍 добавлен в корзину")
        
    elif call.data[0:7]=="collek:":
        # print("################################",id)
        try:
            db.add_sevimlilar(call.from_user.id, id)
            await call.message.answer(f"✅ #id{id} \nТовар ♥️ добавлен в избранное")
            await call.answer(f"#id:{id} ♥️ добавлен в избранное")
        except :
            await call.answer(f"#id:{id} ♥️ доступно в избранном")
        
    # await call.message.delete()
    
    
    # data = await state.get_data()
    # category = data.get("category")
    # subcategory = data.get("subcategory")

    # len_pro = db.select_product_category(category, subcategory)

    # products = len_pro[tr-1]
    products = db.select_product(id, id)
    
    print(products)
    

    matn = f"id: {products[0]}\n"
    matn += f"Name: {products[1]}\n\n"
    matn += f"{products[2]}\n"

    
    user_id = call.from_user.id
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
            
        for tr in pro_dict:
            # raqam += 1
            
            product = db.select_product(tr, tr)
            narx += pro_dict[tr] * product[3]
    

    # await bot.edit_message_media(media=InputMedia(type='photo', media=products[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_products(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0]))	
    try:
        
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=add_pocket_ru(id,len(pro_count), products[3], products[1], len(sevimlilar), narx))
    except :
        pass
    await state.set_state("find-pro_ru")



@dp.message_handler(state="find-pro_ru")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    if message.text.isdigit():
        
            
        pro_id = int(message.text)
        product_a = db.select_product(pro_id, pro_id)
        # print("sssssssssss-------:",product_a)
        if product_a:
            matn = f"id: {product_a[0]}\n"
            matn += f"Product Name: {product_a[1]}\n\n"
            matn += f" {product_a[2]}\n"

            user_id = message.from_user.id
            # pro_count = db.select_sells_product(user_id, user_id)
            sevimlilar = db.select_sevimlilar(user_id, user_id)
            
            pro_count = db.select_sells_product(user_id, user_id)
            # print("dddddddD------",pro_count)
            # print(pro_count)
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
                    # print(":duct------",pro_dict)
                    # print(product)
                    
                    # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                    narx += pro_dict[id] * product[3]
            
            # await message.reply(matn, reply_markup=admin_main_btn_ru)
            print(pro_id)
            try:
                await bot.send_animation(chat_id=message.chat.id, animation=product_a[6], caption=matn , reply_markup=add_pocket_ru(pro_id,len(pro_count), product_a[3], product_a[1], len(sevimlilar), narx)) 
                
            except :
                
                await bot.send_photo(chat_id=message.chat.id, photo=product_a[6], caption=matn , reply_markup=add_pocket_ru(pro_id,len(pro_count), product_a[3], product_a[1], len(sevimlilar),narx))
    
            # await bot.send_photo(message.chat.id, user[6], matn , reply_markup=add_pocket_ru(id,len(pro_count)))
            
            
        else:
            await message.answer("❌ Товар не найден для этого идентификатора.", reply_markup=back_btn_ru)
    else:
        await message.answer("❌ Просто отправьте идентификатор продукта", reply_markup=back_btn_ru)   
    await message.answer("Если вы ищете другой продукт, отправьте идентификатор:")
    # await state.finish()
    await state.set_state("find-pro_ru")
 ### mahsulotlarni izlash yakunlandi




    
@dp.message_handler(IsPrivate(), text="📞 Связаться с администратором",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    text = f"Связаться с администраторами моего образования: \n\n"
    text += f"Телеграм: @Jaloliddin_Mamatmusayev \n"
    text += f"телефон: +998932977419\n"
    text += f"телефон: +998332977419\n"
    text += f"Адрес: Ташкент, Юнусабад, Шахристан, 10009"
    await message.answer(text)
    await bot.send_location(message.from_user.id, 41.353467, 69.288314)



@dp.message_handler(IsPrivate(), text="🌐 Социальные сети",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    
    text = f"Следите за нами в социальных сетях \n\n"
    text += f"<b>Telegram:</b> <a href='https://t.me/Jaloliddin_Mamatmusayev'>Jaloliddin_Mamatmusayev </a>\n"
    text += f"<b>Instagram:</b><a href='https://instagram.com/jaloliddin_1006'> jaloliddin_1006</a>\n"
    text += f"<b>You Tube:</b> JaloliddinMamatmusayev\n"
    await message.answer(text)




###########  sevimlilar bolimi
global my_tr
my_tr = 0
@dp.message_handler(text="♥️ Избранное", state=None)
async def sevimlilar(message: types.Message, state=FSMContext):
    my_tr = 0
    user_id = message.from_user.id
    my_products = db.select_sevimlilar(user_id, user_id)
    if my_products:
        await message.answer("Ваши любимые продукты", reply_markup=ReplyKeyboardRemove())
    
        i = my_products[my_tr]
        product = db.select_product(i[1], i[1])
        
        # for id in pro_dict:
        # raqam += 1
        
        # product = db.select_product(id, id)
        # print(pro_dict)
        # print(product)
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n\n"
        matn += f" {product[2]}\n"
        
        
        
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
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]

        try:
            await bot.send_animation(chat_id=message.chat.id, animation=product[6], caption=matn, reply_markup=show_like_products_ru(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))
            
        except :
            await bot.send_photo(message.chat.id, product[6], matn, reply_markup=show_like_products_ru(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))

        #     pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
        #     narx += pro_dict[id] * product[3]
        # pro_text += f"\nJami: {narx}"
        await state.set_state("likes-next-ru")
        # print(product)
    else:
        await message.reply("У вас нет выбранных продуктов", reply_markup=main_btn_ru)


@dp.message_handler(IsPrivate(), text="/start",  state="likes-next-ru")
async def bot_start(message: types.Message, state=FSMContext):
    await message.delete()
    await message.answer(f"""Привет {message.from_user.full_name}. Sizni bu yerda ko'rib turganimizdan hursandmiz.""", reply_markup=main_btn_ru)
    await state.finish()


@dp.callback_query_handler(text="back_gr",  state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
     
    await call.message.answer(f"Домашняя страница", reply_markup=main_btn_ru)
    await state.finish()
    
    
    

@dp.callback_query_handler(text="next", state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    global my_tr
    my_tr += 1
    user_id = call.from_user.id
    my_products = db.select_sevimlilar(user_id, user_id)
    
    if len(my_products)>=my_tr+1:
        
            
        i = my_products[my_tr]
        product = db.select_product(i[1], i[1])
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n\n"
        matn += f" {product[2]}\n"
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
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]
        await bot.edit_message_media(media=InputMedia(type='photo', media=product[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_like_products_ru(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))	
    else:
        await call.answer("Это конечный продукт")

        my_tr -= 1

    await state.set_state("likes-next-ru")


        # pro_count = db.select_sells_product(user_id, user_id)



@dp.callback_query_handler(text="prev", state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    global my_tr
    my_tr -= 1
    user_id = call.from_user.id
    my_products = db.select_sevimlilar(user_id, user_id)
    
    if 0 < my_tr+1:
        
            
        i = my_products[my_tr]
        product = db.select_product(i[1], i[1])
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n\n"
        matn += f"{product[2]}\n"
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
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]
        
        await bot.edit_message_media(media=InputMedia(type='photo', media=product[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_like_products_ru(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))	
    else:
        await call.answer("Это первый продукт")

        my_tr += 1

    await state.set_state("likes-next-ru")

    # await call.message.delete()

@dp.callback_query_handler(text="place", state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):

    await call.answer(f"Количество продуктов")
    await state.set_state("likes-next-ru")



@dp.callback_query_handler(text="payme", state="likes-next-ru")
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
        
    

@dp.callback_query_handler( state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    pro_id = call.data[7:]
    user_id = call.from_user.id
    if call.data[0:7]=="pocket:":
        db.add_sell_product(call.from_user.id, pro_id)
    # db.add_sell_product(call.from_user.id, pro_id)
        
        await call.answer(f"#id:{pro_id} 🛍 добавлено в корзину")
    elif call.data[0:7]=="delete:":
        # print("################################",id)
        db.delete_sevimlilar(user_id, pro_id)
        await call.answer(f"#id:{pro_id} 💔 sevimlilardan o'chirildi")
        
        
    my_products = db.select_sevimlilar(user_id, user_id)
    
    if 0 < my_tr:
        
            
        i = my_products[my_tr-1]
        print(my_tr)
        product = db.select_product(i[1], i[1])
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n\n"
        matn += f"{product[2]}\n"from aiogram import types , Bot
from keyboards.default.default_btn_ru import main_btn_ru, maktab_ichi_ru, user_settings_ru, phone_num_ru, regions_btn_ru, back_btn_ru, bogcha_ichi_ru
from keyboards.inline.inline_btn_ru import select_lang_ru, add_pocket_ru, savatcha_btn_ru, show_like_products_ru, guruhlar_ru
from keyboards.default.default_btn import user_settings
from filters import IsPrivate
from states.reg_state_ru import update_user_ru
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery, InputMedia

from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
import sqlite3



@dp.message_handler(IsPrivate(), text="🔙 Назад")
async def bot_start(message: types.Message):
    await message.reply("Главная страница", reply_markup=main_btn_ru)
    


# @dp.message_handler(IsPrivate(), text="Для детского сада",  state=None)
# async def bot_start(message: types.Message, state=FSMContext):
#     print("bogcha ichi rus")
#     await message.reply("Выберите группу", reply_markup=guruhlar_ru("bogcha"))
    

# @dp.message_handler(IsPrivate(), text="Для школы",  state=None)
# async def bot_start(message: types.Message, state=FSMContext):
#     await message.reply("Выберите группу", reply_markup=guruhlar_ru("maktab"))
    
    
    
    
@dp.message_handler(IsPrivate(), text="⚙️ Настройки",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.reply("Информацию о каком разделе вы хотите отредактировать?", reply_markup=user_settings_ru)
    
    
    
@dp.message_handler(IsPrivate(), text="Язык 🇺🇿 / 🇷🇺",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.answer(f" O'zingizga qulay tilni tanlang 🇺🇿 / 🇷🇺  \n    ------------------------------------------  \n Выберите предпочитаемый язык 🇷🇺 / 🇺🇿 ", reply_markup=select_lang_ru)
    await state.set_state("change_lang_ru")

@dp.callback_query_handler( state="change_lang_ru")
async def select_lang_ru_func(call: CallbackQuery, state:FSMContext):
    print(call.data)
    try:
        if call.data=="uzbek":
            lang = 'uzbek'
            db.update_user_lan(lang, call.from_user.id)
            await call.message.answer("⚙️ Sozlamalar", reply_markup=user_settings)
        else:
            lang = 'russian'
            db.update_user_lan(lang, call.from_user.id)
            await call.message.answer("⚙️ Настройки", reply_markup=user_settings_ru)

    except Exception as err:
        print("tilni o'zgartirishda xatolik", err)
    await call.message.delete()
    await state.finish()
    
    
    
@dp.message_handler(IsPrivate(), text="👤 Личная информация",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    await message.answer("Имя Введите вашу фамилию (введите только буквы). \n \n <i><b>Например: </b> Джалолиддин Маматмусаев </i>", reply_markup=ReplyKeyboardRemove())
    await update_user_ru.name.set()

        
@dp.message_handler(IsPrivate(), state=update_user_ru.name)
async def user_name(message: types.Message, state:FSMContext):
   
    name = message.text
    c=0
    for i in name:
        if i.isnumeric():
            c+=1
        
        
    if not c:
        await state.update_data(
			{"name":name}
		)
        # print("ismda faqat harflar")
        await message.answer("Введите свой номер телефона полностью: \n \n <i><b>Например:</b> +998912345678 </i>", reply_markup=phone_num_ru)
        await update_user_ru.phone.set()
    else:
        await message.answer("Ваше имя должно содержать только буквы!")
        await update_user_ru.name.set()



@dp.message_handler(IsPrivate(),  state=update_user_ru.phone, content_types=["contact","text"])
async def user_name(message: types.Message, state:FSMContext):
    phone = message
    
    if phone.text:
        if phone.text[:4] == '+998' and  len(phone.text)==13:
            await state.update_data(
            	{"phone": phone.text}
            )
            await message.answer("Выберите адрес.", reply_markup=regions_btn_ru)
            await update_user_ru.adress.set()
        else:
            await message.answer("❌ Вы ввели неверный формат!, \nВведите еще раз!")
            
            await message.answer("Или отправить через кнопку ниже! 👇🏻", reply_markup=phone_num_ru)
            await update_user_ru.phone.set()
    
    elif phone.contact:
        await state.update_data(
        	{"phone": phone.contact.phone_number}
        )
        await message.answer("Выберите адрес.", reply_markup=regions_btn_ru)
        await update_user_ru.adress.set()
    else:
        await message.answer("❌ Вы ввели неверный формат!, \nВведите еще раз!")
            
        await message.answer("Или отправить через кнопку ниже! 👇🏻", reply_markup=phone_num_ru)
        await update_user_ru.phone.set()



@dp.message_handler(IsPrivate(), state=update_user_ru.adress)
async def user_name(message: types.Message, state:FSMContext):
    adress = message.text
    await state.update_data(
        {"adress":adress}
    )
    id = message.from_user.id
    
    data = await state.get_data()
    name = data.get("name")
   
    phone = data.get("phone")
    adress = data.get("adress")
    try:
        db.update_user_info(name, phone, adress, id)
    except Exception as err:
        print("yangilashda xatolik>>>>>", err)
        
        
    await message.answer("⚙️ Настройки", reply_markup=user_settings_ru)
    await state.finish()
    
        
        

## maxsulotni izlash ###
@dp.message_handler(text="🔎 Поиск товара", state=None)
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Пожалуйста, отправьте идентификатор продукта, который вы ищете:", reply_markup=back_btn_ru)
    await state.set_state("find-pro_ru")

    
# @dp.callback_query_handler( state="find-pro")
# async def select_pro(call: CallbackQuery, state:FSMContext):
#     await call.message.delete()
#     db.delete_product(call.data, call.data)
#     await call.message.answer(f"#id : {call.data}  -  maxsulot o'chirildi ✅")
#     await call.message.answer("Bosh sahifa", reply_markup=admin_main_btn_ru)
#     await state.finish()


@dp.message_handler(text="🔙 Назад",state="find-pro_ru")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    await message.answer("Домашняя страница", reply_markup=main_btn_ru)
    await state.finish()
    


@dp.callback_query_handler(text="payme",state="find-pro_ru")
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
            # print(pro_dict)
            # print(product)
            
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
    
    


@dp.callback_query_handler(state="find-pro_ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    # print(call.data)
    id = call.data[7:]
    if call.data[0:7]=="pocket:":
        db.add_sell_product(call.from_user.id, id)
        await call.answer(f"#id:{id} 🛍 добавлено в корзину")
        await call.message.answer(f"✅ #id{id} \nТовар 🛍 добавлен в корзину")
        
    elif call.data[0:7]=="collek:":
        # print("################################",id)
        try:
            db.add_sevimlilar(call.from_user.id, id)
            await call.message.answer(f"✅ #id{id} \nТовар ♥️ добавлен в избранное")
            await call.answer(f"#id:{id} ♥️ добавлен в избранное")
        except :
            await call.answer(f"#id:{id} ♥️ доступно в избранном")
        
    # await call.message.delete()
    
    
    # data = await state.get_data()
    # category = data.get("category")
    # subcategory = data.get("subcategory")

    # len_pro = db.select_product_category(category, subcategory)

    # products = len_pro[tr-1]
    products = db.select_product(id, id)
    
    print(products)
    

    matn = f"id: {products[0]}\n"
    matn += f"Name: {products[1]}\n\n"
    matn += f"{products[2]}\n"

    
    user_id = call.from_user.id
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
            
        for tr in pro_dict:
            # raqam += 1
            
            product = db.select_product(tr, tr)
            narx += pro_dict[tr] * product[3]
    

    # await bot.edit_message_media(media=InputMedia(type='photo', media=products[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_products(len(len_pro), tr, "prev", "next", len(pro_count) ,products[0]))	
    try:
        
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=add_pocket_ru(id,len(pro_count), products[3], products[1], len(sevimlilar), narx))
    except :
        pass
    await state.set_state("find-pro_ru")



@dp.message_handler(state="find-pro_ru")
async def send_ad_to_all(message: types.Message, state=FSMContext):
    if message.text.isdigit():
        
            
        pro_id = int(message.text)
        product_a = db.select_product(pro_id, pro_id)
        # print("sssssssssss-------:",product_a)
        if product_a:
            matn = f"id: {product_a[0]}\n"
            matn += f"Product Name: {product_a[1]}\n\n"
            matn += f" {product_a[2]}\n"

            user_id = message.from_user.id
            # pro_count = db.select_sells_product(user_id, user_id)
            sevimlilar = db.select_sevimlilar(user_id, user_id)
            
            pro_count = db.select_sells_product(user_id, user_id)
            # print("dddddddD------",pro_count)
            # print(pro_count)
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
                    # print(":duct------",pro_dict)
                    # print(product)
                    
                    # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                    narx += pro_dict[id] * product[3]
            
            # await message.reply(matn, reply_markup=admin_main_btn_ru)
            print(pro_id)
            try:
                await bot.send_animation(chat_id=message.chat.id, animation=product_a[6], caption=matn , reply_markup=add_pocket_ru(pro_id,len(pro_count), product_a[3], product_a[1], len(sevimlilar), narx)) 
                
            except :
                
                await bot.send_photo(chat_id=message.chat.id, photo=product_a[6], caption=matn , reply_markup=add_pocket_ru(pro_id,len(pro_count), product_a[3], product_a[1], len(sevimlilar),narx))
    
            # await bot.send_photo(message.chat.id, user[6], matn , reply_markup=add_pocket_ru(id,len(pro_count)))
            
            
        else:
            await message.answer("❌ Товар не найден для этого идентификатора.", reply_markup=back_btn_ru)
    else:
        await message.answer("❌ Просто отправьте идентификатор продукта", reply_markup=back_btn_ru)   
    await message.answer("Если вы ищете другой продукт, отправьте идентификатор:")
    # await state.finish()
    await state.set_state("find-pro_ru")
 ### mahsulotlarni izlash yakunlandi




    
@dp.message_handler(IsPrivate(), text="📞 Связаться с администратором",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    text = f"Связаться с администраторами моего образования: \n\n"
    text += f"Телеграм: @Jaloliddin_Mamatmusayev \n"
    text += f"телефон: +998932977419\n"
    text += f"телефон: +998332977419\n"
    text += f"Адрес: Ташкент, Юнусабад, Шахристан, 10009"
    await message.answer(text)
    await bot.send_location(message.from_user.id, 41.353467, 69.288314)



@dp.message_handler(IsPrivate(), text="🌐 Социальные сети",  state=None)
async def bot_start(message: types.Message, state=FSMContext):
    
    text = f"Следите за нами в социальных сетях \n\n"
    text += f"<b>Telegram:</b> <a href='https://t.me/Jaloliddin_Mamatmusayev'>Jaloliddin_Mamatmusayev </a>\n"
    text += f"<b>Instagram:</b><a href='https://instagram.com/jaloliddin_1006'> jaloliddin_1006</a>\n"
    text += f"<b>You Tube:</b> JaloliddinMamatmusayev\n"
    await message.answer(text)




###########  sevimlilar bolimi
global my_tr
my_tr = 0
@dp.message_handler(text="♥️ Избранное", state=None)
async def sevimlilar(message: types.Message, state=FSMContext):
    my_tr = 0
    user_id = message.from_user.id
    my_products = db.select_sevimlilar(user_id, user_id)
    if my_products:
        await message.answer("Ваши любимые продукты", reply_markup=ReplyKeyboardRemove())
    
        i = my_products[my_tr]
        product = db.select_product(i[1], i[1])
        
        # for id in pro_dict:
        # raqam += 1
        
        # product = db.select_product(id, id)
        # print(pro_dict)
        # print(product)
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n\n"
        matn += f" {product[2]}\n"
        
        
        
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
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]

        try:
            await bot.send_animation(chat_id=message.chat.id, animation=product[6], caption=matn, reply_markup=show_like_products_ru(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))
            
        except :
            await bot.send_photo(message.chat.id, product[6], matn, reply_markup=show_like_products_ru(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))

        #     pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
        #     narx += pro_dict[id] * product[3]
        # pro_text += f"\nJami: {narx}"
        await state.set_state("likes-next-ru")
        # print(product)
    else:
        await message.reply("У вас нет выбранных продуктов", reply_markup=main_btn_ru)


@dp.message_handler(IsPrivate(), text="/start",  state="likes-next-ru")
async def bot_start(message: types.Message, state=FSMContext):
    await message.delete()
    await message.answer(f"""Привет {message.from_user.full_name}. Sizni bu yerda ko'rib turganimizdan hursandmiz.""", reply_markup=main_btn_ru)
    await state.finish()


@dp.callback_query_handler(text="back_gr",  state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
     
    await call.message.answer(f"Домашняя страница", reply_markup=main_btn_ru)
    await state.finish()
    
    
    

@dp.callback_query_handler(text="next", state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    global my_tr
    my_tr += 1
    user_id = call.from_user.id
    my_products = db.select_sevimlilar(user_id, user_id)
    
    if len(my_products)>=my_tr+1:
        
            
        i = my_products[my_tr]
        product = db.select_product(i[1], i[1])
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n\n"
        matn += f" {product[2]}\n"
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
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]
        await bot.edit_message_media(media=InputMedia(type='photo', media=product[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_like_products_ru(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))	
    else:
        await call.answer("Это конечный продукт")

        my_tr -= 1

    await state.set_state("likes-next-ru")


        # pro_count = db.select_sells_product(user_id, user_id)



@dp.callback_query_handler(text="prev", state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    global my_tr
    my_tr -= 1
    user_id = call.from_user.id
    my_products = db.select_sevimlilar(user_id, user_id)
    
    if 0 < my_tr+1:
        
            
        i = my_products[my_tr]
        product = db.select_product(i[1], i[1])
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n\n"
        matn += f"{product[2]}\n"
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
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]
        
        await bot.edit_message_media(media=InputMedia(type='photo', media=product[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_like_products_ru(len(my_products), my_tr+1, len(pro_count), product[0], product[3], product[1], narx))	
    else:
        await call.answer("Это первый продукт")

        my_tr += 1

    await state.set_state("likes-next-ru")

    # await call.message.delete()

@dp.callback_query_handler(text="place", state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):

    await call.answer(f"Количество продуктов")
    await state.set_state("likes-next-ru")



@dp.callback_query_handler(text="payme", state="likes-next-ru")
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
        
    

@dp.callback_query_handler( state="likes-next-ru")
async def select_pro(call: CallbackQuery, state: FSMContext):
    pro_id = call.data[7:]
    user_id = call.from_user.id
    if call.data[0:7]=="pocket:":
        db.add_sell_product(call.from_user.id, pro_id)
    # db.add_sell_product(call.from_user.id, pro_id)
        
        await call.answer(f"#id:{pro_id} 🛍 добавлено в корзину")
    elif call.data[0:7]=="delete:":
        # print("################################",id)
        db.delete_sevimlilar(user_id, pro_id)
        await call.answer(f"#id:{pro_id} 💔 sevimlilardan o'chirildi")
        
        
    my_products = db.select_sevimlilar(user_id, user_id)
    
    if 0 < my_tr:
        
            
        i = my_products[my_tr-1]
        print(my_tr)
        product = db.select_product(i[1], i[1])
        
        matn = f"id: {product[0]}\n"
        matn += f"<b>Name: {product[1]}</b>\n\n"
        matn += f"{product[2]}\n"
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
                
                producta = db.select_product(id, id)
                # print(pro_dict)
                # print(product)
                
                # pro_text += f"{raqam}. id: {product[0]} - {product[1]}: \n \t  {product[3]} x {pro_dict[id]} ta  =  {pro_dict[id] * product[3]} so'm \n"
                narx += pro_dict[id] * producta[3]
        
        await bot.edit_message_media(media=InputMedia(type='photo', media=product[6], caption = matn), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=show_like_products_ru(len(my_products), my_tr, len(pro_count), product[0], product[3], product[1], narx))	
    else:
        await call.message.delete()
        await call.message.answer("У вас не осталось избранных сообщений", reply_markup=main_btn_ru)
        await call.answer("У вас не осталось избранных сообщений")

    #     my_tr += 1

    await state.set_state("likes-next-ru")
