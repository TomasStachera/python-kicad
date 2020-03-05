#Class for moving block of components to specified position
#Tomas Stachera
#version 1.0

import pcbnew

# Class for store original compnents position
class CompPositions:
    def __init__(self,name,x_pos,y_pos,orientation):
        self.name=name
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.orientation=orientation
    
#Class for store components wiht reference name
# and components maximal border in X axis and y_aaxis
class ComponentsArea():
    def __init__(self,name=None,x_left=0,x_right=0,y_top=0,y_bottom=0):
        self.x_left=x_left
        self.x_right=x_right
        self.y_top=y_top
        self.y_bottom=y_bottom
        self.name=name
  
        
    
#Class for find component and find componets corner
#ComponetsName: Return string array with components reference according range
#  Example ComponenetsName(R,2,6) return R2,R3,R4,R5,R6
#Function COmponentsCorner(x,y) Calculates maximal x,y corner from componets shape
#x,y is array witch componets contours in x,y axis
class Componentsx:    
    def ComponentsName(self,cmpx,start_r,end_r):
        components_name=[]
        for xx in range(end_r-start_r+1):
            ind=start_r+xx
            name1=cmpx+str(ind)
            components_name.append(name1)
        return components_name
    def ComponetCorners(self,x,y):
        x.sort()
        x_left=x[0]
        x.sort(reverse=True)
        x_right=x[0]
        y.sort()
        y_top=y[0]
        y.sort(reverse=True)
        y_bot=y[0]
        return x_left,x_right,y_top,y_bot

#Class for find components and set new components in PcbNew class
#FindPosition: function find actual position and orintation according reference
#FindShape(name); function find components shape according reference
#SetNewPosition(name,x,yxorient) Place compobe=nent to new postion
class PCBComponents:
    def __init__(self):
        self.board=pcbnew.GetBoard()
    def FindPosition(self,name):
        mod=self.board.FindModuleByReference(name)
        if(mod==None):
            print("Module {} was not found".format(name))
            return 0,0,0
        x=mod.GetPosition().x
        y=mod.GetPosition().y
        orient=0
        return x,y,orient
    def FindShape(self,name):
        mod=self.board.FindModuleByReference(name)
        x=[]
        y=[]
        if(mod==None):
            print("Module {} was not found".format(name))
            return x,y
        polyx=mod.GetBoundingPoly()
        linech=polyx.Outline(0)
        for nmv in range(linech.PointCount()):
            x.append(linech.Point(nmv).x)
            y.append(linech.Point(nmv).y)
            
        return x,y
    def SetNewPosition(self,name,x,y,orient):
        mod=self.board.FindModuleByReference(name)
        if(mod==None):
            print("Module {} was not found".format(name))
            return
        point=pcbnew.wxPoint(0,0)
        point.x=x
        point.y=y
        mod.SetPosition(point)
        mod.SetOrientation(orient)
        
    def OnlyOrientation(self,name,orient):
        mod=self.board.FindModuleByReference(name)
        if(mod==None):
            print("Module {} was not found".format(name))
            return
        mod.SetOrientation(orient)
        
    def Flip(self,name):
        mod=self.board.FindModuleByReference(name)
        if(mod==None):
            print("Module {} was not found".format(name))
            return
        point=pcbnew.wxPoint(0,0)
        point.x=mod.GetPosition().x
        point.y=mod.GetPosition().y
        mod.Flip(point)
    def UpdateAll(self):
        pcbnew.Refresh()
        print("Updated")
        
    
