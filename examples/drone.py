m1=False
m2=False
m3=False
m4=False
v0=20
speed=0
import math
import mix
class motor:
    def __init__(self):
        pass
    def ig(self):
        print(mix.igx())
        
    def fly(self):
        self.ig()
        payload=float(input("Enter your payload:"))
        thrust=float(input("Enter individual motor thrust:"))
        load_per_motor=payload/4
        safety_factor=thrust/load_per_motor
        print(safety_factor)
        if safety_factor>1.5:
            m1=m2=m3=m4=True
            print("Stable flight")
        elif 1<=safety_factor<1.5:print("Dangerous flight")
        else: print("Unstability")
    def foward(self):
        m1=m2=mm4=True
        speed=v0
        speed -=1
        print(speed)
    def reverse(self):
        m1=m2=m3=m4=True
        speed=v0
        speed +=1
        print(speed)
class drone:
    def __init__(self):
        self.motor=motor()
        pass
    def take_off(self):
        password=3005
        PIN=int(input("PASSWORD"))
        if PIN==password:self.motor.fly()
        else:print("ACCESS DENIED")

ignasi=drone()
print(ignasi.take_off())


 