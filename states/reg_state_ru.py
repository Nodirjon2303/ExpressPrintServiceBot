from aiogram.dispatcher.filters.state import StatesGroup,State



class reg_user_ru(StatesGroup):

    lang = State()
    name = State()
    phone = State()
    adress = State()



class update_user_ru(StatesGroup):

    lang = State()
    name = State()
    phone = State()
    adress = State()



class products_ru(StatesGroup):

    name = State()
    caption = State()
    category = State()
    subcategory = State()
    price = State()
    photo = State()
    finish = State()
    


class show_buy_ru(StatesGroup):
 
    category = State()
    subcategory = State()
    price = State()
    next = State()
    prev = State()



class savatcha_state_ru(StatesGroup):
 
    category = State()
    subcategory = State()
    price = State()
    next = State()
    prev = State()
                                                                                    from aiogram.dispatcher.filters.state import StatesGroup,State



class reg_user_ru(StatesGroup):

    lang = State()
    name = State()
    phone = State()
    adress = State()



class update_user_ru(StatesGroup):

    lang = State()
    name = State()
    phone = State()
    adress = State()



class products_ru(StatesGroup):

    name = State()
    caption = State()
    category = State()
    subcategory = State()
    price = State()
    photo = State()
    finish = State()
    


class show_buy_ru(StatesGroup):
 
    category = State()
    subcategory = State()
    price = State()
    next = State()
    prev = State()



class savatcha_state_ru(StatesGroup):
 
    category = State()
    subcategory = State()
    price = State()
    next = State()
    prev = State()
