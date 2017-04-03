# Selector toolbar for FreeCAD
# Copyright (C) 2015, 2016 (as part of TabBar) triplus @ FreeCAD
# Copyright (C) 2017 triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""Selector toolbar for FreeCAD."""

# Create toolbar.
pathTB = "User parameter:BaseApp/Workbench/Global/Toolbar/Selector"
pTB = FreeCAD.ParamGet(pathTB)
pTB.SetString("Name", "Selector")
pTB.SetBool("Active", 1)


def selectorToolbar():
    """Selector toolbar for FreeCAD."""

    import FreeCAD as App
    import FreeCADGui as Gui
    from PySide import QtCore
    from PySide import QtGui

    actions = {}
    mw = Gui.getMainWindow()
    group = QtGui.QActionGroup(mw)
    dList = "ArchWorkbench,PartDesignWorkbench"
    p = App.ParamGet("User parameter:BaseApp/SelectorToolbar")

    aMenu = QtGui.QAction(mw)
    sMenu = QtGui.QMenu()
    aMenu.setMenu(sMenu)

    def onSelector(a):
        """Activate workbench on selection."""

        Gui.doCommand('Gui.activateWorkbench("' + a.data() + '")')

    def wbIcon(i):
        """Create workbench icon."""

        if str(i.find("XPM")) != "-1":

            icon = []

            for a in ((((i
                         .split('{', 1)[1])
                        .rsplit('}', 1)[0])
                       .strip())
                      .split("\n")):
                icon.append((a
                             .split('"', 1)[1])
                            .rsplit('"', 1)[0])

            icon = QtGui.QIcon(QtGui.QPixmap(icon))
        else:
            icon = QtGui.QIcon(QtGui.QPixmap(i))

        if icon.isNull():
            icon = QtGui.QIcon.fromTheme("freecad")
        else:
            pass

        return icon

    def wbActions():
        """Create workbench actions."""

        wbList = Gui.listWorkbenches()

        for i in wbList:
            if i and i not in actions:
                action = QtGui.QAction(group)
                action.setCheckable(True)
                action.setText(wbList[i].MenuText)
                action.setData(i)

                try:
                    action.setIcon(wbIcon(wbList[i].Icon))
                except:
                    action.setIcon(QtGui.QIcon.fromTheme("freecad"))

                actions[i] = action
            else:
                pass

    def onOrientationChanged():
        """Style buttons based on the toolbar orientation."""

        tb = mw.findChild(QtGui.QToolBar, "Selector")

        if tb:
            if tb.orientation() == QtCore.Qt.Orientation.Horizontal:
                for b in tb.findChildren(QtGui.QToolButton):
                    b.setProperty("toolbar_orientation", "horizontal")
                    b.style().polish(b)
            else:
                for b in tb.findChildren(QtGui.QToolButton):
                    b.setProperty("toolbar_orientation", "vertical")
                    b.style().polish(b)
        else:
            pass

    def onStyle():
        """Manage the toolbutton style."""

        tb = mw.findChild(QtGui.QToolBar, "Selector")

        if tb:
            if p.GetString("Style") == "IconText":
                tb.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            elif p.GetString("Style") == "Text":
                tb.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
            else:
                tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        else:
            pass

    def selectorMenu():
        """Selector button with menu."""

        sMenu.clear()
        active = Gui.activeWorkbench().__class__.__name__

        keys = list(actions)
        keys.sort()

        for key in keys:
            sMenu.addAction(actions[key])
            if key == active:
                sMenu.setDefaultAction(actions[key])
                aMenu.setText(actions[key].text())
                aMenu.setIcon(actions[key].icon())
            else:
                pass

    def onWorkbenchActivated():
        """Populate the selector toolbar."""

        wbActions()
        selectorMenu()

        menu = p.GetString("Menu")
        enabled = p.GetString("Enabled", dList)
        enabled = enabled.split(",")
        active = Gui.activeWorkbench().__class__.__name__

        if active not in enabled:
            enabled.append(active)
        else:
            pass

        tb = mw.findChild(QtGui.QToolBar, "Selector")

        if tb:
            tb.clear()

            if menu == "Front" or menu == "End" and active in enabled:
                enabled.remove(active)
            else:
                pass

            if menu == "Front":
                tb.addAction(aMenu)
                w = tb.widgetForAction(aMenu)
                w.setPopupMode(QtGui.QToolButton
                               .ToolButtonPopupMode
                               .InstantPopup)
            else:
                pass

            for i in enabled:
                for key in actions:
                    if i == actions[key].data():
                        a = actions[key]
                        tb.addAction(a)
                        if active == a.data():
                            group.blockSignals(True)
                            a.setChecked(True)
                            group.blockSignals(False)
                        else:
                            pass
                    else:
                        pass

            if menu == "End":
                tb.addAction(aMenu)
                w = tb.widgetForAction(aMenu)
                w.setPopupMode(QtGui.QToolButton
                               .ToolButtonPopupMode
                               .InstantPopup)
            else:
                pass
        else:
            pass

    def prefDialog():
        """Preferences dialog."""

        dialog = QtGui.QDialog(mw)
        dialog.resize(800, 450)
        dialog.setWindowTitle("Selector toolbar")

        layout = QtGui.QVBoxLayout()
        dialog.setLayout(layout)

        selector = QtGui.QListWidget(dialog)
        selector.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        btnClose = QtGui.QPushButton("Close", dialog)
        btnClose.setToolTip("Close the preferences dialog")
        btnClose.setDefault(True)

        btnUp = QtGui.QToolButton(dialog)
        btnUp.setToolTip("Move selected item up")
        btnUp.setArrowType(QtCore.Qt.UpArrow)

        btnDown = QtGui.QToolButton(dialog)
        btnDown.setToolTip("Move selected item down")
        btnDown.setArrowType(QtCore.Qt.DownArrow)

        l0 = QtGui.QVBoxLayout()
        g0 = QtGui.QGroupBox("Style:")
        g0.setLayout(l0)

        r0 = QtGui.QRadioButton("Icon", g0)
        r0.setObjectName("Icon")
        r0.setToolTip("Toolbar button icon style")
        r1 = QtGui.QRadioButton("Text", g0)
        r1.setObjectName("Text")
        r1.setToolTip("Toolbar button text style")
        r2 = QtGui.QRadioButton("Icon and text", g0)
        r2.setObjectName("IconText")
        r2.setToolTip("Toolbar button icon and text style")

        l0.addWidget(r0)
        l0.addWidget(r1)
        l0.addWidget(r2)

        l1 = QtGui.QVBoxLayout()
        g1 = QtGui.QGroupBox("Menu:")
        g1.setLayout(l1)

        r3 = QtGui.QRadioButton("Disabled", g1)
        r3.setObjectName("Off")
        r3.setToolTip("Disable selector menu")
        r4 = QtGui.QRadioButton("Front", g1)
        r4.setObjectName("Front")
        r4.setToolTip("Selector menu at front")
        r5 = QtGui.QRadioButton("End", g1)
        r5.setObjectName("End")
        r5.setToolTip("Selector menu at end")

        l1.addWidget(r3)
        l1.addWidget(r4)
        l1.addWidget(r5)

        l2 = QtGui.QHBoxLayout()
        l2.addWidget(btnUp)
        l2.addWidget(btnDown)
        l2.addStretch(1)
        l2.addWidget(btnClose)

        l3 = QtGui.QHBoxLayout()
        l3.addStretch()

        l4 = QtGui.QVBoxLayout()
        l4.addWidget(g0)
        l4.addWidget(g1)
        l4.addStretch()
        l4.insertLayout(0, l3)

        l5 = QtGui.QHBoxLayout()
        l5.addWidget(selector)
        l5.insertLayout(1, l4)

        layout.insertLayout(0, l5)
        layout.insertLayout(1, l2)

        def onAccepted():
            """Close dialog on button close."""

            dialog.done(1)

        def onFinished():
            """Delete dialog on close."""

            dialog.deleteLater()

        def onItemChanged():
            """Save enabled workbenches list."""

            item = []

            for index in range(selector.count()):
                if selector.item(index).checkState() == QtCore.Qt.Checked:
                    item.append(selector.item(index).data(32))
                else:
                    pass

            p.SetString("Enabled", ",".join(item))

            onWorkbenchActivated()

        def onUp():
            """Save workbench position list."""

            currentIndex = selector.currentRow()

            print currentIndex

            if currentIndex != 0:
                currentItem = selector.takeItem(currentIndex)
                selector.insertItem(currentIndex - 1, currentItem)
                selector.setCurrentRow(currentIndex - 1)

                position = []

                for index in range(selector.count()):
                    position.append(selector.item(index).data(32))

                p.SetString("Position", ",".join(position))
            else:
                pass

            onItemChanged()

        def onDown():
            """Save workbench position list."""

            currentIndex = selector.currentRow()

            if currentIndex != selector.count() - 1 and currentIndex != -1:
                currentItem = selector.takeItem(currentIndex)
                selector.insertItem(currentIndex + 1, currentItem)
                selector.setCurrentRow(currentIndex + 1)

                position = []

                for index in range(selector.count()):
                    position.append(selector.item(index).data(32))

                p.SetString("Position", ",".join(position))
            else:
                pass

            onItemChanged()

        def onG0(r):
            """Set toolbar button style."""

            if r:
                for i in g0.findChildren(QtGui.QRadioButton):
                    if i.isChecked():
                        p.SetString("Style", i.objectName())
                    else:
                        pass
            else:
                pass

            onStyle()
            onWorkbenchActivated()

        def onG1(r):
            """Manage the selector menu."""

            if r:
                for i in g1.findChildren(QtGui.QRadioButton):
                    if i.isChecked():
                        p.SetString("Menu", i.objectName())
                    else:
                        pass
            else:
                pass

            onWorkbenchActivated()

        enabled = p.GetString("Enabled", dList)
        enabled = enabled.split(",")

        position = p.GetString("Position")

        if not position:
            selector.setSortingEnabled(True)
            selector.sortItems(QtCore.Qt.AscendingOrder)
        else:
            pass

        position = position.split(",")

        for i in actions:
            if actions[i].data() not in position:
                position.append(actions[i].data())
            else:
                pass

        for i in position:
            if i in actions:
                item = QtGui.QListWidgetItem(selector)
                item.setText(actions[i].text())
                item.setIcon(actions[i].icon())
                item.setData(32, actions[i].data())

                if actions[i].data() in enabled:
                    item.setCheckState(QtCore.Qt.CheckState(2))
                else:
                    item.setCheckState(QtCore.Qt.CheckState(0))
            else:
                pass

        selector.setSortingEnabled(False)

        style = p.GetString("Style")

        if style == "Text":
            r1.setChecked(True)
        elif style == "IconText":
            r2.setChecked(True)
        else:
            r0.setChecked(True)

        menu = p.GetString("Menu")

        if menu == "Front":
            r4.setChecked(True)
        elif style == "End":
            r5.setChecked(True)
        else:
            r3.setChecked(True)

        r0.toggled.connect(onG0)
        r1.toggled.connect(onG0)
        r2.toggled.connect(onG0)
        r3.toggled.connect(onG1)
        r4.toggled.connect(onG1)
        r5.toggled.connect(onG1)
        btnUp.clicked.connect(onUp)
        btnDown.clicked.connect(onDown)
        selector.itemChanged.connect(onItemChanged)
        dialog.finished.connect(onFinished)
        btnClose.clicked.connect(onAccepted)

        return dialog

    def onPreferences():
        """Open the preferences dialog."""

        dialog = prefDialog()
        dialog.show()

    def onClose():
        """Remove the toolbar on FreeCAD close."""

        path = "User parameter:BaseApp/Workbench/Global/Toolbar"
        p = App.ParamGet(path)
        p.RemGroup("Selector")

    def accessoriesMenu():
        """Add selector toolbar preferences to accessories menu."""

        mw = Gui.getMainWindow()
        pref = QtGui.QAction(mw)
        pref.setText("Selector toolbar")
        pref.setObjectName("SelectorToolbar")
        pref.triggered.connect(onPreferences)

        try:
            import AccessoriesMenu
            AccessoriesMenu.addItem("SelectorToolbar")
        except ImportError:
            a = mw.findChild(QtGui.QAction, "AccessoriesMenu")

            if a:
                a.menu().addAction(pref)
            else:
                actionAccessories = QtGui.QAction(mw)
                actionAccessories.setObjectName("AccessoriesMenu")
                actionAccessories.setIconText("Accessories")
                menu = QtGui.QMenu(mw)
                actionAccessories.setMenu(menu)
                menu.addAction(pref)

                def addMenu():
                    """Add accessories menu to the menubar."""

                    mb = mw.menuBar()

                    toolsMenu = mb.findChild(QtGui.QMenu, "&Tools")

                    if toolsMenu:
                        toolsMenu.addAction(actionAccessories)
                    else:
                        pass

                addMenu()
                mw.workbenchActivated.connect(addMenu)

    accessoriesMenu()
    onWorkbenchActivated()

    tb = mw.findChild(QtGui.QToolBar, "Selector")

    if tb:
        tb.orientationChanged.connect(onOrientationChanged)
    else:
        pass

    group.triggered.connect(onSelector)
    mw.mainWindowClosed.connect(onClose)
    mw.workbenchActivated.connect(onWorkbenchActivated)

# Selector toolbar start
import SelectorToolbarPath

t = SelectorToolbarPath.timer()
t.setSingleShot(True)
t.timeout.connect(selectorToolbar)
t.start()