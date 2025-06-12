# Generated migration file

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('duration', models.IntegerField(help_text='Duration in minutes')),
                ('release_date', models.DateField()),
                ('poster', models.ImageField(blank=True, null=True, upload_to='movie_posters/')),
                ('trailer_url', models.URLField(blank=True, null=True)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('genres', models.ManyToManyField(blank=True, to='booking.genre')),
            ],
            options={
                'ordering': ['-release_date'],
            },
        ),
        migrations.CreateModel(
            name='SeatType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price_multiplier', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('total_capacity', models.IntegerField()),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['city', 'name'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shows', to='booking.movie')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shows', to='booking.theater')),
            ],
            options={
                'ordering': ['date', 'time'],
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.CharField(max_length=1)),
                ('number', models.IntegerField()),
                ('seat_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.seattype')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='booking.theater')),
            ],
            options={
                'ordering': ['row', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='booking.show')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-booking_date'],
            },
        ),
        migrations.CreateModel(
            name='BookingSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.seat')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='seats',
            field=models.ManyToManyField(through='booking.BookingSeat', to='booking.seat'),
        ),
        migrations.AlterUniqueTogether(
            name='show',
            unique_together={('theater', 'date', 'time')},
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together={('theater', 'row', 'number')},
        ),
        migrations.AlterUniqueTogether(
            name='bookingseat',
            unique_together={('booking', 'seat')},
        ),
    ]
