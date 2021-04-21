# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSString
from AppKit import NSColor, NSBezierPath
import math
import traceback

COLOR = 0, .6, 1, 0.75

class ShowNodeCountInCorner( ReporterPlugin ):

	@objc.python_method
	def settings(self):
		try:
			self.menuName = Glyphs.localize({
				'en': "Node Count In Corner",
			})
			
			# print(self.menuName, "Version 1.0.5")
			self.thisMenuTitle = {"name": u"%s:" % self.menuName, "action": None }
			self.vID = "com.wwwhhhhh.ShowNodeCountInCorner" # vendorID
			Glyphs.registerDefault( "%s.fontSize"%self.vID, 10 )

		except:
			print(traceback.format_exc())

	@objc.python_method
	def foregroundInViewCoords(self, layer=None):
		if not layer:
			layer = self.controller.activeLayer()
		if layer:
			try:
				self.drawNodeCountText( layer )
			except:
				print(traceback.format_exc())

	# @objc.python_method
	# def background(self, layer):
	# 	try:
	# 		try:
	# 			selection = layer.selection
	# 		except:
	# 			selection = layer.selection()
	# 		if len(selection) == 2:
	# 			if hasattr(selection[0], "component"):
	# 				x1, y1 = selection[0].bounds.origin.x + selection[0].bounds.size.width/2, selection[0].bounds.origin.y + selection[0].bounds.size.height/2
	# 			else:
	# 				x1, y1 = selection[0].x, selection[0].y
	# 			if hasattr(selection[1], "component"):
	# 				x2, y2 = selection[1].bounds.origin.x + selection[1].bounds.size.width/2, selection[1].bounds.origin.y + selection[1].bounds.size.height/2
	# 			else:
	# 				x2, y2 = selection[1].x, selection[1].y

	# 			toolEventHandler = self.controller.view().window().windowController().toolEventHandler()

	# 			toolIsTextTool = toolEventHandler.className() == "GlyphsToolText"
	# 			toolIsToolHand = toolEventHandler.className() == "GlyphsToolHand"

	# 			currentController = self.controller.view().window().windowController()
	# 			if currentController:
	# 				if not toolIsTextTool and not toolIsToolHand:
	# 					self.drawLine(x1, y1, x2, y2)
	# 	except:
	# 		print(traceback.format_exc())

	@objc.python_method
	def drawNodeCountText( self, layer ):
		if layer is None:
			return
		try:
			Glyph = layer.parent
			Font = Glyph.parent
			selectedLayer = Font.selectedLayers[0]

			xHeight = Font.selectedFontMaster.xHeight
			angle = Font.selectedFontMaster.italicAngle
			# rotation point is half of x-height
			offset = math.tan(math.radians(angle)) * xHeight/2

			nodeCounter = 0
			for thisPath in selectedLayer.paths:
				nodeCounter += len(thisPath.nodes)

			self.drawText( u"· %s" % nodeCounter)
		except:
			print(traceback.format_exc())
			pass

	@objc.python_method
	def drawText( self, text, fontColor=NSColor.whiteColor() ):
		try:
			fontSize = Glyphs.defaults["%s.fontSize"%self.vID]

			fontAttributes = { 
				#NSFontAttributeName: NSFont.labelFontOfSize_(10.0),
				NSFontAttributeName: NSFont.monospacedDigitSystemFontOfSize_weight_(fontSize,0.0),
				NSForegroundColorAttributeName: NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.5, 0.5, 0.5, 1 )
			}
			
			displayText = NSAttributedString.alloc().initWithString_attributes_(text, fontAttributes)
			textAlignment = 2  # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			upperRightCorner = NSPoint( self.controller.viewPort.origin.x + self.controller.viewPort.size.width - 5 , self.controller.viewPort.origin.y + self.controller.viewPort.size.height - 16)
			displayText.drawAtPoint_alignment_(upperRightCorner, textAlignment)
		except:
			print(traceback.format_exc())

	def needsExtraMainOutlineDrawingForInactiveLayer_( self, layer ):
		return True

	@objc.python_method
	def RefreshView(self):
		try:
			Glyphs = NSApplication.sharedApplication()
			currentTabView = Glyphs.font.currentTab
			if currentTabView:
				currentTabView.graphicView().setNeedsDisplay_(True)
		except:
			pass

	@objc.python_method
	def getScale( self ):
		try:
			return self._scale
		except:
			return 1 # Attention, just for debugging!

	@objc.python_method
	def logToConsole( self, message ):
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
