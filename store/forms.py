from django import forms

DigitalChoices =(
("1", "Digital"),
("2", "Not Digital")
)

class Product_Form(forms.Form):
    name = forms.CharField(label='Product Name', max_length=200)
    price = forms.FloatField(label='Price')
    description = forms.CharField(label='Product Description', max_length=500)
    digital = forms.ChoiceField(label='Is the Product Digital', choices = DigitalChoices)
    image = forms.ImageField(label='Upload an Image')

class User_Form(forms.Form):
    name = forms.CharField(label='Username', max_length=200)
    email = forms.CharField(label='Email', max_length=200)
