# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 19:52:19 2021

@author: Bruno
"""

import xml.dom.minidom as md
import os
import numpy as np
from time import process_time as timer



    #executando o SUMO
def sumo():
    os.system('powershell.exe cd D:\Programas\sumo2\TCC; sumo 2sumo.sumocfg') #-noexit
    return()

#SALVAR EM CSV O TEMPO MEDIO DE VIAGEM
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
    


def main():
#    sumo()
    t_start=timer()
    file = md.parse("2osm.net.xml")
#    file:///D:/Programas/sumo2/TCC/resumo_rede.xml


# =============================================================================
# #    capturar valores da variavel duration do XML
# =============================================================================
    
#    tl10= int(file.getElementsByTagName("phase")[0].getAttribute("duration"))
#    tl11= int(file.getElementsByTagName("phase")[2].getAttribute("duration"))
#    tl20= int(file.getElementsByTagName("phase")[4].getAttribute("duration"))
#    tl21= int(file.getElementsByTagName("phase")[6].getAttribute("duration"))
#    tl30= int(file.getElementsByTagName("phase")[8].getAttribute("duration"))
#    tl31= int(file.getElementsByTagName("phase")[10].getAttribute("duration"))

#    tll=[tl10,tl11,tl20,tl21,tl30,tl31]

#    sumo()
#    salvar(tl10,tl20,tl30)

    
# =============================================================================
#     #Varredura de tempos semaforicos
# =============================================================================
    
    #Variaveis de varredura
    tmin=10
    tmax=70
    gap=5
    interval=4
    r=int(((tmax-tmin)/gap)-1)
    cycle_time=tmin+tmax
    
    tl10=tmin
    tl11=tmax
    i=0
    
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
                file.getElementsByTagName("phase")[0].setAttribute("duration",str(tl10))
                file.getElementsByTagName("phase")[3].setAttribute("duration",str(tl11))
                file.getElementsByTagName("phase")[6].setAttribute("duration",str(tl20))
                file.getElementsByTagName("phase")[9].setAttribute("duration",str(tl21))
                file.getElementsByTagName("phase")[12].setAttribute("duration",str(tl30))
                file.getElementsByTagName("phase")[15].setAttribute("duration",str(tl31))
                
                if (interval*gap>abs(tl30-tl20)) and (interval*gap>abs(tl20-tl10)) and (interval*gap>abs(tl30-tl10)) :
                    i=i+1
                    print("sem 1 ",tl10,abs(cycle_time-tl10),"sem 2 ",tl20,abs(cycle_time-tl20),"sem 3 ",tl30,abs(cycle_time-tl30))

# =============================================================================
#     #SALVA MODIFICACOES NO ARQ DE REDE .XML
# =============================================================================
                    with open( "2osm.net.xml", "w" ) as fs:

                        fs.write( file.toxml() )
                        fs.close()
                    
                    sumo()
                    salvar(tl10,tl20,tl30)
                    
#                    
    #tempo de execucao
    t_stop=timer()
    print("elapsed time(min): ",(t_stop-t_start)/60)
    print("número de simulações= ",i)
    

#

if __name__=="__main__":
    main();
