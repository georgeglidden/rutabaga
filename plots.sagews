︠dbaacc76-c03e-44df-89fb-7529b94a4139s︠
x=var('x')

BD = load('Q polynomials with roots')  #denominators less than 131.
︡cd4f6a7b-acee-463f-9572-4dc7efc4b9f5︡{"stderr":"Error in lines 2-2\n"}︡{"stderr":"Traceback (most recent call last):\n  File \"/cocalc/lib/python2.7/site-packages/smc_sagews/sage_server.py\", line 1230, in execute\n    exec(\n  File \"\", line 1, in <module>\n  File \"/cocalc/lib/python2.7/site-packages/smc_sagews/sage_salvus.py\", line 3919, in load\n    exec(\n  File \"<string>\", line 1, in <module>\n  File \"sage/misc/persist.pyx\", line 157, in sage.misc.persist.load (build/cythonized/sage/misc/persist.c:2920)\n    with open(filename, 'rb') as fobj:\n  File \"sage/misc/persist.pyx\", line 158, in sage.misc.persist.load (build/cythonized/sage/misc/persist.c:2870)\n    X = loads(fobj.read(), compress=compress, **kwargs)\n  File \"sage/misc/persist.pyx\", line 935, in sage.misc.persist.loads (build/cythonized/sage/misc/persist.c:7537)\n    return unpickler.load()\n  File \"sage/symbolic/expression.pyx\", line 752, in sage.symbolic.expression.Expression.__setstate__ (build/cythonized/sage/symbolic/expression.cpp:6941)\n    self._gobj = GEx(ar.unarchive_ex(sym_lst, <unsigned>0))\nRuntimeError: archive node contains no class name\n"}︡{"done":true}
︠6d45bf2b-3829-48c6-85c0-8abf97d435d5s︠
def Q(pair):
    p=pair[0]
    q=pair[1]
    return BD[q][p][1]

def rt(pair):
    p=pair[0]
    q=pair[1]
    return BD[q][p][2]
︡4f69e116-2cda-47bf-86fd-daa3efd4b6c7︡{"done":true}
︠3ccc15a9-4c25-4f3c-9d65-a866e96ed5c1s︠
def corner(c): # Left and right corners of Triangle(c)
    p, q, left, right, s = c[0], c[1], x, x, 1
    while left==x or right==x: 
        if left==x and  ((p*s-1)%q)==0:  left=vector([(p*s-1)/q,s])
        if right==x and ((p*s+1)%q)==0:  right=vector([(p*s+1)/q,s])
        s+=1
    return [left, right]

def lowcorner(c):
    pair=corner(c)
    if pair[0][1]<pair[1][1]: return pair[1]
    else: return pair[0]

def center(c):
    pair=corner(c)
    if pair[0][1]>pair[1][1]: return pair[1]
    else: return pair[0]
    
def deeper_vtx(c,n):
    cen=vector(center(c))
    return vector(c)+n*cen

def dQ(r): return (-1)^r[0]*x^r[1]

def DiscQ(r): return Q(r)^2-4*dQ(r)

def quot(r): return r[0]/r[1]

def list_product(L):
    return reduce(lambda x, y: x*y, L)

def zeta(j,z):
    if j==1: return 1/(1-z)
    else: return (z-1)/z

def fedges(r):  #computes the 'horizontal' edges of the funnel F(r).
    r=vector(r)
    rr=quot(r)
    edges=[map(vector,[[0,1],[1,1]])]
    e=map(vector,[[0,1],[1,1]])
    mid=sum(e)
    while mid!=r:
        if rr<quot(mid): 
            edges.append([e[0],mid])
        else:
            edges.append([mid,e[1]])
        e=edges[-1]
        mid=sum(e)
    return edges

def edgeslope(e):   #evaluates the sign of the slope of an edge e
    if e[1][1]<e[0][1]: return 1
    else: return -1

