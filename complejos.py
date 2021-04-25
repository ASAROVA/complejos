''' 
Libreria Complejos ASAROVA:

* Esta versión usa 4 notacione y guarda el argumento solo en
  radianes (más eficiente)
* Puede operar con Reales (enteros y flotantes)
* PROBLEMA CORREGIDO al usar rad(): 
  TypeError: rad() missing 1 required positional argument: 'ind'
  (se confundía con la función de radicación y se renombró)
'''     

import math

POLRAD, RECTAN, POLPIR, POLSEX = range(4)
#   0       1       2       3
RAD,    RECT,   PIRAD,  DEG    = range(4)
rad,    rect,   pirad,  deg    = range(4) 
RAD,    RECT,   PIRAD,  SEX    = range(4)
rad,    rect,   pirad,  sex    = range(4) 



class complejo:

    __notacion  = RECTAN
    __precs     = 3

    #__auditor = { int : self.__ }

    def __init__ ( self, coor1 : float,  \
                         coor2 : float,  \
                         modo = RECTAN  ):

        mapa = { bool : self.__constructor, 
                 int  : self.__constructor,
                 str  : self.__deletreador }
        mapa[type(modo)](coor1,coor2,modo)

    def __constructor (self,coor1,coor2,modo):
        if (modo==RECTAN):
            self.__r = coor1
            self.__i = coor2
            self.__actualizar_rectagular()
        elif (modo == POLRAD):
            self.__mod = coor1
            self.__arg = coor2 % (2*math.pi)
            self.__actualizar_polar()
        elif (modo == POLPIR):
            self.__mod = coor1
            self.__arg = (coor2%2)*math.pi
            self.__actualizar_polar()
        elif (modo == POLSEX):
            self.__mod = coor1
            self.__arg = math.radians(coor2%360)
            self.__actualizar_polar()
        else:
            raise ValueError ( "No es una notación válida. Usar \
                                RECTAN, POLRAD, POLPIR, POLSEX" )
        self.__notacion = modo

    def __deletreador (self,coor1,coor2,modo):
        if "rectangulares".startswith(modo):
            self.__constructor(coor1,coor2,RECTAN)
        elif "polares".startswith(modo) or          \
             "radianes".startswith(modo):
            self.__constructor(coor1,coor2,POLRAD)
        elif "sexagesimales".startswith(modo) or   \
             "degrees".startswith(modo):
            self.__constructor(coor1,coor2,POLSEX)
        elif ("piradianes".startswith(modo)) or    \
             ("pi_radianes".startswith(modo)) or   \
             ("p_radianes".startswith(modo)):
            self.__constructor(coor1,coor2,POLPIR)
        else:
            raise ValueError ( "No es una notación válida. Usar \
                                RECTAN, POLRAD, POLPIR, POLSEX" )
 

    def __actualizar_rectagular(self):
        self.__mod = (self.__r**2 + self.__i**2)**.5
        self.__arg = math.atan2(self.__i,self.__r)
    def __actualizar_polar(self):
        self.__r = self.__mod*math.cos(self.__arg)
        self.__i = self.__mod*math.sin(self.__arg)

    def rectangular(self)   : self.__notacion = RECTAN
    def rect(self)          : self.__notacion = RECTAN
    def polar(self)         : self.__notacion = POLRAD
    def radianes(self)      : self.__notacion = POLRAD
    def rad(self)           : self.__notacion = POLRAD
    def sexagesimales(self) : self.__notacion = POLSEX
    def sex(self)           : self.__notacion = POLSEX
    def degrees(self)       : self.__notacion = POLSEX
    def piradianes(self)    : self.__notacion = POLPIR
    def pirad(self)         : self.__notacion = POLPIR
    def rectan(self)        : self.__notacion = RECTAN
    def polrad(self)        : self.__notacion = POLRAD
    def polsex(self)        : self.__notacion = POLSEX
    def polpir(self)        : self.__notacion = POLPIR

    #""" Conjugado ########################
    def conju (self):
        conjugado = complejo(self.__r,-self.__i)
        return conjugado
    ###################################"""#

    #######################################
    #""" Operaciones Matemáticas ##########

    #def __acomplejar(self,y):
    #    return (complejo(y,0))

    def __mul__ (self,y):   # Sobrecarga operador x*y
        if not isinstance(y, complejo): y = complejo(y,0)
        producto = complejo ( self.__r*y.__r - self.__i*y.__i,
                              self.__r*y.__i + self.__i*y.__r  )
        producto.__notacion = self.__notacion
        return producto

    def __truediv__ (self,y):   # Sobrecarga operador x/y
        if not isinstance(y, complejo): y = complejo(y,0)
        cociente = complejo ( self.__mod/y.__mod, 
                              self.__arg-y.__arg, POLRAD )
        cociente.__notacion = self.__notacion
        return cociente

    def __add__ (self,y):   # Sobrecarga operador x+y
        if not isinstance(y, complejo): y = complejo(y,0)
        suma = complejo ( self.__r+y.__r , self.__i+y.__i )
        suma.__notacion = self.__notacion
        return suma

    def __sub__ (self,y):   # Sobrecarga operador x-y
        if not isinstance(y, complejo): y = complejo(y,0)
        diferencia = complejo ( self.__r-y.__r , self.__i-y.__i )
        diferencia.__notacion = self.__notacion
        return diferencia

    def __pow__(self,y:float):
        potencia = complejo (self.__mod**y, self.__arg*y, POLRAD)
        potencia.__notacion = self.__notacion
        return potencia

    def raiz(self,ind:int):
        mod = self.__mod ** (1/ind)
        raiz = [0]*ind
        for k in range(ind) :
            raiz[k] = complejo ( mod,
                                 (self.__arg+2*math.pi*k)/ind,  
                                 POLRAD                         
                               )
            raiz[k].__cambiar_notacion(self.__notacion)
        raiz.__notacion = self.__notacion
        return raiz

    ###################################"""#


    #######################################
    #""" Notacion Selectiva ###############
    def __str__(self):
        cadena = ""
        if (self.__notacion == RECTAN):
            if (self.__r != 0 or self.__i == 0):
                cadena += str (round(self.__r,self.__precs))
            if (self.__i != 0):
                signo_imag = ''
                if self.__i > 0 and self.__r != 0:
                    signo_imag = '+'
                if self.__i < 0:
                    signo_imag = '-'            
                if abs(self.__i) != 1.0:
                    cadena += signo_imag +                             \
                              str(abs(round(self.__i,self.__precs))) + \
                              'j'
                else:
                    cadena += signo_imag + 'j'

        #elif (self.__notacion == POLRAD):
        else:
            mapa =  { POLRAD : (' rad'  , self.__arg),
                      POLPIR : ('π rad' , self.__arg/math.pi),
                      POLSEX : ('°'     , math.degrees(self.__arg)) }

            (unidad,argumento) = mapa[self.__notacion]

            cadena += str(round(self.__mod,self.__precs)) +     \
                      ' ∡ ' +                                   \
                      str(round( argumento,self.__precs)) +     \
                      unidad

        return cadena

    def __repr__(self):
        return self.__str__()
    ###################################"""#


    #######################################
    #""" Mostrar todo #####################
    def mostrar(self):
        notacion_actual = self.__notacion
        for self.__notacion in (1,0,2,3):
            print (self.__str__())
        self.__notacion = notacion_actual
    ###################################"""#



