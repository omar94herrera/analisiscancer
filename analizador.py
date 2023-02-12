from scipy.interpolate import lagrange
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
import math as m
import shutil, os
import subprocess
import time


def caldim():
    file=bordesV.get()
    archivo=open(file,"r")
    Area={}
    Largo={}
    Alto={}
    frames={}

    #este bloque me ordena la información por frames
    for linea in archivo:
        linea=linea.strip().split(",")
        frame=int(linea[len(linea)-1])
        if frame not in frames:
            frames[frame]=list(map(int,linea[:len(linea)-1]))
        else:
            for i in range(len(linea)-1):
                frames[frame].append(int(linea[i]))
    archivo.close()
    
    #este bloque cuenta la cantidad de figuras que hay
    datos=frames[1]
    indices=datos[::4]
    n=1
    nfig=1 #número de figuras
    while n!=0:
        n=indices.count(nfig)
        if n!=0:
            Area[nfig]=[]
            Largo[nfig]=[]
            Alto[nfig]=[]
        nfig+=1
    nfig=nfig-2

    #aquí se calcula área, largo y alto
    for i in range(len(frames)):
        datos=frames[i+1]
        indices=datos[::4]
        y_inf=datos[2::4]
        y_sup=datos[3::4]
        pivot=0
        for j in range(nfig):
            largo=indices.count(j+1)
            y_inf_j=y_inf[pivot:pivot+largo]
            y_sup_j=y_sup[pivot:pivot+largo]
            alto=max([y_sup_j[k]-y_inf_j[k]+1 for k in range(len(y_inf_j))])
            area=0
            #print("el largo de la figura",nfig,"en el frame",i,"es",largo)
            for i in range(largo):
                area+=y_sup_j[i]-y_inf_j[i]+1
                #print(area,y_sup_j[i]-y_inf_j[i]+1)
            area=area*1.609425**2
            pivot+=largo+1
            Area[j+1].append(area)
            Largo[j+1].append(largo*1.609425)
            Alto[j+1].append(alto*1.609425)
    #print(dim)
    #print("Area:",Area)
    #print("")
    #print("Largo:",Largo)
    #print("")
    #print("Alto",Alto)
    #print("")
    return (Area,Largo,Alto,nfig,len(frames))

def caldim2(file):
    archivo=open(file,"r")
    Area={}
    Largo={}
    Alto={}
    frames={}

    #este bloque me ordena la información por frames
    for linea in archivo:
        linea=linea.strip().split(",")
        frame=int(linea[len(linea)-1])
        if frame not in frames:
            frames[frame]=list(map(int,linea[:len(linea)-1]))
        else:
            for i in range(len(linea)-1):
                frames[frame].append(int(linea[i]))
    archivo.close()
    
    #este bloque cuenta la cantidad de figuras que hay
    datos=frames[1]
    indices=datos[::4]
    n=1
    nfig=1 #número de figuras
    while n!=0:
        n=indices.count(nfig)
        if n!=0:
            Area[nfig]=[]
            Largo[nfig]=[]
            Alto[nfig]=[]
        nfig+=1
    nfig=nfig-2

    #aquí se calcula área, largo y alto
    for i in range(len(frames)):
        datos=frames[i+1]
        indices=datos[::4]
        y_inf=datos[2::4]
        y_sup=datos[3::4]
        pivot=0
        for j in range(nfig):
            largo=indices.count(j+1)
            y_inf_j=y_inf[pivot:pivot+largo]
            y_sup_j=y_sup[pivot:pivot+largo]
            alto=max([y_sup_j[k]-y_inf_j[k]+1 for k in range(len(y_inf_j))])*1.609425
            area=0
            for i in range(largo):
                area+=y_sup_j[i]-y_inf_j[i]+1
            area=area*(1.609425**2)
            pivot+=largo
            Area[j+1].append(area)
            Largo[j+1].append(largo*1.609425)
            Alto[j+1].append(alto)
    #print(dim)
    #print("Area:",Area)
    #print("")
    #print("Largo:",Largo)
    #print("")
    #print("Alto",Alto)
    #print("")
    return (Area,Largo,Alto,nfig,len(frames))

