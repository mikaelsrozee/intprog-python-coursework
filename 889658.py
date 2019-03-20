# ==============================================================================
# INTPROG Python Assignment 2018 by Mikael Rozee
# ==============================================================================

from graphics import *

VALID_SIZES = [5, 7, 9]
VALID_COLOURS = ["red", "green", "blue", "magenta", "orange", "pink"]
COLOUR_KEYS = ["r", "g", "b", "m", "o", "p"]


def main():
    size, colourA, colourB, colourC = getInputs()   # Get inputs from the user, store them as variables.
    win = GraphWin("Patchwork", size * 100, size * 100)     # Create graphics window
    patchSize = int(win.getWidth() / size)  # Calculate the size of each patch

    # Create two empty 2D arrays that will store patches and colours later on.
    patchGrid = []
    colourGrid = []
    for i in range(size):
        patchGrid.append([])
        colourGrid.append([])
    for val in patchGrid:
        for i in range(size):
            val.append([])
    for val in colourGrid:
        for i in range(size):
            val.append([])

    # Draw patches
    for i in range(size):  # Iterate by column
        colour = colourC
        if i % 2 == 0:  # Alternate colours between columns
            colour = colourA

        penultimatePatches, penultimatePoses = drawPatchGrid(win, "penultimate", i, i, 1, size - i, colour, patchSize)

        for patch in penultimatePatches:
            index = penultimatePatches.index(patch)
            gridPos = penultimatePoses[index]
            x = gridPos[0] // patchSize
            y = gridPos[1] // patchSize
            patchGrid[x][y] = patch
            colourGrid[x][y] = colour

        if i > 0:  # Draw 'final' pattern in all but the first column
            finalPatches, finalPoses = drawPatchGrid(win, "final", i, i - 1, size - i, 1, colourB, patchSize)
            for patch in finalPatches:
                index = finalPatches.index(patch)
                gridPos = finalPoses[index]
                x = gridPos[0] // patchSize
                y = gridPos[1] // patchSize
                patchGrid[x][y] = patch
                colourGrid[x][y] = colourB

    # Extra challenge code
    handleKeyPresses(win, patchSize, patchGrid, colourGrid)


def getInputs():
    size = input("Enter patchwork size:")
    while not size.isnumeric() or int(size) not in VALID_SIZES:  # If size was not valid, ask for input until it is.
        if not size.isnumeric():
            print("[ERROR] Please enter a numeric value.")
        else:
            print("[ERROR] Non-valid size. Valid sizes are", VALID_SIZES)
        size = input("Enter patchwork size:")
    size = int(size)

    usedColours = []

    colourA = input("Enter first colour:")
    while colourA not in VALID_COLOURS:  # If colourA was not valid, ask for input.
        print("[ERROR] Please enter a valid colour. Valid colours are", VALID_COLOURS)
        colourA = input("Enter first colour:")
    usedColours.append(colourA)

    colourB = input("Enter second colour:")
    while colourB not in VALID_COLOURS or colourB in usedColours:  # If colourB was not valid, ask for input.
        print("[ERROR] Please enter a valid colour that has not been used already. Valid colours are", VALID_COLOURS)
        colourB = input("Enter second colour:")
    usedColours.append(colourB)

    colourC = input("Enter third colour:")
    while colourC not in VALID_COLOURS or colourC in usedColours:  # If colourC was not valid, ask for input.
        print("[ERROR] Please enter a valid colour that has not been used already. Valid colours are", VALID_COLOURS)
        colourC = input("Enter third colour:")
    usedColours.append(colourC)

    return size, colourA, colourB, colourC


def drawChevron(win, x, y, fill, outline, size):
    points = [Point(x, y), Point(x + size / 2, y + size / 2), Point(x + size, y), Point(x + size, y + size / 2),
              Point(x + size / 2, y + size), Point(x, y + size / 2), Point(x, y)]
    chevron = Polygon(points)
    chevron.setOutline(outline)
    chevron.setFill(fill)
    chevron.draw(win)
    return chevron


