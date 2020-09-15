from .models import CustomUserManager, User, Form, Report, Notification, Skill, Position, Division, Timeline
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .serializers import FormSerializer, ReportSerializer
from rest_framework import viewsets, generics
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import xlwt
import xlsxwriter
from datetime import datetime
from django.db.models.functions import ExtractDay
import json

UserModel = get_user_model()


def index(request):
    """View function for home page of site."""
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login-user'))
    # email = request.user
    # # Generate counts of some of the main objects
    # context = {
    # 	'email': email,
    # }
    # return render(request, 'index.html', context=context)
    return redirect(reverse_lazy('timeline'))


def about_us(request):
    return render(request, 'about_us.html')


# -----------------------------------------------------------------------------------------------------------------------------------------
# Login/logout view
# -----------------------------------------------------------------------------------------------------------------------------------------

def loginUser(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('home'))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, _('You are logged in sucessfully!!!'))
            return redirect('home')
        else:
            messages.info(request, _('username or password is incorrect'))

    context = {
    }
    return render(request, '../templates/sign_up/login.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, _('You are logged out'))
    return redirect('login-user')


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('/')
    '''
	Please work on me -> success & error messages & style templates
	'''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            update_session_auth_hash(request, user)

            messages.success(request, 'Password changed successfully',
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('changepassword')
        else:
            messages.error(request, 'Error,changing password', extra_tags='alert alert-warning alert-dismissible show')
            return redirect('changepassword')

    form = PasswordChangeForm(request.user)
    return render(request, '../templates/sign_up/password_reset_form.html', {'form': form})


# -----------------------------------------------------------------------------------------------------------------------------------------
# Request form view
# -----------------------------------------------------------------------------------------------------------------------------------------

def getMyForms(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login-user'))
    return render(request, 'formrequest/list_form_request_employee.html')


def getFormRequest(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login-user'))
    if request.user.is_manager == True:
        return render(request, 'formrequest/list_form_request_manager.html')
    return HttpResponse(status=404)


class MyForms(viewsets.ModelViewSet):
    # queryset = Form.objects.filter(form_type="il")
    serializer_class = FormSerializer

    def get_queryset(self):
        return Form.objects.filter(sender=self.request.user)


class FormRequest(viewsets.ModelViewSet):
    serializer_class = FormSerializer

    def get_queryset(self):
        return Form.objects.filter(receiver=self.request.user)


class FormCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login-user'
    redirect_field_name = 'redirect_to'
    model = Form
    template_name = 'formrequest/form_request.html'
    fields = (
        'title', 'content', 'form_type', 'compensation_from', 'compensation_to', 'leave_from', 'leave_to',
        'checkin_time',
        'checkout_time')
    success_url = reverse_lazy('my_forms')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        form.instance.receiver = self.request.user.manager
        form.instance.sender = self.request.user
        form.instance.division = self.request.user.division
        form.instance.created_at = timezone.now()
        return super(FormCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return redirect(reverse_lazy('my_forms'))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = None
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FormUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Form
    template_name = 'formrequest/update_form_request.html'
    fields = ('title', 'content', 'form_type', 'compensation_from', 'compensation_to',
              'leave_from', 'leave_to', 'checkin_time', 'checkout_time', 'status')
    success_url = reverse_lazy('my_forms')

    def test_func(self):
        if (self.get_object().status == 'p') and (self.get_object().sender == self.request.user):
            return True
        return False


@login_required
@csrf_exempt
def form_delete(request, pk):
    form = get_object_or_404(Form, pk=pk)
    data = dict()
    if (request.method == 'POST') and (form.sender == request.user):
        form.delete()
        data['form_is_valid'] = True
        return JsonResponse(data)
    return JsonResponse(data)


@login_required
@csrf_exempt
def manager_update(request, pk):
    form = get_object_or_404(Form, pk=pk)
    if (form.status != 'r') and (form.status != 'a') and (form.receiver == request.user) and (request.method == 'POST'):
        form.status = request.POST['status']
        form.save()
        return JsonResponse({'status': 'Success', 'msg': 'Update successfully'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


# -----------------------------------------------------------------------------------------------------------------------------------------
# Report view
# -----------------------------------------------------------------------------------------------------------------------------------------

def getListReport(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login-user'))
    return render(request, 'report/list_report.html')


def getListReportManager(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login-user'))
    if request.user.is_manager == True:
        return render(request, 'report/manager_list_report.html')
    return HttpResponse(status=404)


class ListReport(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        return Report.objects.filter(sender=self.request.user)


class ListReportManager(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        return Report.objects.filter(receiver=self.request.user)


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    login_url = 'login-user'
    redirect_field_name = 'redirect_to'
    template_name = 'report/report_create.html'
    fields = ('plan', 'actual', 'issue', 'next')
    success_url = reverse_lazy('reports')

    def form_valid(self, report):
        if self.request.user.is_authenticated:
            report.instance.sender = self.request.user
            report.instance.receiver = self.request.user.manager
            report.instance.division = self.request.user.division
            report.instance.created_at = timezone.now()
        return super(ReportCreateView, self).form_valid(report)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return redirect(reverse_lazy('report_create'))

    def post(self, request, *args, **kwargs):
        report = self.get_form()
        self.object = None
        if report.is_valid():
            return self.form_valid(report)
        else:
            return self.form_invalid(report)


class ReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Report
    template_name = 'report/report_update.html'
    fields = ('plan', 'actual', 'issue', 'next')
    success_url = reverse_lazy('reports')

    def test_func(self):
        if self.get_object().sender == self.request.user:
            return True
        return False


@login_required
@csrf_exempt
def report_delete(request, pk):
    report = get_object_or_404(Report, pk=pk)
    data = dict()
    if (request.method == 'POST') and (report.sender == request.user):
        report.delete()
        data['form_is_valid'] = True
        return JsonResponse(data)

    return JsonResponse(data)


# -----------------------------------------------------------------------------------------------------------------------------------------
# Profile view
# -----------------------------------------------------------------------------------------------------------------------------------------

def profile(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login-user'))
    return render(request, 'profile/profile.html')


def profiletUser(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login-user'))
    return render(request, 'profile.html')


def profile_update(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login-user'))
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile/profile_update.html', context)


# -----------------------------------------------------------------------------------------------------------------------------------------
# Active account view
# -----------------------------------------------------------------------------------------------------------------------------------------

def success_activation(request):
    return render(request, '../templates/sign_up/verification_success.html')


def fail_activation(request):
    return render(request, '../templates/sign_up/verification_fail.html')


def inform(request):
    return render(request, '../templates/sign_up/inform_to_verify.html')


@staff_member_required
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('../templates/sign_up/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email],
            )
            email.content_subtype = "html"
            email.send()
            return HttpResponseRedirect(reverse('inform'))
    else:
        form = SignUpForm()
    return render(request, '../templates/sign_up/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('success_activation'))
    else:
        return HttpResponseRedirect(reverse('fail_activation'))


def division_view(request):
    return render(request, 'division/division_view.html')


def get_notification_info(request):
    if not request.user.is_authenticated:
        context = {
            'unreaded_notification_count': '',
            'unreaded_notifications': '',
            'old_notifications': ''
        }
        return JsonResponse(context)

    notifications = Notification.objects.filter(receiver=request.user).order_by('-created_at')
    old_notifications = notifications.filter(is_read=True)
    unreaded_notifications = notifications.filter(is_read=False).order_by('-created_at')
    context = {
        'unreaded_notification_count': unreaded_notifications.count(),
        'unreaded_notifications': serializers.serialize('json', unreaded_notifications[:5]),
        'old_notifications': serializers.serialize('json', old_notifications[:3])
    }
    return JsonResponse(context)


def mark_notification_as_readed(request):
    if not request.method == 'POST':
        return JsonResponse({})
    if not request.user.is_authenticated:
        return JsonResponse({})
    notifications = request.user.receiver
    unreaded_notifications = notifications.filter(is_read=False)
    for notification in unreaded_notifications.order_by('created_at'):
        notification.is_read = True
        notification.save()
    return JsonResponse({'unreaded_notification_count': unreaded_notifications.count()})


def export_reports_xls(request):
    # user = request.user
    # reports = Report.objects.filter(receiver=user)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reports.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Reports Data')  # this will make a sheet named Users Data

    # Sheet header, first row

    row_num = 0

    font_style1 = xlwt.XFStyle()
    font_style1.font.bold = True

    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    font_style1.borders = borders

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['light_blue']
    font_style1.pattern = pattern

    columns = ['Sender', 'Date creeated', 'Plan', 'Actual', 'Issue', 'Tomorrow', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style1)  # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    font_style.borders = borders

    # data
    rp = request.user
    rep = Report.objects.filter(receiver=rp)
    # orders = rep.order_by('created_at')
    rows = rep.values_list('sender__name', 'created_at', 'plan__title', 'actual', 'issue', 'next')
    # for row in rows:
    # 	row_num += 1
    # 	for col_num in range(len(row)):
    # 		ws.write(row_num, col_num, row[col_num], font_style)

    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                val = val.strftime('%H:%M %d/%m/%Y')
            ws.write(row_num, col, val, font_style)

    wb.save(response)

    return response


def export_forms_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="forms.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Forms Data')  # this will make a sheet named Users Data
    ws2 = wb.add_sheet('Forms Leave Early')
    ws3 = wb.add_sheet('Forms Leave Out')
    ws4 = wb.add_sheet('Forms In Late')

    # header
    row_num = 0
    row_num2 = 0
    row_num3 = 0
    row_num4 = 0

    font_style1 = xlwt.XFStyle()

    font_style1.font.bold = True

    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    font_style1.borders = borders

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['light_blue']
    font_style1.pattern = pattern

    # sheet 1 first row
    columns = ['Title', 'Type', 'Sender', 'Date creeated', 'Division', 'Reason', 'Status']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style1)  # at 0 row 0 column

    # sheet 2 first row
    columns2 = ['Title',
                'Division',
                'Date creeated',
                'Sender',
                'Checkout',
                'Compensation_from',
                'Compensation_to',
                'Reason',
                'Status']
    for col_num in range(len(columns2)):
        ws2.write(row_num2, col_num, columns2[col_num], font_style1)  # at 0 row 0 column

    # sheet 3 first row
    columns3 = ['Title',
                'Division',
                'Date creeated',
                'Sender',
                'Leave_from',
                'Leave_to',
                'Compensation_from',
                'Compensation_to',
                'Reason',
                'Status']
    for col_num in range(len(columns3)):
        ws3.write(row_num3, col_num, columns3[col_num], font_style1)  # at 0 row 0 column

    # sheet 4 first row
    columns4 = ['Title',
                'Division',
                'Date creeated',
                'Sender',
                'Ckeckin',
                'Leave_from',
                'Leave_to',
                'Reason',
                'Status']
    for col_num in range(len(columns4)):
        ws4.write(row_num4, col_num, columns4[col_num], font_style1)  # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    font_style.borders = borders

    # data
    rp = request.user
    rep = Form.objects.filter(receiver=rp)
    # orders = rep.order_by('created_at')
    le = Form.objects.filter(receiver=rp, form_type='le')
    lo = Form.objects.filter(receiver=rp, form_type='lo')
    il = Form.objects.filter(receiver=rp, form_type='il')

    # row of sheet 1
    rows = rep.values_list(
        'title',
        'form_type',
        'sender__name',
        'created_at',
        'division__name',
        'content',
        'status'
    )

    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                val = val.strftime('%H:%M %d/%m/%Y')
            ws.write(row_num, col, val, font_style)

    # row of sheet 2
    rows2 = le.values_list(
        'title',
        'division__name',
        'created_at',
        'sender__name',
        'checkout_time',
        'compensation_from',
        'compensation_to',
        'content',
        'status'
    )

    for row, rowdata in enumerate(rows2):
        row_num2 += 1
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                val = val.strftime('%H:%M %d/%m/%Y')
            ws2.write(row_num2, col, val, font_style)

    # row of sheet 3
    rows3 = lo.values_list(
        'title',
        'division__name',
        'created_at',
        'sender__name',
        'leave_from',
        'leave_to',
        'compensation_from',
        'compensation_to',
        'content',
        'status'
    )

    # wb.save(response)
    for row, rowdata in enumerate(rows3):
        row_num3 += 1
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                val = val.strftime('%H:%M %d/%m/%Y')
            ws3.write(row_num3, col, val, font_style)

    # row of sheet 4
    rows4 = il.values_list(
        'title',
        'division__name',
        'created_at',
        'sender__name',
        'checkin_time',
        'leave_from',
        'leave_to',
        'content',
        'status'
    )

    # wb.save(response)
    for row, rowdata in enumerate(rows4):
        row_num4 += 1
        for col, val in enumerate(rowdata):
            if isinstance(val, datetime):
                val = val.strftime('%H:%M %d/%m/%Y')
            ws4.write(row_num4, col, val, font_style)

    wb.save(response)

    return response


from django.core.paginator import Paginator, InvalidPage


def timeline_pagination(request):
    # Pull the data
    object_list = Timeline.objects.filter(user_id=request.user).order_by("-created_at")
    timeline = []
    if object_list.count() > 0:
        new_dic = {
            "date": object_list[0].created_at.strftime('%d-%m-%Y'),
            "events": [],
        }
        for ob in object_list:
            if ob.created_at.strftime('%d-%m-%Y') == new_dic["date"]:
                new_dic["events"].append({
                    "time": ob.created_at.strftime('%H:%M'),
                    "event": ob.event,
                    "content": ob.content,
                })
            else:
                timeline.append(new_dic)
                new_dic = {
                    "date": ob.created_at.strftime('%d-%m-%Y'),
                    "events": [],
                }
                new_dic["events"].append({
                    "time": ob.created_at.strftime('%H:%M'),
                    "event": ob.event,
                    "content": ob.content,
                })
        timeline.append(new_dic)
    # Grab the first page of 100 items
    paginator = Paginator(timeline, 3)
    page_obj = paginator.page(1)
    # Pass out the data
    context = {
        "object_list": page_obj.object_list,
        "page": page_obj,
    }
    template = 'timeline.html'
    return render(request, template, context)


def timeline_pagination_json(request, page):
    # Pull the data
    object_list = Timeline.objects.filter(user_id=request.user).order_by("-created_at")
    timeline = []
    if object_list.count() > 0:
        new_dic = {
            "date": object_list[0].created_at.strftime('%d-%m-%Y'),
            "events": [],
        }
        for ob in object_list:
            if ob.created_at.strftime('%d-%m-%Y') == new_dic["date"]:
                new_dic["events"].append({
                    "time": ob.created_at.strftime('%H:%M'),
                    "event": ob.event,
                    "content": ob.content,
                })
            else:
                timeline.append(new_dic)
                new_dic = {
                    "date": ob.created_at.strftime('%d-%m-%Y'),
                    "events": [],
                }
                new_dic["events"].append({
                    "time": ob.created_at.strftime('%H:%M'),
                    "event": ob.event,
                    "content": ob.content,
                })
        timeline.append(new_dic)
    paginator = Paginator(timeline, 3)
    try:
        page_obj = paginator.page(page)
    except InvalidPage:
        # Return 404 if the page doesn't exist
        raise Http404
    # Pass out the data
    context = {
        "object_list": page_obj.object_list,
        "page": page,
        "hasNext": page_obj.has_next()
    }
    return JsonResponse(context)