#esta funcion retorna dos diccionarios, uno es el de velocidades de los objetos y el otro
#es el de los angulos en que se movieron los objetos
def calculovelyan():
    file=centroidesV.get()
    archivo=open(file,'r')
    nobjeto=1
    spd={}
    angulos={}
    dst={}
    for linea in archivo:
        linea=list(map(int,linea.strip().split(",")))
        coordx=linea[::2]
        coordy=linea[1::2]
        spds=[]
        #spdx=[]
        #spdy=[]
        verif=0
        dsts=[]
        distancia=0
        if verif==0:
            verif=1
            primerx=coordx[0]
            primery=coordy[0]
        for i in range(len(coordx)):
            #DISTANCIA EUCLIDEANA (en linea recta, desde el punto de origen al punto actual)
            #para calcular distancia euclideana descomentar las siguientes dos lineas y comentar
            #las de distancia acumulada más abajo
            #distancia=m.sqrt((coordx[i]-primerx)**2+(coordy[i]-primery)**2)
            #dsts.append(distancia)
            if i<len(coordx)-1:
                #las siguientes dos lineas son para velocidad por componentes
                #spdx.append(abs(coordx[i+1]-coordx[i]))
                #spdy.append(abs(coordy[i+1]-coordy[i]))
                #DISTANCIA ACUMULADA (o total recorrida)
                #para calcular las distancia acumulada descomentar las siguientes dos lineas de código
                #y comentar las de distancia euclideana más arriba
                distancia+=m.sqrt((coordx[i+1]-coordx[i])**2+(coordy[i+1]-coordx[i])**2)
                dsts.append(distancia)
                #velocidad real (instantanea)
                velocidad=m.sqrt(((coordx[i+1]-coordx[i])/15)**2+((coordy[i+1]-coordy[i])/15)**2)
                spds.append(velocidad)
                #print(velocidad)
                try:
                    angulo=m.degrees(m.atan((coordy[i+1]-primery)/(coordx[i+1]-primerx)))
                except ZeroDivisionError:
                    if coordy[i+1]>primery:
                        angulo=90
                    elif coordy[i+1]<primery:
                        angulo=-90
                    else:
                        angulo=0
            else:
                continue
        dst[nobjeto]=dsts
        spd[nobjeto]=spds
        angulos[nobjeto]=angulo
        nobjeto+=1
    archivo.close()
    #print("velocidades:",spd)
    #print("angulos:",angulos)
    return (spd,angulos,dst)

def calculovelyan2(file):
    archivo=open(file,'r')
    nobjeto=1
    spd={}
    angulos={}
    dst={}
    for linea in archivo:
        linea=list(map(int,linea.strip().split(",")))
        coordx=linea[::2]
        coordy=linea[1::2]
        spds=[]
        #spdx=[]
        #spdy=[]
        verif=0
        dsts=[]
        if verif==0:
            verif=1
            primerx=coordx[0]
            primery=coordy[0]
        for i in range(len(coordx)):
            #distancia euclideana (en linea recta, desde el punto de origen al punto actual)
            #para calcular distancia euclideana descomentar las siguientes dos lineas y comentar
            #las de distancia acumulada más abajo
            distancia=m.sqrt((coordx[i]-primerx)**2+(coordy[i]-primery)**2)
            dsts.append(distancia)
            if i<len(coordx)-1:
                #las siguientes dos lineas son para velocidad por componentes
                #spdx.append(abs(coordx[i+1]-coordx[i]))
                #spdy.append(abs(coordy[i+1]-coordy[i]))
                #distancia acumulada (o total recorrida)
                #para calcular las distancia acumulada descomentar las siguientes dos lineas de código
                #y comentar las de distancia euclideana más arriba
                #distancia+=m.sqrt((coordx[i+1]-coordx[i])**2+(coordy[i+1]-coordx[i])**2)
                #dsts.append(distancia)
                #velocidad real
                velocidad=m.sqrt(((coordx[i+1]-coordx[i])/15)**2+((coordy[i+1]-coordy[i])/15)**2)
                spds.append(velocidad)
                #print(velocidad)
                try:
                    angulo=m.degrees(m.atan((coordy[i+1]-primery)/(coordx[i+1]-primerx)))
                except ZeroDivisionError:
                    if coordy[i+1]>primery:
                        angulo=90
                    elif coordy[i+1]<primery:
                        angulo=-90
                    else:
                        angulo=0
            else:
                continue
        dst[nobjeto]=dsts
        spd[nobjeto]=spds
        angulos[nobjeto]=angulo
        nobjeto+=1
    archivo.close()
    #print("velocidades:",spd)
    #print("angulos:",angulos)
    return (spd,angulos,dst)

