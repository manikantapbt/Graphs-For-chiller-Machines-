from Tkinter import *
import ttk
import tkMessageBox
import MySQLdb
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

#global declarations
ab=0
p= []
p1=[]
p2=[]
p3=[]
xc=[]
yc=[]
xe=[]
ye=[]
xco=[]
yco=[]
f=0
f2=0
w=0
w1=0
l=0
rk=0
comb=0



def quit():
    mexit=tkMessageBox.askyesno(title="Quit",message="Do you want to quit")
    plt.close('all')
    if mexit>0:
        
        master.destroy()
        return


def ok():
    
    global comb
    if comb.get()=="----Select Chiller----":
        tkMessageBox.showinfo(title="Error",message="Please Select Chiller")


    else:
	    db = MySQLdb.connect("localhost","root","root123","iiit")
	    mycursor = db.cursor()
	    global lb
	    mycursor.execute("""SELECT * FROM coefficientscapft WHERE  Chiller= %s""", comb.get())
	    
	    for row in iter(mycursor.fetchone, None):
		        p=row 
	    
	    s=int(p[7])+1
	    l=int(p[8])
	    s1=int(p[9])+1
	    l1=int(p[10])+1     
	    #print s,l  
	    #print s1,l1
	    root = Tk()
            root.geometry("300x200")
            root.title("Set MIN X and MIN Y")
	    tframe=Frame(root)
	    tframe.pack()
	    bframe=Frame(root)
	    bframe.pack()
	    global w
	    global w1
	    label11=Label(tframe,text="X-Value")
	    label11.pack()
	    w = Scale(tframe, from_=s, to=l, orient=HORIZONTAL,tickinterval=0.1,length=200)
	    w.pack()
	    label12=Label(tframe,text="Y-Value")
	    label12.pack()
	    w1 =Scale(tframe, from_=s1, to=l1, orient=HORIZONTAL,length=200)
	    w1.pack()
	    bs=Button(bframe,text="okay",command=okok)
	    bs.pack()
	    bs2=Button(bframe,text="Quit",command=root.quit)
	    bs2.pack()
	    #root.destroy()
	    mainloop()

def okok():
      global ab
      global f
      global w
      global w1
      global f2
      f= w.get()
      f2=w1.get()
      #print f
      #print f2
     
         

