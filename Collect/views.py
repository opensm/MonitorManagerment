from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View


class IndexView(View):
    template_name = 'index.html'

    @method_decorator(login_required)
    def post(self, request):
        return render(request, self.template_name)

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)
