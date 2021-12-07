from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView

from .forms import SignUpForm, ProductForm, BuyForm, ReturnForm
from .models import Goods, Customer, ReturnModel, BuyModel

from datetime import datetime, timedelta, timezone
from django.urls import reverse_lazy
from django.db.models import F, Q


class HomePage(TemplateView):
    template_name = 'home.html'
    extra_context = {'create_form': BuyForm, 'return_form': ReturnForm}

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['goods'] = Goods.objects.all()
        return context


class MyLogin(LoginView):
    template_name = 'signin.html'


class MyRegister(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


class MyLogOut(LogoutView):
    template_name = 'signout.html'


class CreateProduct(CreateView):
    template_name = 'create_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')


class UpdateProduct(UpdateView):
    template_name = 'update_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Goods.objects.all()


class BuyProduct(CreateView):
    template_name = 'buy_product.html'
    form_class = BuyForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.good = Goods.objects.get(id=self.request.POST.get('good_id'))
        obj.user = self.request.user
        amount_in_form = int(self.request.POST.get('amount'))

        if amount_in_form > obj.good.amount:
            form.add_error('amount', 'Amount is bigger than expected!')
            return super().form_invalid(form)

        elif self.request.user.purse < obj.good.price * amount_in_form:
            form.add_error(None, 'Not enough money on purse!')
            return super().form_invalid(form)

        Customer.objects.filter(id=self.request.user.id).update(purse=F('purse') - obj.good.price * amount_in_form)
        Goods.objects.filter(id=self.request.POST.get('good_id')).update(amount=F('amount') - amount_in_form)
        obj.save()
        return super().form_valid(form)

        # print(self.request.POST)
        # print(self.request.user.purse, ' - purse of User')
        # print(self.request.POST.get('amount'), ' - amount in Form')
        # print(self.request.POST.get('good_id'), ' - id of Good')
        # print(Goods.objects.get(id=self.request.POST.get('good_id')).amount, ' - amount of Good')


class ReturnProduct(CreateView):
    template_name = 'return_product.html'
    success_url = reverse_lazy('home')
    form_class = ReturnForm

    def get_form_kwargs(self):
        kwargs = super(ReturnProduct, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['good_id'] = self.request.POST.get('good_id')
        return kwargs


class ReturnPage(TemplateView):
    template_name = 'return_page.html'
    extra_context = {'all_returns': ReturnModel.objects.all()}


class DeleteReturnObj(DeleteView):
    template_name = 'success_del_return.html'
    model = ReturnModel
    success_url = '/return-page/'
