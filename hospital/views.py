from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def homepage(request):
    return render(request, 'index.html')


def aboutpage(request):
    return render(request, 'about.html')


def createaccount(request):
    # initialize user
    user = "none"
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']

        try:
            if password == repeatpassword:
               
                Patient.objects.create(name=name,
                                       email=email,
                                       gender=gender,
                                       phonenumber=phonenumber,
                                       address=address,
                                       birthdate=birthdate,
                                       bloodgroup=bloodgroup)

                user = User.objects.create_user(
                    first_name=name, 
                    email=email, 
                    password=password,
                      username=email)
               
                
                pat_group = Group.objects.get(name='Patient')
               
                pat_group.user_set.add(user)
                
                user.save()
                error = 'no'
            else:
                error = 'yes'
        except Exception as e:
            #raise e
            error = 'yes'
   
    d = {'error': error}
    
    return render(request, 'createaccount.html', d)



def loginpage(request):
    return render(request, 'login.html')




def loginpage(request):
    error = ""
    
    if request.method == 'POST':
        
        u = request.POST['email']
        p = request.POST['password']
        
        user = authenticate(request, username=u, password=p)
        print("This is "+str(user))
        try:
            
            if user is not None:
                error = "no"
                print("I AM")
               
                login(request,user)


                g = request.user.groups.all()[0].name
                #print(g)
                if g == 'Patient':
                    d = {'error': error}
                    #return HttpResponse("Patient Logged in Successfully")
                    return render(request, 'patienthome.html', d)
                elif g =='Doctor':
                    d= {'error': error}
                    return HttpResponse('Doctor Logged in Successfully')
       
        except Exception as e:
            error = "yes"
            print(e)
           
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('loginpage')

def Home(request):
   
    if not request.user.is_active:
        return redirect('loginpage')

    
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        return render(request, 'patienthome.html')

@login_required(login_url='/login')
def profile(request):
   
    if not request.user.is_active:
        return redirect('loginpage')

    
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        print(request.user)
        patient_details = Patient.objects.all().filter(email=request.user)
        d = {'patient_details': patient_details}
        return render(request, 'patientprofile.html', d)

@login_required(login_url='/login')
def MakeAppointments(request):
    error = ""
    if not request.user.is_active:
        return redirect('loginpage')
   
    alldoctors = Doctor.objects.all()
    d = {'alldoctors': alldoctors}
    g = request.user.groups.all()
    print(g)
    g = request.user.groups.all()[0].name
    g='Patient'
    if g == 'Patient':
        if request.method == 'POST':
            temp = request.POST['doctoremail']
            doctoremail = temp.split()[0]
            doctorname = temp.split()[1]
            patientname = request.POST['patientname']
            patientemail = request.POST['patientemail']
            appointmentdate = request.POST['appointmentdate']
            appointmenttime = request.POST['appointmenttime']
            symptoms = request.POST['symptoms']
            try:
                Appointment.objects.create(doctorname=doctorname, doctoremail=doctoremail, patientname=patientname, patientemail=patientemail,
                                           appointmentdate=appointmentdate, appointmenttime=appointmenttime, symptoms=symptoms, status=True, prescription="")
                error = "no"
            except:
                error = "yes"
            e = {"error": error}
            return render(request, 'patientmakeappointments.html', e)
        elif request.method == 'GET':
            return render(request, 'patientmakeappointments.html', d)


def viewappointments(request):
    if not request.user.is_active:
        return redirect('loginpage')
   
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        # appointmentdate__gte -> greater than
       
        upcomming_appointments = Appointment.objects.filter(patientemail = request.user, appointmentdate__gte = timezone.now(), status = True).order_by('appointmentdate')
       
        previous_appointments = Appointment.objects.filter(patientemail = request.user, appointmentdate__lt = timezone.now()).order_by('-appointmentdate')| Appointment.objects.filter(patientemail = request.user, status = False).order_by('-appointmentdate')
       
        d = {"upcomming_appointments": upcomming_appointments,"previous_appointments": previous_appointments}
        return render(request, 'patientviewappointments.html', d)

@login_required(login_url='/login')
def update_profile(request):
        
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']

        query_set = Patient.objects.get(email=request.user.email)

        query_set.name = name
        query_set.gender = gender
        query_set.phonenumber = phonenumber
        query_set.address = address
        query_set.birthdate = birthdate
        query_set.bloodgroup = bloodgroup

        query_set.save()

        return redirect('profile')



    patient_details = Patient.objects.all().filter(email=request.user)
    print(patient_details)
    d = {'patient_details': patient_details}
    return render(request, 'updatedetails.html',d)

def doc_register(request):
    # initialize user
    user = "none"
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        nmcnumber = request.POST['nmcnumber']
        qualification = request.POST['qualification']
        specialization = request.POST['specialization']
        photo = request.FILES.get('doc_image')
        license_image = request.FILES.get('license_image')

        try:
            if password == repeatpassword:
               
                Doctor.objects.create(name=name,
                                       email=email,
                                       gender=gender,
                                       phonenumber=phonenumber,
                                       address=address,
                                       birthdate=birthdate,
                                       nmc=nmcnumber,
                                       qualification=qualification,
                                       specialization=specialization,
                                       doc_image=photo,
                                       doc_license_image=license_image
                                      )

                user = User.objects.create_user(
                    first_name=name, 
                    email=email, 
                    password=password,
                      username=email)
               
                
                doc_group = Group.objects.get(name='Doctor')
               
                doc_group.user_set.add(user)
                
                user.save()
                error = 'no'
            else:
                error = 'yes'
        except Exception as e:
            #raise e
            print(e)
            error = 'yes'
   
    d = {'error': error}
    
    return render(request, 'tem.html', d)



    
    
