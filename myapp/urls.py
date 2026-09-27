from django.urls import path
from . import views

urlpatterns = [
    # ─── Public ───────────────────────────────────────
    path('',          views.index,          name='home'),
    path('reg/',      views.reg,            name='register'),
    path('log/',      views.log,            name='login'),
    path('logout/',   views.logout_view,    name='logout'),

    # ─── User ─────────────────────────────────────────
    path('up/',             views.userp,          name='user_page'),
    path('profile/',        views.edit_profile,   name='edit_profile'),
    path('passs/',          views.changepassword, name='change_password'),
    path('ord/<int:id>/',   views.order,          name='order'),
    path('vc/',             views.viewcart,       name='view_cart'),
    path('delp/<int:id>/',  views.removeitem,     name='remove_item'),
    path('pay/',            views.payment,        name='payment'),
    path('upay/',           views.userpayment,    name='user_payment'),
    path('myp/',            views.viewsales,      name='my_orders'),
    path('ms/<int:salesno>/', views.viewsalessub, name='order_detail'),

    # ─── Admin Dashboard ──────────────────────────────
    path('sap/',    views.showadminpanel,      name='admin_panel'),

    # Admin: Products
    path('aap/',              views.showadminaddproduct, name='admin_add'),
    path('aapl/',             views.showproductlist,     name='admin_list'),
    path('del/<int:id>/',     views.deleteproductlist,   name='admin_delete'),
    path('edit/<int:id>/',    views.editproductlist,     name='admin_edit'),
    path('astock/<int:id>/',  views.admin_update_stock,  name='admin_stock'),

    # Admin: Orders & Status
    path('inv/',                     views.adminorderstatus,   name='admin_orders'),
    path('aumd/<int:salesno>/',      views.adminordersub,      name='admin_order_sub'),
    path('ostatus/<int:id>/',        views.update_order_status, name='update_order_status'),
    path('invn/<int:id>/',           views.invoiceitems,       name='admin_invoice_item'),

    # Admin: Sales Report
    path('sreport/',              views.salesreport,     name='sales_report'),
    path('aumd1/<int:salesno>/', views.salesreportsub,   name='sales_sub'),

    # Admin: User Management
    path('ausers/',              views.admin_user_list,   name='admin_users'),
    path('atoggle/<int:id>/',    views.admin_toggle_user, name='admin_toggle_user'),
]