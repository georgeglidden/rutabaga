#####################################################
# Independent functions
#####################################################

def q_to_v(r):   #Convert a rational number to a vector [p,q]
    return [r.numerator(), r.denominator()]

def fib_fn(M,seed):  # Fibonacci function given by the matrix M and the first two values 'seed'.
    return lambda j: (M^(j-1)*seed)[0,0]


def calF(a,b,c,d):   # Fibonnacci function given by M=[[0,1],[a,b]] and seed = [c,d]
    return fib_fn(matrix([[0,1],[a,b]]), matrix([[c],[d]]))

def row_simplify(R):  # Simplifys the entries of a row
    return list(map(lambda v: v.full_simplify(), R))

def mtx_simplify(X):  # Simplifys the entries of a matrix
    return matrix(list(map(row_simplify, X)))

def nfactor(f):
    if f.full_simplify()==0:
        return 0
    else:
        return f.factor()

def row_factor(R): # Factors the entries of a row
    return list(map(nfactor, R))
    #return list(map(lambda v: v.factor(), R))

def mtx_factor(X): # Factors the entries of a matrix
    return matrix(list(map(row_factor, X)))

def mtx_inv(X): #Inverts an element of (P)SL_2
    return matrix([[X[1,1],-X[0,1]],[-X[1,0],X[0,0]]])

def mobX(X,z):
    if z=='inf': 
        if X[1,0]==0: return 'inf'
        else: return X[0,0]/X[1,0]
    else: 
        if (X[1,0]*z+X[1,1])==0: return 'inf'
        else: return (X[0,0]*z+X[0,1])/(X[1,0]*z+X[1,1])

def polydet(PL):  #Finds first fib coordinates for a list of 4 recursion polys
    return ((PL[2]^2-PL[3]*PL[1])/(PL[1]^2-PL[2]*PL[0])).factor()

def recursion(PL):  #Finds second fib coordinates for a list of 4 recursion polys
    return ((PL[2]+polydet(PL)*PL[0])/PL[1]).factor()

def fibcoors(PL):
    return [-polydet(PL), recursion(PL)]

def Pfibfunction(PL):
    return calF(fibcoors(PL)[0], fibcoors(PL)[1], PL[0], PL[1])

def gen_fn(p,q,f0,f1):
    return (f0*(1-t*q)+t*f1)/(1-p*t^2-t*q)

def Pgen_fn(PL):
    return gen_fn(fibcoors(PL)[0], fibcoors(PL)[1], PL[0], PL[1])

def ndifft(f,n):
    nf=f
    for j in range(n):
        nf=nf.diff(t)
    return nf

def generatepolys(g,n):
    return [ndifft(g,j).substitute(t=0)/factorial(j) for j in range(n)]

#####################################################
# Classes
#####################################################

class PZ:
    def __init__(self, v):
        self.p = v[0]
        self.q = v[1]
        self.description = "The point ", [self.p,self.q], "in P^1 Z"

    def SBcoor(self): # The Stern-Brocot coordinate for self
        return [self.p/self.q, 1/self.q]

    def v(self):   # self as a vector
        return vector([self.p, self.q])

    def __add__(self, other):  # Farey sum
        return PZ(self.v()+other.v())

    def __spin__(self,other,n):  #'self' Farey summed with 'other' n times
        return PZ(self.v()+n*other.v())

