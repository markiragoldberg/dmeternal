#  *******************
#  ***   ANCHORS   ***
#  *******************
# Each anchor function takes two rect: a parent and a child.
# The child is arranged relative to the parent.

def northwest(par,chi):
    chi.topleft = par.topleft

def north( par,chi ):
    chi.midtop = par.midtop

def northeast(par,chi):
    chi.topright = par.topright

def west(par,chi):
    chi.midleft = par.midleft

def middle( par,chi):
    chi.center = par.center

def east(par,chi):
    chi.midright = par.midright

def southwest(par,chi):
    chi.bottomleft = par.bottomleft

def south( par,chi ):
    chi.midbottom = par.midbottom

def southeast(par,chi):
    chi.bottomright = par.bottomright

