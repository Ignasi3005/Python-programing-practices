import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

class engineering_economics:
    def __init__(self):
        pass
    def composite_interest_rate(self,i,λ):
        θ=(i/100-λ/100)/(1+λ/100)
        return θ
    def Compound_interest(self,P,i,n):
        F=P*(1+i/100)**n
        return F
    def simple_interest(self,P,i,n):
        I=(i*P)/100
        F=P*(1+(i*n)/100)
        return I,F
    def i_Future_cost(self,PC,λ,n):
        FC=PC(1+λ/100)**n
        return FC
    def i_Future_value(self,PV,λ,n):
        FV=PV/(1+λ/100)**n
        return FV
    def InterestInflation(self,PV,i,λ,n):
        FV=PV*((1+i/100)/(1+λ/100))**n
        return FV
    def efectiveinterest_rate(self,m,k):
        r=(1+k/100*m)**m -1
        return r 
    def Present_value(self,FV,i,n):
        PV=FV*(1/(1+i/100))**n
        return PV 
    def compoundingmorethanone_a_year(self,PV,i,n,m):
        FV=PV*(1+i/100*m)**(m*n)
        return FV 
    def fishereqn(self,i,λ):
        I=(1+i/100)/(1+λ/100)-1     
        return I
if __name__ == "__main__":
    engc=engineering_economics()
print(engc.Present_value(100000,12,3))

    
    
