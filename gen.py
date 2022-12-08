import cairo
import os
from math import atan2, cos, sin, tan, pi, sqrt, sqrt
from draw import draw_line, draw_descending_line


nameTree="tree_smol"

width = 1100/4
height= 1800/4
full = True

nStepWidth = 6
nStepHeight = 6

nCut = -1
IncreasingCut = True

widthCut = 12/4
karc = 0.4
radiusHole = 1.8/4
distanceHole = 14/4

widthTab = 12 /4
reverseTab = True
offsetFirstTab = 15/4

distSmallHole = 60/4
radiusSmallHole = 1.5/4
distBetweenHoles = 13/4
radiusBigHole = 25/4
distBetweenHoles2 = 50/4
radiusBigBigHole = 45/4

corner = True

colorInside = (0,0,1)
colorHole = (0,0,0)
colorBorder = (0,1,0)

scaleFactor = 1
width *= scaleFactor
height *= scaleFactor
widthCut *= scaleFactor
radiusHole *= scaleFactor
distanceHole *= scaleFactor
widthTab *= scaleFactor


with cairo.SVGSurface(f"tmp.svg", width, height) as surface:
    # creating a cairo context object
    context = cairo.Context(surface)
    surface.set_document_unit(6)

    # Setting group
    # context.push_group()

    # Setting color
    context.set_source_rgba(colorInside[0], colorInside[1], colorInside[2], 1)

    stepWidth = width / nStepWidth
    stepHeight =  height / nStepHeight

    listOfHoles = []
    listOfTabs = []


    varNCut = nCut

    if full:
        stepWidth /= 2

    nLine = min(nStepWidth,nStepHeight)
    for i in range(nLine-1,-1,-1):
        if IncreasingCut:
            varNCut += 1

        if full:
            stepWidthCut = (width/2 - i * stepWidth) / (varNCut * 2 + 2)
        else:
            stepWidthCut = (width - i * stepWidth) / (varNCut * 2 + 2)

        stepHeightCut = (height - i * stepHeight) / (varNCut * 2 + 2)

        xVal, yVal = draw_line(
                context,
                i*2*stepWidthCut,
                height,
                varNCut,
                stepWidthCut,
                stepHeightCut,
                widthCut,
                widthTab,
                karc,
                radiusHole,
                distanceHole,
                listOfHoles,
                listOfTabs,
                reverseTab,
                False,
                i==0 and corner,
                True,
                offsetFirstTab=offsetFirstTab
                )
        if full:
            xValSave = xVal
            yValSave = yVal
            xVal, yVal = draw_line(
                    context,
                    xVal,
                    yVal,
                    varNCut,
                    stepWidthCut,
                    stepHeightCut,
                    widthCut,
                    widthTab,
                    karc,
                    radiusHole,
                    distanceHole,
                    listOfHoles,
                    listOfTabs,
                    reverseTab,
                    False,
                    i == 0 and corner,
                    False,
                    prevLine=True,
                    offsetFirstTab=offsetFirstTab
                    )

            # Adding more circle
            cx =xValSave
            cy = yValSave + distSmallHole + radiusSmallHole
            listOfHoles.append((cx,cy,radiusSmallHole))

            cy = yValSave + distSmallHole + radiusSmallHole*2 + distBetweenHoles + radiusBigHole
            listOfHoles.append((cx,cy,radiusBigHole))

            cy = yValSave + distSmallHole + radiusSmallHole*2 + distBetweenHoles + radiusBigHole * 2 + distBetweenHoles2 + radiusSmallHole
            listOfHoles.append((cx,cy,radiusSmallHole))
            cy = yValSave + distSmallHole + radiusSmallHole*2 + distBetweenHoles + radiusBigHole * 2 + distBetweenHoles2 + radiusSmallHole*2+distBetweenHoles + radiusBigBigHole
            listOfHoles.append((cx,cy,radiusBigBigHole))


        if corner and i != 0:
            xVal, yVal = draw_line(
                context,
                0,
                (nLine -i)*2*stepHeightCut,
                varNCut,
                stepWidthCut,
                stepHeightCut,
                widthCut,
                widthTab,
                karc,
                radiusHole,
                distanceHole,
                listOfHoles,
                listOfTabs,
                reverseTab,
                True,
                False,
                True
                )
            if full:
                xVal, yVal = draw_line(
                    context,
                    xVal + (i) * 4 *stepWidthCut,
                    yVal,
                    varNCut,
                    stepWidthCut,
                    stepHeightCut,
                    widthCut,
                    widthTab,
                    karc,
                    radiusHole,
                    distanceHole,
                    listOfHoles,
                    listOfTabs,
                    reverseTab,
                    True,
                    False,
                    False
                    )

    context.stroke()




    context.set_source_rgba(colorHole[0], colorHole[1], colorHole[2], 1)
    for tab in listOfTabs:
        context.move_to(tab[0][0],tab[0][1])
        for (xVal,yVal) in tab[1:]:
            context.line_to(xVal,yVal)

    for (cx,cy,r) in listOfHoles:
        context.move_to(cx+r,cy)
        context.arc(cx,cy,r,0,2*pi)

    context.stroke()

    context.set_source_rgba(colorBorder[0], colorBorder[1], colorBorder[2], 1)
    context.move_to(0,height)
    context.line_to(width,height)
    if not full or corner:
        context.line_to(width,0)
        if corner:
            context.line_to(0,0)
            context.line_to(0,height)
    context.stroke()

i = 1
with open(f"{nameTree}.svg","w+") as out_file:
    with open("tmp.svg", "r") as f:
        for line in f.readlines():
            if "path" in line:
                out_file.write(f"""  <g
    inkscape:groupmode="layer"
    id="layer{i}"
    inkscape:label="Layer {i}"
    >""")
            out_file.write(line)
            if "path" in line:
                out_file.write("  </g>")
                i+=1
try:
    os.remove("tmp.svg")
except FileNotFoundError:
    print("Temporary file could not be removed")