def drawPenultimateDigitPatch(win, x, y, fill, size):
    parts = []
    xPos = x * size
    yPos = y * size
    chevronSize = int(size / 5)
    for row in range(5):
        for col in range(5):
            parts.append(drawChevron(win, xPos + row * chevronSize, yPos + col * chevronSize, fill, fill,
                                     chevronSize))
    parts.append(drawChevron(win, xPos + chevronSize, yPos + chevronSize, "white", fill, chevronSize))
    parts.append(drawChevron(win, xPos + 3 * chevronSize, yPos + chevronSize, "white", fill, chevronSize))
    parts.append(drawChevron(win, xPos + chevronSize, yPos + 3 * chevronSize, "white", fill, chevronSize))
    parts.append(drawChevron(win, xPos + 3 * chevronSize, yPos + 3 * chevronSize, "white", fill, chevronSize))

    return parts


def drawFinalDigitPatch(win, x, y, fill, size):
    xPos = x * size
    yPos = y * size
    lines = []
    for i in range(0, size, size // 5):
        lines.append(Line(Point(i + xPos, yPos), Point(size + xPos, size - i + yPos)))
        lines.append(Line(Point(xPos, i + yPos), Point(size - i + xPos, size + yPos)))
        lines.append(Line(Point(i + xPos, yPos), Point(xPos, i + yPos)))
        lines.append(Line(Point(size + xPos, i + yPos), Point(i + xPos, size + yPos)))
    for line in lines:
        line.setOutline(fill)
        line.draw(win)
    return lines


def drawPatchGrid(win, patch_type, x, y, width, height, fill, size):
    patches = []
    poses = []
    for row in range(width):
        for col in range(height):
            xPos = x + row
            yPos = y + col
            if patch_type == "penultimate":
                patches.append(drawPenultimateDigitPatch(win, xPos, yPos, fill, size))
                poses.append([xPos * size, yPos * size])
            elif patch_type == "final":
                patches.append(drawFinalDigitPatch(win, xPos, yPos, fill, size))
                poses.append([xPos * size, yPos * size])
    return patches, poses


def drawSelector(win, x, y, patch_size):
    xPos = int(x // patch_size) * patch_size
    yPos = int(y // patch_size) * patch_size

    selector = Rectangle(Point(xPos, yPos), Point(xPos + patch_size, yPos + patch_size))
    selector.setOutline("black")
    selector.setWidth(5)
    selector.draw(win)
    return selector


def undrawPatch(patch):
    for part in patch:
        part.undraw()


def handleKeyPresses(win, patch_size, patch_grid, colour_grid):
    selectedPos = None
    selector = None
    while win.isOpen():
        if selectedPos is None:
            selectedPos = win.getMouse()
            selector = drawSelector(win, selectedPos.getX(), selectedPos.getY(), patch_size)
        else:
            key = win.getKey().lower()
            xPos = int(selectedPos.getX() // patch_size)
            yPos = int(selectedPos.getY() // patch_size)
            if key == "d" and patch_grid[xPos][yPos] is not None:  # Delete the patch
                undrawPatch(patch_grid[xPos][yPos])
                patch_grid[xPos][yPos] = None
                colour_grid[xPos][yPos] = None
                selector.undraw()
                selector = drawSelector(win, selectedPos.getX(), selectedPos.getY(), patch_size)
            elif key == "s" and patch_grid[xPos][yPos] is not None:  # Switch the patch
                if type(patch_grid[xPos][yPos][0]) == Polygon:
                    undrawPatch(patch_grid[xPos][yPos])
                    patch = drawFinalDigitPatch(win, xPos, yPos, colour_grid[xPos][yPos], patch_size)
                    patch_grid[xPos][yPos] = patch
                elif type(patch_grid[xPos][yPos][0]) == Line:
                    undrawPatch(patch_grid[xPos][yPos])
                    patch = drawPenultimateDigitPatch(win, xPos, yPos, colour_grid[xPos][yPos], patch_size)
                    patch_grid[xPos][yPos] = patch
                selector.undraw()
                selector = drawSelector(win, selectedPos.getX(), selectedPos.getY(), patch_size)
            elif patch_grid[xPos][yPos] is None and key in COLOUR_KEYS:  # Draw coloured final patch
                index = COLOUR_KEYS.index(key)
                patch = drawFinalDigitPatch(win, xPos, yPos, VALID_COLOURS[index], patch_size)
                patch_grid[xPos][yPos] = patch
                colour_grid[xPos][yPos] = VALID_COLOURS[index]
                selector.undraw()
                selector = drawSelector(win, selectedPos.getX(), selectedPos.getY(), patch_size)
            elif key == "return":   # Deselect the patch
                selector.undraw()
                selectedPos = None


main()
