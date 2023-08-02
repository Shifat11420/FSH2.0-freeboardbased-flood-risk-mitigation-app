import numpy as np
def len_wid_bldg(bld_area,aspect_ratio=1.5,aspect="True"):
    if aspect == "True":    
        B = np.sqrt(bld_area/aspect_ratio)
        L = bld_area/B 
        return (B,L)

def slab_on_fill (bld_area,h,aspect_ratio,aspect="True",s=3,a=3,i=0.1,g=0.15,W=0.41,σ=30,t=0.1,D=0.51,h_=0.2):
    B,L =  len_wid_bldg(bld_area,aspect_ratio,aspect)  
    swell_fact = σ/100 
    
    Ar = (L+2*a+2*s*h) * (B+2*a+2*s*h) #rough grade area
    A1 = (L+2*a) * (B+2*a)
    A2 = (L+2*a+2*s*h) * (B+2*a+2*s*h)
    if h<=t+i+g-h_:
        Vf = 0 #fill volume 
        Ve = (2*(L+B+2*i-2*W)*(D-t-i)*(W+2*i)) + ((L+2*i)*(B+2*i)*(t+i+g-h_-h)) #excavation volume                
    if h>t+i+g-h_:
        Vf = ((h/3)*(A1+A2+np.sqrt(A1*A2)) - (L+2*i)*(B+2*i)*(t+i+g-h_))*(1+swell_fact) #fill volume 
        Ve = 2*(L+B+2*i-2*W)*(D-t-i)*(W+2*i)  #excavation volume                
    #Vg = (L*B)*g #volume of gravel
    Ag = L*B #area of gravel            
    Av = (L*B) + 4*(L+B)*D #area of vapour barrier            
    Ai = (L-2*W)*(B-2*W) + 4*(L+B)*(D-h_)  #area of insulation material            
    Vcs = L*B*t #Volume of concrete slab            
    Lcb = 2*(L+B-2*W)  #running length of concrete edge beam
    
    #Costs 
    if Ar<464:
        rough_grading = 1639
    elif Ar>464 and Ar<929:
        rough_grading = 1150
    else:
        rough_grading = 1010
              
    fill = (1.56 + 10.66 + (3.25/1.3)) * Vf
    excavation = 10.67 * Ve
    gravel = Ag * 9.15
    insulation = Ai * 13.78
    vapour_barrier = Av * 2.15
    slab = Vcs * 387.8
    slab_edge = Lcb * 112.47
    total = rough_grading+fill+excavation+gravel+insulation+vapour_barrier+slab_edge+slab
    list1 = []
    list2 = []            
    list1.append([bld_area,aspect_ratio,h,rough_grading,fill,insulation,gravel,excavation,vapour_barrier,slab,slab_edge,total])
    list2.append([bld_area,aspect_ratio,h,Ar,Vf,Ag,Ve,Av,Ai,Vcs,Lcb]) 
    return (round(total,0),list1, list2)
    
def CS1 (bld_area,h,aspect_ratio,aspect="True",i=0.1,g=0.15,W=0.41,σ=30,t=0.1,D=0.51,h_=0.2,w=0.2):
    B,L =  len_wid_bldg(bld_area,aspect_ratio,aspect)  
    swell_fact = σ/100   
    
    Ar = L * B #rough grade area
    if h<i+g:
        Vf = 0 #fill volume 
        Ve = 2*(L+B-2*w)* W * h_ + (L-W)*(B-W)*(i+g-h)#excavation volume                
    if h>i+g:
        Vf = (L-2*w)*(B-2*w)*(h-i-g)*(1+swell_fact) #fill volume 
        Ve = 2*(L+B-2*w)* W * h_ #excavation volume                
    
    Ag = 2* (L+B-2*w)*W + (L-2*w)*(B-2*w) #area of gravel            
    Av = (L*B)  #area of vapour barrier            
    Ai = (L-2*w)*(B-2*w) + 2*(L+B)*(h+h_-D)  #area of insulation material            
    Lcf = 2*(L+B-2*w)
    Am = 2*(L+B)*(h+h_-D)
    Vcs = L*B*t #Volume of concrete slab            
    
    #Costs 
    if Ar<464:
        rough_grading = 1639
    elif Ar>464 and Ar<929:
        rough_grading = 1150
    else:
        rough_grading = 1010
              
    fill = (1.56 + 10.66 + (3.25/1.3)) * Vf
    excavation = 10.67 * Ve
    gravel = Ag * 9.15
    insulation = Ai * 13.78
    vapour_barrier = Av * 2.15
    slab = Vcs * 387.8
    footing = Lcf * 128.38 ##
    if w==0.2:
        cmu = Am * 94.08
    elif w==0.3:
        cmu = Am * 155
    
    total = rough_grading+fill+excavation+gravel+insulation+vapour_barrier+footing+cmu+slab  
    list1 = []
    list2=[]            
    list1.append([bld_area,aspect,h,w,cmu,fill,insulation,gravel,excavation,vapour_barrier,slab,footing,rough_grading,total])
    list2.append([bld_area,aspect,h,w,Am,Vf,Ai,Ag,Ve,Av,Vcs,Lcf,Ar])
    return (round(total,0),list1, list2)

