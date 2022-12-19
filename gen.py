import cairo
import os
from math import atan2, cos, sin, tan, pi, sqrt, sqrt
from draw import draw_line, draw_descending_line

# Name of the svg file
nameTree="tree"

width = 1100 # mm
height= 1800 # mm

# Half of tree of full tree
full = True

# Number of different lines
# Better to keep it the same
nStepWidth = 5
nStepHeight = 5

# Number of cut in a line
nCut = -1
# Should this number increase
IncreasingCut = True

# Half width of the cut
widthCut = 12

# Percentage of widthCut to convert to a circle
karc = 0.4

# Radius and distance of the small holes
radiusHole = 1.8
distanceHole = 14

# Width of the tab (and thus of the material)
widthTab = 12

# Should reverse the tab
reverseTab = True

# Offset the first tab in height (to have something stronger)
offsetFirstTab = 15


# Distance from the top to the small holes
distSmallHole = 60
radiusSmallHole = 1.5

# distance between the small holes and the medium holes
distBetweenHoles = 13
radiusBigHole = 25

# distance between the medium and the big holes
distBetweenHoles2 = 50
radiusBigBigHole = 45

# Generate corner for full usage of the the sheet
corner = True

# Close the path and other stuff
CNC = True

# Change color of the stroke
colorInside = (0,0,1)
colorHole = (0,0,0)
colorBorder = (0,1,0)


with cairo.SVGSurface(f"tmp.svg", width, height) as surface:
    # creating a cairo context object
    context = cairo.Context(surface)
    surface.set_document_unit(6)


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
            if CNC:
                context.close_path()
                context.stroke()

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
                True,
                offsetFirstTab=offsetFirstTab
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
                    False,
                    offsetFirstTab=offsetFirstTab
                    )

    context.stroke()




    context.set_source_rgba(colorHole[0], colorHole[1], colorHole[2], 1)
    for tab in listOfTabs:
        context.move_to(tab[0][0],tab[0][1])
        for (xVal,yVal) in tab[1:]:
            context.line_to(xVal,yVal)
        # if CNC:
            # context.close_path()

    for (cx,cy,r) in listOfHoles:
        context.move_to(cx+r,cy)
        context.arc(cx,cy,r,0,2*pi)

    context.stroke()

    if CNC:
        context.set_source_rgba(colorBorder[0], colorBorder[1], colorBorder[2], 1)
        context.move_to(0,height)
        context.line_to(width,height)
        if not full or corner:
            context.line_to(width,0)
            if corner:
                context.line_to(0,0)
                context.line_to(0,height)
        context.close_path()
        context.stroke()

# Add each path in a layer
# also clean the svg to be understandable with easle
i = 1
with open(f"{nameTree}.svg","w+") as out_file:
    with open("tmp.svg", "r") as f:
        for line in f.readlines():
            if "<svg" in line:
                line = line.replace(">", """
  xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
  xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
>
""")
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