#Eg: bound=[PZ([1,2]).__spin__(PZ([3,7]),n) for n in range(20)]

    def rat(self): # Rational representation
        return self.v()[0]/self.v()[1]

    def cf_list(self): # Continued fraction
        return list(self.rat().continued_fraction())

    def parent(self): # Parent in the Stern-Brocot tree
        L=self.cf_list()
        L[-1]=L[-1]-1
        return PZ(q_to_v(continued_fraction(L).value()))

    def children(self): # Children in the Stern-Brocot tree
        L1=self.cf_list()
        L2=self.cf_list()
        L1[-1]=L1[-1]+1
        L2[-1]=L2[-1]-1
        L2.append(2)
        return sorted(list(map(lambda f: PZ(q_to_v(continued_fraction(f).value())), [L1,L2]), key=lambda g: g.rat()))

    def corners(self): # Left and right corners of Triangle(c)
        left, right, t = 1, 1, 1
        while left==1 or right==1:
            if left==1 and  ((self.p*t-1)%self.q)==0:  left=PZ([(self.p*t-1)/self.q,t])
            if right==1 and ((self.p*t+1)%self.q)==0:  right=PZ([(self.p*t+1)/self.q,t])
            t+=1
        return [left, right]

    def triangle_data(self): # [corner, center, index] for the two triangles that have self as a side vertex. Doesn't work if r[0]=1?
        c=self.corners()
        k=list(map(lambda f: f.corners(),c))
        corner_center=[[k[0][1],c[0]], [k[1][0],c[1]]]
        return list(map(lambda f: f+[(self.p-f[0].p)/f[1].p], corner_center))

    def index_triangle(self): # Triangle data for self which has index > 1.
        if self.p==1: return [PZ([1,0]),PZ([0,1]),self.q]
        for t in self.triangle_data():
            if t[2]>1: return t

    def act(self,X):
        return PZ(X*self.v())

#####################################################

class FareyFunction:   # The Farey recursive function for a quad (d, x, y, z)
    def __init__(self, det, zero, infinity, one):
        self.det = det
        self.zero = zero
        self.inf = infinity
        self.one = one
        self.description = "The Farey recursive function for a quad (d, x, y, z)"

    def eval(self, r):  # evaluate the Farey function at a vertex r
        if r.v()==vector([0,1]): return self.zero
        elif r.v()==vector([1,0]): return self.inf
        elif r.v()==vector([1,1]): return self.one
        else:
            t=r.index_triangle()
            k=t[0]
            c=t[1]
            ind=t[2]
            return calF(-(self.det)(c), self.eval(c), self.eval(k), self.eval(k+c))(ind+1)

    def discrim(self, r):  # evaluate the discriminant at a vertex r
        return self.eval(r)^2-4*(self.det)(r)

    def factored(self,r): # evaluates and factors the Farey function at a vertex r
        return self.eval(r).factor()

    def factored_disc(self,r): # evaluates and factors the discriminant at a vertex r
        return self.discrim(r).factor()

#####################################################

class FareyFunction2:   # The Farey recursive function for a quad (d, x, y, z)
    def __init__(self, det, d2, zero, infinity, one):
        self.det = det
        self.d2 =d2
        self.zero = zero
        self.inf = infinity
        self.one = one
        self.description = "The Farey recursive function for a quad (d, x, y, z)"

    def eval(self, r):  # evaluate the Farey function at a vertex r
        if r.v()==vector([0,1]): return self.zero
        elif r.v()==vector([1,0]): return self.inf
        elif r.v()==vector([1,1]): return self.one
        else:
            t=r.index_triangle()
            k=t[0]
            c=t[1]
            ind=t[2]
            return calF(-(self.det)(c), self.d2(c), self.eval(k), self.eval(k+c))(ind+1)

    def discrim(self, r):  # evaluate the discriminant at a vertex r
        return self.eval(r)^2-4*(self.det)(r)

    def factored(self,r): # evaluates and factors the Farey function at a vertex r
        return self.eval(r).factor()

    def factored_disc(self,r): # evaluates and factors the discriminant at a vertex r
        return self.discrim(r).factor()

#####################################################

def cleanpair(p):
    r=p[0]/p[1]
    return PZ([r.numerator(), r.denominator()])

def fractionline(n):   #fractions in (0,1/2) with denominator n.  Note that Q([q-p,q])=Q([p,q]).substitute(x=-x)
    n=Integer(n)
    top=(n/2).ceil()
    L=[cleanpair([j,n]) for j in range(1,top) ]
    return list(filter(lambda r: r.q==n ,L))

def longfractionline(n):   #fractions in (0,1) with denominator n.
    n=Integer(n)
    L=[cleanpair([j,n]) for j in range(1,n) ]
    return list(filter(lambda r: r.q==n ,L))
