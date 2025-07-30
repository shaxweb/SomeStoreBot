from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.views import LoginView
from rest_framework.response import Response
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.urls import reverse
from django.views import View
import requests, secrets
import json, time

pings = []

class PingApi(APIView):
	def get(self, request):
		res = requests.get("https://somestorebackend.onrender.com/ping/")
		pings.append({
		    "len": len(pings),
		    "response": res.json()
		})
		return Response({"status": True, "data": pings})

