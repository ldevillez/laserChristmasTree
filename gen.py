import cairo
from math import atan2, cos, sin, tan, pi

nameTree="tree"

width = 200
height= 300
Full = True

nStepWidth = 4
nStepHeight = 4

nCut = -1
IncreasingCut = True

widthCut = 15
karc = 0.4
radiusHole = 2
distanceHole = 10

widthTab = 3
ReverseTab = True

full = True

scaleFactor = 1
width *= scaleFactor
height *= scaleFactor
widthCut *= scaleFactor
radiusHole *= scaleFactor
distanceHole *= scaleFactor
widthTab *= scaleFactor


with cairo.SVGSurface(f"{nameTree}.svg", width, height) as surface:
    # creating a cairo context object
    context = cairo.Context(surface)

    # Setting color
    context.set_source_rgba(0, 0, 1, 1)

    # Setting the border
    context.line_to(0,height)
    context.line_to(width,height)
    if not full:
        context.line_to(width,0)

    listOfHoles = []

    stepWidth = width / nStepWidth
    stepHeight =  height / nStepHeight

    varNCut = nCut

    if full:
        stepWidth /= 2

    for i in range(min(nStepWidth,nStepHeight)-1,-1,-1):
        if IncreasingCut:
            varNCut += 1
            pass
        if full:
            stepWidthCut = (width/2 - i * stepWidth) / (varNCut * 2 + 2)
        else:
            stepWidthCut = (width - i * stepWidth) / (varNCut * 2 + 2)

        stepHeightCut = (height - i * stepHeight) / (varNCut * 2 + 2)

        angle = atan2(stepHeightCut,stepWidthCut+widthCut)
        lossArcLength = karc * widthCut
        lossArcX = lossArcLength * cos(angle)
        lossArcY = lossArcLength * sin(angle)
        radius = lossArcLength * tan(angle/2)

        xVal = i*stepWidth
        yVal = height
        context.move_to(i*stepWidth,height)

        xVal += stepWidthCut + widthCut - lossArcX
        yVal -= stepHeightCut - lossArcY
        context.line_to(xVal, yVal)

        xVal += lossArcX - lossArcLength
        yVal += -lossArcY + radius

        context.arc_negative(xVal,yVal, radius, pi/2-angle, -pi/2)
        yVal -= radius
        xVal += lossArcLength - widthCut

        context.line_to(xVal,yVal)
        listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2)))

        for j in range(varNCut):

            xVal -= widthCut - lossArcLength
            context.line_to(xVal,yVal)

            yVal -= radius
            context.arc(xVal,yVal, radius, pi/2, 3*pi/2 - angle)

            xVal += 2 * widthCut + 2*stepWidthCut - lossArcLength - lossArcX
            yVal -= 2*stepHeightCut - radius - lossArcY
            context.line_to(xVal,yVal)
            xVal += lossArcX - lossArcLength
            yVal -= lossArcY - radius
            context.arc_negative(xVal,yVal, radius, pi/2-angle, -pi/2)
            yVal -= radius

            xVal -= widthCut - lossArcLength
            context.line_to(xVal, yVal)
            listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2)))


        xVal -= widthCut - lossArcLength
        context.line_to(xVal,yVal)

        yVal -= radius
        context.arc(xVal,yVal, radius, pi/2, 3*pi/2 - angle)
        xVal = width

        if full:
            xVal /= 2
        yVal = i*stepHeight
        context.line_to(xVal,yVal)
        if full:
            xVal += stepWidthCut + widthCut - lossArcX
            yVal += stepHeightCut - lossArcY
            context.line_to(xVal, yVal)

            radius = lossArcLength * tan(angle/2)
            xVal += lossArcX - lossArcLength
            yVal += lossArcY - radius

            context.arc(xVal,yVal, radius, -pi/2 + angle, pi/2)
            yVal += radius
            xVal += lossArcLength - widthCut
            context.line_to(xVal, yVal)
            listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2)))

            for j in range(varNCut):
                xVal -= widthCut - lossArcLength
                context.line_to(xVal,yVal)
                yVal += radius
                context.arc_negative(xVal,yVal, radius, 3*pi/2, pi/2 + angle)
                xVal += 2 * widthCut + 2*stepWidthCut -lossArcX - lossArcLength
                yVal += 2*stepHeightCut -lossArcY - radius
                context.line_to(xVal,yVal)

                xVal += lossArcX - lossArcLength
                yVal += lossArcY - radius

                context.arc(xVal,yVal, radius, -pi/2 + angle, pi/2)
                yVal += radius
                xVal -= widthCut - lossArcLength
                context.line_to(xVal, yVal)
                listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2)))

            xVal -= widthCut - lossArcLength
            context.line_to(xVal,yVal)
            yVal += radius
            context.arc_negative(xVal,yVal, radius, 3*pi/2, pi/2 + angle)
            context.line_to(width - i * stepWidth,height)


        for j in range(varNCut + 1):
            xVal = i * stepWidth + stepWidth/2 + j * stepWidth
            yVal = height - j * stepHeightCut * 2
            heightTab = stepHeightCut - widthCut * tan(angle)
            diffHeightTab = widthTab * tan(angle) / 2
            if j == 0:
                if not ReverseTab:
                    diffHeightTab = 0
                heightTab /= 2
                yVal -= heightTab

            if ReverseTab:
                heightTab *= -1

            context.move_to(xVal-widthTab/2,yVal+heightTab+diffHeightTab)
            context.line_to(xVal-widthTab/2,yVal)
            context.line_to(xVal+widthTab/2,yVal)
            context.line_to(xVal+widthTab/2,yVal+heightTab-diffHeightTab)

            if full:
                xVal = width - xVal
                context.move_to(xVal-widthTab/2,yVal+heightTab-diffHeightTab)
                context.line_to(xVal-widthTab/2,yVal)
                context.line_to(xVal+widthTab/2,yVal)
                context.line_to(xVal+widthTab/2,yVal+heightTab+diffHeightTab)

    context.stroke()

    for (cx,cy) in listOfHoles:
        context.move_to(cx+radiusHole,cy)
        context.arc(cx,cy,radiusHole,0,2*pi)
    context.stroke()

def draw_line(
        context,
        xVal,
        yVal,
        nVarCut,
        stepWidthCut,
        stepHeightCut,
        widthCut,
        widthTab,
        kArc,
        radiusHole,
        distanceHole,
        listOfHoles,
        listOfTabs,
        reverseTab=False,
        aboveTabAndHoles=False, # for above corners, the tabs and holes are above the line
        limitLine=False, # The main diagonal is common for the above and the below triangle. This will ensure that the tabs and holes are generated for both triangle
        ascending=True,
        ):
    pass
    # Return end point to link ascending and descending for a full triangle
