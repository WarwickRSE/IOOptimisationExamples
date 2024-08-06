#H Ratcliffe, University of Warwick

from math import sqrt, atan2, pi

#A semi-heuristic colour naming tool using LAB colour space
#This segments the region by angle in the A-B plane
# and into 5 degrees of darkness in the l axis
#It also tries to capture white, grey and black
# and account for pink and brown

def nameColourLAB(colourTriplet):
  """Returns a two element list of strings describing the colour"""

  l, a, b = colourTriplet
  # a- red-green. b- blue-yellow 
  
  r = sqrt((a-128)**2 + (b-128)**2)
  theta = atan2((128-b),(a-128)) + pi
  
  #Handle central balanced region specially
  if r < 10:
    # Generally balanced greys
    
    if l > 220:
      return ["","white"]
    elif l > 180:
      return ["l.", "grey"]
    elif l > 120:
      return ["","grey"]
    elif l > 50:
      return ["d.","grey"]
    else:
      return ["","black"]

  if l > 220:
    name = ["vl."]
  elif l > 180:
    name = ["l."]
  elif l > 120:
    name = [""]
  elif l > 50:
    name = ["d."]
  else:
    name = ["vd."]

  # Work in 8 regions of angle, with tweaks to bounds
  
  #print(a, b, r, theta, pi/8, 3*pi/8)
  if theta > 0 and theta < 3*pi/16:
    name.append("green")
  elif theta < 7*pi/16:
    name.append("lime")
  elif theta < 10*pi/16:
    name.append("yellow")
  elif theta < 12*pi/16:
    name.append("orange")
  elif theta < 17*pi/16:
    name.append("red")
  elif theta < 21*pi/16:
    name.append("purple")
  elif theta < 27*pi/16:
    name.append("blue")
  elif theta < 29*pi/8:
    name.append("cyan")
  else:
    name.append("green")

  # Amend a few special names 
  
  if name[0] == "d." and (name[1] == "orange" or name[1] == "yellow"):
    name = ["","brown"]
  elif name[0] == "vd." and (name[1] == "orange" or name[1] == "yellow"):
    name = ["d.","brown"]
  elif name[0] == "l." and (name[1] == "orange" or name[1] == "red"):
    name = ["","pink"]
  elif name[0] == "vl." and (name[1] == "orange" or name[1] == "red"):
    name = ["l.","pink"]
    
  # Amend brightnesses for those removed
  if "yellow" in name or "orange" in name:
    if name[0] == "":
      name[0] = "d."
    elif name[0] == "l.":
      name[0] = ""
    elif name[0] == "vl.":
      name[0] = "l."

  return name

