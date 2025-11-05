from krita import *

from .scripts import copyAndFlipHorizontally, copyAndFlipVertically

class KritaEasyScriptsExtension(Extension):

    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        copyFlipH = window.createAction("kes_DupAndFlipSelectionH", "Krita Easy Scripts", "tools/scripts")
        copyFlipH.triggered.connect(copyAndFlipHorizontally)
        
        copyFlipV = window.createAction("kes_DupAndFlipSelectionV", "Krita Easy Scripts", "tools/scripts")
        copyFlipV.triggered.connect(copyAndFlipVertically)

# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(KritaEasyScriptsExtension(Krita.instance()))
