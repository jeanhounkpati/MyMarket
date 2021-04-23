
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User,auth
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,View,DetailView,ListView
from django.views.generic.edit import DeleteView,UpdateView,CreateView,FormView
from .models import *

# from .forms import CreateUserForm
from .forms import PlatForm,CheckoutForm,CustomerRegistrationForm,CustomerLoginForm,AdminLoginForm
from django.db.models import Q



class BlogMixin(object):
    def dispatch(self,request,*args,**kwargs):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request,*args,**kwargs)

def index(request):
    return render(request,'index.html')
    pass

def home(request):
	plats = Plat.objects.all()
	return render(request,'home.html',{'plats': plats})


def show(request,id):
    plat = Plat.objects.get(pk=id)
    return render(request,'show.html',{'plat': plat}) 

#  Cart
def cart(request,id):
    # get plat  
    plat_obj = Plat.objects.get(pk =id) 
    # check if cart exists
    cart_id =request.session.get('cart_id',None)
    if cart_id:
        cart_obj = Cart.objects.get(id =cart_id)                   
        this_plat_in_cart = cart_obj.cartplat_set.filter(plat = plat_obj)
        if this_plat_in_cart.exists():
            cartplat = this_plat_in_cart.last()
            cartplat.quantity+=1
            cartplat.subtotal+=plat_obj.selling_price
            cartplat.save()
            cart_obj.total+=plat_obj.selling_price
            cart_obj.save()
        else:
            cartplat = CartPlat.objects.create(cart=cart_obj, plat = plat_obj,rate = plat_obj.selling_price,quantity = 1,subtotal = plat_obj.selling_price)
            cart_obj.total+=plat_obj.selling_price
            cart_obj.save()
    else:
        cart_obj = Cart.objects.create(total = 0)
        request.session['cart_id'] = cart_obj.id 
        cartplat = CartPlat.objects.create(cart =cart_obj,plat = plat_obj,rate = plat_obj.selling_price,quantity =1,subtotal=plat_obj.selling_price)
        cart_obj.total += plat_obj.selling_price
        cart_obj.save()

    return render(request,'cart.html',{"cart_obj":cart_obj}) 



class ManageCart(BlogMixin,View):
    def get(self,request,*args,**kwargs):
        cp_id = self.kwargs["id"]
        data=request.GET.get('action', None)
        print(data,cp_id)
        # get cart plat 
        cp_obj = CartPlat.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if data =='inc':
            cp_obj.quantity+=1
            cp_obj.subtotal+=cp_obj.rate
            cp_obj.save()
            cart_obj.total+=cp_obj.rate
            cart_obj.save()
            print("succes")
            
        elif data == 'dcr':
            cp_obj.quantity-=1
            cp_obj.subtotal-=cp_obj.rate
            cp_obj.save()
            cart_obj.total-= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity ==0:
                    cp_obj.delete()
            print("unsucces")
        elif data =='rmv':
            cart_obj.total-= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
            print("resucces")

        else:
            pass
        return redirect("blog:addtocart")
        # return render(request,'addtocart.html') 

def emptycart(request):
    cart_id =request.session.get('cart_id',None)
    if cart_id:
        cart = Cart.objects.get(id = cart_id)
        cart.cartplat_set.all().delete()
        cart.total = 0
        cart.save()
    return redirect("blog:addtocart")

class AddtoCart(BlogMixin,TemplateView):
    template_name = "addtocart.html"
    """docstring for addtocart"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


# CRUD




def platform(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlatForm(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            messages.info(request,'formulaire correct')          
            return redirect('blog:home')
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
        else:
            messages.info(request,'formulaire incorrect')  

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PlatForm()
    return render(request,'adminpages/platform.html',{'form':form}) 



class PlatUpdate(UpdateView):
    model = Plat
    # template_name = "update-plat.html"
    # form_class= PlatForm
    fields = ["title","description","image","selling_price","slug"]
    success_url = reverse_lazy('blog:home')
    
   


class PlatDelete(DeleteView):
    # Template_name ="delete.html"
    model = Plat
    success_url = reverse_lazy('blog:home')
    context_object_name = 'plat '
    # success_url ="/"

 # success_url = reverse_lazy('blog:home')



# Authentification et autorisation

class CustomerRegistrationForm(CreateView):
    template_name = "customerregistrationform.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("blog:home") 
    def form_valid(self,form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username,email,password)
        form.instance.user = user
        login(self.request,user)
        
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
                next_url =self.request.GET.get('next')
                return next_url
        else:
            return self.success_url


class CustomerLoginForm(FormView):
    template_name = "customerloginform.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("blog:home")
    def form_valid(self,form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username =uname,password = pword)
        if usr is not None and usr.customer:
            login(self.request,usr)
        else:
            return render (self.request,self.template_name,{'form':self.form_class,"error": "invalid credentials"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
                next_url =self.request.GET.get('next')
                return next_url
        else:
            return self.success_url


class CustomerLogoutForm(View):
    def get(self,request):
        logout(request)
        return redirect ("blog:home")



class CheckoutForm(BlogMixin,CreateView):
    template_name = "checkoutform.html"
    form_class= CheckoutForm
    success_url = reverse_lazy("blog:home")

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect ("/blog/login/?next=/blog/checkout/")
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self,form):
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
        else:
            return redirect("blog:home")        
        return super().form_valid(form)







class CustomerProfil(BlogMixin,TemplateView):
    template_name = "customerprofil.html"

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return ("/blog/login/?next=blog/profil/")
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        print("cool")
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer = customer).order_by('id')      
        context['orders'] = orders
        return context
 





class CustomerOrderDetail(DetailView):
    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = 'ord_obj'

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and request.user.customer:
            order_id = self.kwargs['pk']
            order = Order.objects.get(id = order_id)
            if request.user.customer != order.cart.customer:
                return redirect ('Blog:customerprofil')
        else:
            return ("/blog/login/?next=blog/profil/")
        return super().dispatch(request,*args,**kwargs)





#Admin pages
class AdminRequireMixin(object):
   def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user = request.user).exists():
            pass
        else:
            return redirect("adminloginform")
        return super().dispatch(request,*args,**kwargs)




class AdminLoginForm(FormView):
    template_name = "adminpages/adminloginform.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("blog:adminhome")
    def form_valid(self,form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username =uname,password = pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request,usr)
        else:
            return render (self.request,self.template_name,{'form':self.form_class,'error' :"invalid credentials"})
        return super().form_valid(form)

        
class AdminHome(AdminRequireMixin,TemplateView):
    template_name = "adminpages/adminhome.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(order_status="Order Received")
        return context




class AdminOrderDetail(AdminRequireMixin,DetailView):
    template_name = "adminpages/adminorderdetail.html" 
    model = Order
    context_object_name ='ord_obj'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context



class AdminOrderList(AdminRequireMixin,ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by('-id')
    context_object_name ='allorders'


class AdminOrderStatusChange(AdminRequireMixin,View):
    def post(self,request,*args,**kwargs):
        order_id = self.kwargs['pk']
        order_obj =Order.objects.get(id = order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect ((reverse_lazy("blog:adminorderdetail",kwargs={"pk":order_id})))

class SearchForm(TemplateView):
        template_name = "search.html"

        def get_context_data(self,**kwargs):
            context = super().get_context_data(**kwargs)
            kw = self.request.GET.get('keyword')
            results = Plat.objects.filter(Q(title__icontains = kw)|Q(description__icontains = kw))
            context['results'] = results
            return context
         