def sfunctions(r):  #computes the list of shape functions for r
    edges=fedges(r)[1:-1]
    dets=[dQ(e[(edgeslope(e)+1)/2])^(-edgeslope(e)) for e in edges ]
    FL=[((Q(edges[j][0])/Q(edges[j][1]))^2*list_product(dets[:j+1])).factor() for j in range(len(edges)) ]
    return FL

def Z(r,j): #the jth shape function
    return sfunctions(deeper_vtx(r,5))[j-1]

def num_tetrahedra(r): return len(fedges(r))-2
︡346f2227-6a93-4332-90ae-d4ef031ff048︡{"done":true}
︠d92d1a40-aefb-4b37-a7fe-34801597e583s︠
def coor(z): return (z.real(), z.imag())

def num_list(q): return [p for p in range(2,floor(q/2)+1) if gcd(p,q)==1]

def sageit(r):
    sageroot=sage_eval(str(r))
    return sageroot
︡117293a5-2a82-432c-992a-3286d55b839a︡{"done":true}
︠4d0b7ad4-0036-430a-a73f-eca5ac27928cs︠
show(sum([sum([line(map(lambda verts: coor(rt(verts)), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in [[p,q] for p in num_list(q)]]) for q in range(6,101)])+
     sum([point(map(lambda pair: coor(rt(pair)), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(6,101)])+
     point(map(coor, [(1/4)*sec(pi/n)^2 for n in range(3,30)]), size=1, color='red', zorder=10)+
     line([[1,0],[1/4,0]], thickness=.3, color='orange')+line([[1,0],coor(rt([2,5]))], thickness=.3, color='orange')+
     arc((0,0), 1, sector=(0,pi/2),thickness=.3, color='red')+
     arc((0,0), 1/4, sector=(0,pi/2),thickness=.3, color='red')
     , aspect_ratio=1, figsize=5, axes=False)
︡e73278aa-1c84-45f1-b19a-8cbd19124b1b︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/6495/tmp_rCXPXc.svg","show":true,"text":null,"uuid":"f6d5e0be-7672-4dba-b053-bdbae5ac8fe4"},"once":false}︡{"done":true}
︠01f46559-0e0a-49cc-b23a-0ec52fc71181s︠
show(sum([sum([line(map(lambda verts: coor(gp.subst(Z(verts,2),x,rt(verts)) ), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in filter(lambda pair: num_tetrahedra(pair)>1,[[p,q] for p in num_list(q)])]) for q in range(7,101)])+
     sum([point(map(lambda pair: coor(gp.subst(Z(pair,2),x,rt(pair))), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(6,101)])+
     arc((0,0), 1/9, sector=(0,pi/2),thickness=.3, color='red')+
     line([(1,0),(0,0),(0,1.5),(2,1.5)], thickness=.3, color='red')
     #point(map(coor, [(1/4)*sec(pi/n)^2 for n in range(3,30)]), size=1, color='red', zorder=10)+
     #line([[1,0],[1/4,0]], thickness=.3, color='orange')+line([[1,0],coor(rt([2,5]))], thickness=.3, color='orange')+
     , aspect_ratio=1, figsize=15, axes=False)
︡0a79cb44-2e6f-4d6c-8f32-30873b3f9198︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_Wt6goR.svg","show":true,"text":null,"uuid":"039a5ed3-85c6-41b2-8850-afcbb8426431"},"once":false}︡{"done":true}
︠6c19577a-70a9-41a9-9bb2-69d84cf3a8c8s︠
show(sum([sum([line(map(lambda verts: coor(gp.subst(Z(verts,3),x,rt(verts)) ), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in filter(lambda pair: num_tetrahedra(pair)>2,[[p,q] for p in num_list(q)])]) for q in range(7,101)])+
     sum([point(map(lambda pair: coor(gp.subst(Z(pair,3),x,rt(pair))), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(6,101)])+
     arc((0,0), 1/16, sector=(0,pi/2),thickness=.3, color='red')+
     line([(1,0),(0,0),(0,5/2),(6,5/2)], thickness=.3, color='red')
     #point(map(coor, [(1/4)*sec(pi/n)^2 for n in range(3,30)]), size=1, color='red', zorder=10)+
     #line([[1,0],[1/4,0]], thickness=.3, color='orange')+line([[1,0],coor(rt([2,5]))], thickness=.3, color='orange')+
     , aspect_ratio=1, figsize=15, axes=False)
︡b3a10513-b53b-4720-b47a-f52f9a330688︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_vbiSgL.svg","show":true,"text":null,"uuid":"5c576c52-6ef9-4eda-93a1-f85a9f04c283"},"once":false}︡{"done":true}
︠89037ca7-e83d-4b46-adf0-4fe2e08010cas︠
dlist=[]
for q in range(6,101):
    for p in num_list(q):
        dlist.append(gp.subst(dQ(center([p,q])),x,rt([p,q])))
︡45954eff-a276-488e-8934-f427cb37a8d2︡{"done":true}
︠06beed27-6bb5-4b63-9fc3-71c6f118c0e1s︠
show(#sum([sum([line(map(lambda verts: coor(rt(verts)), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in [[p,q] for p in num_list(q)]]) for q in range(6,101)])+
     point(map(coor, dlist), size=1)+
     point(map(coor, [(1/4)*sec(pi/n)^2 for n in range(3,30)]), size=1, color='red', zorder=10)+
     line([[0,-1/4],[0,0],[1/4,0]], thickness=.3, color='red')+#line([[1,0],coor(rt([2,5]))], thickness=.3, color='orange')+
     #arc((0,0), 1, sector=(0,pi/2),thickness=.3, color='red')+
     arc((0,0), 1/4, sector=(0,-pi/2),thickness=.3, color='red')
     , aspect_ratio=1, figsize=15, axes=False)
︡8c76d33c-0466-4d87-88de-bfb573b8e09d︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_qJGHKd.svg","show":true,"text":null,"uuid":"2129995b-854a-4787-a0d2-21e57a82d937"},"once":false}︡{"done":true}
︠016e515e-a070-4b1c-b5ea-df228bdb99c0s︠
show(
     point(map(coor, filter(lambda d: gp.abs(d)<1/8,dlist)), size=1)+
     line([[0,-1/8],[0,0],[1/8,0]], thickness=.3, color='red')
     , aspect_ratio=1, figsize=5, axes=False)
︡baea251c-b794-46d0-b310-768967f0791f︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_O9kiXt.svg","show":true,"text":null,"uuid":"66284e3c-9987-455e-b23c-3121b5dfbf40"},"once":false}︡{"done":true}
︠74bac202-fdc2-44cd-aa8f-b79c6fd20363s︠
show(
     point(map(coor, filter(lambda d: gp.abs(d)<1/64,dlist)), size=1)+
     line([[0,-1/64],[0,0],[1/64,0]], thickness=.3, color='red')
     , aspect_ratio=1, figsize=5, axes=False)
︡19c6acb4-0c65-443f-a655-7405e4502589︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_UAQVIc.svg","show":true,"text":null,"uuid":"7a04c641-0c5a-4b75-9083-55c77f284b03"},"once":false}︡{"done":true}
︠7045404a-bdcd-4d4e-beeb-6fd1c272a3c7s︠
def lam_plus(r):
    return (1/2)*(Q(center(r))+sqrt(DiscQ(center(r))))

def lam_minus(r):
    return (1/2)*(Q(center(r))-sqrt(DiscQ(center(r))))

def lam_rat(r):
    return lam_plus(r)/lam_minus(r)
︡83bb8ca9-de49-4cc8-8e1a-1c5a4597c146︡{"done":true}
︠8ed80ade-f802-4c49-a776-3f3c12403f3cs︠
show(#sum([sum([line(map(lambda verts: coor(lam_rat(verts).substitute(x=sageit(rt(verts))) ), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in filter(lambda pair: num_tetrahedra(pair)>1,[[p,q] for p in num_list(q)])]) for q in range(7,50)])+
     sum([point(map(lambda pair: coor(lam_rat(pair).substitute(x=sageit(rt(pair)))), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(6,55)])+
     arc((0,0), 1, sector=(0,pi/2),thickness=.3, color='red')
     , aspect_ratio=1, figsize=5, axes=False)
︡77cafcf2-5ece-4c3f-8ed9-3612814bef6a︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_sJfDv8.svg","show":true,"text":null,"uuid":"a2df2038-c11e-47ae-a9d5-9e0157d9165e"},"once":false}︡{"done":true}
︠12800c1e-423a-43fc-bf3b-0589e1ef00d2s︠
def qcoor(z):
    return map(lambda t: gp.abs(t), coor(z))
︡b9b1f50a-ff23-4745-8d91-b337cbc544d6︡{"done":true}
︠1ab1fa40-7d8f-4863-a7dc-abbd455349c2s︠
show(#sum([sum([line(map(lambda verts: qcoor(log(lam_rat(verts).substitute(x=sageit(rt(verts)))) ), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in filter(lambda pair: num_tetrahedra(pair)>1,[[p,q] for p in num_list(q)])]) for q in range(7,50)])+
     sum([point(map(lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(6,55)])+
     line([[0,2.5],[0,0],[1,0]], thickness=.3, color='red')
     , aspect_ratio=1, figsize=5, axes=False)
︡053bb0dc-9e9f-4fb6-8ad9-677e9907c29d︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_EgIrtu.svg","show":true,"text":null,"uuid":"94656239-5f59-40ef-9f65-88fd92b2c985"},"once":false}︡{"done":true}
︠11e404bf-7716-4488-af39-3a3db846d646s︠
show(#sum([sum([line(map(lambda verts: qcoor(log(lam_rat(verts).substitute(x=sageit(rt(verts)))) ), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in filter(lambda pair: num_tetrahedra(pair)>1,[[p,q] for p in num_list(q)])]) for q in range(7,50)])+
     sum([point(map(lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(5,55)])+
     line([[0,2.5],[0,0],[1,0]], thickness=.3, color='red')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [n*vector([1,2])+vector([2,5]) for n in range(10)] ), thickness=.3, color='orange')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [n*vector([1,3])+vector([2,7]) for n in range(10)] ), thickness=.3, color='orange')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[2,n] for n in range(5,15)] )), thickness=.3, color='green')#+
     #line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[3,n] for n in range(7,35)] )), thickness=.3, color='green')
     , aspect_ratio=1, figsize=8, axes=False)
︡13ae45b2-1010-4eba-8cab-ce36b731c393︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_lijKex.svg","show":true,"text":null,"uuid":"6a6c54d2-4212-4cfc-9e71-4284d1ae0e74"},"once":false}︡{"done":true}
︠080ac070-97c1-421d-9bb7-e451e149012ds︠
show(#sum([sum([line(map(lambda verts: qcoor(log(lam_rat(verts).substitute(x=sageit(rt(verts)))) ), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in filter(lambda pair: num_tetrahedra(pair)>1,[[p,q] for p in num_list(q)])]) for q in range(7,50)])+
     sum([point(map(lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(5,55)])+
     line([[0,2.5],[0,0],[1,0]], thickness=.3, color='red')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [n*vector([1,2])+vector([2,5]) for n in range(10)] ), thickness=.3, color='orange')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [n*vector([1,3])+vector([2,7]) for n in range(10)] ), thickness=.3, color='orange')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[2,n] for n in range(5,15)] )), thickness=.3, color='green')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[3,n] for n in range(7,35,3)] )), thickness=.3, color='red')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[3,n] for n in range(8,35,3)] )), thickness=.3, color='black')
     , aspect_ratio=1, figsize=5, axes=False)
