from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Userpayment, ProductCategory, ProductInventory, ProductDiscount, Product, cartItem, PaymentDetails, OrderDetails, OrderItem


class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'first_name', 'middle_name',
                  'last_name', 'contact', 'tc', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('first_name', 'middle_name',
                                    'last_name', 'contact', 'tc')}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'first_name', 'middle_name',
                     'last_name', 'contact', 'password1', 'password2'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)

admin.site.register(Userpayment)
admin.site.register(ProductCategory)
admin.site.register(ProductInventory)
admin.site.register(ProductDiscount)
admin.site.register(Product)
admin.site.register(cartItem)
admin.site.register(PaymentDetails)
admin.site.register(OrderDetails)
admin.site.register(OrderItem)
