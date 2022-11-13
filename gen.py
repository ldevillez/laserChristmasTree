import cairo
from math import atan2, cos, sin, tan, pi

width = 200
height= 600
Full = True
nStepWidth = 4
nStepHeight = 4

nCut = -1
IncreasingCut = True

widthCut = 10
karc = 0.4
radiusHole = 5
distanceHole = 20

widthTab = 3
ReverseTab = True

full = False

with cairo.SVGSurface("tree.svg", width, height) as surface:
    # creating a cairo context object
    context = cairo.Context(surface)

    context.move_to(0,0)
    context.line_to(0,height)
    context.line_to(width,height)

    stepWidth = width / nStepWidth
    stepHeight =  height / nStepHeight
    context.set_source_rgba(1, 0, 0, 1)
    listOfHoles = []

    # Red drawout
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

        xVal = i*stepWidth
        yVal = height
        context.move_to(i*stepWidth,height)

        xVal += stepWidthCut + widthCut
        yVal -= stepHeightCut
        context.line_to(xVal,yVal)
        xVal -= widthCut
        context.line_to(xVal,yVal)

        for j in range(varNCut):
            xVal -= widthCut
            context.line_to(xVal,yVal)
            xVal += 2 * widthCut + 2*stepWidthCut
            yVal -= 2*stepHeightCut
            context.line_to(xVal,yVal)

            xVal -= widthCut
            context.line_to(xVal, yVal)


        xVal -= widthCut
        context.line_to(xVal,yVal)
        xVal = width
        if full:
            xVal /= 2
        yVal = i*stepHeight
        context.line_to(xVal,yVal)
        if full:

            angle = atan2(stepHeightCut,stepWidthCut+widthCut)

            xVal += stepWidthCut + widthCut
            yVal += stepHeightCut
            context.line_to(xVal, yVal)

            xVal = width/2 + stepWidthCut
            context.line_to(xVal, yVal)
            for j in range(varNCut):
                xVal -= widthCut
                context.line_to(xVal,yVal)
                xVal += 2 * widthCut + 2*stepWidthCut
                yVal += 2*stepHeightCut
                context.line_to(xVal,yVal)

                xVal -= widthCut
                context.line_to(xVal, yVal)
            xVal -= widthCut
            context.line_to(xVal,yVal)
            context.line_to(width - i * stepWidth,height)


    context.stroke()
    context.set_source_rgba(0, 0, 1, 1)
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


            xVal += stepWidthCut + widthCut
            yVal += stepHeightCut
            context.line_to(xVal, yVal)

            xVal = width/2 + stepWidthCut
            context.line_to(xVal, yVal)
            for j in range(varNCut):
                xVal -= widthCut
                context.line_to(xVal,yVal)
                xVal += 2 * widthCut + 2*stepWidthCut
                yVal += 2*stepHeightCut
                context.line_to(xVal,yVal)

                xVal -= widthCut
                context.line_to(xVal, yVal)
            xVal -= widthCut
            context.line_to(xVal,yVal)
            context.line_to(width - i * stepWidth,height)


    context.stroke()








    context.set_source_rgba(0, 0, 0, 1)
    varNCut = nCut
    for i in range(min(nStepWidth,nStepHeight)-1,-1,-1):
        if IncreasingCut:
            varNCut += 1
            pass
        stepWidthCut = (width - i * stepWidth) / (varNCut * 2 + 2)
        stepHeightCut = (height - i * stepHeight) / (varNCut * 2 + 2)

        context.move_to(0,i*stepHeight)
        angle = atan2(stepHeightCut,stepWidthCut+widthCut)
        lossArcLength = karc * widthCut
        lossArcX = lossArcLength * cos(angle)
        lossArcY = lossArcLength * sin(angle)
        xVal = stepWidthCut + widthCut - lossArcX
        yVal = i*stepHeight + stepHeightCut - lossArcY
        context.line_to(xVal, yVal)

        radius = lossArcLength * tan(angle/2)
        xVal += lossArcX - lossArcLength
        yVal += lossArcY - radius

        context.arc(xVal,yVal, radius, -pi/2 + angle, pi/2)
        yVal += radius
        xVal = stepWidthCut
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
        if ReverseTab:
            for j in range(varNCut + 1):
                xVal = width - i * stepWidth - stepWidth/2 - widthTab / 2 - j * stepWidth
                yVal = height - j * stepHeightCut * 2
                heightDiff = widthTab * tan(angle)
                if j == 0:
                    heightSlot1 = stepWidth / 4 * tan(angle)
                    yVal -= (stepWidth/2 - widthTab/2) * tan(angle)
                else:
                    heightSlot1 = stepWidth / 2 * tan(angle)
                    yVal -= (stepWidth/2 - widthTab/2) * tan(angle)

                context.move_to(xVal,yVal - heightDiff)
                context.line_to(xVal,yVal + heightSlot1)
                context.line_to(xVal+widthTab,yVal + heightSlot1)
                context.line_to(xVal+widthTab,yVal)

        else:
            for j in range(varNCut + 1):
                xVal = width - i * stepWidth - stepWidth/2 - widthTab / 2 - j * stepWidth
                yVal = height - j * stepHeightCut * 2
                if j == 0:
                    heightSlot1 = stepWidth / 4 * tan(angle)
                    heightDiff = 0
                else:
                    heightSlot1 = stepWidth / 2 * tan(angle)
                    yVal += (stepWidth/2 - widthTab/2) * tan(angle)
                    heightDiff = widthTab * tan(angle)

                context.move_to(xVal,yVal)
                context.line_to(xVal,yVal - heightSlot1)
                context.line_to(xVal+widthTab,yVal - heightSlot1)
                context.line_to(xVal+widthTab,yVal + heightDiff)


    context.stroke()
    for (cx,cy) in listOfHoles:
        context.move_to(cx+radiusHole,cy)
        context.arc(cx,cy,radiusHole,0,2*pi)
    context.stroke()
