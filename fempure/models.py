from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255,null=False,blank=False)
    walletid = models.CharField(max_length=255,null=False,blank=False)
    about = models.CharField(max_length=255,null=True,blank=True)
    youtube=models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='images/',null=True,blank=True)

    def __str__(self):
        return self.username

class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    price = models.FloatField()
    description = models.CharField(max_length=3000,null=True,blank=True)

    def __str__(self):
        return self.user.username

class UserHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fromUser = models.CharField(max_length=255,null=False,blank=False)
    toUser = models.CharField(max_length=255,null=False,blank=False)

    def __str__(self):
        return self.fromUser
        
