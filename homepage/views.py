# from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pysftp, os
from django.shortcuts import render, redirect


from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

from django.contrib.auth.decorators import login_required

import time
import os
from urllib.parse import urlparse

from  .OCRMongoDB import document_info, document_info_new

from pdf2image import convert_from_bytes
from io import BytesIO

import base64

import paramiko
from PyPDF2 import PdfReader

# Create your views here.
def user_login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      user = authenticate(request, username=cd['username'], password=cd['password'])
      if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse('Authenticated Sucessfully')
        else:
            return HttpResponse('Disabled account')
      else:
          return HttpResponse('Invalid login')
    else:
      form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})


def index(request):
  return render(request, 'homepage/index.html')



###### START - OCR INVOICES
file_list_param = []

@login_required
def homepage(request):
  global file_list_param
  file_list_param.clear()
  cnopts = pysftp.CnOpts()
  cnopts.hostkeys = None
  if request.method == 'POST':
    for upfile in request.FILES.getlist('files[]'):
      # print(request.FILES.getlist('files[]'))
      filename = upfile.name
      fss = FileSystemStorage()
      file = fss.save(upfile.name, upfile)
      file_url = fss.url(file)
      file_list_param.append(filename)
      with pysftp.Connection('gpt.helpbots.sg', username='root', password='EPIKLAH2023', cnopts=cnopts) as sftp:
          with sftp.cd('meggit_invoice/'):   
            sftp.put('/var/www/html/ocrweb/media/' + file)      
      os.remove('/var/www/html/ocrweb/media/' + file)
            
    return redirect('/sftp/')
  return render(request, 'homepage/home.html')

@login_required
def sftp_view(request):
  # SFTP server details
  host = 'gpt.helpbots.sg'
  port = 22  # Port number for SFTP (usually 22)
  username = 'root'
  password = 'EPIKLAH2023'
  remote_path = '/root/meggit_invoice/'

  # Connect to the SFTP server
  ssh_client = paramiko.SSHClient()
  ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh_client.connect(host, port=port, username=username, password=password)
  sftp_client = ssh_client.open_sftp()

  # List files and folders in the remote path
  file_list = sftp_client.listdir(remote_path)   

  # print(file_list_param)

  data_list = []
  for file_name in file_list_param: 
    data_dic = {}
    remote_file_path = remote_path + '/' + file_name
    remote_file = sftp_client.open(remote_file_path, 'rb')
    pdf_content = remote_file.read()
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    # print('base64',pdf_content, pdf_base64)
    spreadsheet_id, page_id = document_info(file_name)
    # time.sleep(3)
    spreadsheet_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={page_id}'
        
    data_dic['filename'] = file_name
    data_dic['base64'] = pdf_base64
    data_dic['spreadsheet_url'] = spreadsheet_url
    print(spreadsheet_url)
    data_list.append(data_dic)
   
  # Close the SFTP connection
  sftp_client.close()
  ssh_client.close() 
  return render(request, 'homepage/sftp.html', {'data_list': data_list})

@login_required
def validation(request):
  # SFTP server details
  host = 'gpt.helpbots.sg'
  port = 22  # Port number for SFTP (usually 22)
  username = 'root'
  password = 'EPIKLAH2023'
  remote_path = '/root/meggit_invoice/'

  # Connect to the SFTP server
  ssh_client = paramiko.SSHClient()
  ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh_client.connect(host, port=port, username=username, password=password)
  sftp_client = ssh_client.open_sftp()

  # List files and folders in the remote path
  file_list = sftp_client.listdir(remote_path)   


  data_list = []
  for file_name in file_list: 
    data_dic = {}
    remote_file_path = remote_path + '/' + file_name
    remote_file = sftp_client.open(remote_file_path, 'rb')
    pdf_content = remote_file.read()
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    
    spreadsheet_id, page_id = document_info(file_name)
    # time.sleep(3)
    spreadsheet_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={page_id}'
        
    data_dic['filename'] = file_name
    data_dic['base64'] = pdf_base64
    data_dic['spreadsheet_url'] = spreadsheet_url
    # print(spreadsheet_url)
    data_list.append(data_dic)
    # print(data_dic)
   
  # Close the SFTP connection
  sftp_client.close()
  ssh_client.close()

  return render(request, 'homepage/validation.html', {'data_list': data_list})

