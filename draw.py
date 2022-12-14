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
        prevLine=False,
        offsetFirstTab=0,
        ):
    # Return end point to link ascending and descending for a full triangle

    xVal = xValInit
    yVal = yValInit

    angle = atan2(stepHeightCut,stepWidthCut+widthCut)
    lossArcLength = kArc * widthCut
    lossArcX = lossArcLength * cos(angle)
    lossArcY = lossArcLength * sin(angle)
    radius = lossArcLength * tan(angle/2)

    if not prevLine:
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
            listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2), radiusHole))
        else:
            listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2), radiusHole))
    if aboveTabAndHoles or limitLine:
        if ascending:
            listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal + distanceHole*sin(angle/2), radiusHole))
        else:
            listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal + distanceHole*sin(angle/2), radiusHole))

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
                listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2), radiusHole))
            else:
                listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal - distanceHole*sin(angle/2), radiusHole))
        if aboveTabAndHoles or limitLine:
            if ascending:
                listOfHoles.append((xVal + widthCut - distanceHole*cos(angle/2),yVal + distanceHole*sin(angle/2), radiusHole))
            else:
                listOfHoles.append((xVal - widthCut + distanceHole*cos(angle/2),yVal + distanceHole*sin(angle/2), radiusHole))


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

    # TABS
    if aboveTabAndHoles:
        reverseTab = not reverseTab

    angleDrawLine = atan2(stepHeightCut,stepWidthCut+widthCut)
    varOffsetX = 0.1 * (stepWidthCut + widthCut) * 0
    varOffsetY = varOffsetX * tan(angleDrawLine)
    offsetX = (widthTab /2 + stepWidthCut/2) * 0
    offsetY = offsetX * tan(angle)

    for j in range(nCut + 1):
        xVal = xValInit + j * stepWidthCut * 2  + stepWidthCut /2
        yVal = yValInit - j * stepHeightCut * 2 - stepWidthCut /2 * tan(angleDrawLine)



        heightTab = stepHeightCut
        diffHeightTab = widthTab * tan(angle) / 2

        if aboveTabAndHoles:
            diffHeightTab *= -1


        if (not ascending and not aboveTabAndHoles) or (ascending and aboveTabAndHoles):
            xVal +=  stepWidthCut
            yVal -=  (stepWidthCut+2*widthCut) * tan(angleDrawLine) # reversed
            heightTab *= -1
            diffHeightTab *= -1


        # Special small tab
        smallTab = False
        if (j == 0 and (ascending and not aboveTabAndHoles) ):
            # xVal += (stepWidthCut + widthCut)/2
            # yVal -= (stepWidthCut + widthCut) * tan(angle) / 2
            smallTab = True

        elif (j == nCut and ((not ascending and not aboveTabAndHoles))):
            #xVal -= (stepWidthCut + widthCut)/2
            #yVal -= (stepWidthCut + widthCut) * tan(angle) / 2
            smallTab = True

        elif (j == nCut and ascending and aboveTabAndHoles):
            #xVal -= (stepWidthCut + widthCut)/2
            #yVal += (stepWidthCut + widthCut) * tan(angle) / 2
            smallTab = True

        elif (j == 0 and not ascending and aboveTabAndHoles):
            #xVal += (stepWidthCut + widthCut)/2
            #yVal += (stepWidthCut + widthCut) * tan(angle) / 2
            smallTab = True

        if smallTab:
            heightTab = abs(stepWidthCut/2 * tan(angleDrawLine)/2) + offsetFirstTab

            if not reverseTab:
                diffHeightTab = 0
                print("yosh")
        else:
            if (ascending and not aboveTabAndHoles):
                xVal += offsetX - j*varOffsetX
                yVal -= offsetY - j * varOffsetY
            elif (not ascending and not aboveTabAndHoles):
                xVal -= offsetX - (nCut-j) *varOffsetX
                yVal -= offsetY + (nCut-j)* varOffsetY
            elif (ascending and aboveTabAndHoles):
                xVal -= offsetX - (nCut - j) * varOffsetX
                yVal += offsetY - (nCut - j) * varOffsetY
            else:
                xVal += offsetX + j * varOffsetX
                yVal += offsetY - j * varOffsetY


        if smallTab and not reverseTab and aboveTabAndHoles:
            heightTab *= -1

        yVal += heightTab


        if smallTab and not reverseTab and not aboveTabAndHoles:
            heightTab -= 2 * offsetFirstTab
        elif smallTab and not reverseTab and aboveTabAndHoles:
            heightTab += 2 * offsetFirstTab


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

            if smallTab:
                if not reverseTab :
                    heightTab += 2*offsetFirstTab
                    # yVal += offsetFirstTab
                else:
                    heightTab += 2*offsetFirstTab
                    # yVal += offsetFirstTab

            if (j == 0 and ascending and not aboveTabAndHoles) or (j == nCut and not ascending and not aboveTabAndHoles):
                if (not reverseTab and not aboveTabAndHoles) or (aboveTabAndHoles and reverseTab):
                    if not ascending:
                        diffHeightTab = -widthTab * tan(angle) / 2
                    else:
                        diffHeightTab = widthTab * tan(angle) / 2
                else:
                    diffHeightTab = 0

            listOfTabs.append([
                    (xVal-widthTab/2,yVal+heightTab+diffHeightTab),
                    (xVal-widthTab/2,yVal),
                    (xVal+widthTab/2,yVal),
                    (xVal+widthTab/2,yVal+heightTab-diffHeightTab)
                ])

    return (xValSave,yValSave)
