from django.shortcuts import render
import mysql.connector
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

# Create your views here.

mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="car")
mycursor=mydb.cursor(buffered=True)
def index(request):
    chkSql="""select * from car where status='0'"""
    mycursor.execute(chkSql)
    carlis=mycursor.fetchall()
    return render(request,'index.html',{"carlis":carlis})

def cars(request):
    chkSql="""select * from car where status='0'"""
    mycursor.execute(chkSql)
    carlis=mycursor.fetchall()
    return render(request,'cars.html',{"carlis":carlis})

def login(request):
    return render(request,'login.html')

def register(request):    
    return render(request,'register.html')

def user(request):   
    id=request.session['uid'] 
    chkSql="""select * from car where uid=%s and status='2'"""
    val=(str(id),)
    mycursor.execute(chkSql,val)
    carliss=mycursor.fetchall()
    print(carliss)
    carlis=[]
    for i in carliss:
        j=0
        lst=[]
        while j<len(i):
            if j==10:                
                chkSql="""select * from user where id=%s"""
                val=(str(i[j]),)
                mycursor.execute(chkSql,val)
                plis=mycursor.fetchone()
                print(plis)
                lst.append(plis[1])
            else:
                lst.append(i[j])
            
            j+=1
        carlis.append(lst)
    return render(request,'user.html',{"carlis":carlis})

def admin(request):
    chkSql="""select * from car where pid=%s and status='1'"""
    val=(str(0),)
    mycursor.execute(chkSql,val)
    carliss=mycursor.fetchall()
    print(carliss)
    carlis=[]
    for i in carliss:
        j=0
        lst=[]
        while j<len(i):
            if j==9:                
                chkSql="""select * from user where id=%s"""
                val=(str(i[j]),)
                mycursor.execute(chkSql,val)
                plis=mycursor.fetchone()
                print(plis)
                lst.append(plis[1])
            else:
                lst.append(i[j])
            
            j+=1
        carlis.append(lst)
    return render(request,'admin.html',{"carlis":carlis})

def cart(request):
    id=request.GET.get('id')    
    chkSql="""select * from car where id='"""+id+"""'"""
    mycursor.execute(chkSql)
    carlis=mycursor.fetchone()
    print(carlis)
    tax=int(carlis[6])*0.18
    total=int(carlis[6])+tax
    return render(request,'cart.html',{"carlis":carlis,"tax":tax,"total":total})

def ausers(request):
    sql="""select * from user"""
    mycursor.execute(sql)
    carliss=mycursor.fetchall()
    print(carliss)
    return render(request,'ausers.html',{"carlis":carliss})

def addproduct(request):
    return render(request,'addproduct.html')

def puchases(request):
    id=request.session['uid'] 
    chkSql="""select * from car where pid=%s and status='2'"""
    val=(str(id),)
    mycursor.execute(chkSql,val)
    carliss=mycursor.fetchall()
    print(carliss)
    carlis=[]
    for i in carliss:
        j=0
        lst=[]
        while j<len(i):
            if j==10:                
                chkSql="""select * from user where id=%s"""
                val=(str(i[j]),)
                mycursor.execute(chkSql,val)
                plis=mycursor.fetchone()
                print(plis)
                lst.append(plis[1])
            else:
                lst.append(i[j])
            
            j+=1
        carlis.append(lst)
    return render(request,'puchases.html',{"carlis":carlis})

def regform(request):
    name=request.GET['name']
    uname=request.GET['uname']
    mobile=request.GET['mobile']
    email=request.GET['email']
    password=request.GET['pass']
    dob=request.GET['dob']
    chkSql="""select * from user where username=%s"""
    val=(uname,)
    mycursor.execute(chkSql,val)
    count=mycursor.rowcount
    if count >0:        
        return HttpResponseRedirect(redirect_to='login')
    else:
        insertUserSql="""insert into user (name,username,mobile,password,email,dob)values(%s,%s,%s,%s,%s,%s)"""
        insertVal=(name,uname,mobile,password,email,dob)
        mycursor.execute(insertUserSql,insertVal)
        mydb.commit()
        return HttpResponseRedirect(redirect_to='login')
    
def loginform(request):    
    uname=request.GET['uname']
    password=request.GET['pass']
    if uname=="admin" and password=="admin":
        request.session['uid']="admin"
        request.session['name']="admin"
        return HttpResponseRedirect(redirect_to='admin')
    else: 
        chkSql="""select * from user where username=%s and password=%s"""
        val=(uname,password,)
        mycursor.execute(chkSql,val)
        count=mycursor.rowcount
        if count >0:             
            user=mycursor.fetchone()
            request.session['uid']=user[0]
            request.session['name']=user[1]
            return HttpResponseRedirect(redirect_to='user')
        
def add_products(request):    
    uid=request.session['uid']
    if request.method=="POST":        
        year=request.POST.get('year')
        style=request.POST.get('style')
        make=request.POST.get('make')
        condition=request.POST.get('condition')
        model=request.POST.get('model')
        price=request.POST.get('price')
        print(year,make,style,condition,model,price,uid)
    if len(request.FILES) !=0:
        img=request.FILES['img1'] 
        fs = FileSystemStorage()
        filename = fs.save(img.name, img)
        uploaded_file_url = fs.url(filename)
        img=uploaded_file_url
        img1=request.FILES['img2'] 
        fs = FileSystemStorage()
        filename1 = fs.save(img1.name, img1)
        uploaded_file_url = fs.url(filename1)
        img1=uploaded_file_url
        proInsertSql="""insert into car (year,make,style,conditions,model,price,imgone,imgtwo,uid,pid,status)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        vals=(year,make,style,condition,model,price,img,img1,uid,'0','1')
        mycursor.execute(proInsertSql,vals)
        mydb.commit()
        return HttpResponseRedirect(redirect_to='addproduct')
        
def purchase(request):
    pro=request.GET.get('id')
    pid=request.session['uid']
    insertUserSql="""update car set status='2',pid='"""+str(pid)+"""' where id='"""+str(pro)+"""'"""    
    mycursor.execute(insertUserSql)
    mydb.commit()
    return HttpResponseRedirect(redirect_to='login')

def approve(request):    
    pro=request.GET.get('id')
    insertUserSql="""update car set status='0' where id='"""+str(pro)+"""'"""    
    mycursor.execute(insertUserSql)
    mydb.commit()
    return HttpResponseRedirect(redirect_to='admin')

def approveuser(request):    
    pro=request.GET.get('id')
    insertUserSql="""update user set status='0' where id='"""+str(pro)+"""'"""    
    mycursor.execute(insertUserSql)
    mydb.commit()
    return HttpResponseRedirect(redirect_to='admin')

def logout(request):
    del request.session['uid']
    del request.session['name']
    return HttpResponseRedirect(redirect_to='index')