class InsertComponents:
    def __init__(self):
        self.OldPosition=[]
        self.NewPosition=[]
        self.CompArea=[]
        self.fp=PCBComponents()
 
    def ReadParams(self,name,start_r,end_r,x,y,orient):
        del self.OldPosition[:]
        del self.NewPosition[:]
        del self.CompArea[:]
        cx=Componentsx()
        compx=cx.ComponentsName(name,start_r,end_r)
        x=x*1000000
        y=y*1000000
        orient=orient*10   
        for c in compx:
            x,y,orient=self.fp.FindPosition(c)
            self.OldPosition.append(CompPositions(c,x,y,orient))
            x_ar,y_ar=self.fp.FindShape(c)
            x_l,x_r,y_t,y_b=cx.ComponetCorners(x_ar,y_ar)
            self.CompArea.append(ComponentsArea(c,x_l,x_r,y_t,y_b))
    def InsertNewPosH(self,name,start_r,end_r,x,y,space,orient):
        self.ReadParams(name,start_r,end_r,x,y,orient)
        self.NewPosition[:]
        x=x*1000000
        y=y*1000000
        orient=orient*10
        space=space*1000000
        if len(self.OldPosition)==0:
            print("Any components was found")
            return -1
        ofset_x=0
        for (xx,cc) in zip(self.OldPosition,self.CompArea):
            if ofset_x == 0:
                x_actual=x
            else:
                x_actual=ofset_x+space+(xx.x_pos-cc.x_left)
            self.NewPosition.append(CompPositions(xx.name,x_actual,y,orient))
            ofset_x=x_actual+(cc.x_right-xx.x_pos)
        for cc in self.NewPosition:
            self.fp.SetNewPosition(cc.name,cc.x_pos,cc.y_pos,cc.orientation)
        self.fp.UpdateAll()
       
    def InsertNewPosV(self,name,start_r,end_r,x,y,space,orient):
        self.ReadParams(name,start_r,end_r,x,y,orient)
        self.NewPosition[:]
        x=x*1000000
        y=y*1000000
        orient=orient*10
        space=space*1000000
        if len(self.OldPosition)==0:
            print("Any components was found")
            return -1
        ofset_y=0
        for (xx,cc) in zip(self.OldPosition,self.CompArea):
            if ofset_y == 0:
                y_actual=y
            else:
                y_actual=ofset_y+space+(cc.y_bottom-xx.y_pos)
            self.NewPosition.append(CompPositions(xx.name,x,y_actual,orient))
            ofset_y=y_actual+(xx.y_pos-cc.y_top)
        for cc in self.NewPosition:
            self.fp.SetNewPosition(cc.name,cc.x_pos,cc.y_pos,cc.orientation)
        self.fp.UpdateAll()
    
    def ReturnBack(self):
        for cc in self.OldPosition:
            self.fp.SetNewPosition(cc.name,cc.x_pos,cc.y_pos,cc.orientation)
        self.fp.UpdateAll()
    def Changeorient(self,name,start_r,end_r,orient):
        self.ReadParams(name,start_r,end_r,0,0,orient)
        orient=orient*10
        if len(self.OldPosition)==0:
            print("Any components was found")
            return -1
        for cc in self.OldPosition:
            self.fp.OnlyOrientation(cc.name,orient)
        self.fp.UpdateAll()
    def FlipBlock(self,name,start_r,end_r):
        self.ReadParams(name,start_r,end_r,0,0,0)
        if len(self.OldPosition)==0:
            print("Any components was found")
            return -1
        for cc in self.OldPosition:
            self.fp.Flip(cc.name)
        self.fp.UpdateAll()

f=InsertComponents()            

#Function inserts block of components in horizontal axis
#name: name of reference (without number)
#start_r= start reference number
#end_r= end reference number
#Example: name =R ,start_r=1,end_r=5, Components R1,R2,R3,R4,R5
#x: position of first components (left corner of block) in x axis
#y=position of first components (left corner of block) in y axis
# space: space between comonents in x axis (space between comonents corners)
#orient: Final orientation of all components in  block
def InsPosH(name,start_r,end_r,x,y,space,orient):
    global f
    f.InsertNewPosH(name,start_r,end_r,x,y,space,orient)

#Function inserts block of components in verticall axis
#name: name of reference (without number)
#start_r= start reference number
#end_r= end reference number
#Example: name =R ,start_r=1,end_r=5, Components R1,R2,R3,R4,R5
#x: position of first components (left corner of block) in x axis
#y=position of first components (left corner of block) in y axis
# space: space between comonents in y axis (space between comonents corners)
#orient: Final orientation of all components in  block
def InsPosV(name,start_r,end_r,x,y,space,orient):
    global f
    f.InsertNewPosV(name,start_r,end_r,x,y,space,orient)
    
#Function return set all compnents to previous position
def RetBack():
    global f
    f.ReturnBack()

#Function set block of components to new orientation
#name: name of reference (without number)
#start_r= start reference number
#end_r= end reference number
#Example: name =R ,start_r=1,end_r=5, Components R1,R2,R3,R4,R5
#orient: orientation of components
def ChangeOrient(name,start_r,end_r,orient):
    global f
    f.Changeorient(name,start_r,end_r,orient)

#Function flip all components in block
#name: name of reference (without number)
#start_r= start reference number
#end_r= end reference number
#Example: name =R ,start_r=1,end_r=5, Components R1,R2,R3,R4,R5
    
def FlipBlock(name,start_r,end_r):
    global f
    f.FlipBlock(name,start_r,end_r)
              
            
        
        


    
