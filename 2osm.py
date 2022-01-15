# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 19:52:19 2021

@author: Bruno Ferreira
"""

import xml.dom.minidom as md
import os
import numpy as np


# =============================================================================
# #    executando o SUMO
# =============================================================================
def sumo():
    os.system('powershell.exe cd D:\Programas\sumo2\TCC; sumo 2sumo.sumocfg') #-noexit
    return()

# =============================================================================
#      executando o SUMO random
# =============================================================================
def sumo_random():
    os.system('powershell.exe cd D:\Programas\sumo2\TCC; sumo -c 2sumo.sumocfg --random')
    return()

# =============================================================================
# #CALCULAR O TEMPO DE VIAGEM E SALVAR EM CSV 
# =============================================================================
def salvar(sem1,sem2,sem3):
    
    #capturando o tempo medio de viagem
    mtt=[]
    summary= md.parse("resumo_rede.xml")
    out= summary.getElementsByTagName("step")
    for i in out:
        mtt.append(float(i.getAttribute("meanTravelTime")))
#
    #removendo os 10min inciais da simulacao
    mediav=sum(mtt[600:])/(len(mtt[600:]))
    print(mediav)
    
    temp=np.array([sem1,sem2,sem3,mediav])
    temp2=np.loadtxt("dados.csv",delimiter=',')
    save=np.vstack([temp2,temp])
    np.savetxt("dados.csv", save, delimiter=",",fmt='%10.2f')
    return(mediav)
    
# =============================================================================
#     #ALTERA AS VARIAVEIS NO ARQ DE REDE .XML
# =============================================================================
def alterar(tl10,tl11,tl20,tl21,tl30,tl31):
    
    file = md.parse("2osm.net.xml")
    file.getElementsByTagName("phase")[0].setAttribute("duration",str(tl10))
    file.getElementsByTagName("phase")[3].setAttribute("duration",str(tl11))
    file.getElementsByTagName("phase")[6].setAttribute("duration",str(tl20))
    file.getElementsByTagName("phase")[9].setAttribute("duration",str(tl21))
    file.getElementsByTagName("phase")[12].setAttribute("duration",str(tl30))
    file.getElementsByTagName("phase")[15].setAttribute("duration",str(tl31))
    with open( "2osm.net.xml", "w" ) as fs:
        fs.write( file.toxml() )
        fs.close()
        
        
# =============================================================================
#     #Varredura de tempos semaforicos
# =============================================================================
def varredura():
    #Variaveis de varredura
    tmin=10
    tmax=75
    gap=5
    interval=4
    r=int(((tmax-tmin)/gap)-1)
    cycle_time=tmin+tmax
    
    tl10=tmin
    tl11=tmax
    n_sim=0
    
    for i1 in range(r):
        tl10=tl10+gap
        tl11=tl11-gap
        tl20=tmin
        tl21=tmax
        for i2 in range(r):
            tl20=tl20+gap
            tl21=tl21-gap
            tl30=tmin
            tl31=tmax
            for i3 in range(r):
                tl30=tl30+gap
                tl31=tl31-gap
                
                if (interval*gap>abs(tl30-tl20)) and (interval*gap>abs(tl20-tl10)) and (interval*gap>abs(tl30-tl10)) :                   
                    alterar(tl10,tl11,tl20,tl21,tl30,tl31)                    
                    sumo()
                    salvar(tl10,tl20,tl30)
                    
                    n_sim+=1
                    print("sem 1 ",tl10,abs(cycle_time-tl10),"sem 2 ",tl20,abs(cycle_time-tl20),"sem 3 ",tl30,abs(cycle_time-tl30))
    print(n_sim)
def main():
# =============================================================================
# #executar o otimizador
# =============================================================================
    varredura()

# =============================================================================
# #executar o simulador randomico com os tempos de verde do sem1,sem2 e sem3
# =============================================================================
#    for i in range(5):
#        sumo_random()
#        salvar(20,20,20)


if __name__=="__main__":
    main();
