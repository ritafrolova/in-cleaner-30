from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomUserCreationForm, ProfileSettingsForm, OrderForm, ReportForm
from .models import Profile, CustomUser, Specialty, Order, Report


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['photo'].widget.attrs['enctype'] = 'multipart/form-data'  # Устанавливаем атрибут enctype поля формы
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        profile = Profile(user=self.object, photo=self.request.FILES.get('photo'))
        profile.save()
        return response


def home(request):
    context = {}
    if not request.user.is_authenticated:
        pass

    elif request.user.is_worker:
        user_specialty = request.user.profile.specialty
        context['orders'] = Order.objects.all().filter(is_accepted=False, specialty=user_specialty)
    else:
        specialties = Specialty.objects.all()
        workers = CustomUser.objects.filter(is_worker=True)[:5]
        context['specialties'] = specialties
        context['workers'] = workers

    return render(request, 'home.html', context=context)


def profile_settings(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = ProfileSettingsForm(instance=profile)

    context = {
        'form': form,
    }
    return render(request, 'profile-settings.html', context)


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('home')
    else:
        context = {
            'form': OrderForm
        }
    return render(request, 'create-order.html', context=context)


def user_orders(request):
    if request.user.is_worker:
        orders = Order.objects.all().filter(worker=request.user.id)
    else:
        orders = Order.objects.all().filter(user=request.user.id)
    return render(request, 'user-orders.html', {'orders': orders})


def assign_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.is_accepted = True
    order.worker = request.user
    order.save()
    return redirect('user-orders')


def create_report(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.order = order
            report.save()
            order.is_done = True
            order.report = report
            order.save()
            return redirect('user-orders')
    else:
        form = ReportForm()

    return render(request, 'create-report.html', {'form': form, 'order': order})


def show_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if report.order.user.id == request.user.id:
        return render(request, 'report.html', {'report': report})
    return redirect('user-orders')


def confirm_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not order.is_confirmed:
        user = order.user
        worker = order.worker

        user.balance -= order.price
        worker.balance += order.price
        order.is_confirmed = True
        user.save()
        order.save()
        worker.save()
    return redirect('user-orders')


def tinder(request):
    context = {}
    if request.user.is_worker:
        context['orders'] = Order.objects.all().filter(is_accepted=False, worker=request.user)
    else:
        context['workers'] = CustomUser.objects.filter(is_worker=True)
    return render(request, 'tinder.html', context=context)


def assign_tinder_order(request, worker_id):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        print(form.__dict__)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            worker = get_object_or_404(CustomUser, pk=worker_id)
            order.worker = worker
            order.save()
            return redirect('home')
    else:
        return render(request, 'create-tinder-order.html', {'form': OrderForm})


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order.delete()
    return redirect('home')
