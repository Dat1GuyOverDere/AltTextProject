from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from PIL import Image

# Create your models here.
class PermissionLevel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank = True)
    

class MyUser(User):

    permission_level = models.ForeignKey(PermissionLevel, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            default_permission_level = PermissionLevel.objects.get(name='Base')
            self.permission_level = default_permission_level
        super().save(*args, **kwargs)
     

class Profile(models.Model):
    user = models.OneToOneField(MyUser,on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile_pic.jpg',upload_to='profile_pics')
    desc = models.TextField(max_length=150, default='')
        
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
    #Clears all perms and gives the user perms listed in the below list
    def set_default_perms(self):
        permissions = []  #Add to list to add default perms
        self.user.user_permissions.clear()
        for perm in permissions:
            self.add_permission(perm)
        
    #NOTE this gives every permission. Only use if needed 
    def give_admin_perms(self):
        self.user.is_superuser = True
        self.user.save()
        
    #Returns true if the user has a specified permission and returns false if they don't. 
    #Raises a TypeError exception if perm is not a string 
    def has_permission(self, perm):
        if type(perm) != str:
            raise TypeError("Function takes string as argument") 
        if self.user.has_perm(perm):
            return True
        return False
    
    #Returns true if ther permission was successfully added and false if it was not
    def add_permission(self, perm):
        #TODO: Check if permission can be used
        if self.has_permission(perm):
            return True
        self.user.user_permissions.add(perm)
        return True
    
    #Returns true if it removes a permission and false if it does not
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.user.user_permissions.remove(perm)
            return True
        return False
