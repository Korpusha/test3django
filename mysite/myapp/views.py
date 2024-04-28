from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView

from .forms import SignUpForm, ProductForm, BuyForm, ReturnForm
from .models import Goods, Customer, ReturnModel, BuyModel

from datetime import datetime, timedelta, timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import F
from django.contrib import messages


class HomePage(ListView):
    template_name = 'home.html'
    paginate_by = 8
    model = Goods

    def get_queryset(self):
        return Goods.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = BuyForm

        return context


class CartPage(ListView):
    template_name = 'interacts_html/cart_product.html'
    model = BuyModel
    paginate_by = 10

    def get_queryset(self):
        return BuyModel.objects.filter(user=self.request.user)


class MyLogin(SuccessMessageMixin, LoginView):
    template_name = 'sign_html/signin.html'
    success_message = "You have successfully logged in."


class MyRegister(SuccessMessageMixin, CreateView):
    template_name = 'sign_html/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    success_message = "User has been created successfully."


class MyLogOut(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class CreateProduct(SuccessMessageMixin, CreateView):
    template_name = 'interacts_html/create_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')
    success_message = "Product have been created successfully."


class UpdateProduct(SuccessMessageMixin, UpdateView):
    template_name = 'interacts_html/update_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')
    success_message = "Product has been updated successfully."

    def get_queryset(self):
        return Goods.objects.all()


class BuyProduct(SuccessMessageMixin, CreateView):
    template_name = 'interacts_html/buy_product.html'
    form_class = BuyForm
    success_url = reverse_lazy('home')
    success_message = "Product has been bought successfully. (3 mins to return)"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.good = Goods.objects.get(id=self.request.POST.get('good_id'))
        obj.user = self.request.user
        amount_in_form = int(self.request.POST.get('amount'))

        if not obj.good.amount:
            form.add_error(None, 'No products are available, Sorry!')
            return super().form_invalid(form)

        elif amount_in_form > obj.good.amount:
            form.add_error('amount', 'Amount is bigger than expected!')
            return super().form_invalid(form)

        elif self.request.user.purse < obj.good.price * amount_in_form:
            form.add_error(None, 'Not enough money on purse!')
            return super().form_invalid(form)

        Customer.objects.filter(id=self.request.user.id).update(purse=F('purse') - obj.good.price * amount_in_form)
        Goods.objects.filter(id=self.request.POST.get('good_id')).update(amount=F('amount') - amount_in_form)
        obj.save()
        return super().form_valid(form)


class ReturnProduct(CreateView):
    template_name = 'return_html/return_product.html'
    success_url = reverse_lazy('home')
    form_class = ReturnForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        purchase = BuyModel.objects.filter(id=self.request.POST.get('return_id'), interact_date__gte=(
                    datetime.now(timezone.utc) - timedelta(minutes=3)).astimezone())
        if not purchase:
            form.add_error(None, 'Time to return this product has gone!')
            return super().form_invalid(form)
        obj.purchase = purchase[0]
        obj.save()
        return super().form_valid(form)


class ReturnPage(TemplateView):
    template_name = 'return_html/return_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_returns'] = ReturnModel.objects.all()
        return context


class DeleteReturnObj(DeleteView):
    next_page = reverse_lazy('home')
    model = ReturnModel
    success_url = reverse_lazy('return_page')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.POST.get('return_id'):
            return_id = self.request.POST.get('return_id')

            return_query = ReturnModel.objects.filter(id=return_id).values('purchase_id')
            buy_id = return_query[0].get('purchase_id')

            buy_query = BuyModel.objects.filter(id=buy_id).values()
            amount_form = buy_query[0].get('amount')
            prod_id = buy_query[0].get('good_id')

            goods_query = Goods.objects.filter(id=prod_id).values()
            good_price = goods_query[0].get('price')
            add_to_purse = amount_form * good_price

            Customer.objects.filter(id=self.request.user.id).update(purse=F('purse') + add_to_purse)
            Goods.objects.filter(id=prod_id).update(amount=F('amount') + amount_form)

        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
