#This program is used to convert Quternion to Euler angle that can describe the sensor orientation.
import os,csv,math

quaternion=[]
root1=input('the file with all Quaternion data:\n')
for path, subdirs, files in os.walk(root1): #search director and all sub director
    for name in files:
        if 'csv'and 'Quaternion' in name:
            srcfile=os.path.join(path, name)
            quaternion.append(srcfile)
            f= open(srcfile, newline='')
            reader = csv.reader(f)
            data=list(reader)           
            ls=[]              
            for i in data[1::]:
                a=eval(i[2])
                b=eval(i[3])
                c=eval(i[4])
                d=eval(i[5])
                x=math.atan2(2*(c*d+a*b), a**2+d**2-b**2-c**2)/math.pi*180
                y=-math.asin(2*b*d-2*a*c)/math.pi*180
                z=math.atan2(2*(b*c+a*d), a**2+b**2-c**2-d**2)/math.pi*180
                R=[i[0], i[1], x, y, z]              
                try:
                    ls.append(R)
                except:
                    print('error')
            data[0][2:6]=['X','Y','Z', '']
            ls.insert(0, data[0])
            
            dirfile=srcfile.replace('Quaternion','Eular')
            fw=open(dirfile, 'w', newline='')
            wr=csv.writer(fw, dialect='excel')
            wr.writerows(ls)
            fw.close()
            
            new=name.replace('Quaternion','Euler')
            print('the {} has been created\n'.format(new))
            
input("Press Enter to exit") 
