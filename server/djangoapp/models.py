from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data


class Dealership(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=2)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=5)
    lat = models.FloatField()
    long = models.FloatField()

class Review(models.Model):
    name = models.CharField(max_length=100)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    review = models.TextField()
    purchase = models.BooleanField()
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()

class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    # Puoi aggiungere altri campi qui se necessario

    def __str__(self):
        return self.name

CAR_TYPE_CHOICES = [
    ('SEDAN', 'Sedan'),
    ('SUV', 'SUV'),
    ('WAGON', 'Wagon'),
    # Puoi aggiungere altre scelte qui
]

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()  # Questo fa riferimento a un concessionario nel tuo database Cloudant
    name = models.CharField(max_length=255)
    car_type = models.CharField(max_length=50, choices=CAR_TYPE_CHOICES)
    year = models.DateField()
    # Puoi aggiungere altri campi qui se necessario

    def __str__(self):
        return self.name

