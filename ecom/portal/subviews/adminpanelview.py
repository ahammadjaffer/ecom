from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from datetime import datetime
from ..models import *

def dashboard(request):
    context = {}
    return render(request, 'portal/admin/base.html', context)