def analisisuno():
    print("el informe se está creando, porfavor espere")
    dims=["Area","Largo","Alto"]
    a=corrertest()
    file=open("informe.tex",'w')
    basetex(file)
    intro(file)
    ### gráficos vs tiempo
    for dim in dims:
        if dim=="Area":
            file.write("A continuaci\\'on se presentan los gr\\'aficos de \\'Area vs tiempo\\\\\n")
        else:
            file.write("A continuaci\\'on se presentan los gr\\'aficos de "+dim+" vs tiempo\\\\\n")
        creagraficos(a[dim],a["nframes"],a["nfig"],dim,1)
        contador=1
        for i in range(a["nfig"]):
            if dim=="Area":
                printimage(file,"Area_de_celula_"+str(i+1)+"_vs_tiempo.png")
            else:
                printimage(file,dim+"_de_celula_"+str(i+1)+"_vs_tiempo.png")
            if contador==2:
                file.write("\\\\\n")
                contador=1
            else:
                contador+=1
        file.write("\\newpage\n")
    ### gráficos de velocidades
    file.write("A continuaci\\'on se presentan los gr\\'aficos de velocidades vs tiempo.\\\\\n")
    creagraficosvel(a["spd"],a["nframes"],a["nfig"],1)
    contador=1
    for i in range(a["nfig"]):
        printimage(file,"Velocidad_de_celula_"+str(i+1)+".png")
        if contador==2:
            file.write("\\\\\n")
            contador=1
        else:
            contador+=1
    file.write("\\newpage\n")
    ### gráficos de variaciones
    for dim in dims:
        if dim=="Area":
            file.write("A continuaci\\'on se presentan los gr\\'aficos de variaciones del \\'Area vs tiempo\\\\\n")
        else:
            file.write("A continuaci\\'on se presentan los gr\\'aficos de variaciones del "+dim+" vs tiempo\\\\\n")
        creagraficosv(a[dim],a["nframes"],a["nfig"],dim,1)
        contador=1
        for i in range(a["nfig"]):
            if dim=="Area":
                printimage(file,"Variacion_de_Area_de_celula_"+str(i+1)+".png")
            else:
                printimage(file,"Variacion_de_"+dim+"_de_celula_"+str(i+1)+".png")
            if contador==2:
                file.write("\\\\\n")
                contador=1
            else:
                contador+=1
        file.write("\\newpage\n")
    ### cálculo de correlaciones entre dimensiones
    file.write("\\textbf{Correlaciones entre dimensiones:}\\\\\n")
    verificador=0
    rickydicky={0:"Area",1:"Largo",2:"Alto"}
    for i in range(a["nfig"]):
        if verificador==0:
            verificador=1
            macorr=matrizcorr([a["Area"][i+1],a["Largo"][i+1],a["Alto"][i+1]])
        else:
            macorr+=matrizcorr([a["Area"][i+1],a["Largo"][i+1],a["Alto"][i+1]])
    macorr=macorr/a["nfig"]
    for i in range(3):
        for j in range(3):
            if i<j:
                ancorrim(rickydicky[i],rickydicky[j],file,macorr[i,j])
                file.write("\\\\\n")             
    
    ### cálculo de correlaciones entre dimensiones y velocidad
    file.write("\\textbf{Correlaciones entre dimensiones y velocidad:}\\\\\n")
    for dim in dims:
        verificador=0
        for i in range(a["nfig"]):
            if verificador==0:
                macorrv=matrizcorr2(a["spd"][i+1],a[dim][i+1])
                #la siguiente linea es un análisis de la correlación entre la dimension correspondiente de la célula y su velocidad
                #ancorrim("valocidad",dim+" de la figura "+str(i+1),file,macorrv)
                #file.write("\\\\\n")
                verificador=1
            else:
                macorrv+=matrizcorr2(a["spd"][i+1],a[dim][i+1])
        macorrv=macorrv/a["nfig"]
        ancorrim("valocidad",dim,file,macorrv)
        file.write("\\\\\n")

    ### relación entre cociente de Largo y alto con la velocidad
    macorrv=0
    file.write("\\textbf{An\\'alisis de relaci\\'on entre cociente de largo y alto con la velocidad, esto quiere decir que si la c\\'elula adquiere una forma m\\'as esf\\'erica (o cuadrada) puede tener alguna relaci\\'on con la velocidad.}\\\\\n")
    for i in range(a["nfig"]):
        if macorrv==0:
            macorrv=matrizcorr2(a["spd"][i+1],[a["Alto"][i+1][j]/a["Largo"][i+1][j] for j in range(len(a["Alto"][1]))])
        else:
            macorrv+=matrizcorr2(a["spd"][i+1],[a["Alto"][i+1][j]/a["Largo"][i+1][j] for j in range(len(a["Alto"][1]))])
    macorrv=macorrv/a["nfig"]
    ancorrim("valocidad","cociente entre Largo y Alto",file,macorrv)
    file.write("\\\\\n")


    
    ### relación entre distancia acumulada vs área
    file.write("\\textbf{Correlaciones entre distancia acumulada y \\'area:}\\\\\n")
    verificador=0
    for i in range(a["nfig"]):
        if verificador==0:
            macorrv=matrizcorr2(a["Area"][i+1],a["dst"][i+1])
            #la siguiente linea es un análisis de la correlación entre la dimension correspondiente de la célula y su velocidad
            #ancorrim("distancia recorrida","\\'area de la figura "+str(i+1),file,macorrv)
            #file.write("\\\\\n")
            verificador=1
        else:
            macorrv+=matrizcorr2(a["Area"][i+1],a["dst"][i+1])
    macorrv=macorrv/a["nfig"]
    ancorrim("distancia recorrida","\\'area",file,macorrv)
    file.write("\\\\\n")

    ### ángulos de desplazamiento
    file.write("A continuaci\\'on se motrar\\'an los \\'angulos de desplazamiento de cada c\\'elula, considerando su posici\\'on inicial y su posici\\'on final.\\\\\n")
    for i in range(a["nfig"]):
        file.write("C\\'elula "+str(i+1)+": $"+str(round(a["angulos"][i+1]))+"^o$ \\\\\n")
    file.write("\\\\\n")

    findoc(file)
    file.close()
    print("el archivo fue creado con éxito")
    ventana_fin(1)


