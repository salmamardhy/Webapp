from django.shortcuts import render, redirect  
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from website_a7f.forms import MemberForm 
from website_a7f.models import Member, generate_member_id
from django.http import Http404

def index(request):  
    employees = Member.objects.all()  
    return render(request, "show.html", {'employees': employees}) 

# def regis(request):
#     if request.method == "POST":
#         form = MemberForm(request.POST)
#         if form.is_valid():
#             form.save()  # Automatically handles memberid generation
#             return redirect('/')
#         else:
#             print("Error in form:", form.errors)  # Print errors for debugging
#             return render(request, 'index.html', {'form': form, 'error': 'Invalid data. Please try again.'})
#     else:
#         form = MemberForm()
#     # messages.success(request, 'Registration successful. You can now log in.')
#     return render(request, 'index.html', {'form': form})

def regis(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()  # Automatically handles memberid generation
            messages.success(request, 'Registration successful. You can now log in.')
            request.session['message_shown'] = True  # Track that the message has been shown
            return redirect('/')
        else:
            print("Error in form:", form.errors)  # Print errors for debugging
            return render(request, 'index.html', {'form': form, 'error': 'Invalid data. Please try again.'})
    else:
        form = MemberForm()

    # Only show the message if it hasn't been shown before
    success_message = request.session.get('message_shown', False)
    if success_message:
        request.session['message_shown'] = False  # Reset it so it can be shown again next time
    else:
        success_message = None

    return render(request, 'index.html', {'form': form, 'success_message': success_message})

def destroy(request, memberid):
    employee = Member.objects.get(memberid=memberid)
    employee.delete()
    return redirect("/")

def edit(request, memberid):  # Change employee_id to memberid
    try:
        employee = Member.objects.get(memberid=memberid)  
    except Member.DoesNotExist:
        raise Http404("Employee not found")
    
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to the index page after updating
    else:
        form = MemberForm(instance=employee)

    return render(request, 'edit.html', {'form': form, 'employee': employee})

def update(request, memberid):  
    try:
        employee = Member.objects.get(memberid=memberid)  
    except Member.DoesNotExist:
        raise Http404("Member not found")

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=employee)  
        if form.is_valid():  
            form.save()  
            employee = Member.objects.get(memberid=memberid) 
            return redirect('edit', memberid=employee.memberid)  # Redirect to the index page after updating
        else:
            messages.warning(request, 'Failed to update. Please check your input.')
    else:
        form = MemberForm(instance=employee)

    return render(request, 'edit.html', {'form': form, 'employee': employee})

def login(request):
    if request.method == 'POST':
        ktpname = request.POST.get('ktpname')
        password = request.POST.get('password')

        # Mencari member berdasarkan KTP name
        try:
            ktp = Member.objects.get(ktpname=ktpname)

            # Periksa password
            if ktp.password == password:
                # Simpan ID member dalam sesi
                # request.session['memberid'] = ktp.memberid  # Gantilah dengan atribut ID yang sesuai
                # messages.success(request, f"Welcome, {ktpname}!")

                # Redirect ke halaman edit
                return redirect('edit', memberid=ktp.memberid)  # Redirect ke edit dengan memberid
            else:
                messages.warning(request, 'Invalid KTP Name or Password. Please try again')
        except Member.DoesNotExist:
            messages.warning(request, 'Invalid KTP Name or Password. Please try again.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')