def drawgraph():
     
    fig=plt.figure()
    global xc,yc,xe,ye,xco,yco
    db = MySQLdb.connect("localhost","root","root123","iiit")
    mycursor = db.cursor()
    global lb
    mycursor.execute("""SELECT * FROM coefficientscapft WHERE  Chiller= %s""",comb.get() )
    # calls fetchone until None is returned (no more rows)
    for row in iter(mycursor.fetchone, None):
                p=row 
   

    c=p[1]
    x=p[2]
    x2=p[3]
    y=p[4]
    y2=p[5]
    xy=p[6] 
    xmin=p[9]
    xmax=p[10]     
    #print xmax,xmin  

    #global f
    #print f      
    t=xmin
    while t<xmax:
        xc.append(t)
	#global f
        t1=((c)+(x*f)+(x2*f*f)+(y*t)+(y2*t*t)+(xy*f*t))
	yc.append(t1)
        t=t+0.5
    



    #execute sql command and gets the whole tuple if matched name is matched
    mycursor.execute("""SELECT * FROM coefficientseirft WHERE  Chiller= %s""", comb.get())
    # calls fetchone until None is returned (no more rows)
    global p1
    for row in iter(mycursor.fetchone, None):
		   
                     p1=row 

    #print p1
    
    c5=p1[1]
    x5=p1[2]
    x25=p1[3]
    y5=p1[4]
    y25=p1[5]
    xy5=p1[6] 
    xmin5=p1[9]
    xmax5=p1[10]     
    #print xmax5,xmin5  
    #print f      
    t5=xmin5
    while t5<xmax5:
        xe.append(t5)
	#global f
        t15=((c5)+(x5*f)+(x25*f*f)+(y5*t5)+(y25*t5*t5)+(xy5*f*t5))
	ye.append(t15)
        t5=t5+0.5

    #global f
    global f2
    capft=((c)+(x*f)+(x2*f*f)+(y*f2)+(y2*f2*f2)+(xy*f*f2))
    eirft=((c5)+(x5*f)+(x25*f*f)+(y5*f2)+(y25*f2*f2)+(xy5*f*f2))
    #print capft	   
    #print eirft             
    capeir = capft*eirft
    #print capeir
 

    #global lb
    mycursor.execute("""SELECT * FROM eirfplr WHERE  Chiller= %s""", comb.get())
    # calls fetchone until None is returned (no more rows)
    #global p1
    for row in iter(mycursor.fetchone, None):
		   
                     p2=row 
    #print p2
    z=p2[1]
    z1=p2[2]
    z2=p2[3]

    #global lb
    mycursor.execute("""SELECT * FROM namesandcapacities WHERE  Chiller= %s""", comb.get())
    # calls fetchone until None is returned (no more rows)
    #global p1
    for row in iter(mycursor.fetchone, None):
		   
                     p3=row 
  
    powr=(p3[3]/p3[5])
    
    q=0.1
    while q<1.1:
       eirfplr=(z+(z1*q)+(z2*q*q))
       pekw=eirfplr*capeir*powr
       cop=((q*p3[3])/pekw)
       xco.append(q)
       yco.append(cop)
       q=q+0.05
  

    #print xco
    #print yco
    
    ax1=fig.add_subplot(2,2,1)
    ax1.plot(xc,yc,'c',linewidth=3)
    ax1.tick_params(axis='x',colors='r')
    ax1.tick_params(axis='y',colors='r')
    ax1.spines['bottom'].set_color('w')
    ax1.spines['top'].set_color('w')
    ax1.spines['left'].set_color('w')
    ax1.spines['right'].set_color('w')
    ax1.yaxis.label.set_color('b')
    ax1.xaxis.label.set_color('b')
    ax1.set_title('CAPFT',color='b')
    ax1.yaxis.grid(True)
    ax1.xaxis.grid(True)
    
    ax1.set_xlabel('Condenser Water Temperature($^\circ$C)',size=15)
    ax1.set_ylabel('Capacity Ratio',size=15) 


    ax2=fig.add_subplot(2,2,2)
    ax2.plot(xe,ye,'c',linewidth=3)
    ax2.tick_params(axis='x',colors='r')
    ax2.tick_params(axis='y',colors='r')
    ax2.spines['bottom'].set_color('w')
    ax2.spines['top'].set_color('w')
    ax2.spines['left'].set_color('w')
    ax2.spines['right'].set_color('w')
    ax2.yaxis.label.set_color('b')
    ax2.xaxis.label.set_color('b')
    ax2.set_title('EIRFT',color='b')
    ax2.set_xlabel('Condenser Water temperature($^\circ$C)',size=15)
    ax2.set_ylabel('EIR Ratio',size=15)
    ax2.yaxis.grid(True)
    ax2.xaxis.grid(True)
    

    ax3=fig.add_subplot(2,1,2)
    ax3.plot(xco,yco,'c',linewidth=3)
    ax3.tick_params(axis='x',colors='r')
    ax3.tick_params(axis='y',colors='r')
    ax3.spines['bottom'].set_color('w')
    ax3.spines['top'].set_color('w')
    ax3.spines['left'].set_color('w') 
    ax3.spines['right'].set_color('w')
    ax3.yaxis.label.set_color('b')

    ax3.xaxis.label.set_color('b')
    ax3.set_title('COP',color='b')
    ax3.set_xlabel('Part Load Ratio',size=22)
    ax3.set_ylabel('COP',size=22)
    ax3.yaxis.grid(True)
    ax3.xaxis.grid(True)
    plt.title(comb.get(),size=23)
    plt.show()





