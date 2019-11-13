from ipywidgets import widgets 
from ipywidgets import Layout, HBox, VBox
from IPython.display import display

with open('input.txt','w') as file:
    file.write('')

b = widgets.ToggleButton(description='',button_style='',layout=Layout(width='50px', height='50px'))
u = widgets.ToggleButton(description='▲',button_style='',layout=Layout(width='50px', height='50px'))
d = widgets.ToggleButton(description='▼',button_style='',layout=Layout(width='50px', height='50px'))
l = widgets.ToggleButton(description='◀︎',button_style='',layout=Layout(width='50px', height='50px'))
r = widgets.ToggleButton(description='►',button_style='',layout=Layout(width='50px', height='50px'))
o = widgets.ToggleButton(description='O',button_style='',layout=Layout(width='50px', height='50px'))
x = widgets.ToggleButton(description='X',button_style='',layout=Layout(width='50px', height='50px'))

line = []
line.append( widgets.HBox([b,u,b,b,b,o]) )
line.append( widgets.HBox([l,b,r,b,x,b]) )
line.append( widgets.HBox([b,d,b,b,b,b]) )
display(widgets.VBox(line))

def given_u(obs_u):
    if u.value:
        with open('input.txt','a') as file:
            file.write('u')
        u.value = False
        
def given_d(obs_d):
    if d.value:
        with open('input.txt','a') as file:
            file.write('d')
        d.value = False
    
def given_l(obs_l):
    if l.value:
        with open('input.txt','a') as file:
            file.write('l')
        l.value = False
    
def given_r(obs_r):
    if r.value:
        with open('input.txt','a') as file:
            file.write('r')
        r.value = False
    
def given_x(obs_x):
    if x.value:
        with open('input.txt','a') as file:
            file.write('x')
        x.value = False
    
def given_o(obs_o):
    if o.value:
        with open('input.txt','a') as file:
            file.write('o')
        o.value = False
    
def given_b(obs_b):
    if b.value:
        b.value = False
    
    
u.observe(given_u)
d.observe(given_d)
l.observe(given_l)
r.observe(given_r)
o.observe(given_o)
x.observe(given_x)
b.observe(given_b)