︡f13ebd91-d9fa-4612-af40-a869e045954b︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_HOBW4e.svg","show":true,"text":null,"uuid":"da935513-7c84-47dd-aac5-48d4c80cd072"},"once":false}︡{"done":true}
︠69a8d682-4d5d-4651-a0b1-c8478104d03es︠
show(#sum([sum([line(map(lambda verts: qcoor(log(lam_rat(verts).substitute(x=sageit(rt(verts)))) ), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in filter(lambda pair: num_tetrahedra(pair)>1,[[p,q] for p in num_list(q)])]) for q in range(7,50)])+
     sum([point(map(lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(5,55)])+
     line([[0,2.5],[0,0],[1,0]], thickness=.3, color='red')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [n*vector([1,2])+vector([2,5]) for n in range(10)] ), thickness=.3, color='orange')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [n*vector([1,3])+vector([2,7]) for n in range(10)] ), thickness=.3, color='orange')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[2,n] for n in range(5,15)] )), thickness=.3, color='green')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[3,n] for n in range(7,35,3)] )), thickness=.3, color='red')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[3,n] for n in range(8,35,3)] )), thickness=.3, color='black')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[4,n] for n in range(9,35,4)] )), thickness=.3, color='green')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[4,n] for n in range(11,35,4)] )), thickness=.3, color='red')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(11,50,5)] )), thickness=.3, color='green')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(12,50,5)] )), thickness=.3, color='red')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(13,50,5)] )), thickness=.3, color='black')+
     line(map( lambda pair: coor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(14,50,5)] )), thickness=.3, color='orange')
     , aspect_ratio=1, figsize=8, axes=False)
