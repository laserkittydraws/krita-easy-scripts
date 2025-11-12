from krita import *
from PyQt5.QtCore import QPointF, QByteArray
from PyQt5.QtWidgets import QAction


def copyAndFlipHorizontally():
    activeDoc = krita.Krita.instance().activeDocument()
    activeNode = activeDoc.activeNode()

    if activeNode.type() != 'paintlayer':
        return

    activeNodeHasKeyframeAtCurrentTime: bool = activeNode.hasKeyframeAtTime(activeDoc.currentTime())
    if activeNode.animated() and not activeNodeHasKeyframeAtCurrentTime:
        return # avoid unintended changes on a different keyframe

    krita.Krita.instance().action('copy_selection_to_new_layer').activate(QAction.Trigger)

    if activeNode.animated() and activeNodeHasKeyframeAtCurrentTime:
        newNode = activeNode.parentNode().childNodes()[activeNode.index()+1]
        newNodeBounds = [newNode.bounds().x(), newNode.bounds().y(), newNode.bounds().width(), newNode.bounds().height()]
        newNodeCenter = QPointF(newNode.bounds().x() + newNode.bounds().width()/2, newNode.bounds().y() + newNode.bounds().height()/2)


        # move newNode layer's keyframe from frame 0 to current frame
        #   so that when merging newNode back down into activeNode,
        #   no unintended pixels merged onto other keyframes

        # uncomment if copy_selection_to_new_layer doesn't set newNode as active node
        # activeDoc.setActiveNode(newNode)

        currFrame = activeDoc.currentTime()
        copiedPixelData: QByteArray = newNode.pixelDataAtTime(*newNodeBounds, 0)

        # new keyframe at current frame
        krita.Krita.instance().action('add_blank_frame').activate(QAction.Trigger)
        newNode.setPixelData(copiedPixelData, *newNodeBounds)

        # remove keyframe at frame 0
        activeDoc.setCurrentTime(0)
        krita.Krita.instance().action('remove_frames').activate(QAction.Trigger)
        activeDoc.setCurrentTime(currFrame)


    else: # non-animated paintlayer
        newNode = activeNode.parentNode().childNodes()[activeNode.index()+1]
        newNodeCenter = QPointF(newNode.bounds().x() + newNode.bounds().width()/2, newNode.bounds().y() + newNode.bounds().height()/2)
        newNode.scaleNode(
            # center of selection
            newNodeCenter,
            -newNode.bounds().width(), # mirror horizontally
            newNode.bounds().height(),
            'Bicubic'
        )
        activeDoc.setActiveNode(newNode)

    krita.Krita.instance().action('KritaTransform/KisToolMove').activate(QAction.Trigger)
    activeDoc.refreshProjection()



def copyAndFlipVertically():
    activeDoc = krita.Krita.instance().activeDocument()
    activeNode = activeDoc.activeNode()

    krita.Krita.instance().action('copy_selection_to_new_layer').activate(QAction.Trigger)

    newNode = activeNode.parentNode().childNodes()[activeNode.index()+1]
    newNode.scaleNode(
        # center of selection
        QPointF(
            newNode.bounds().x() + newNode.bounds().width()/2,
            newNode.bounds().y() + newNode.bounds().height()/2
        ),
        newNode.bounds().width(),
        -newNode.bounds().height(), # mirror vertically
        'Bicubic'
    )

    activeDoc.setActiveNode(newNode)
    krita.Krita.instance().action('KritaTransform/KisToolMove').activate(QAction.Trigger)

    activeDoc.refreshProjection()