def analisistotal():
    print("Los informes se están creando, porfavor espere")
    dims=["Area","Largo","Alto"]
    carpeta=os.listdir(".")
    videos=[]
    #print(carpeta)
    for i in carpeta: #aquí guardo los nombres de los videos en una lista para su posterior análisis
        j=i.split(".")
        if j[len(j)-1]=="tif":
            videos.append(i)
    #print(videos)
    for video in videos:
        nombrecarpeta=video[:len(video)-4]
        #aquí si la carpeta existe la sobreescribo
        if nombrecarpeta in carpeta:
            os.rmdir(nombrecarpeta)
            os.mkdir(os.getcwd()+os.sep+nombrecarpeta)
        else:
            os.mkdir(os.getcwd()+os.sep+nombrecarpeta)
        subprocess.run(["matlab.exe","-r","main('"+video+"',"+str(ncelulasV.get())+")"])
        time.sleep(segundosV.get()) #aquí se deja de avanzar en el script de python para que matlab pueda ejecutarse,
        #aumentar el numero de segundos en caso de que su computador tarde más en ejecutar este proceso
        #esto funciona con la versión 2019b de MATLAB
        a=corrertest2(nombrecarpeta+"_boundaries.txt",nombrecarpeta+"_centroids.txt")
        file=open(nombrecarpeta+"_informe.tex",'w')
        basetex(file)
        intro(file)
        ### gráficos vs tiempo
        for dim in dims:
            if dim=="Area":
                file.write("A continuaci\\'on se presentan los gr\\'aficos de \\'Area vs tiempo.\\\\\n")
            else:
                file.write("A continuaci\\'on se presentan los gr\\'aficos de "+dim+" vs tiempo.\\\\\n")
            creagraficos(a[dim],a["nframes"],a["nfig"],dim,1)
            contador=1
            for i in range(a["nfig"]):
                if dim=="Area":
                    printimage(file,"Area_de_celula_"+str(i+1)+"_vs_tiempo.png")
                else:
                    printimage(file,dim+"_de_celula_"+str(i+1)+"_vs_tiempo.png")
                if contador==2:
                    file.write("\\\\\n")
                    contador=1
                else:
                    contador+=1
            file.write("\\newpage\n")
        ### gráficos de velocidades
        file.write("A continuaci\\'on se presentan los gr\\'aficos de velocidades vs tiempo.\\\\\n")
        creagraficosvel(a["spd"],a["nframes"],a["nfig"],1)
        contador=1
        for i in range(a["nfig"]):
            printimage(file,"Velocidad_de_celula_"+str(i+1)+".png")
            if contador==2:
                file.write("\\\\\n")
                contador=1
            else:
                contador+=1
        file.write("\\newpage\n")
        ### gráficos de variaciones
        for dim in dims:
            if dim=="Area":
                file.write("A continuaci\\'on se presentan los gr\\'aficos de variaciones del \\'Area vs tiempo\\\\\n")
            else:
                file.write("A continuaci\\'on se presentan los gr\\'aficos de variaciones del "+dim+" vs tiempo\\\\\n")
            creagraficosv(a[dim],a["nframes"],a["nfig"],dim,1)
            contador=1
            for i in range(a["nfig"]):
                if dim=="Area":
                    printimage(file,"Variacion_de_Area_de_celula_"+str(i+1)+".png")
                else:
                    printimage(file,"Variacion_de_"+dim+"_de_celula_"+str(i+1)+".png")
                if contador==2:
                    file.write("\\\\\n")
                    contador=1
                else:
                    contador+=1
            file.write("\\newpage\n")
        ### cálculo de correlaciones entre dimensiones
        file.write("\\textbf{Correlaciones entre dimensiones:}\\\\\n")
        verificador=0
        rickydicky={0:"Area",1:"Largo",2:"Alto"}
        for i in range(a["nfig"]):
            if verificador==0:
                verificador=1
                macorr=matrizcorr([a["Area"][i+1],a["Largo"][i+1],a["Alto"][i+1]])
            else:
                macorr+=matrizcorr([a["Area"][i+1],a["Largo"][i+1],a["Alto"][i+1]])
        macorr=macorr/a["nfig"]
        for i in range(3):
            for j in range(3):
                if i<j:
                    ancorrim(rickydicky[i],rickydicky[j],file,macorr[i,j])
                    file.write("\\\\\n")
                
    
        ### cálculo de correlaciones entre dimensiones y velocidad
        file.write("\\textbf{Correlaciones entre dimensiones y velocidad:}\\\\\n")
        for dim in dims:
            verificador=0
            for i in range(a["nfig"]):
                if verificador==0:
                    macorrv=matrizcorr2(a["spd"][i+1],a[dim][i+1])
                    #la siguiente linea es un análisis de la correlación entre la dimension correspondiente de la célula y su velocidad
                    #ancorrim("valocidad",dim+" de la c\\'elula "+str(i+1),file,macorrv)
                    #file.write("\\\\\n")
                    verificador=1
                else:
                    macorrv+=matrizcorr2(a["spd"][i+1],a[dim][i+1])
            macorrv=macorrv/a["nfig"]
            ancorrim("valocidad",dim,file,macorrv)
            file.write("\\\\\n")

        ### relación entre cociente de Largo y Área con la velocidad
        macorrv=0
        file.write("\\textbf{An\\'alisis de relaci\\'on entre cociente de largo y alto con la velocidad, esto quiere decir que si la c\\'elula adquiere una forma m\\'as esf\\'erica (o cuadrada) puede tener alguna relaci\\'on con la velocidad.}\\\\\n")
        for i in range(a["nfig"]):
            if macorrv==0:
                macorrv=matrizcorr2(a["spd"][i+1],[a["Alto"][i+1][j]/a["Largo"][i+1][j] for j in range(len(a["Alto"][1]))])
            else:
                macorrv+=matrizcorr2(a["spd"][i+1],[a["Alto"][i+1][j]/a["Largo"][i+1][j] for j in range(len(a["Alto"][1]))])
        macorrv=macorrv/a["nfig"]
        ancorrim("valocidad","cociente entre Largo y Alto",file,macorrv)
        file.write("\\\\\n")
        
        ### relación entre distancia acumulada vs area
        file.write("\\textbf{Correlaciones entre distancia acumulada y \\'area:}\\\\\n")
        verificador=0
        for i in range(a["nfig"]):
            if verificador==0:
                macorrv=matrizcorr2(a["Area"][i+1],a["dst"][i+1])
                #la siguiente linea es un análisis de la correlación entre la dimension correspondiente de la célula y su velocidad
                #ancorrim("distancia recorrida","\\'area de la c\\'elula "+str(i+1),file,macorrv)
                #file.write("\\\\\n")
                verificador=1
            else:
                macorrv+=matrizcorr2(a["Area"][i+1],a["dst"][i+1])
        macorrv=macorrv/a["nfig"]
        ancorrim("distancia recorrida","\\'area",file,macorrv)
        file.write("\\\\\n")

        ### ángulos de desplazamiento
        file.write("A continuaci\\'on se motrar\\'an los \\'angulos de desplazamiento de cada c\\'elula, considerando su posici\\'on inicial y su posici\\'on final.\\\\\n")
        for i in range(a["nfig"]):
            file.write("Figura "+str(i+1)+": $"+str(round(a["angulos"][i+1]))+"^o$ \\\\\n")
        file.write("\\\\\n")

        findoc(file)
        file.close()
        
        #ahora muevo los archivos a la carpeta correspondiente
        shutil.move(nombrecarpeta+"_informe.tex",nombrecarpeta)
        os.remove(nombrecarpeta+"_binarized.tif") #aquí borro un archivo que se creó en el programa de matlab que no se usa para nada
        shutil.move(nombrecarpeta+"_boundaries.txt",nombrecarpeta)
        shutil.move(nombrecarpeta+"_centroids.txt",nombrecarpeta)
        carpeta=os.listdir(".")
        for i in carpeta:
            j=i.split(".")
            if j[len(j)-1]=="png":
                shutil.move(i,nombrecarpeta)
        
    if len(videos)==1:
        print("el informe fue creado con éxito")
        ventana_fin(1)
    else:
        print("los informes fueron creados con éxito")
        ventana_fin(2)