######### END - OCR INVOICES


###### START - 62 INVOICES
@login_required
def homepage_invoices(request):
  global file_list_param
  file_list_param.clear()

  cnopts = pysftp.CnOpts()
  cnopts.hostkeys = None
  if request.method == 'POST':
    for upfile in request.FILES.getlist('files[]'):
      filename = upfile.name
      # #file_list_param.append(filename)
      fss = FileSystemStorage()
      file = fss.save(upfile.name, upfile)
      file_url = fss.url(file)
      file_list_param.append(filename)
      with pysftp.Connection('gpt.helpbots.sg', username='root', password='EPIKLAH2023', cnopts=cnopts) as sftp:
          with sftp.cd('general_invoice/'):   
            sftp.put('/var/www/html/ocrweb/media/' + file)      
      os.remove('/var/www/html/ocrweb/media/' + file)

    time.sleep(30)
    return redirect('/sftp_invoices/')      
  return render(request, 'homepage/homepage_invoices.html')



@login_required
def sftp_invoices(request):
  # SFTP server details
  host = 'gpt.helpbots.sg'
  port = 22  # Port number for SFTP (usually 22)
  username = 'root'
  password = 'EPIKLAH2023'
  remote_path = '/root/general_invoice/'

  # Connect to the SFTP server
  ssh_client = paramiko.SSHClient()
  ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh_client.connect(host, port=port, username=username, password=password)
  sftp_client = ssh_client.open_sftp()

  # List files and folders in the remote path
  file_list = sftp_client.listdir(remote_path)   

  # print(file_list_param)

  data_list = []
  for file_name in file_list_param: 
    data_dic = {}
    remote_file_path = remote_path + '/' + file_name
    remote_file = sftp_client.open(remote_file_path, 'rb')
    pdf_content = remote_file.read()
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    # print('base64',pdf_content, pdf_base64)
    spreadsheet_id, page_id = document_info_new(file_name)
    # time.sleep(3)
    spreadsheet_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={page_id}'
        
    data_dic['filename'] = file_name
    data_dic['base64'] = pdf_base64
    data_dic['spreadsheet_url'] = spreadsheet_url
    print(spreadsheet_url)
    data_list.append(data_dic)
   
  # Close the SFTP connection
  sftp_client.close()
  ssh_client.close() 
  return render(request, 'homepage/sftp_invoices.html', {'data_list': data_list})

@login_required
def validation_invoices(request):
  # SFTP server details
  host = 'gpt.helpbots.sg'
  port = 22  # Port number for SFTP (usually 22)
  username = 'root'
  password = 'EPIKLAH2023'
  remote_path = '/root/general_invoice/'

  # Connect to the SFTP server
  ssh_client = paramiko.SSHClient()
  ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh_client.connect(host, port=port, username=username, password=password)
  sftp_client = ssh_client.open_sftp()

  # List files and folders in the remote path
  file_list = sftp_client.listdir(remote_path)   


  data_list = []
  for file_name in file_list: 
    data_dic = {}
    remote_file_path = remote_path + '/' + file_name
    remote_file = sftp_client.open(remote_file_path, 'rb')
    pdf_content = remote_file.read()
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    
    spreadsheet_id, page_id = document_info_new(file_name)
    # time.sleep(3)
    spreadsheet_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={page_id}'
        
    data_dic['filename'] = file_name
    data_dic['base64'] = pdf_base64
    data_dic['spreadsheet_url'] = spreadsheet_url
    # print(spreadsheet_url)
    data_list.append(data_dic)
    # print(data_dic)
   
  # Close the SFTP connection
  sftp_client.close()
  ssh_client.close()

  return render(request, 'homepage/validation_invoices.html', {'data_list': data_list})

###### END - 62 INVOICES