# Generated by Django 3.1.4 on 2020-12-20 18:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('email', models.EmailField(error_messages={'unique': 'User already exists.'}, max_length=254, unique=True, verbose_name='email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField(blank=True, max_length=220, null=True)),
            ],
            options={
                'verbose_name_plural': 'Product_categories',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(blank=True, max_length=60, null=True)),
                ('dni', models.CharField(blank=True, error_messages={'unique': 'Un cliente ya tiene este rut.'}, max_length=10, null=True, unique=True, verbose_name='dni')),
                ('phone_number', models.CharField(error_messages={'unique': 'Un cliente ya tiene este numero de telefono.'}, max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message='The phone number must be entered in the format: +9999999. Up to 15 digits are allowed.', regex='\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(blank=True, error_messages={'unique': 'Un cliente(empresa) con ese email ya existe.'}, max_length=254, null=True, unique=True, verbose_name='email')),
                ('region', models.CharField(default='Región de Ñuble', max_length=20)),
                ('province', models.CharField(default='Diguillin', max_length=20)),
                ('commune', models.CharField(default='Chillán', max_length=20)),
                ('address_exact', models.CharField(blank=True, max_length=60, null=True)),
                ('latitud', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is Active')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('name_enterprise', models.CharField(max_length=55)),
                ('logo', models.ImageField(upload_to='')),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('exact_address', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('name_service', models.CharField(max_length=120)),
                ('description', models.CharField(blank=True, max_length=220, null=True)),
                ('is_tax_porcent', models.BooleanField(default=False)),
                ('tax_porcent', models.FloatField(blank=True, default=0.0, null=True)),
                ('is_tax_static_value', models.BooleanField(default=False)),
                ('tax_static_value', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name_plural': 'Deliveries',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('note_order', models.TextField(blank=True, max_length=250, null=True)),
                ('note_delivery', models.TextField(blank=True, max_length=250, null=True)),
                ('total_amount', models.IntegerField(blank=True, default=0, null=True)),
                ('total_with_taxts', models.IntegerField(blank=True, default=0, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_null', models.BooleanField(default=False)),
                ('is_delivery', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_client', to='crm.client')),
                ('delivery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_delivery_service', to='crm.delivery')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('is_tax_porcent', models.BooleanField(default=False)),
                ('tax_porcent', models.FloatField(blank=True, default=0.0, null=True)),
                ('is_tax_static_value', models.BooleanField(default=False)),
                ('tax_static_value', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name': 'Payments_type_payment',
            },
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('address', models.TextField(max_length='200')),
                ('note', models.TextField(blank=True, max_length='350', null=True)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_shipping', to='crm.delivery')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_shipping', to='crm.order')),
            ],
            options={
                'verbose_name_plural': 'Orders_shipping',
            },
        ),
        migrations.CreateModel(
            name='SalesModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('initial_amount', models.IntegerField()),
                ('finish_amount', models.IntegerField(default=0)),
                ('quanity_orders', models.IntegerField(default=0)),
                ('date_finish', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales_module_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('name', models.CharField(max_length=140)),
                ('slug', models.SlugField(blank=True, max_length=140)),
                ('description', models.TextField(blank=True, max_length=220, null=True)),
                ('is_stock', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_category', to='crm.category')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('price', models.IntegerField()),
                ('title', models.CharField(max_length=130)),
                ('is_normal_price', models.BooleanField(default=False)),
                ('is_delivery', models.BooleanField(default=False)),
                ('delivery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.delivery')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.product')),
            ],
            options={
                'verbose_name_plural': 'Product_prices',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('amount_pay', models.IntegerField()),
                ('amount_change', models.IntegerField(blank=True, null=True)),
                ('amount_final', models.IntegerField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_order', to='crm.order')),
                ('sales_module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales_module_payment', to='crm.salesmodule')),
                ('type_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_pyment', to='crm.typepayment')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='crm.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_product', to='crm.price')),
            ],
            options={
                'verbose_name_plural': 'Orders_items',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date modified', verbose_name='modified at')),
                ('stock', models.IntegerField()),
                ('alert_stock', models.IntegerField()),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='crm.product')),
            ],
            options={
                'verbose_name_plural': 'Product_inventories',
            },
        ),
    ]
