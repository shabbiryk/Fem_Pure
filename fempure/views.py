from django.shortcuts import render,redirect
from .models import User,Product,UserHistory
from django.http import JsonResponse
from cart.cart import Cart

loadedUserName=""
isSupporterDone=False
# Create your views here.
def Home(request):
    request.session['WalletAddress'] = "xxxxxx"
    context={}
    return render(request,'seller_home.html',context)


def CreateOrValidateUser(request):

    if request.POST:
        t_username = request.POST.get('username-id')
        try:
            temp = User.objects.get(username=t_username)
        except:
            temp=False
        if temp:
            request.session['WalletAddress'] =temp.walletid
            return redirect('userpage',temp.username)
        else:
            print('update userdetails')
            t_username = request.POST.get('username-id')
            t_wallet = request.POST.get('wallet-address')
            t_about = request.POST.get('about')
            t_youtube = request.POST.get('youtube')
            request.session['WalletAddress'] =t_wallet
            t_user = User.objects.get_or_create(username=t_username,walletid=t_wallet,about=t_about,youtube=t_youtube)
            return redirect('userpage',t_username)
    else:
        return redirect('home')



def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        print(username)
        data = {
            'username': User.objects.filter(username=username).count()
        }
        return JsonResponse(data)
    return redirect('home')


def UserPage(request,username):

    global loadedUserName
    loadedUserName=username
    request.session['userName']= username
    try:
        presentUserWallet=request.session['WalletAddress']
    except:
        presentUserWallet ='xxx'


    temp = User.objects.get(username=username)

    userhistory=UserHistory.objects.filter(user=temp)
    context={
        'username':username,
        'walletaddr':temp.walletid,
        'about':temp.about,
        'youtube':temp.youtube,
        'products': Product.objects.filter(user=temp),
        'userhistory':userhistory

    }


    if(presentUserWallet != temp.walletid):
        return render(request,'seller_page.html',context)
    else:
        return render(request,'seller_admin_page.html',context)

def add_product(request):
    temp = User.objects.get(username=loadedUserName)
    
    name=request.POST.get('productname')
    image=request.FILES.get('image')
    price=request.POST.get('price')
    description=request.POST.get('description')
    x=Product.objects.create(user=temp,name=name,image=image,price=price,description=description)

    return redirect('userpage',temp.username)


def cart_add(request, id):
    global isSupporterDone
    isSupporterDone = False
    global loadedUserName

    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect('userpage',loadedUserName)


def item_clear(request, id):

    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


def item_increment(request, id):
    global isSupporterDone
    isSupporterDone = False

    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


def item_decrement(request, id):


    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


def cart_clear(request):


    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

def cart_detail(request):
    global loadedUserName
    global isSupporterDone
    temp = User.objects.get(username=request.session['userName'])
    cart = Cart(request)
    dic = list(cart.session['cart'].values())
    total_price = sum([each['quantity']*(float(each['price'])) for each in dic])
    context = {"total":total_price,'receiverWalletAddress':temp.walletid,'isSupporterDone':isSupporterDone}

    return render(request, 'cart_detail.html',context)


#reload Page for clean up
def clean_user_cart(request):
    cart = Cart(request)
    cart.clear()
    temp = User.objects.get(username=request.session['userName'])
    sender = request.POST.get('sender')

    x = UserHistory.objects.create(user=temp,fromUser=sender,toUser=temp.walletid)

    global isSupporterDone
    isSupporterDone = True
    return redirect('cart_detail')
