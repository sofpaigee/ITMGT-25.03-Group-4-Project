from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from blog.models import Resource

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30, required=True, help_text="Maximum of 30 characters.")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)
    
    ROLE_CHOICES = [
        ('tutor', 'Tutor'),
        ('tutee', 'Tutee'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True)
 
    subjects = forms.MultipleChoiceField(
        choices=[
            ('MATH 31.1', 'MATH 31.1'),
            ('LAS 21', 'LAS 21'),
            ('MATH 31.2', 'MATH 31.2'),
            ('DECSC 22', 'DECSC 22'),
            ('ITMGT 25.03', 'ITMGT 25.03'),
            ('MATH 31.3', 'MATH 31.3'),
            ('ACCT 115', 'ACCT 115'),
            ('LLAW 113', 'LLAW 113'),
            ('MATH 70.1', 'MATH 70.1'),
            ('ECON 110', 'ECON 110'),
            ('ACCT 125', 'ACCT 125'),
            ('LLAW 115', 'LLAW 115'),
            ('MATH 61.2', 'MATH 61.2'),
            ('DECSC 25', 'DECSC 25'),
            ('ECON 121', 'ECON 121'),
            ('FINN 115', 'FINN 115'),
            ('QUANT 121', 'QUANT 121'),
            ('QUANT 162', 'QUANT 162'),
            ('LAS 111', 'LAS 111'),
            ('MKTG 111', 'MKTG 111'),
            ('QUANT 163', 'QUANT 163'),
            ('LAS 123', 'LAS 123'),
            ('QUANT 192', 'QUANT 192'),
            ('LAS 120', 'LAS 120'),
            ('LAS 140', 'LAS 140'),
            ('OPMAN 125', 'OPMAN 125'),
            ('QUANT 164', 'QUANT 164'),
            ('QUANT 199', 'QUANT 199'),
            ('LAS 197.10', 'LAS 197.10'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="For tutors, enter your subject expertise. For tutees, enter subject needs. Select all that apply"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'role', 'subjects']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account is already associated with this email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            role_group_name = self.cleaned_data['role']
            role_group, created = Group.objects.get_or_create(name=role_group_name)
            user.groups.add(role_group)
            
            selected_subjects = self.cleaned_data['subjects']
            for subject in selected_subjects:
                subject_group, created = Group.objects.get_or_create(name=subject)
                user.groups.add(subject_group)
        return user

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    email = forms.EmailField()
    subjects = forms.MultipleChoiceField(
        choices=[
            ('MATH 31.1', 'MATH 31.1'),
            ('LAS 21', 'LAS 21'),
            ('MATH 31.2', 'MATH 31.2'),
            ('DECSC 22', 'DECSC 22'),
            ('ITMGT 25.03', 'ITMGT 25.03'),
            ('MATH 31.3', 'MATH 31.3'),
            ('ACCT 115', 'ACCT 115'),
            ('LLAW 113', 'LLAW 113'),
            ('MATH 70.1', 'MATH 70.1'),
            ('ECON 110', 'ECON 110'),
            ('ACCT 125', 'ACCT 125'),
            ('LLAW 115', 'LLAW 115'),
            ('MATH 61.2', 'MATH 61.2'),
            ('DECSC 25', 'DECSC 25'),
            ('ECON 121', 'ECON 121'),
            ('FINN 115', 'FINN 115'),
            ('QUANT 121', 'QUANT 121'),
            ('QUANT 162', 'QUANT 162'),
            ('LAS 111', 'LAS 111'),
            ('MKTG 111', 'MKTG 111'),
            ('QUANT 163', 'QUANT 163'),
            ('LAS 123', 'LAS 123'),
            ('QUANT 192', 'QUANT 192'),
            ('LAS 120', 'LAS 120'),
            ('LAS 140', 'LAS 140'),
            ('OPMAN 125', 'OPMAN 125'),
            ('QUANT 164', 'QUANT 164'),
            ('QUANT 199', 'QUANT 199'),
            ('LAS 197.10', 'LAS 197.10'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    role = forms.ChoiceField(
        choices=[
            ('tutor', 'Tutor'),
            ('tutee', 'Tutee'),
        ],
        label='Role'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'subjects', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            user_groups = self.instance.groups.values_list('name', flat=True)
            self.fields['subjects'].initial = [group for group in user_groups if group in dict(self.fields['subjects'].choices)]
            role_group = [group for group in user_groups if group in ['tutor', 'tutee']]
            if role_group:
                self.fields['role'].initial = role_group[0]

class ResourceUpload(forms.ModelForm):
    SUBJECT_CHOICES = [
        ('', ''),  # Add a placeholder choice
        ('MATH 31.1', 'MATH 31.1'),
        ('LAS 21', 'LAS 21'),
        ('MATH 31.2', 'MATH 31.2'),
        ('DECSC 22', 'DECSC 22'),
        ('ITMGT 25.03', 'ITMGT 25.03'),
        ('MATH 31.3', 'MATH 31.3'),
        ('ACCT 115', 'ACCT 115'),
        ('LLAW 113', 'LLAW 113'),
        ('MATH 70.1', 'MATH 70.1'),
        ('ECON 110', 'ECON 110'),
        ('ACCT 125', 'ACCT 125'),
        ('LLAW 115', 'LLAW 115'),
        ('MATH 61.2', 'MATH 61.2'),
        ('DECSC 25', 'DECSC 25'),
        ('ECON 121', 'ECON 121'),
        ('FINN 115', 'FINN 115'),
        ('QUANT 121', 'QUANT 121'),
        ('QUANT 162', 'QUANT 162'),
        ('LAS 111', 'LAS 111'),
        ('MKTG 111', 'MKTG 111'),
        ('QUANT 163', 'QUANT 163'),
        ('LAS 123', 'LAS 123'),
        ('QUANT 192', 'QUANT 192'),
        ('LAS 120', 'LAS 120'),
        ('LAS 140', 'LAS 140'),
        ('OPMAN 125', 'OPMAN 125'),
        ('QUANT 164', 'QUANT 164'),
        ('QUANT 199', 'QUANT 199'),
        ('LAS 197.10', 'LAS 197.10'),
    ]

    subjects = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select,
        required=True,
    )

    class Meta:
        model = Resource
        fields = ['title', 'description', 'subjects', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_subjects(self):
        subjects = self.cleaned_data.get('subjects')
        if subjects == '':
            raise forms.ValidationError('Please select a valid subject.')
        return subjects

class ResourceUpdateForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'subject', 'file']

    def __init__(self, *args, **kwargs):
        initial_file = kwargs.pop('initial_file', None)
        super().__init__(*args, **kwargs)
        if initial_file:
            self.fields['file'].initial = initial_file
        self.fields['file'].required = False

    def clean_file(self):
        cleaned_file = self.cleaned_data.get('file', False)
        if not cleaned_file:
            return self.initial.get('file', None)
        return cleaned_file