︡d56bdf29-4d6c-428f-9f7b-13abea19df89︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_oKRQ96.svg","show":true,"text":null,"uuid":"a2390596-0f13-48a7-83de-44e17d36e62e"},"once":false}︡{"done":true}
︠ff5c1f68-7bdc-4039-81ac-a9340f2a296ds︠
show(#sum([sum([line(map(lambda verts: qcoor(log(lam_rat(verts).substitute(x=sageit(rt(verts)))) ), [pair,lowcorner(pair)]), thickness=.3, color='orange') for pair in filter(lambda pair: num_tetrahedra(pair)>1,[[p,q] for p in num_list(q)])]) for q in range(7,50)])+
     sum([point(map(lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(5,55)])+
     line([[0,2.5],[0,0],[1,0]], thickness=.3, color='red')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [n*vector([1,2])+vector([2,5]) for n in range(10)] ), thickness=.3, color='orange')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [n*vector([1,3])+vector([2,7]) for n in range(10)] ), thickness=.3, color='orange')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[2,n] for n in range(5,15)] )), thickness=.3, color='green')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[3,n] for n in range(7,35,3)] )), thickness=.3, color='red')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[3,n] for n in range(8,35,3)] )), thickness=.3, color='black')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[4,n] for n in range(9,35,4)] )), thickness=.3, color='green')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[4,n] for n in range(11,35,4)] )), thickness=.3, color='red')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(11,50,5)] )), thickness=.3, color='green')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(12,50,5)] )), thickness=.3, color='red')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(13,50,5)] )), thickness=.3, color='black')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(14,50,5)] )), thickness=.3, color='orange')
     , aspect_ratio=1, figsize=15, axes=False)
