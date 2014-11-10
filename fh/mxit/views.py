from django.views.generic import View, TemplateView

  

class HomepageView(TemplateView):
    template_name = 'mxit/home.html'

    def get_context_data(self, *args, **kwargs):
        page_context = {}

        page_context['categories'] = self.get_categories()

        return page_context

    def get_categories(self):
        return []
        