def addentry():
        root1 = Tk()
        root1.title("ADD ENTRY")
        northframe=Frame(root1)
        northframe.pack(anchor=NW)



        topframe = Frame(root1)
        topframe.pack(anchor=NW,padx=5,pady=10)

	bottomframe = Frame(root1)
	bottomframe.pack(anchor=SW,padx=5,pady=10)


	mm = Frame(root1,)
	mm.pack(anchor=W,padx=5,pady=10)

	m = Frame(root1)
	m.pack(padx=5,pady=10,anchor=SW)
        
        iframe=Frame(root1)
        iframe.pack(padx=5,pady=10,anchor=SW)
        def signin1():

          if unameentry.get()=="root" and passwdentry.get()=="root123":

      
		     rm.configure(state="normal")
		     rm1.configure(state="normal")
		     rm2.configure(state="normal")
		     rm3.configure(state="normal")
		     rm4.configure(state="normal")
		     rm5.configure(state="normal")
		     rm6.configure(state="normal")
		     rm7.configure(state="normal")
		     rm8.configure(state="normal")
		     rm9.configure(state="normal")
		     rm10.configure(state="normal")
		     rm11.configure(state="normal")
		     rm12.configure(state="normal")
		     rm13.configure(state="normal")
		     rm14.configure(state="normal")
		     rm15.configure(state="normal")
		     rm16.configure(state="normal")
		     rm17.configure(state="normal")
		     rm18.configure(state="normal")
		     rm19.configure(state="normal")  
		     rm20.configure(state="normal") 
		     rm21.configure(state="normal") 
		     rm22.configure(state="normal") 
		     rm23.configure(state="normal") 
		     rm24.configure(state="normal") 
                     insert.configure(state="normal")
                     logged=Label(northframe,text="logged as: root")
                     logged.pack()
                     unameentry.configure(state="disabled")
                     passwdentry.configure(state="disabled") 
          else:
                     tkMessageBox.showinfo(title="Error",message="Incorrect Password/Username")

        def go():
          b=0
          i=str(rm.get())
          i1=str(rm1.get())
          i2=str(rm2.get())
          while True:
               # for error handling and validation 
               try:
                   i3 = float(rm3.get())
                   print i3
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for kW")
                   break    
          while True:
 
               try:
                   i4 = float(rm4.get())
                   print i4
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for TR")
                   break    
          while True:
               try:
                   i5 = float(rm5.get())
                   print i5
                   b=b+1           
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for COP")
                   break    
          while True:                

               try:
                   i6 = float(rm6.get())
                   print i6
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for constant of CAPFT")
                   break
          while True:   
               try:
                   i7 = float(rm7.get())
                   print i7
                   b=b+1
                   break         
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of x in CAPFT")
                   break    
          while True:  
               try:
                   i8 = float(rm8.get())
                   print i8
                   b=b+1
                   break         
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of x2 in CAPFT")
                   break    
          while True:         
               try:
                   i9 = float(rm9.get())
                   print i9
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of y in CAPFT")
                   break    
          while True:            
               try:
                   i10 = float(rm10.get())
                   print i10
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of y2 in CAPFT")
                   break    
          while True:        
               try:
                   i11 = float(rm11.get())
                   print i11
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of xy in CAPFT")
                   break    
          while True:       
               try:
                   i12 = float(rm12.get())
                   print i12
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for constant  in EIRFT")
                   break    
          while True:       
               
               try:
                   i13 = float(rm13.get())
                   print i13
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of x in EIRFT")
                   break    
          while True:        
               try:
                   i14 = float(rm14.get())
                   print i14
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of x2 in EIRFT")
                   break    
          while True:        
               try:
                   i15 = float(rm15.get())
                   print i15
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of y in EIRFT")
                   break    
          while True:       
               try:
                   i16 = float(rm16.get())
                   print i16
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of y2 in EIRFT")
                   break
          while True:          
               try:
                   i17 = float(rm17.get())
                   print i17
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of xy in EIRFT")
                   break
          while True:            
               try:
                   i18 = float(rm18.get())
                   print i18
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for constant of COP")
                   break
          while True:                       
               try:
                   i19 = float(rm19.get())
                   print i19
                   b=b+1
                   break
               
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of PLR")
                   break 
          while True:            
               try:
                   i20 = float(rm20.get())
                   print i20
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of PLR2")
                   break     
          while True:         
               try:
                   i21 = float(rm21.get())
                   print i21
                   b=b+1
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for MIN X")
                   break 
          while True:          
               try:
                   i22 = float(rm22.get())
                   print i22
                   b=b+1              
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for MAX X")
                   break
          while True:            
               try:
                   i23 = float(rm23.get())
                   print i23
                   b=b+1        
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for MIN Y")
                   break 
          while True:              
               try:
                   i24 = float(rm24.get())
                   print i24
                   b=b+1             
                   break
               except ValueError:
                   print("Oops!  That was not valid number. please enter ID")
                   tkMessageBox.showinfo(title="Error",message="Enter number for coe of xy in EIRFT")
                   break
          #b= 22 when all the conditions are satisfied        
          if b==22:

                   conn = MySQLdb.connect("localhost","root","root123","iiit")
                   x86 = conn.cursor()
                   x86.execute("""INSERT INTO namesandcapacities VALUES (%s,%s,%s,%s,%s,%s)""",(i,i1,i2,i3,i4,i5))
                   x86.execute("""INSERT INTO coefficientscapft VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(i,i6,i7,i8,i9,i10,i11,i21,i22,i23,i24))
                   x86.execute("""INSERT INTO coefficientseirft VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(i,i12,i13,i14,i15,i16,i17,i21,i22,i23,i24))
                   x86.execute("""INSERT INTO eirfplr VALUES (%s,%s,%s,%s,%s,%s)""",(i,i18,i19,i20,0,1))
                   conn.commit()
                   conn.close()
                   rm.delete(0,'end') 
                   rm1.delete(0,'end') 
                   rm2.delete(0,'end') 
                   rm3.delete(0,'end') 
                   rm4.delete(0,'end') 
                   rm5.delete(0,'end') 
                   rm6.delete(0,'end') 
                   rm7.delete(0,'end') 
                   rm8.delete(0,'end') 
                   rm9.delete(0,'end')                    
                   rm10.delete(0,'end')
                   rm11.delete(0,'end') 
                   rm12.delete(0,'end') 
                   rm13.delete(0,'end') 
                   rm14.delete(0,'end') 
                   rm15.delete(0,'end') 
                   rm16.delete(0,'end') 
                   rm17.delete(0,'end') 
                   rm18.delete(0,'end') 
                   rm19.delete(0,'end')                    
                   rm20.delete(0,'end') 
                   rm21.delete(0,'end') 
                   rm22.delete(0,'end') 
                   rm23.delete(0,'end') 
                   rm24.delete(0,'end') 
                   b=0
        


	uname=Label(northframe,text="Username")
	uname.pack(pady=20,padx=10,side=LEFT)

	unameentry=Entry(northframe)
	unameentry.pack(side=LEFT)

	passwd=Label(northframe,text="Password")
	passwd.pack(pady=20,padx=30,side=LEFT)
	passwdentry=Entry(northframe,show="*")
	passwdentry.pack(pady=20,padx=30,side=LEFT)

	signin=Button(northframe,text="Signin",command=signin1)
	signin.pack(pady=20,padx=30,side=LEFT)


	heading1 = Label(topframe,text="TYPES",bg="white")
	heading1.pack(padx=5,pady=10,side=LEFT)


	o = Label(topframe, text="Chiller")
	o.pack(padx=12, pady=10, side=LEFT)
	rm=Entry(topframe,state="disabled")
	rm.pack(padx=5,pady=10,side=LEFT)

	o1 = Label(topframe, text="Condenser")
	o1.pack(padx=5, pady=20, side=LEFT)
	rm1=Entry(topframe,state="disabled")
	rm1.pack(padx=5,pady=10,side=LEFT)

	o2 = Label(topframe, text="Type")
	o2.pack(padx=10, pady=20, side=LEFT)
	rm2=Entry(topframe,state="disabled")
	rm2.pack(padx=5,pady=10,side=LEFT)

	o3 = Label(topframe, text="Kw")
	o3.pack(padx=25, pady=20, side=LEFT)
	rm3=Entry(topframe,state="disabled")
	rm3.pack(padx=5,pady=10,side=LEFT)

	o4 = Label(topframe, text="Tr")
	o4.pack(padx=5, pady=20, side=LEFT)
	rm4=Entry(topframe,state="disabled")
	rm4.pack(padx=5,pady=10,side=LEFT)

	o5 = Label(topframe, text="Cop")
	o5.pack(padx=5, pady=20, side=LEFT)
	rm5=Entry(topframe,state="disabled")
	rm5.pack(padx=5,pady=10,side=LEFT)


	heading2 = Label(mm,text="CAPFT",bg="white")
	heading2.pack(padx=5,pady=10,side=LEFT)


	o6 = Label(mm, text="Constant")
	o6.pack(padx=5, pady=20, side=LEFT)
	rm6=Entry(mm,state="disabled")
	rm6.pack(padx=5,pady=10,side=LEFT)

	o7 = Label(mm, text="Coef.of X")
	o7.pack(padx=5, pady=20, side=LEFT)
	rm7=Entry(mm,state="disabled")
	rm7.pack(padx=5,pady=10,side=LEFT)

	o8 = Label(mm, text="Coef.of X2")
	o8.pack(padx=5, pady=20, side=LEFT)
	rm8=Entry(mm,state="disabled")
	rm8.pack(padx=5,pady=10,side=LEFT)

	o9 = Label(mm, text="Coef.of Y")
	o9.pack(padx=5, pady=20, side=LEFT)
	rm9=Entry(mm,state="disabled")
	rm9.pack(padx=5,pady=10,side=LEFT)

	o10 = Label(mm, text="Coef.of Y2")
	o10.pack(padx=5, pady=20, side=LEFT)
	rm10=Entry(mm,state="disabled")
	rm10.pack(padx=5,pady=10,side=LEFT)

	o11 = Label(mm, text="Coef.of XY")
	o11.pack(padx=5, pady=20, side=LEFT)
	rm11=Entry(mm,state="disabled")
	rm11.pack(padx=5,pady=10,side=LEFT)

	heading = Label(bottomframe,text="EIRFT",bg="white")
	heading.pack(padx=5,pady=10,side=LEFT)

	o12 = Label(bottomframe, text="Constant")
	o12.pack(padx=5, pady=20,side=LEFT)
	rm12=Entry(bottomframe,state="disabled")
	rm12.pack(padx=5,pady=10,side=LEFT)

	o13 = Label(bottomframe, text="Coef.of X")
	o13.pack(padx=5, pady=20, side=LEFT)
	rm13=Entry(bottomframe,state="disabled")
	rm13.pack(padx=5,pady=10,side=LEFT)

	o14 = Label(bottomframe, text="Coef.of X2")
	o14.pack(padx=5, pady=20, side=LEFT)
	rm14=Entry(bottomframe,state="disabled")
	rm14.pack(padx=5,pady=10,side=LEFT)

	o15 = Label(bottomframe, text="Coef.of Y")
	o15.pack(padx=5, pady=20, side=LEFT)
	rm15=Entry(bottomframe,state="disabled")
	rm15.pack(padx=5,pady=10,side=LEFT)

	o16 = Label(bottomframe, text="Coef.of Y2")
	o16.pack(padx=5, pady=20, side=LEFT)
	rm16=Entry(bottomframe,state="disabled")
	rm16.pack(padx=5,pady=10,side=LEFT)

	o17 = Label(bottomframe, text="Coef.of XY")
	o17.pack(padx=5, pady=20, side=LEFT)
	rm17=Entry(bottomframe,state="disabled")
	rm17.pack(padx=5,pady=10,side=LEFT)


	heading4 = Label(m,text="COP",bg="white")
	heading4.pack(padx=5,pady=10,side=LEFT)

	o18 = Label(m, text="Constant")
	o18.pack(padx=12, pady=5,side=LEFT)
	rm18=Entry(m,state="disabled")
	rm18.pack(padx=5,pady=10,side=LEFT)

	o19 = Label(m, text="Coef.of PLR")
	o19.pack(padx=5, pady=5, side=LEFT)
	rm19=Entry(m,state="disabled")
	rm19.pack(padx=5,pady=10,side=LEFT)

	o20 = Label(m, text="Coef.of PLR2")
	o20.pack(padx=5, pady=5, side=LEFT)
	rm20=Entry(m,state="disabled")
	rm20.pack(padx=5,pady=10,side=LEFT)
      
        o21 = Label(m, text="min x")
        o21.pack(padx=10,pady=5,side=LEFT)
	rm21=Entry(m,state="disabled",width=10)
	rm21.pack(padx=5,pady=5,side=LEFT)

        o22 = Label(m, text="max x")
        o22.pack(padx=10,pady=5,side=LEFT)
	rm22=Entry(m,state="disabled",width=10)
	rm22.pack(padx=5,pady=5,side=LEFT)

        o23 = Label(m, text="min y")
        o23.pack(padx=10,pady=5,side=LEFT)
	rm23=Entry(m,state="disabled",width=10)
	rm23.pack(padx=5,pady=5,side=LEFT)

        o24 = Label(m, text="max y")
        o24.pack(padx=10,pady=5,side=LEFT)
	rm24=Entry(m,state="disabled",width=10)
	rm24.pack(padx=5,pady=5,side=LEFT)




        insert=Button(iframe,text="GO",command=go,state="disabled")
        insert.pack(side=LEFT,padx=20)
        quit2=Button(iframe,text="Quit",command=root1.quit)
        quit2.pack(side=LEFT)

        mainloop()


