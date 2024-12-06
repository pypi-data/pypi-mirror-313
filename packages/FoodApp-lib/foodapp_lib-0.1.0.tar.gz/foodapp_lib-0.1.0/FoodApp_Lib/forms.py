from django import forms
from .models import Employee
from .models import Product 
# Registration Form (not using ModelForm, handling manually)
class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        employee = Employee(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=data['password']
        )
        employee.save()  # Save to database
        return employee

# Login Form (no changes needed here, it's fine as-is)
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)


# ProductForm (removed product_id)
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # Make sure to import and define the Product model
        fields = ['name', 'price', 'image']  #
