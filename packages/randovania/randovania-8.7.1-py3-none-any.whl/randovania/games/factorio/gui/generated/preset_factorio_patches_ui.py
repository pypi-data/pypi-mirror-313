# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_factorio_patches.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetFactorioPatches(object):
    def setupUi(self, PresetFactorioPatches):
        if not PresetFactorioPatches.objectName():
            PresetFactorioPatches.setObjectName(u"PresetFactorioPatches")
        PresetFactorioPatches.resize(466, 552)
        self.centralWidget = QWidget(PresetFactorioPatches)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.root_layout = QVBoxLayout(self.centralWidget)
        self.root_layout.setSpacing(6)
        self.root_layout.setContentsMargins(11, 11, 11, 11)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(4, 4, 4, 4)
        self.full_tech_tree_check = QCheckBox(self.centralWidget)
        self.full_tech_tree_check.setObjectName(u"full_tech_tree_check")
        self.full_tech_tree_check.setEnabled(True)

        self.root_layout.addWidget(self.full_tech_tree_check)

        self.full_tech_tree_label = QLabel(self.centralWidget)
        self.full_tech_tree_label.setObjectName(u"full_tech_tree_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.full_tech_tree_label.sizePolicy().hasHeightForWidth())
        self.full_tech_tree_label.setSizePolicy(sizePolicy)
        self.full_tech_tree_label.setMaximumSize(QSize(16777215, 60))
        self.full_tech_tree_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.full_tech_tree_label.setWordWrap(True)
        self.full_tech_tree_label.setOpenExternalLinks(True)

        self.root_layout.addWidget(self.full_tech_tree_label)

        self.full_tech_tree_line = QFrame(self.centralWidget)
        self.full_tech_tree_line.setObjectName(u"full_tech_tree_line")
        self.full_tech_tree_line.setFrameShape(QFrame.Shape.HLine)
        self.full_tech_tree_line.setFrameShadow(QFrame.Shadow.Sunken)

        self.root_layout.addWidget(self.full_tech_tree_line)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.root_layout.addItem(self.vertical_spacer)

        PresetFactorioPatches.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetFactorioPatches)

        QMetaObject.connectSlotsByName(PresetFactorioPatches)
    # setupUi

    def retranslateUi(self, PresetFactorioPatches):
        PresetFactorioPatches.setWindowTitle(QCoreApplication.translate("PresetFactorioPatches", u"Other", None))
        self.full_tech_tree_check.setText(QCoreApplication.translate("PresetFactorioPatches", u"Full Tech Tree", None))
        self.full_tech_tree_label.setText(QCoreApplication.translate("PresetFactorioPatches", u"<html><head/><body><p>Include checks for every single tier of the damage and speed upgrades. When unchecked only the first two tiers are used.</p></body></html>", None))
    # retranslateUi