#función test
def corrertest():
    (Area,Largo,Alto,nfig,nframes)=caldim()
    (spd,angulos,dst)=calculovelyan()
    return {"spd":spd,"angulos":angulos,"dst":dst,"Area":Area,"Largo":Largo,"Alto":Alto,"nfig":nfig,"nframes":nframes}

#función test 2
def corrertest2(bordes,centroides):
    (Area,Largo,Alto,nfig,nframes)=caldim2(bordes)
    (spd,angulos,dst)=calculovelyan2(centroides)
    return {"spd":spd,"angulos":angulos,"dst":dst,"Area":Area,"Largo":Largo,"Alto":Alto,"nfig":nfig,"nframes":nframes}

#¡¡¡¡IMPORTANTE LEER!!!!
#para probar las funciones, escribir los nombres de los archivos en sus casillas correspondientes
#luego cerrar la interfaz y escribir (con eso se podran probar las funciones de graficos de abajo)
#a=corrertest()


#FUNCIONES PARA GRÁFICOS
#######################################################

#aquí se hacen los gráficos vs tiempo
def creagraficos(dic,nframes,nfig,title,save=0,size=(8,8)):#poner save=1 si se desean guardar los gráficos
    x=np.array(range(nframes))
    for j in range(nfig):
        plt.figure(figsize=size)#tamaño de gráfico
        plt.plot(15*x,[dic[j+1][i] for i in x])
        if title=="Area":
            plt.title("Área de célula "+str(j+1)+" vs tiempo")
        else:
            plt.title(title+" de célula "+str(j+1)+" vs tiempo")
        plt.xlabel("tiempo (min)") #nombre de eje x
        if title=="Area":
            plt.ylabel("Área de célula "+str(j+1)+" $(\mu m)^2$")  #nombre de eje y
        else:
            plt.ylabel(title+" de célula "+str(j+1)+" $(\mu m)$")  #nombre de eje y
        if save==1:
            plt.savefig(title+"_de_celula_"+str(j+1)+"_vs_tiempo") #con esto guardo la imagen
            plt.close()
        elif save==0:
            plt.show()


#creagraficos(a["Area"],a["nframes"],a["nfig"],"Área")

