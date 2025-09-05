menu = [{'title': "Создать заказ-наряд", 'url_name': 'zakaz_naryad'},
        {'title': "Взять аванс", 'url_name': 'get_avans'},
        {'title': "Добавить расходник", 'url_name': 'raskhod'},
        {'title': "Оплата", 'url_name': 'oplata'},
        ]


class DataMixin:
    paginate_by = 10
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'mainmenu' not in self.extra_context:
            self.extra_context['mainmenu'] = menu

