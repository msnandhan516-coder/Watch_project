from django.shortcuts import render, redirect
from django.utils import timezone
from myapp.models import signup, watchcart, watchstock, watchsales, watchsalessub
from django.db.models.functions import Coalesce
from django.db.models import Sum, Max, Value, F
import re


# ─── HELPERS ───────────────────────────────────────────────────────────────
def is_logged_in(request):
    return request.session.get('id') is not None

def is_admin(request):
    return request.session.get('rights') == 'A'

def login_required_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_logged_in(request):
            return redirect('/log/')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_logged_in(request):
            return redirect('/log/')
        if not is_admin(request):
            return redirect('/up/')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─── PUBLIC VIEWS ──────────────────────────────────────────────────────────
def index(request):
    wrec = watchstock.objects.filter(qty__gt=0).order_by('-is_featured', 'id')[:6]
    return render(request, "index.html", {"wrec": wrec})


def reg(request):
    if is_logged_in(request):
        return redirect('/up/') if not is_admin(request) else redirect('/sap/')

    if request.method == "POST":
        fname = request.POST.get("fname", "").strip()
        lname = request.POST.get("lname", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        uname = request.POST.get("uname", "").strip()
        password = request.POST.get("password", "")
        cpassword = request.POST.get("cpassword", "")

        errors = []
        if not fname:
            errors.append("First name is required.")
        if not lname:
            errors.append("Last name is required.")
        if not email or not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            errors.append("A valid email address is required.")
        if not phone or not re.match(r'^\d{10}$', phone):
            errors.append("A valid 10-digit phone number is required.")
        if not uname or len(uname) < 4:
            errors.append("Username must be at least 4 characters.")
        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if password != cpassword:
            errors.append("Passwords do not match.")
        if signup.objects.filter(uname=uname).exists():
            errors.append(f"Username '{uname}' is already taken.")
        if email and signup.objects.filter(email=email).exists():
            errors.append(f"Email '{email}' is already registered.")

        if errors:
            return render(request, 'reg.html', {"msg": " | ".join(errors)})

        full_name = f"{fname} {lname}"
        s = signup(
            name=full_name, first_name=fname, last_name=lname,
            email=email, phone=phone, uname=uname,
            pas=password, rights='U', is_active=True
        )
        s.save()
        return render(request, 'notfound.html', {
            "msg": f"Welcome {fname}! Account created successfully. Please sign in.",
            "success": True
        })

    return render(request, "reg.html")


def log(request):
    if is_logged_in(request):
        return redirect('/up/') if not is_admin(request) else redirect('/sap/')

    if request.method == "POST":
        uname = request.POST.get("username", "").strip()
        pas = request.POST.get("pass", "")

        if not uname:
            return render(request, 'login.html', {"msg": "Username is required."})
        if not pas:
            return render(request, 'login.html', {"msg": "Password is required."})

        user = None
        qs = signup.objects.filter(uname=uname)
        if not qs.exists():
            qs = signup.objects.filter(uname__iexact=uname)
        if qs.exists():
            user = qs.first()

        if user is None:
            qs2 = signup.objects.filter(name=uname)
            if not qs2.exists():
                qs2 = signup.objects.filter(name__iexact=uname)
            if qs2.exists():
                user = qs2.first()

        if user is None or user.pas != pas:
            return render(request, 'login.html', {
                "msg": "Incorrect username or password."
            })

        if not user.is_active:
            return render(request, 'login.html', {"msg": "Your account is deactivated. Contact support."})

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        request.session['name'] = user.first_name or user.name
        request.session['id'] = user.id
        request.session['email'] = user.email or ''
        request.session['pnumber'] = user.phone or ''
        request.session['uname'] = user.uname or user.name
        request.session['pword'] = user.pas
        request.session['rights'] = user.rights

        if user.rights == "A":
            return redirect("/sap/")
        return redirect("/up/")

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    return redirect('/')


# ─── USER VIEWS ────────────────────────────────────────────────────────────
@login_required_redirect
def userp(request):
    wrec = watchstock.objects.all().order_by('-is_featured', 'id')
    return render(request, "userpage.html", {"wrec": wrec})


@login_required_redirect
def edit_profile(request):
    uid = request.session['id']
    try:
        user = signup.objects.get(id=uid)
    except signup.DoesNotExist:
        return redirect('/up/')

    if request.method == "POST":
        fname = request.POST.get("fname", "").strip()
        lname = request.POST.get("lname", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()

        errors = []
        if not fname:
            errors.append("First name is required.")
        if not lname:
            errors.append("Last name is required.")
        if not email or not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            errors.append("Valid email required.")
        if not phone or not re.match(r'^\d{10}$', phone):
            errors.append("Valid 10-digit phone required.")
        if email and signup.objects.filter(email=email).exclude(id=uid).exists():
            errors.append("This email is already used by another account.")

        if errors:
            return render(request, 'profile.html', {"user": user, "msg": " | ".join(errors), "msg_type": "error"})

        full_name = f"{fname} {lname}"
        signup.objects.filter(id=uid).update(
            first_name=fname, last_name=lname,
            name=full_name, email=email, phone=phone
        )
        request.session['name'] = fname
        request.session['email'] = email
        request.session['pnumber'] = phone
        user.refresh_from_db()
        return render(request, 'profile.html', {
            "user": user, "msg": "Profile updated successfully!", "msg_type": "success"
        })

    return render(request, "profile.html", {"user": user})


@login_required_redirect
def order(request, id):
    try:
        watch = watchstock.objects.get(id=id)
    except watchstock.DoesNotExist:
        return render(request, 'notfound.html', {"msg": "Watch not found.", "error": True})

    if watch.qty <= 0:
        return render(request, 'notfound.html', {"msg": "Sorry, this watch is out of stock.", "error": True})

    qts = list(range(1, min(watch.qty + 1, 11)))

    if request.method == "POST":
        if 'b1' in request.POST:
            oq = int(request.POST.get('qtys', 1))
            if oq > watch.qty:
                return render(request, 'notfound.html', {"msg": f"Only {watch.qty} units available.", "error": True})
            tot = oq * watch.price
            max_slno = watchcart.objects.filter(userid=request.session['id']).aggregate(
                max_slno=Coalesce(Max('slno'), Value(0)))['max_slno']
            watchcart(
                slno=int(max_slno) + 1, pname=watch.wname,
                rate=watch.price, qty=oq, total=tot,
                userid=request.session['id']
            ).save()
            return render(request, 'notfound.html', {
                "msg": f"'{watch.wname}' added to cart!", "success": True
            })
        if 'b2' in request.POST:
            mrec = watchcart.objects.filter(userid=request.session['id'])
            tot = watchcart.objects.filter(userid=request.session['id']).aggregate(Sum('total'))
            amt = str(tot['total__sum'] or 0)
            request.session['total'] = amt
            return render(request, 'vieworder.html', {"mrec": mrec, "amt": amt})

    return render(request, "order.html", {
        "fname": watch.wname, "price": watch.price,
        "qts": qts, "photo": watch.photo,
        "watch_id": id, "watch": watch,
    })


@login_required_redirect
def carts(request):
    return render(request, "cart.html")


@login_required_redirect
def viewcart(request):
    mrec = watchcart.objects.filter(userid=request.session['id'])
    if not mrec.exists():
        return render(request, 'vieworder.html', {"mrec": mrec, "amt": 0})
    tot = watchcart.objects.filter(userid=request.session['id']).aggregate(Sum('total'))
    amt = str(tot['total__sum'] or 0)
    request.session['total'] = amt
    return render(request, 'vieworder.html', {"mrec": mrec, "amt": amt})


@login_required_redirect
def removeitem(request, id):
    watchcart.objects.filter(id=id, userid=request.session['id']).delete()
    mrec = watchcart.objects.filter(userid=request.session['id'])
    tot = watchcart.objects.filter(userid=request.session['id']).aggregate(Sum('total'))
    amt = str(tot['total__sum'] or 0)
    request.session['total'] = amt
    return render(request, 'vieworder.html', {"mrec": mrec, "amt": amt})


@login_required_redirect
def payment(request):
    amt = request.session.get('total', '0')
    if request.method == "POST":
        if 'p1' in request.POST:
            return render(request, "userpayment.html", {"amt": amt})
        if 'p2' in request.POST:
            return redirect('/vc/')
    return render(request, "payment.html", {"amt": amt})


@login_required_redirect
def userpayment(request):
    if request.method == "POST":
        shipment = request.POST.get("t1", "").strip()
        cardno = request.POST.get("t2", "").replace(" ", "")
        amt = request.session.get('total', '0')

        if not shipment:
            return render(request, 'userpayment.html', {"amt": amt, "msg": "Shipping address is required."})
        card_clean = cardno.replace(" ", "")
        if not card_clean or len(card_clean) != 16 or not card_clean.isdigit():
            return render(request, 'userpayment.html', {"amt": amt, "msg": "Please enter a valid 16-digit card number."})

        id = request.session['id']
        fname = request.session['name']
        pnumber = request.session.get('pnumber', '')

        max_salesno = watchsales.objects.aggregate(
            max_salesno=Coalesce(Max('salesno'), Value(0)))['max_salesno']
        bno = int(max_salesno) + 1

        watchsales(
            salesno=bno, userid=id, uname=fname,
            shipment=shipment, phone=pnumber,
            cardno=card_clean, total=int(float(amt)),
            status='New Order'
        ).save()

        mrec = watchcart.objects.filter(userid=id)
        for j in mrec:
            watchsalessub(
                salesno=bno, slno=j.slno,
                pname=j.pname, rate=j.rate,
                qty=j.qty, total=j.total
            ).save()
            # Decrease stock
            watchstock.objects.filter(wname=j.pname).update(qty=F('qty') - j.qty)

        watchcart.objects.filter(userid=id).delete()
        request.session['total'] = '0'

        return render(request, 'notfound.html', {
            "msg": f"Order #{bno} placed successfully! Your G-SHOCK is on its way. Thank you!",
            "success": True
        })

    return redirect('/pay/')


@login_required_redirect
def changepassword(request):
    if request.method == "POST":
        oldpass = request.POST.get("old", "")
        newpass = request.POST.get("n1", "")
        confrmpass = request.POST.get("n2", "")
        uid = request.session['id']
        p = request.session['pword']

        if not oldpass:
            return render(request, 'changepass.html', {"msg": "Current password is required."})
        if not newpass or len(newpass) < 6:
            return render(request, 'changepass.html', {"msg": "New password must be at least 6 characters."})
        if newpass != confrmpass:
            return render(request, 'changepass.html', {"msg": "New passwords do not match."})
        if p != oldpass:
            return render(request, 'changepass.html', {"msg": "Current password is incorrect."})

        signup.objects.filter(id=uid).update(pas=newpass)
        request.session['pword'] = newpass
        return render(request, 'notfound.html', {
            "msg": "Password changed successfully!", "success": True
        })

    return render(request, "changepass.html")


@login_required_redirect
def viewsales(request):
    mrec = watchsales.objects.filter(userid=request.session['id']).order_by('-salesno')
    return render(request, "mysales.html", {"mrec": mrec})


@login_required_redirect
def viewsalessub(request, salesno):
    mrec = watchsalessub.objects.filter(salesno=salesno)
    sale = watchsales.objects.filter(salesno=salesno).first()
    return render(request, "mysalessub.html", {"mrec": mrec, "sale": sale})


# ─── ADMIN VIEWS ───────────────────────────────────────────────────────────
@admin_required_redirect
def showadminpanel(request):
    total_products = watchstock.objects.count()
    total_users = signup.objects.filter(rights='U').count()
    new_orders = watchsales.objects.filter(status='New Order').count()
    processing_orders = watchsales.objects.filter(status='Processing').count()
    shipped_orders = watchsales.objects.filter(status='Shipped').count()
    delivered_orders = watchsales.objects.filter(status='Delivered').count()
    total_revenue = watchsales.objects.exclude(
        status='Cancelled'
    ).aggregate(Sum('total'))['total__sum'] or 0
    low_stock = watchstock.objects.filter(qty__gt=0, qty__lte=5).count()
    out_of_stock = watchstock.objects.filter(qty=0).count()
    recent_orders = watchsales.objects.order_by('-salesno')[:8]
    return render(request, "adminpanel.html", {
        "total_products": total_products,
        "total_users": total_users,
        "new_orders": new_orders,
        "processing_orders": processing_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "total_revenue": total_revenue,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "recent_orders": recent_orders,
    })


@admin_required_redirect
def showadminaddproduct(request):
    if request.method == "POST":
        wname = request.POST.get('wname', '').strip()
        price = request.POST.get('price', '')
        qty = request.POST.get('qty', '')
        brand = request.POST.get('brand', '').strip()
        category = request.POST.get('category', 'Classic')
        description = request.POST.get('description', '').strip()
        is_featured = request.POST.get('is_featured') == 'on'
        photo = request.FILES.get('photo')

        errors = []
        if not wname:
            errors.append("Watch name is required.")
        try:
            if not price or int(price) < 1:
                errors.append("Valid price required.")
        except ValueError:
            errors.append("Price must be a number.")
        if qty == '':
            errors.append("Stock quantity is required.")
        if not photo:
            errors.append("Product photo is required.")
        if wname and watchstock.objects.filter(wname__iexact=wname).exists():
            errors.append(f"A watch named '{wname}' already exists.")

        if errors:
            return render(request, "AdminAddwatch.html", {"msg": " | ".join(errors)})

        watchstock(
            wname=wname, brand=brand, category=category,
            description=description, price=int(price),
            qty=int(qty), photo=photo, is_featured=is_featured
        ).save()
        return render(request, "AdminAddwatch.html", {
            "msg": f"'{wname}' added successfully!", "success": True
        })

    return render(request, "AdminAddwatch.html")


@admin_required_redirect
def showproductlist(request):
    prec = watchstock.objects.all().order_by('-is_featured', 'id')
    return render(request, "AdminListwatch.html", {"prec": prec})


@admin_required_redirect
def deleteproductlist(request, id):
    try:
        watchstock.objects.get(id=id).delete()
    except watchstock.DoesNotExist:
        pass
    return redirect("/aapl/")


@admin_required_redirect
def editproductlist(request, id):
    try:
        watch = watchstock.objects.get(id=id)
    except watchstock.DoesNotExist:
        return redirect('/aapl/')

    if request.method == "POST":
        wname = request.POST.get('wname', '').strip()
        price = request.POST.get('price', '')
        qty = request.POST.get('qty', '')
        brand = request.POST.get('brand', '').strip()
        category = request.POST.get('category', watch.category)
        description = request.POST.get('description', '').strip()
        is_featured = request.POST.get('is_featured') == 'on'
        photo = request.FILES.get('photo')

        errors = []
        if not wname:
            errors.append("Watch name is required.")
        try:
            if not price or int(price) < 1:
                errors.append("Valid price required.")
        except ValueError:
            errors.append("Price must be a number.")
        if qty == '':
            errors.append("Quantity required.")

        if errors:
            return render(request, "AdminEditwatch.html", {"watch": watch, "msg": " | ".join(errors)})

        update_fields = {
            'wname': wname, 'brand': brand, 'category': category,
            'description': description, 'price': int(price),
            'qty': int(qty), 'is_featured': is_featured
        }
        if photo:
            update_fields['photo'] = photo
            watchstock.objects.filter(id=id).update(**{k: v for k, v in update_fields.items() if k != 'photo'})
            w = watchstock.objects.get(id=id)
            w.photo = photo
            w.save()
        else:
            watchstock.objects.filter(id=id).update(**update_fields)

        return redirect("/aapl/")

    return render(request, "AdminEditwatch.html", {"watch": watch})


# ─── ADMIN: ORDER STATUS MANAGEMENT ────────────────────────────────────────
@admin_required_redirect
def adminorderstatus(request):
    status_filter = request.GET.get('status', 'all')
    # Handle URL-encoded 'New+Order' → 'New Order'
    status_filter = status_filter.replace('+', ' ')

    if status_filter == 'all':
        rec = watchsales.objects.all().order_by('-salesno')
    else:
        rec = watchsales.objects.filter(status=status_filter).order_by('-salesno')

    counts = {
        'all':        watchsales.objects.count(),
        'new':        watchsales.objects.filter(status='New Order').count(),
        'processing': watchsales.objects.filter(status='Processing').count(),
        'shipped':    watchsales.objects.filter(status='Shipped').count(),
        'delivered':  watchsales.objects.filter(status__in=['Delivered','Invoiced']).count(),
        'cancelled':  watchsales.objects.filter(status='Cancelled').count(),
    }
    return render(request, "AdminInvoice.html", {
        "rec": rec,
        "counts": counts,
        "active_status": status_filter,
    })


@admin_required_redirect
def update_order_status(request, id):
    """Update delivery status of an order"""
    if request.method == "POST":
        new_status = request.POST.get('status', '')
        valid_statuses = ['New Order', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
        if new_status in valid_statuses:
            watchsales.objects.filter(id=id).update(status=new_status)
    return redirect(request.META.get('HTTP_REFERER', '/inv/'))


@admin_required_redirect
def adminordersub(request, salesno):
    rec = watchsalessub.objects.filter(salesno=salesno)
    sale = watchsales.objects.filter(salesno=salesno).first()
    return render(request, "AdminInvoiceSub.html", {"rec": rec, "sale": sale})


@admin_required_redirect
def invoiceitems(request, id):
    watchsales.objects.filter(id=id).update(status='Invoiced')
    return redirect("/inv/")


@admin_required_redirect
def salesreport(request):
    # Include all non-cancelled orders in sales analytics
    rec = watchsales.objects.exclude(status='Cancelled').order_by('-salesno')
    grand_total = rec.aggregate(Sum('total'))['total__sum'] or 0
    avg_order = round(grand_total / rec.count()) if rec.count() > 0 else 0
    return render(request, "AdminSalesReport.html", {
        "rec": rec, "grand_total": grand_total, "avg_order": avg_order,
    })


@admin_required_redirect
def salesreportsub(request, salesno):
    rec = watchsalessub.objects.filter(salesno=salesno)
    return render(request, "AdminSalesSub.html", {"rec": rec})


# ─── ADMIN: USER MANAGEMENT ─────────────────────────────────────────────────
@admin_required_redirect
def admin_user_list(request):
    users = signup.objects.filter(rights='U').order_by('-id')
    active_count = users.filter(is_active=True).count()
    inactive_count = users.filter(is_active=False).count()
    return render(request, "AdminUsers.html", {
        "users": users,
        "active_count": active_count,
        "inactive_count": inactive_count,
    })


@admin_required_redirect
def admin_toggle_user(request, id):
    try:
        user = signup.objects.get(id=id)
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
    except signup.DoesNotExist:
        pass
    return redirect('/ausers/')


@admin_required_redirect
def admin_update_stock(request, id):
    """Quick stock update from product list"""
    if request.method == "POST":
        qty = request.POST.get('qty', '')
        try:
            watchstock.objects.filter(id=id).update(qty=int(qty))
        except (ValueError, TypeError):
            pass
    return redirect('/aapl/')


# ─── 404 HANDLER ───────────────────────────────────────────────────────────
def custom_404(request, exception):
    return render(request, 'notfound.html', {
        "msg": "The page you're looking for doesn't exist.",
        "error": True
    }, status=404)
