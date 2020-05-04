from django.urls import path
from restaurant.views import views
from restaurant.views.ingredient_views import (IngredientListView,
                                               IngredientDetailView,
                                               IngredientCreateView,
                                               IngredientUpdateView,
                                               IngredientDeleteView,
                                               )
from restaurant.views.inventory_views import (InventoryListView,
                                              InventoryDetailView,
                                              InventoryCreateView,
                                              InventoryUpdateView,
                                              InventoryDeleteView
                                              )

from restaurant.views.menu_item_views import (MenuItemListView,
                                              MenuItemDetailView,
                                              MenuItemCreateView,
                                              MenuItemUpdateView,
                                              MenuItemDeleteView
                                              )

from restaurant.views.sale_views import (SaleListView,
                                         SaleDetailView,
                                         #SaleCreateView,
                                         SaleUpdateView)
from restaurant.views.transaction_views import (#TransactionCreateView,
                                                TransactionListView,
                                                TransactionDetailView)

urlpatterns = [
    path('', views.home, name='restaurant-home'),
    path('about/', views.about, name='restaurant-about'),
    #path('transaction/start/', views.process_transaction, name='restaurant-start-transaction'),

    path('inventories/', InventoryListView.as_view(), name='restaurant-inventories'),
    path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='restaurant-inventory-detail'),
    path('inventory/new/', InventoryCreateView.as_view(), name='restaurant-inventory-create'),
    path('inventory/<int:pk>/update/', InventoryUpdateView.as_view(), name='restaurant-inventory-update'),
    path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='restaurant-inventory-delete'),

    path('ingredients/', IngredientListView.as_view(), name='restaurant-ingredients'),
    path('ingredient/<int:pk>/', IngredientDetailView.as_view(), name='restaurant-ingredient-detail'),
    path('ingredient/new/', IngredientCreateView.as_view(), name='restaurant-ingredient-create'),
    path('ingredient/<int:pk>/update/', IngredientUpdateView.as_view(), name='restaurant-ingredient-update'),
    path('ingredient/<int:pk>/delete/', IngredientDeleteView.as_view(), name='restaurant-ingredient-delete'),

    path('menuitems/', MenuItemListView.as_view(), name='restaurant-menuitems'),
    path('menuitem/<int:pk>/', MenuItemDetailView.as_view(), name='restaurant-menuitem-detail'),
    path('menuitem/new/', MenuItemCreateView.as_view(), name='restaurant-menuitem-create'),
    path('menuitem/<int:pk>/update/', MenuItemUpdateView.as_view(), name='restaurant-menuitem-update'),
    path('menuitem/<int:pk>/delete/', MenuItemDeleteView.as_view(), name='restaurant-menuitem-delete'),

    path('transaction/new/', views.process_transaction, name='restaurant-transaction-create'),
    path('sales/', SaleListView.as_view(), name='restaurant-sales'),
    path('sale/<int:pk>/', SaleDetailView.as_view(), name='restaurant-sale-detail'),
    path('sale/<int:pk>/update/', SaleUpdateView.as_view(), name='restaurant-sale-update'),


    #path('transactions/new/', TransactionCreateView.as_view(), name='restaurant-transaction-create'),
    path('transactions/', TransactionListView.as_view(), name='restaurant-transactions'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='restaurant-transaction-detail'),

]