def deleteentry():
       
       def loginf1():
 
          if unameentry1.get()=="root" and passwdentry1.get()=="root123":
                          comb.configure(state='normal')
          else:
                     tkMessageBox.showinfo(title="Error",message="Incorrect Password/Username")


       def deletef1():
           x=comb.get() #this is not global
           print x
           conn = MySQLdb.connect("localhost","root","root123","iiit")
           rp = conn.cursor()
           rp.execute("""DELETE FROM namesandcapacities WHERE Chiller=%s""",(x))
           rp.execute("""DELETE FROM coefficientscapft WHERE Chiller=%s""",(x))
           rp.execute("""DELETE FROM coefficientseirft WHERE Chiller=%s""",(x))
           rp.execute("""DELETE FROM eirfplr WHERE Chiller=%s""",(x))

           conn.commit()
           conn.close()
           


       root2=Tk()
       root2.title("DELETE ENTRY")
       root2.geometry('600x100')
       pframe=Frame(root2)
       pframe.pack(side=TOP,anchor=N)
       p2frame=Frame(root2)
       p2frame.pack(side=TOP,anchor=N)
       uname1=Label(pframe,text="Username")
       uname1.pack(side=LEFT,padx=10,pady=10)
       unameentry1=Entry(pframe)
       unameentry1.pack(side=LEFT,padx=10,pady=10)
       passwd1=Label(pframe,text="Password")
       passwd1.pack(side=LEFT,padx=10,pady=10)
       passwdentry1=Entry(pframe,show="*")
       passwdentry1.pack(side=LEFT,padx=10,pady=10)
       login1=Button(pframe,text="Login",command=loginf1)
       login1.pack()
       
       db = MySQLdb.connect("localhost","root","root123","iiit")
       mycursor = db.cursor()
       mycursor.execute("SELECT Chiller FROM namesandcapacities")
       xnames1=[]
       xnamess1=[]
       
       # calls fetchone until None is returned (no more rows)
       for row in iter(mycursor.fetchone, None):
		  xnames1.append(row[0])
       xnamess1=sorted(xnames1)
       comb = ttk.Combobox(p2frame, textvariable=variable,width=30, values=xnamess1,state='disabled')
       comb.pack(side=LEFT)
       delete1=Button(p2frame,text="Delete",command=deletef1)
       delete1.pack(side=LEFT,padx=10)




master = Tk()
master.title("Select Chiller")
tframe=Frame(master)
tframe.pack()
bframe=Frame(master)
bframe.pack(side=BOTTOM)


menu = Menu(master)
master.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Add Entry",command=addentry)
subMenu.add_command(label="delete Entry",command=deleteentry)
subMenu.add_command(label="Quit",command=master.quit)
subMenu.add_separator()

xnames=[]
xnamess=[]

variable = StringVar(master)
variable.set("----Select Chiller----") # default value

db = MySQLdb.connect("localhost","root","root123","iiit")
mycursor = db.cursor()
mycursor.execute("SELECT Chiller FROM namesandcapacities")

# calls fetchone until None is returned (no more rows)
for row in iter(mycursor.fetchone, None):
    xnames.append(row[0])
xnamess=sorted(xnames)
comb = ttk.Combobox(tframe, textvariable=variable,width=30, values=xnamess)
comb.pack()
button=Button(bframe,text="Okay",command=ok)
button.pack(side=LEFT,padx=15,pady=50)
button1=Button(bframe,text="Drawgraph",command=drawgraph)
button1.pack(side=LEFT,padx=20,pady=50)

mainloop()
