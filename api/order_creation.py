import pandas as pd

def create_link(total_order):
    art_df = pd.read_excel(r"exel_files\total_prod.xlsx")
    add_link = ''
    for key, value in total_order.items():
        if value[1] > 0:
            print(value, art_df[art_df['Наименование рабочее'] == value[0]])
            add_link += str(art_df[art_df['Наименование рабочее'] == value[0]]['Артикул'].values[0])
            add_link += str('_' + str(value[1]) + ';')
    print(add_link)
    link = f'https://owen.ru/upl_files/tests/cart_interface/cart.php?prods={add_link}'
    return link

def form_total_order(user_dict, callback):
    total_order = {
        'vfc': [user_dict[callback.from_user.id]['vfc_model_selected']["Модификация"].values[0], 1], 
        'lpo': [callback.data, 1 if callback.data != 'no' else 0], 
    }
    if user_dict[callback.from_user.id]['prom_protocol']:
        total_order['prom_plata'] = [user_dict[callback.from_user.id]['prom_protocol'],  1]
    
    if user_dict[callback.from_user.id]['res_type'] == 'RB3':
        total_order['rb3'] = [user_dict[callback.from_user.id]['rb3'].values[0],  1 if user_dict[callback.from_user.id]['rb3'].values[0] else 0]
    else:
        total_order['rb1400'] = ['РБ1-400-К20', user_dict[callback.from_user.id]['rb1400'] * 1] 
        total_order['rb1080'] = ['РБ1-080-1К0', user_dict[callback.from_user.id]['rb1080'] * 1] 

    if user_dict[callback.from_user.id]['plata']:
        total_order['plata'] = [str(user_dict[callback.from_user.id]['plata']), 1] 

    if user_dict[callback.from_user.id]['pvv1']:
        total_order['pvv1'] = ['ПВВ1', 1] 

    try:
        total_order['rmt'] = [user_dict[callback.from_user.id]['rmt_model']["Реакторы моторные"].values[0], 1] 
    except:
        print('рмт не подобран')

    return total_order