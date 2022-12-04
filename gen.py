import cairo
import os
from math import atan2, cos, sin, tan, pi, sqrt, sqrt
from draw import draw_line, draw_descending_line


nameTree="tree"

width = 300
height= 500
full = True

nStepWidth = 4
nStepHeight =4

nCut = -1
IncreasingCut = True

widthCut = 3
karc = 0.4
radiusHole = 2
distanceHole = 10

widthTab = 4.5
reverseTab = True
offsetFirstTab = 5

corner = False

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



    # widthCut = 10
    # nCut = 5
    # stepHeight = 70
    # l = sqrt(height ** 2 + (width/2 + (nCut-1)*widthCut)**2)/nCut
    # alpha = atan2(height,width/2 + (nCut-1) * widthCut)
    # for i in range(nCut):
        # xVal, yVal = draw_descending_line(
            # context,
            # width/2,
            # i*stepHeight,
            # widthCut,
            # nCut,
            # l,
            # alpha,
            # False,
            # )
        # xVal, yVal = draw_descending_line(
            # context,
            # width/2,
            # i*stepHeight,
            # widthCut,
            # nCut,
            # l,
            # alpha,
            # True,
            # )
    # context.set_source_rgba(1, 0, 0, 1)
    # context.stroke()



    context.set_source_rgba(colorHole[0], colorHole[1], colorHole[2], 1)
    for tab in listOfTabs:
        context.move_to(tab[0][0],tab[0][1])
        for (xVal,yVal) in tab[1:]:
            context.line_to(xVal,yVal)

    for (cx,cy) in listOfHoles:
        context.move_to(cx+radiusHole,cy)
        context.arc(cx,cy,radiusHole,0,2*pi)

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
