from math import atan2, cos, sin, tan, pi, fabs

def draw_line(
        context,
        xValInit,
        yValInit,
        nCut,
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
    # Return end point to link ascending and descending for a full triangle

    xVal = xValInit
    yVal = yValInit

    angle = atan2(stepHeightCut,stepWidthCut+widthCut)
    lossArcLength = kArc * widthCut
    lossArcX = lossArcLength * cos(angle)
    lossArcY = lossArcLength * sin(angle)
    radius = lossArcLength * tan(angle/2)

    context.move_to(xVal,yVal)
    if not ascending:
        stepHeightCut *= -1
        lossArcY *= -1
        radius *= -1

    xVal += stepWidthCut + widthCut - lossArcX
    yVal -= stepHeightCut - lossArcY
    context.line_to(xVal, yVal)

    xVal += lossArcX - lossArcLength
    yVal += -lossArcY + radius
    if ascending:
        context.arc_negative(xVal,yVal, radius, pi/2-angle, -pi/2)
    else:
        context.arc(xVal,yVal, fabs(radius), -pi/2 + angle, pi/2)
    yVal -= radius
    xVal += lossArcLength - widthCut

    context.line_to(xVal,yVal)
    if not aboveTabAndHoles or limitLine:
        if ascending:
            listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2)))
        else:
            listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2)))
    if aboveTabAndHoles or limitLine:
        if ascending:
            listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal + distanceHole*sin(angle/2)))
        else:
            listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal + distanceHole*sin(angle/2)))

    for j in range(nCut):

        xVal -= widthCut - lossArcLength
        context.line_to(xVal,yVal)

        yVal -= radius
        if ascending:
            context.arc(xVal,yVal, radius, pi/2, 3*pi/2 - angle)
        else:
            context.arc_negative(xVal,yVal, fabs(radius), 3*pi/2, pi/2 + angle)

        xVal += 2 * widthCut + 2*stepWidthCut - lossArcLength - lossArcX
        yVal -= 2*stepHeightCut - radius - lossArcY
        context.line_to(xVal,yVal)
        xVal += lossArcX - lossArcLength
        yVal -= lossArcY - radius
        if ascending:
            context.arc_negative(xVal,yVal, radius, pi/2-angle, -pi/2)
        else:
            context.arc(xVal,yVal, fabs(radius), -pi/2 + angle, pi/2)
        yVal -= radius

        xVal -= widthCut - lossArcLength
        context.line_to(xVal, yVal)
        if not aboveTabAndHoles or limitLine:
            if ascending:
                listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2)))
            else:
                listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2)))
        if aboveTabAndHoles or limitLine:
            if ascending:
                listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal + distanceHole*sin(angle/2)))
            else:
                listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal + distanceHole*sin(angle/2)))


    xVal -= widthCut - lossArcLength
    context.line_to(xVal,yVal)

    yVal -= radius
    if ascending:
        context.arc(xVal,yVal, radius, pi/2, 3*pi/2 - angle)
    else:
        context.arc_negative(xVal,yVal, fabs(radius), 3*pi/2, pi/2 + angle)

    xVal += widthCut + stepWidthCut - lossArcLength
    yVal -= stepHeightCut - radius
    context.line_to(xVal,yVal)


    xValSave = xVal
    yValSave = yVal

    for j in range(nCut + 1):
        xVal = xValInit + stepWidthCut + j * stepWidthCut * 2
        yVal = yValInit - j * stepHeightCut * 2

        heightTab = stepHeightCut - widthCut * tan(angle)
        diffHeightTab = widthTab * tan(angle) / 2

        if not ascending:
            yVal -= 2*stepHeightCut
            heightTab = stepHeightCut + widthCut * tan(angle)
            heightTab *= -1
            diffHeightTab *= -1

        if aboveTabAndHoles:
            if ascending:
                yVal -= stepHeightCut * 2
            else:
                yVal += stepHeightCut * 2
            # heightTab *= -1


        if (j == 0 and ascending and not aboveTabAndHoles) or (j == nCut and not ascending and not aboveTabAndHoles) or (j==0 and not ascending and aboveTabAndHoles) or (j == nCut and ascending and aboveTabAndHoles):
            if (not reverseTab and not aboveTabAndHoles) or (aboveTabAndHoles and reverseTab):
                diffHeightTab = 0
            heightTab /= 2
            if aboveTabAndHoles:
                yVal += heightTab
            else:
                yVal -= heightTab

        if reverseTab:
            heightTab *= -1

        listOfTabs.append([
                (xVal-widthTab/2,yVal+heightTab+diffHeightTab),
                (xVal-widthTab/2,yVal),
                (xVal+widthTab/2,yVal),
                (xVal+widthTab/2,yVal+heightTab-diffHeightTab)
            ])
        if limitLine:
            xVal = 2*xValInit+ (nCut+1) * 2 * abs(stepWidthCut) - xVal
            yVal = (nCut+1) * 2 * abs(stepHeightCut) - yVal

            if (j == 0 and ascending and not aboveTabAndHoles) or (j == nCut and not ascending and not aboveTabAndHoles) or (j==0 and not ascending and aboveTabAndHoles) or (j == nCut and ascending and aboveTabAndHoles):
                diffHeightTab = 0

            listOfTabs.append([
                    (xVal-widthTab/2,yVal+heightTab+diffHeightTab),
                    (xVal-widthTab/2,yVal),
                    (xVal+widthTab/2,yVal),
                    (xVal+widthTab/2,yVal+heightTab-diffHeightTab)
                ])

    return (xValSave,yValSave)