class cmplj     (complejo): pass
class cpj       (complejo): pass
class cj        (complejo): pass
class imag      (complejo): pass
class complex   (complejo): pass
class cmplx     (complejo): pass
class cplx      (complejo): pass
class cpx       (complejo): pass

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& #
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& #


###############################################
""" Pruebas ##################################

print ( complejo( 0,-4) )
print ( complejo( 0, 0) )
print ( complejo( 0, 4) )
print ( complejo(-4, 0) )
print ( complejo( 4, 0) )

print ( )

a = complejo(3,4)
b = a.conju()

a.sexagesimales()
b.degrees()

#a.rad()
#b.rad()

#a.pirad()
#b.pirad()


print()

#a.mostrar()
#b.mostrar()
#print()

print ( "a =", a, "; b =", b, "; a*b =", a*b )
print ( "a =", a, "; b =", b, "; a+b =", a+b )
print ( "a =", a, "; b =", b, "; a-b =", a-b )
print ( "a =", a, "; b =", b, "; a/b =", a/b )
print ( a*3 )
print ( b*4 )

print ()

(a*b).mostrar()

###########################################"""#

""" Pruebas ##################################
a = cpj(3,4)
print(a)

a.rad()
print(a)

b = cmplj(10,2,'rad')
print(b)
b.rect()
print(b)

c = cj(25,270,sex)
print(c)
c.pirad()
print(c)

###########################################"""#