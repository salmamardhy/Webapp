from django import forms  
from website_a7f.models import Member

class MemberForm(forms.ModelForm): 
    STATUS_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    memberstatus = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'})) 

    class Meta:  
        model = Member 
        fields = ['ktpname', 'password', 'firstname', 'middlename', 'lastname', 'memberstatus'] 
        widgets = { 
            'ktpname': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'middlename': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_memberstatus(self):
        memberstatus = self.cleaned_data.get('memberstatus')
        if memberstatus == 'Yes':
            return 1  # Convert 'Yes' to 1
        elif memberstatus == 'No':
            return 0  # Convert 'No' to 0
        raise forms.ValidationError('This field is required.')

    def clean_ktpname(self):
        ktpname = self.cleaned_data.get('ktpname', '').strip()  # Strip whitespace
        if not all(char.isalpha() or char.isspace() for char in ktpname):
            raise forms.ValidationError('KTP name can only contain letters and spaces.')
        return ktpname

    def clean_firstname(self):
        firstname = self.cleaned_data.get('firstname')
        if not firstname.isalpha():
            raise forms.ValidationError('First name can only contain letters.')
        return firstname

    def clean_middlename(self):
        middlename = self.cleaned_data.get('middlename')

        if middlename:
            if not all(char.isalpha() or char.isspace() for char in middlename):
                raise forms.ValidationError('Middle name can only contain letters.')
        return middlename or ''

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not lastname.isalpha():
            raise forms.ValidationError('Last name can only contain letters.')
        return lastname

# class MemberDetailForm(forms.ModelForm):
#     class Meta:
#         model = Memberdetail
#         fields = ['memberid', 'callsign', 'participant', 'instructor', 'author', 'referral', 'dob', 'ktpnumber',
#                   'taxid', 'join_date', 'emailmain', 'emailalt', 'whatsapp', 'phone', 'telegram',
#                   'referralid', 'paidclass', 'freeclass', 'pointtotal', 'pointredeem']
#         widgets = { 
#             'ktpname': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'firstname': forms.TextInput(attrs={'class': 'form-control'}),
#             'middlename': forms.TextInput(attrs={'class': 'form-control'}),
#             'lastname': forms.TextInput(attrs={'class': 'form-control'}),
#         }