︡4cf6526f-fc6e-4864-942f-1fd830c212d3︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_aFFgCE.svg","show":true,"text":null,"uuid":"73809748-aca8-4253-8bbf-fc627e3c1fa2"},"once":false}︡{"done":true}
︠29e1d10e-a2e7-4278-85b8-276e0470346bs︠
show(sum([point(map(lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), [[p,q] for p in num_list(q)] ), size=1, zorder=10^50) for q in range(5,55)])+
     line([[0,2.5],[0,0],[1,0]], thickness=.3, color='red')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[2,n] for n in range(5,15)] )), thickness=.3, color='green')+
     line([qcoor(log(lam_rat([1,3]).substitute(x=N((1/4)*sec(pi/3)^2)))),qcoor(log(lam_rat([2,5]).substitute(x=sageit(rt([2,5]))))) ], thickness=.3, color='green')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[3,n] for n in range(7,35,3)] )), thickness=.3, color='green')+
     line([qcoor(log(lam_rat([1,4]).substitute(x=N((1/4)*sec(pi/4)^2)))),qcoor(log(lam_rat([3,7]).substitute(x=sageit(rt([3,7]))))) ], thickness=.3, color='green')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[3,n] for n in range(8,35,3)] )), thickness=.3, color='black')+
          line([qcoor(log(lam_rat([2,5]).substitute(x=sageit(rt([2,5]))))),qcoor(log(lam_rat([3,8]).substitute(x=sageit(rt([3,8]))))) ], thickness=.3, color='black')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[4,n] for n in range(9,35,4)] )), thickness=.3, color='green')+
     line([qcoor(log(lam_rat([1,5]).substitute(x=N((1/4)*sec(pi/5)^2)))),qcoor(log(lam_rat([4,9]).substitute(x=sageit(rt([4,9]))))) ], thickness=.3, color='green')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[4,n] for n in range(11,35,4)] )), thickness=.3, color='black')+
     line([qcoor(log(lam_rat([3,7]).substitute(x=sageit(rt([3,7]))))),qcoor(log(lam_rat([4,11]).substitute(x=sageit(rt([4,11]))))) ], thickness=.3, color='black')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(11,50,5)] )), thickness=.3, color='green')+
     line([qcoor(log(lam_rat([1,6]).substitute(x=N((1/4)*sec(pi/6)^2)))),qcoor(log(lam_rat([5,11]).substitute(x=sageit(rt([5,11]))))) ], thickness=.3, color='green')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(12,50,5)] )), thickness=.3, color='red')+
     line([qcoor(log(lam_rat([2,7]).substitute(x=sageit(rt([2,7]))))),qcoor(log(lam_rat([5,12]).substitute(x=sageit(rt([5,12]))))) ], thickness=.3, color='red')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(13,50,5)] )), thickness=.3, color='green')+
     line([qcoor(log(lam_rat([3,8]).substitute(x=sageit(rt([3,8]))))),qcoor(log(lam_rat([5,13]).substitute(x=sageit(rt([5,13]))))) ], thickness=.3, color='green')+
     line(map( lambda pair: qcoor(log(lam_rat(pair).substitute(x=sageit(rt(pair))))), filter(lambda p: gcd(p[0],p[1])==1,[[5,n] for n in range(14,50,5)] )), thickness=.3, color='black')+
     line([qcoor(log(lam_rat([4,9]).substitute(x=sageit(rt([4,9]))))),qcoor(log(lam_rat([5,14]).substitute(x=sageit(rt([5,14]))))) ], thickness=.3, color='black')+
     point([qcoor(log(lam_rat([1,n]).substitute(x=N((1/4)*sec(pi/n)^2)))) for n in range(3,10)], size=2)
     , aspect_ratio=1, figsize=15, axes=False)
︡e411da60-b956-4501-95ca-0780eb9e7f7a︡{"file":{"filename":"/home/user/.sage/temp/project-e727d561-07a1-4b80-9f4a-b481a2e97025/227/tmp_4v9xiW.svg","show":true,"text":null,"uuid":"47419f80-c7cd-4ad9-9641-c7d71d7fd39a"},"once":false}︡{"done":true}
︠511897d7-11e4-464c-bcb2-304628343eac︠
︠96852336-2b0e-4617-b435-ec706a8d221a︠