#aquí se hacen los gráficos de variaciones
def creagraficosv(dic,nframes,nfig,title,save=0,size=(8,8)):#poner save=1 si se desean guardar los gráficos
    x=np.array(range(nframes-1))
    for j in range(nfig):
        plt.figure(figsize=size)#tamaño de gráfico
        plt.plot(15*x,[(dic[j+1][i]-dic[j+1][i+1])/15 for i in x])
        plt.title("Variación de "+title+" de célula "+str(j+1)+" vs tiempo")
        plt.xlabel("tiempo (min)") #nombre de eje x
        if title=="Area":
            plt.ylabel("Variación de área de célula "+str(j+1)+" $((\mu m)^2/min)$ ")  #nombre de eje y
        else:
            plt.ylabel("Variación "+title+" de célula "+str(j+1)+" $(\mu m/min)$ ")  #nombre de eje y
        if save==1:
            plt.savefig("Variacion_de_"+title+"_de_celula_"+str(j+1)) #con esto guardo la imagen
            plt.close()
        elif save==0:
            plt.show()

#creagraficosv(a["Area"],a["nframes"],a["nfig"],"Área")

#función para graficar velocidad (es necesario hacer una solo para velocidad puesto que hay que agregar un elemento a la lista)
def creagraficosvel(dic,nframes,nfig,save=0,size=(8,8)):#poner save=1 si se desean guardar los gráficos
    x=np.array(range(nframes-1))
    for j in range(nfig):
        plt.figure(figsize=size)#tamaño de gráfico
        plt.plot(15*x,[dic[j+1][i] for i in x])
        plt.title("Velocidad de célula "+str(j+1)+" vs tiempo")
        plt.xlabel("tiempo (min)") #nombre de eje x
        plt.ylabel("Velocidad de célula "+str(j+1)+" $(\mu m/min)$ ")  #nombre de eje y
        if save==1:
            plt.savefig("Velocidad_de_celula_"+str(j+1)) #con esto guardo la imagen
            plt.close()
        elif save==0:
            plt.show()

#ejemplo de llamar creagraficosvel
#creagraficosvel(a["spd"],a["nframes"],a["nfig"])

#aquí se hacen las matrices de correlación
#a la funcion le paso una lista con las listas con los datos de los cuales
#quiero sacar correlacion, esta función no funciona si la velocidad está
#involucrada, ver siguiente función
def matrizcorr(a):
    x=np.array(a)
    return np.corrcoef(x)

#ejemplo de llamar matrizcorr
#matrizcorr([a["Area"][1],a["Largo"][1],a["Alto"][1]])


#esta función considera solo dos listas y una de ellas debe ser de velocidad
def matrizcorr2(vel,dim,salto=15):
    #las siguientes 4 lineas agregan un elemento al final de la lista velocidad puesto que esta tiene un elemento menos, el elemento que se agrega se obtiene mediante interpolación de lagrange
    if len(vel)==len(dim)-1:
        vel=agregarunoalfinal(vel,salto)
    elif len(vel)==len(dim)+1:
        dim=agregarunoalfinal(dim,salto)
    elif len(vel)-len(dim)>=2 or len(dim)-len(vel)>=2:
        print("la diferencia de elementos en las listas es mayor a uno")
        return 0
    z=np.array([vel,dim])
    return np.corrcoef(z)[0][1]

#ejemplo de llamar matrizcorr2
#matrizcorr2(a["spd"][1],a["Area"][1])

#la siguiente función agrega un elemento al final de la lista velocidad puesto que esta tiene un elemento menos, el elemento que se agrega se obtiene mediante interpolación de lagrange
def agregarunoalfinal(a,salto):
    n=len(a)
    x=list(range(0,salto*n,salto))
    p=lagrange(x,a)(15*n)
    b=a.copy()
    b.append(p)
    return b

#FUNCIONES PARA ESCRIBIR EN ARCHIVO.TEX
######################################################

def intro(file):
    file.write("En este documento se analizar\\'an videos de movimiento de c\\'elulas cancer\\'igenas, para as\\'i poder contribuir al avance de futuros estudios sobre el c\\'ancer. Para esto se mostrar\\'an gr\\'aficos de \\'area, largo y alto vs tiempo, as\\'i como tambi\\'en se mostrar\\'an gr\\'aficos de variaciones del \\'area, largo y alto a medida que pasa el tiempo, luego se mostrar\\'an correlaciones entre las distintas dimensiones de las c\\'elulas y tambi\\'en correlaciones entre las distintas dimensiones y la velocidad. Adem\\'as se analiza la correlaci\\'on entre el cociente del largo y alto con la velocidad, esto es para ver si es que a medida que las c\\'elulas son m\\'as compactas (o esf\\'ericas) su velocidad aumenta o disminuye, adem\\'as se hace un an\\'alisis sobre la correlaci\\'on entre la distancia recorrida por las c\\'elulas y su \\'area y finalmente se muestran los \\'angulos de las c\\'elulas considerando su posici\\'on final e inicial.\\\\\n")

