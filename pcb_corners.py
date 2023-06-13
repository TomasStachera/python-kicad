#Functions drawing PCB bounding area and place holes
import pcbnew

board_width=200000
g_startx=0
g_starty=0
g_width=0
g_height=0

footprint_lib = 'C:/Program Files/KiCad/7.0/share/kicad/footprints/MountingHole.pretty'
hole_type="MountingHole_3.2mm_M3"


# most queries start with a board
def GetCoordinates(pos):
#    return pos*1000000
    return pos
#Function draw bounding area
#1.parameter: startx: Start corner x-coordinates
#2.parameter: starty: Start corner y=coordinates
#3.parameter: width: width of PCB - horizontalsize
#4.parameter: height: height of PCB- vertical size

def DrawBounding(startx,starty,width,height):
     board = pcbnew.GetBoard()
     global g_startx
     g_startx=startx
     global g_starty
     g_starty=starty
     global g_width
     g_width=width
     global g_height
     g_height=height
   
     ds=pcbnew.PCB_SHAPE(board)
     ds.SetStart(pcbnew.VECTOR2I_MM(GetCoordinates(startx),GetCoordinates(starty)))
     ds.SetEnd(pcbnew.VECTOR2I_MM(GetCoordinates(startx+width),GetCoordinates(starty)))
     ds.SetLayer(pcbnew.Edge_Cuts)
     ds.SetWidth(board_width)
     board.Add(ds)
     
     ds=pcbnew.PCB_SHAPE(board)
     ds.SetStart(pcbnew.VECTOR2I_MM(GetCoordinates(startx+width),GetCoordinates(starty)))
     ds.SetEnd(pcbnew.VECTOR2I_MM(GetCoordinates(startx+width),GetCoordinates(starty+height)))
     ds.SetLayer(pcbnew.Edge_Cuts)
     ds.SetWidth(board_width)
     board.Add(ds)
     
     ds=pcbnew.PCB_SHAPE(board)
     ds.SetStart(pcbnew.VECTOR2I_MM(GetCoordinates(startx+width),GetCoordinates(starty+height)))
     ds.SetEnd(pcbnew.VECTOR2I_MM(GetCoordinates(startx),GetCoordinates(starty+height)))
     ds.SetLayer(pcbnew.Edge_Cuts)
     ds.SetWidth(board_width)
     board.Add(ds)
     
     ds=pcbnew.PCB_SHAPE(board)
     ds.SetStart(pcbnew.VECTOR2I_MM(GetCoordinates(startx),GetCoordinates(starty+height)))
     ds.SetEnd(pcbnew.VECTOR2I_MM(GetCoordinates(startx),GetCoordinates(starty)))
     ds.SetLayer(pcbnew.Edge_Cuts)
     ds.SetWidth(board_width)
     board.Add(ds)

     pcbnew.Refresh()

# Function place holes in 4 corners
#1.parameter: dim_cor: dimension of hole centeral from PCB corners (default value 10mm)
def PlaceHoleCorners(dim_cor=10):
     global g_startx
     global g_starty
     global g_width
     global g_height
     global hole_type
     x_coord=[0,0]
     y_coord=[0,0]
     x_coord[0]=dim_cor+ g_startx;
     x_coord[1]=g_startx+g_width-dim_cor
     y_coord[0]= g_starty+dim_cor
     y_coord[1]= g_starty+g_height-dim_cor
     board = pcbnew.GetBoard()
     global footprint_lib
     io = pcbnew.PCB_PLUGIN()
     for xx in x_coord:
         for yy in y_coord:
           mod = io.FootprintLoad(footprint_lib,hole_type )
           mod.SetPosition(pcbnew.VECTOR2I_MM(GetCoordinates(xx),GetCoordinates(yy)))
           board.Add(mod)
 
         
     
     
     pcbnew.Refresh()

#Place hole in center of bounding
# typex=1: horizintal and vertical
#typex=2 : only horizontal
#typex=3: only vertical
def PlaceHoleCenter(typex=1, dim_cor=10):
     global g_startx
     global g_starty
     global g_width
     global g_height
     global hole_type
     x_coord=[0,0]
     y_coord=[0,0]
     if typex==1:
         horizont=1
         vertic=1
     elif typex==2:
         horizont=1
         vertic=0
     else:
         horizont=0
         vertic=1
         
     #horizontal holes
     board = pcbnew.GetBoard()
     global footprint_lib
     io = pcbnew.PCB_PLUGIN()
     
     
     x_coord[0]=g_startx+g_width/2;
     y_coord[0]=g_starty+dim_cor;
     y_coord[1]=g_starty+g_height-dim_cor
     if horizont==1:
         for yy in y_coord:
            mod = io.FootprintLoad(footprint_lib, hole_type)
            mod.SetPosition(pcbnew.VECTOR2I_MM(GetCoordinates(x_coord[0]),GetCoordinates(yy)))
            board.Add(mod)

     #vertical holes
     x_coord[0]=g_startx+dim_cor
     x_coord[1]=g_startx+g_width-dim_cor
     y_coord[0]=g_starty+g_height/2
     if vertic==1:
        for xx in x_coord:
            mod = io.FootprintLoad(footprint_lib, hole_type)
            mod.SetPosition(pcbnew.VECTOR2I_MM(GetCoordinates(xx),y_coord[0]))
            board.Add(mod)
         
     
         
     
     
     pcbnew.Refresh()
