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
from logs.models import Log

from research.models import Research
from department.models import Department
from extensions.models import Extension
from logs.models import Log

from subjects.models import Subject

import csv
from django.utils.encoding import smart_str
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
        Log(log_code='subject_assign', log_message=f'[{ self.request.user.username}] assigned the subject [{ self.object.subject.code}]').save()
        return HttpResponseRedirect(self.get_success_url())

class FacultySubjectAlreadyExists(LoginRequiredMixin, TemplateView):
    template_name = "table/faculty_subject_already_exists.html"

class FacultySubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = FacultySubject
    success_url = "/user/my-subjects"
    template_name = "table/faculty_subject_delete.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        target = FacultySubject.objects.get(id=self.kwargs["pk"])
        code = target.subject.code 
        user = self.request.user.username
        Log(log_code='subject_remove', log_message=f'[{user}] removed the extension [{code}]').save()
        return super().post(request, *args, **kwargs)
 
 

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
        # logs
        code = self.object.ext.code 
        username = self.request.user.username
        if self.get_form().is_valid():
            Log(log_code='extension_assign', log_message=f'[{username}] assigned extension [{code}] to themselves').save()
        return HttpResponseRedirect(self.get_success_url())


class FacultyExtensionDeleteView(LoginRequiredMixin, DeleteView):
    model = FacultyExtension
    success_url = "/user/my-extensions"
    template_name = "table/faculty_ext_delete.html"
    login_url = "/user/login"
    def post(self, request, *args, **kwargs):
        target = FacultyExtension.objects.get(id=self.kwargs["pk"])
        code = target.ext.code 
        user = self.request.user.username
        Log(log_code='department_delete', log_message=f'[{user}] removed the extension [{code}]').save()
        return super().post(request, *args, **kwargs)
 

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

class SubjectsReportsListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name="table/subject_reports.html"
    context_object_name = "subjects"
    login_url = "/user/login"

class LogsReportsListView(LoginRequiredMixin, ListView):
    model = Log
    template_name="table/log_list.html"
    context_object_name = "logs"
    login_url = "/user/login"

class DepartmentReportsListView(LoginRequiredMixin, ListView):
    model = Department
    template_name="table/department_reports.html"
    context_object_name = "departments"
    login_url = "/user/login"

class ResearchReportsListView(LoginRequiredMixin, ListView):
    model = Research
    template_name="table/research_reports.html"
    context_object_name = "research"
    login_url = "/user/login"

class ExtensionReportsListView(LoginRequiredMixin, ListView):
    model = Extension
    template_name="table/extension_reports.html"
    context_object_name = "extensions"
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

def generateSubjectDocument(request):
    subjects = Subject.objects.all().values()
    ext = request.GET.get("ext")
    if ext == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subject_report.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
            smart_str(u"Course Code"),
            smart_str(u"Course Name")
        ])
        for subject in subjects:
            writer.writerow([
                smart_str(subject.get('code')),
                smart_str(subject.get('name')),
            ])

    elif ext == "xls":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="subjectg_report.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Course Code', 'Course Name']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for subject in subjects:
            row_num = row_num + 1
            ws.write(row_num, 0,subject.get('code'), font_style)
            ws.write(row_num, 1,subject.get('name'), font_style)
        wb.save(response)
    return response


def generatDepartmentDocument(request):
    departments = Department.objects.all().values()
    ext = request.GET.get("ext")
    if ext == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="department_report.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
            smart_str(u"Department Code"),
            smart_str(u"Department Name"),
            smart_str(u"Department Description")

        ])
        for department in departments:
            writer.writerow([
                smart_str(department.get('code')),
                smart_str(department.get('name')),
                smart_str(department.get('description')),

            ])

    elif ext == "xls":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="department_report.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Department Code', 'Department Name', 'Department Description']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for department in departments:
            row_num = row_num + 1
            ws.write(row_num, 0,department.get('code'), font_style)
            ws.write(row_num, 1,department.get('name'), font_style)
            ws.write(row_num, 1,department.get('description'), font_style)

        wb.save(response)
    return response


def generateResearchDocument(request):
   
    research = Research.objects.all().values()
    ext = request.GET.get("ext")
    if ext == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="research_report.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
            smart_str(u"Title"),
            smart_str(u"Faculty"),
            smart_str(u"Status"),
        ])
        for item in research:
  
            status = ""
            if (item.get('status') == 1):
                status ="Ongoing"
            elif (item.get('status') == 2):
                status ="Presented"
            else:
                status ="Published"
            user = User.objects.get(id=item.get('user_id'))

            writer.writerow([
                smart_str(item.get('title')),
                smart_str(user.first_name + ' ' + user.last_name),
                smart_str(status),
            ])

    elif ext == "xls":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="research_report.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Title', 'Faculty', 'Status' ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for item in research:
            status = ""
            if (item.get('status') == 1):
                status ="Ongoing"
            elif (item.get('status') == 2):
                status ="Presented"
            else:
                status ="Published"
            user = User.objects.get(id=item.get('user_id'))
            row_num = row_num + 1
            ws.write(row_num, 0,item.get('title'), font_style)
            ws.write(row_num, 1,user.first_name + ' ' + user.last_name, font_style)
            ws.write(row_num, 2,status, font_style)
        wb.save(response)

    return response



def generateExtensionDocument(request):
   
    extensions = Extension.objects.all().values()
    ext = request.GET.get("ext")
    if ext == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ext_report.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
            smart_str(u"Code"),
            smart_str(u"Name"),
            smart_str(u"Description"),
        ])
        for item in extensions:
            writer.writerow([
                smart_str(item.get('code')),
                smart_str(item.get('name')),
                smart_str(item.get('description')),
            ])

    elif ext == "xls":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ext_report.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Code', 'Name', 'Description' ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for item in extensions:
           
            row_num = row_num + 1
            ws.write(row_num, 0,item.get('code'), font_style)
            ws.write(row_num, 1,item.get('name'), font_style)
            ws.write(row_num, 2,item.get('description'), font_style)
        wb.save(response)

    return response


def generateLogsDocument(request):
 
    logs = Log.objects.all().values()
    ext = request.GET.get("ext")
    if ext == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="log_report.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
            smart_str(u"Code"),
            smart_str(u"Message"),
            smart_str(u"Time"),

        ])
        for log in logs:
            writer.writerow([
                smart_str(log.get('log_code')),
                smart_str(log.get('log_message')),
                smart_str(log.get('log_time')),
            ])

    elif ext == "xls":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="log_report.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("sheet1")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Code', 'Message', 'Time' ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        for log in logs:
            row_num = row_num + 1
            ws.write(row_num, 0,log.get('log_code'), font_style)
            ws.write(row_num, 1,log.get('log_message'), font_style)
            ws.write(row_num, 2,log.get('log_time'), font_style)
        wb.save(response)

    return response