def basetex(file):
    file.write("\\documentclass[letterpaper,12pt,oneside]{article}\n")
    file.write("\\usepackage{amsmath}\n")
    file.write("\\usepackage{amsfonts}\n")
    file.write("\\usepackage{listings}\n")
    file.write("\\usepackage{amssymb}\n")
    file.write("\\usepackage{graphicx}\n")
    file.write("\\usepackage[utf8]{inputenc}\n")
    file.write("\\usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}\n")
    file.write("\\usepackage[spanish]{babel}    %caracteres en español\n")
    file.write("\\usepackage{blindtext}% es para generar el texto de ejemplo\n")
    file.write("\\usepackage{amsmath,amssymb,amsfonts}  %caracteres matemáticos\n")
    file.write("\\usepackage{hyperref} %referencias a ecuaciones con hipervínculos\n")
    file.write("\\usepackage{fancyhdr} %encabezados y pies de página\n")
    file.write("\\usepackage{multicol,multirow} %unir celdas en tablas\n")
    file.write("\\usepackage{parskip} %quita la sangría (comentar si quieres empezar los parrafos con sangria)\n")
    file.write("\\usepackage{geometry} %margenes y esquemas\n")
    file.write("%EDITAR TÌTULO AQUÍ!!!!!!!!!\n")
    file.write("\\author{Profesor: Rina Ortiz\\\\\n")
    file.write("Nombre: Omar Herrera}\n")
    file.write("\\title{An\\'alisis de movimiento y morfolog\\'ia de c\\'elulas cancer\\'igenas}\n")
    file.write("\\begin{document}\n")
    file.write("\\maketitle\n")

def findoc(file):
    file.write("\\end{document}")

def printimage(file,img,scale=0.4):
    file.write("\\includegraphics[scale="+str(scale)+"]{"+img+"} \n")
    #\begin{center}
    #\includegraphics[scale=0.5]{grafico-nuevo.png}
    #\end{center}

def ancorrim(att1,att2,file,valor):
    if valor>=0.7:
        file.write("Las variables "+att1.lower()+" y "+att2.lower()+" presentan una fuerte relaci\\'on lineal, es decir, si "+att1.lower()+" aumenta entonces tambi\\'en lo har\\'a "+att2.lower()+" con una fuerte asociaci\\'on lineal, esto es debido a que su valor de correlaci\\'on lineal es mayor o igual que $0.7$. El valor de la correlaci\\'on es"+str(valor)+".\\\\\n")
    elif valor<0.7 and valor>=0.3:
        file.write("Las variables "+att1.lower()+" y "+att2.lower()+" presentan poca relaci\\'on lineal, es decir, si "+att1.lower()+" aumenta, entonces "+att2.lower()+" aumenta tambi\\'en lo har\\'a pero con poca asociaci\\'on lineal, esto es debido a que su valor de correlaci\\'on lineal est\\'a entre $0.3$ y $0.7$. El valor de la correlaci\\'on es"+str(valor)+".\\\\\n")
    elif valor<=-0.7:
        file.write("Las variables "+att1.lower()+" y "+att2.lower()+" presentan una fuerte relaci\\'on lineal inversa, es decir, si "+att1.lower()+" aumenta entonces "+att2.lower()+" disminuir\\'a con una fuerte asociaci\\'on lineal, esto es debido a que su valor de correlaci\\'on lineal es menor o igual que $-0.7$. El valor de la correlaci\\'on es"+str(valor)+".\\\\\n")
    elif valor>-0.7 and valor<-0.3:
        file.write("Las variables "+att1.lower()+" y "+att2.lower()+" presentan poca relaci\\'on lineal inversa, es decir, si "+att1.lower()+" aumenta, entonces "+att2.lower()+" disminuir\\'a pero con poca asociaci\\'on lineal con "+att1.lower()+" y viceversa, esto es debido a que su valor de correlaci\\'on lineal esta entre $-0.7$ y $0.3$. El valor de la correlaci\\'on es"+str(valor)+".\\\\\n")
    else:
        file.write("Las variables "+att1.lower()+" y "+att2.lower()+" no presentan relaci\\'on lineal, es decir, si "+att1.lower()+" aumenta, entonces "+att2.lower()+" puede aumentar o disminuir, los comportamientos no se relacionan el uno con el otro, esto es debido a que su valor de correlaci\\'on lineal est\\'a entre $-0.3$ y $0.3$. El valor de la correlaci\\'on es"+str(valor)+".\\\\\n")

def archivotest():
    file=open("informetest.tex",'w')
    basetex(file)
    intro(file)
    findoc(file)
    file.close()

#INTERFAZ GRÁFICA
######################################################

