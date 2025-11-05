from krita import *
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QAction


def copyAndFlipHorizontally():
    activeDoc = krita.Krita.instance().activeDocument()
    activeNode = activeDoc.activeNode()

    krita.Krita.instance().action('copy_selection_to_new_layer').activate(QAction.Trigger)

    if activeNode.animated():
        activFrame = activeDoc.currentTime()

    newNode = activeNode.parentNode().childNodes()[activeNode.index()+1]
    newNode.scaleNode(
        # center of selection
        QPointF(
            newNode.bounds().x() + newNode.bounds().width()/2,
            newNode.bounds().y() + newNode.bounds().height()/2
        ),
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