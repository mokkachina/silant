# menu = [
#     {'title': "+7-8352-20-12-09, telegram"},
#     {'title': "Авторизация", 'url_name': 'add_user'},
#     {'title': "Электронная сервисная книжка 'Мой Силант'"},
# ]

class TitleMixin:
    title_page = None
    extra_context = {}


    def __init__(self):
        if self.title_page:
            self.extra_context['homepage'] = self.title_page

        # if self.cat_selected is not None:
        #     self.extra_context['cat_selected'] = self.cat_selected



    # def get_mixin_context(self, context, **kwargs):
    #     context['cat_selected'] = None
    #     context.update(kwargs)
    #     return context