#ventana de instrucciones para un solo archivo
def ventana_instrucciones_uno():
    ventana3=Tk()
    ventana3.title("Instrucciones")
    etiqueta1=Label(ventana3,text="Si usted desea analizar un solo archivo, puede analizarlo primero").place(x=0,y=0)
    etiqueta2=Label(ventana3,text="con el programa de MATLAB, para esto abra el archivo main2.m,").place(x=0,y=20)
    etiqueta3=Label(ventana3,text="y donde sale 'filename= ...;' usted debe poner el nombre del").place(x=0,y=40)
    etiqueta4=Label(ventana3,text="video (.tif) que desea analizar, debe poner el nombre entre comillas").place(x=0,y=60)
    etiqueta5=Label(ventana3,text="y además donde sale 'n_objects=...;' usted puede modificar el").place(x=0,y=80)
    etiqueta6=Label(ventana3,text="número de células a las cuales se les hará seguimiento habiendo").place(x=0,y=100)
    etiqueta7=Label(ventana3,text="hecho esto usted corre el programa y recibirá 2 archivos de texto,").place(x=0,y=120)
    etiqueta8=Label(ventana3,text="terminados en 'boundaries' y 'centroids', luego debe ejecutar").place(x=0,y=140)
    etiqueta9=Label(ventana3,text="este programa y en donde se le pide el archivo de bordes debe poner").place(x=0,y=160)
    etiqueta10=Label(ventana3,text="el nombre del archivo terminado en 'boundaries' y donde se le pide el").place(x=0,y=180)
    etiqueta11=Label(ventana3,text="archivo de centroides usted pone el nombre del archivo terminado").place(x=0,y=200)
    etiqueta12=Label(ventana3,text="en centroids, habiendo hecho esto debe apretar el botón que dice análisis").place(x=0,y=220)
    etiqueta13=Label(ventana3,text="uno y esperar que el programa le genere el archivo .tex y así tener.").place(x=0,y=240)
    etiqueta13=Label(ventana3,text="su informe.").place(x=0,y=260)
    cerrar=Button(ventana3, text="Cerrar", command=ventana3.destroy).place(x=180,y=280)
    ventana3.geometry("400x310")

#ventana de instrucciones total
def ventana_instrucciones_total():
    ventana4=Tk()
    ventana4.title("Instrucciones")
    etiqueta1=Label(ventana4,text="Si usted desea analizar más de un archivo (esto también funciona").place(x=0,y=0)
    etiqueta2=Label(ventana4,text="con un solo archivo), usted debe poner los videos (.tif) a anali_").place(x=0,y=20)
    etiqueta3=Label(ventana4,text="zar en esta misma carpeta.").place(x=0,y=40)
    etiqueta4=Label(ventana4,text="Donde se le pide los segundos para ejecutar, se refiere a cuanto").place(x=0,y=60)
    etiqueta5=Label(ventana4,text="tarda en abrirse MATLAB y ejecutarse, esto depende meramente del").place(x=0,y=80)
    etiqueta6=Label(ventana4,text="computador en que se corra este programa y su capacidad de RAM y ").place(x=0,y=100)
    etiqueta7=Label(ventana4,text="procesamiento, en este sentido es mejor que le sobre tiempo a que").place(x=0,y=120)
    etiqueta8=Label(ventana4,text="le falte, puesto que si le falta tiempo tirará error, por lo que si").place(x=0,y=140)
    etiqueta9=Label(ventana4,text="el programa llega a fallar, pruebe nuevamente poniendo más tiempo.").place(x=0,y=160)
    etiqueta10=Label(ventana4,text="En caso de que el programa halla fallado, borre todos los archivos").place(x=0,y=180)
    etiqueta11=Label(ventana4,text="que se crearon, porque si no a la próxima vez que lo corra, tendrá").place(x=0,y=200)
    etiqueta12=Label(ventana4,text="error o no recibirá los resultados deseados.").place(x=0,y=220)
    cerrar=Button(ventana4, text="Cerrar", command=ventana4.destroy).place(x=175,y=240)
    ventana4.geometry("380x270")

#ventana de finalización
def ventana_fin(n):
    ventana2=Tk()
    ventana2.title("Proceso finalizado")
    if n==1:
        etiqueta=Label(ventana2,text="El informe ha sido creado exitosamente").grid(row=0,column=0)
    elif n==2:
        etiqueta=Label(ventana2,text="Los informes han sido creados exitosamente").grid(row=0,column=0)
    ejecutar=Button(ventana2, text="Cerrar", command=ventana2.destroy).grid(row=1,column=0)
    ventana2.mainloop()

#Ventana:
ventana=Tk()
ventana.title("Análisis de cáncer")

#Variables:
bordesV=StringVar()
centroidesV=StringVar()
segundosV=IntVar()
ncelulasV=IntVar()

#Etiquetas:
etiquetabordes=Label(ventana,text="Ingrese archivo de bordes a analizar").grid(row=0,column=0)
etiquetacentroides=Label(ventana,text="Ingrese archivo de centroides a analizar").grid(row=1,column=0)
etiquetasegundos=Label(ventana,text="Ingrese segundos para ejecutar MATLAB").grid(row=3,column=0)
etiquetafiguras=Label(ventana,text="Ingrese número de células a seguir").grid(row=4,column=0)

#Entradas:
bordesVcaja=Entry(ventana,textvariable=bordesV).grid(row=0,column=1)
centroidesVcaja=Entry(ventana,textvariable=centroidesV).grid(row=1,column=1)
segundosVcaja=Entry(ventana,textvariable=segundosV).grid(row=3,column=1)
ncelulasVcaja=Entry(ventana,textvariable=ncelulasV).grid(row=4,column=1)

#botones:
ejecutaruno=Button(ventana, text="Análisis de uno", command=analisisuno).grid(row=2,column=0)
ejecutartodo=Button(ventana, text="Análisis total", command=analisistotal).grid(row=5,column=0)
instrucciones=Button(ventana, text="instrucciones", command=ventana_instrucciones_uno).grid(row=2,column=1)
instrucciones=Button(ventana, text="instrucciones", command=ventana_instrucciones_total).grid(row=5,column=1)

ventana.mainloop()
