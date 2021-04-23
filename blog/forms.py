from django import forms

from django.contrib.auth.models import User,auth
# from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm,TextInput
from .models import Plat,Order,Customer,Admin
from django.core.exceptions import ValidationError


class PlatForm(ModelForm):
	class Meta:
			model = Plat
			fields = ["title","description","image","selling_price","slug"]
			widgets = {
			'title':forms.TextInput(attrs = {'class':'form-control','placeholder':'le nom du produit'}),
			'description':forms.TextInput(attrs = {'class':'form-control','placeholder':'description'}),			
			'selling_price':forms.TextInput(attrs = {'class':'form-control','placeholder':'entrer un selling price'}),		
			'slug':forms.TextInput(attrs = {'class':'form-control','placeholder':'entrer un slug'}),
			'image':forms.ClearableFileInput(attrs = {'class':'form-control','placeholder':'image'})
			}

class CheckoutForm(ModelForm):
	class Meta:
			model = Order
			fields = ["ordered_by","shipping_address","mobile" ,"email"]
			widgets = {
			'ordered_by':forms.TextInput(attrs = {'class':'form-control','placeholder':'Ordered by'}),
			'shipping_address':forms.TextInput(attrs = {'class':'form-control','placeholder':'Shipping address'}),			
			'mobile':forms.TextInput(attrs = {'class':'form-control','placeholder':'mobile'}),		
			'email':forms.TextInput(attrs = {'class':'form-control','placeholder':'email'})
			
			}




class CustomerRegistrationForm(forms.ModelForm):
	username = forms.CharField(label='username', max_length=100,widget=forms.TextInput(attrs = {'class':'form-control','placeholder':'Username'}) )
	password   = forms.CharField(label='password', max_length=100,widget=forms.PasswordInput
			(attrs = {'class':'form-control','placeholder':'Password'}))
	email   = forms.CharField(label='email',max_length=100,widget=forms.EmailInput(attrs = {'class':'form-control','placeholder':'Email'}))
	class Meta:		
			model = Customer
			fields = ["username","password","email","full_name","address"]
			widgets = {		
			'full_name':forms.TextInput(attrs = {'class':'form-control','placeholder':'Full name'}),		
			'address':forms.TextInput(attrs = {'class':'form-control','placeholder':'Adress'})
			
			}

	def clean_username(self):
		uname = self.cleaned_data.get("username")
		print(uname)
		if User.objects.filter(username = uname).exists():
			print(uname)
			raise ValidationError(
				"customer with this username exists")
			print(uname)
		return uname


# class ContactForm(forms.Form):
#     # Everything as before.
#     ...

#     def clean_recipients(self):
#         data = self.cleaned_data['recipients']
#         if "fred@example.com" not in data:
#             raise ValidationError("You have forgotten about Fred!")

#         # Always return a value to use as the new cleaned data, even if
#         # this method didn't change it.
#         return data



class CustomerLoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=100,widget=forms.TextInput(attrs = {'class':'form-control','placeholder':'Username'}) )
	password   = forms.CharField(label='password', max_length=100,widget=forms.PasswordInput
			(attrs = {'class':'form-control','placeholder':'Password'}))





class AdminLoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=100,widget=forms.TextInput(attrs = {'class':'form-control','placeholder':'Username'}) )
	password   = forms.CharField(label='password', max_length=100,widget=forms.PasswordInput
			(attrs = {'class':'form-control','placeholder':'Password'}))