def CS2(bld_area,h,aspect_ratio,aspect="True",C=0.41,P=0.25,W=0.41,t=0.1,D=0.3,h_=0.2,y=3,w=0.2):
    B,L =  len_wid_bldg(bld_area,aspect_ratio,aspect)  

    Nl = round((L/y)-1)
    Nb = round((B/y)-1)
    N = Nl*Nb

    Ar = L * B #rough grade area
    #Vf = (L-2*w)*(B-2*w)*(h+h_-D-i-g)*(1+swell_fact) #fill volume 
    Ve = 2*(L+B-2*w)* W * h_ + N*h_*(C+2*P)**2  #excavation volume                
    Ag = 2* (L+B-2*w)*W + N*(C+2*P)**2 #area of gravel            
    Av = (L-2*w)*(B-2*w) + 2*(L+B-4*w)*h  #area of vapour barrier            
    Ai = (L-2*w)*(B-2*w)   #area of insulation material            
    
    Lm = N*(h+h_-D)
    Lcf = 2*(L+B-2*w)
    Am = 2*(L+B)*(h+h_-D)
    Vcs = L*B*t #Volume of concrete slab            
    
    #Costs 
    if Ar<464:
        rough_grading = 1639
    elif Ar>464 and Ar<929:
        rough_grading = 1150
    else:
        rough_grading = 1010
              
    #fill = (1.56 + 10.66 + (3.25/1.3)) * Vf
    excavation = 10.67 * Ve
    gravel = Ag * 9.15
    insulation = Ai * 13.78
    vapour_barrier = Av * 2.15
    slab = Vcs * 387.8
    
    footing = Lcf* 128.38 ###
    pads =  N * 176
    if w==0.2:
        cmu = Am * 94.08
    elif w==0.3:
        cmu = Am * 155                
    pier = Lm * 165.85
    total = rough_grading+excavation+gravel+insulation+vapour_barrier+pier+cmu+footing+pads+slab
    list1 = []
    list2=[]            
    list1.append([bld_area,aspect,h,w,cmu,pier,insulation,vapour_barrier,gravel,excavation,pads,slab,footing,rough_grading,total])
    list2.append([bld_area,aspect,h,w,Am,Lm,Ai,Av,Ag,Ve,N,Vcs,Lcf,Ar])
    return (round(total,0),list1, list2)
  
