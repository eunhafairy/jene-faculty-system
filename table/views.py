from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.views.generic.edit import DeleteView
import pandas as pd
import xlwt
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import FacultySubject, FacultyExtension
from .forms import FacultySubjectForm, FacultyExtensionForm
from django.conf import settings
from accounts.reports import UserReport
from django.http import HttpResponse
from accounts.models import User
import csv
from django.utils.encoding import smart_str
from io import StringIO
import csv# Create your views here.
class FacultySubjectCreateView(LoginRequiredMixin, CreateView):
    model = FacultySubject
    success_url = "/user/my-subjects"
    template_name = "table/faculty_subject_form.html"
    login_url = "/user/login"
    form_class = FacultySubjectForm
    # authorization
    # def get(self, request, *args, **kwargs):
    #     if self.request.user.role != "1":
    #         return redirect('home')
    #     return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print("Self object ", self.object.subject)
        existing = FacultySubject.objects.filter(subject = self.object.subject, user = self.request.user)
        print('is it existing: ',existing)
        if existing:
            return redirect('table.error.exist')
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class FacultySubjectAlreadyExists(LoginRequiredMixin, TemplateView):
    template_name = "table/faculty_subject_already_exists.html"

class FacultySubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = FacultySubject
    success_url = "/user/my-subjects"
    template_name = "table/faculty_subject_delete.html"
    login_url = "/user/login"
 

class FacultyExtensionCreateView(LoginRequiredMixin, CreateView):
    model = FacultyExtension
    success_url = "/user/my-extensions"
    template_name = "table/faculty_ext_form.html"
    login_url = "/user/login"
    form_class = FacultyExtensionForm
    # authorization
    # def get(self, request, *args, **kwargs):
    #     if self.request.user.role != "1":
    #         return redirect('home')
    #     return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print("Self object ", self.object.ext)
        existing = FacultyExtension.objects.filter(ext = self.object.ext, user = self.request.user)
        print('ext is existing: ',existing)
        if existing:
            return redirect('table.error.exist')
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class FacultyExtensionDeleteView(LoginRequiredMixin, DeleteView):
    model = FacultyExtension
    success_url = "/user/my-extensions"
    template_name = "table/faculty_subject_delete.html"
    login_url = "/user/login"
 

class UserReportsListView(LoginRequiredMixin, ListView):
    model = User
    template_name="table/user_reports.html"
    context_object_name = "users"
    def get_queryset(self):
        role = self.request.GET.get("role")
        print("role selected", role)
        if role == "5": return super().get_queryset().filter(role="5")
        if role == "4": return super().get_queryset().filter(role="4")
        if role == "3": return super().get_queryset().filter(role="3")
        if role == "2": return super().get_queryset().filter(role="2")
        return super().get_queryset()
    login_url = "/user/login"

def generateUserDocument(request):
    role = request.GET.get('role')
    print(role)
    if role:
        users = User.objects.all().filter(role=role).values()
    else:
        users = User.objects.all().values()
    ext = request.GET.get("ext")
    if ext == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_report.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
            smart_str(u"First Name"),
            smart_str(u"Last Name"),
            smart_str(u"Email"),
        ])
        for user in users:
            writer.writerow([
                smart_str(user.get('first_name')),
                smart_str(user.get('last_name')),
                smart_str(user.get('email')),
            ])

    elif ext == "xls":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="user_report.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['First Name', 'Last Name', 'Email' ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for user in users:
            row_num = row_num + 1
            ws.write(row_num, 0,user.get('first_name'), font_style)
            ws.write(row_num, 1,user.get('last_name'), font_style)
            ws.write(row_num, 2,user.get('email'), font_style)
        wb.save(response)

    return response

def querySet_to_list(qs):
    """
    this will return python list<dict>
    """
    return [dict(q) for q in qs]