def CS3(bld_area,h,aspect_ratio,aspect="True",C=0.41,P=0.25,W=0.41,D=0.3,h_=0.6,y=3,w=0.2,beam_spacing=2.44,joist_spacing=0.41,α_g=0.003319,α_j=0.002729):
    B,L =  len_wid_bldg(bld_area,aspect_ratio,aspect)  
   
    Nl = round((L/y)-1)
    Nb = round((B/y)-1)
    N = Nl*Nb

    Ar = L * B #rough grade area
    Ve = 2*(L+B-2*w)* W * h_ + N*h_*(C+2*P)**2  #excavation volume                
    Ag = 2* (L+B-2*w)*W + N*(C+2*P)**2 #area of gravel            
    Av = (L-2*w)*(B-2*w) + 2*(L+B-4*w)*h  #area of vapour barrier            
    Ai = (L*B)   #area of insulation material            
     
    Lm = N*(h+h_-D)
    Am = 2*(L+B)*(h+h_-D)
    Lcf = 2*(L+B-2*w)
    #Vcs = L*B*t #Volume of concrete slab            
    Nwg = np.ceil((L/beam_spacing)+1)
    Nwj = np.ceil((B/joist_spacing)+1)
    
    Vw = Nwg*B*α_g + Nwj*L*α_j
    Aw = L*B
    #Costs 
    if Ar<464:
        rough_grading = 1639
    elif Ar>464 and Ar<929:
        rough_grading = 1150
    else:
        rough_grading = 1010
              
    #fill = (1.56 + 10.66 + (3.25/1.3)) * Vf
    excavation = 10.67 * Ve
    gravel = Ag * 9.15
    insulation = Ai * (23.9+16.9) 
    vapour_barrier = Av * 2.15               
    footing = Lcf* 128.38    ##
    pads =  N * 176
    if w==0.2:
        cmu = Am * 94.08
    elif w==0.3:
        cmu = Am * 155  
    pier = Lm * 165.85
    #slab = Vcs * 387.8
    wood = Vw * 1769.07
    subfloor = Aw * 17.87
    total = rough_grading+excavation+gravel+insulation+vapour_barrier+pier+cmu+footing+pads+wood+subfloor
    list1 = []
    list2=[]
    list1.append([bld_area,aspect,h,w,cmu,pier,vapour_barrier,insulation,gravel,excavation,pads,wood,footing,rough_grading,subfloor,total])
    list2.append([bld_area,aspect,h,w,Am,Lm,Av,Ai,Ag,Ve,N,Vw,Lcf,Ar,Aw])
    return (round(total,0),list1, list2)


def CS4(bld_area,h,aspect_ratio,aspect="True",C=0.41,P=0.25,W=0.41,D=0.3,h_=0.6,y=3,beam_spacing=2.44,joist_spacing=0.41,α_g=0.003319,α_j=0.002729):
    B,L =  len_wid_bldg(bld_area,aspect_ratio,aspect)  
             
    Nl = round((L/y)+1)
    Nb = round((B/y)+1)
    N = Nl*Nb

    Ar = L * B #rough grade area
    Ve =  N*h_*(C+2*P)**2  #excavation volume                
    Ag =  N*(C+2*P)**2 #area of gravel            
    Ai = (L*B)   #area of insulation material            
    
    
    Lm = N*(h+h_-D)
    Nwg = np.ceil((L/beam_spacing)+1)
    Nwj = np.ceil((B/joist_spacing)+1)
    
    Vw = Nwg*B*α_g + Nwj*L*α_j
    Aw = L*B
    #Costs 
    if Ar<464:
        rough_grading = 1639
    elif Ar>464 and Ar<929:
        rough_grading = 1150
    else:
        rough_grading = 1010
              
    #fill = (1.56 + 10.66 + (3.25/1.3)) * Vf
    excavation = 10.67 * Ve
    gravel = Ag * 9.15
    insulation = Ai * (23.9+16.9)
    #vapour_barrier = Av * 2.15           
    pads =  N * 176 # Lcf* 39.13  ##
    # if w==0.2:
    #     cmu = Am * 94.08
    # elif w==0.3:
    #     cmu = Am * 155  
    pier = Lm * 165.85
    wood = Vw * 1769.07
    subfloor = Aw * 17.87
    total = rough_grading+excavation+gravel+insulation+pier+pads+wood+subfloor
    list1 = []
    list2=[]
    list1.append([bld_area,aspect,h,pier,excavation,rough_grading,gravel,insulation,pads,wood,subfloor,total])
    list2.append([bld_area,aspect,h,Lm,Ve,Ar,Ag,Ai,N,Vw,Aw])
    return (round(total,0),list1, list2)
