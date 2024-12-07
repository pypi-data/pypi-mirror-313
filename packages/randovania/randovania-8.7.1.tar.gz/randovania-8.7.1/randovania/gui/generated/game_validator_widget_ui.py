# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_validator_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_GameValidatorWidget(object):
    def setupUi(self, GameValidatorWidget):
        if not GameValidatorWidget.objectName():
            GameValidatorWidget.setObjectName(u"GameValidatorWidget")
        GameValidatorWidget.resize(758, 558)
        self.root_layout = QGridLayout(GameValidatorWidget)
        self.root_layout.setSpacing(6)
        self.root_layout.setContentsMargins(11, 11, 11, 11)
        self.root_layout.setObjectName(u"root_layout")
        self.verbosity_label = QLabel(GameValidatorWidget)
        self.verbosity_label.setObjectName(u"verbosity_label")

        self.root_layout.addWidget(self.verbosity_label, 3, 0, 1, 1)

        self.verbosity_combo = QComboBox(GameValidatorWidget)
        self.verbosity_combo.addItem("")
        self.verbosity_combo.addItem("")
        self.verbosity_combo.addItem("")
        self.verbosity_combo.addItem("")
        self.verbosity_combo.setObjectName(u"verbosity_combo")

        self.root_layout.addWidget(self.verbosity_combo, 3, 1, 1, 1)

        self.status_label = QLabel(GameValidatorWidget)
        self.status_label.setObjectName(u"status_label")

        self.root_layout.addWidget(self.status_label, 3, 2, 1, 1)

        self.start_button = QPushButton(GameValidatorWidget)
        self.start_button.setObjectName(u"start_button")

        self.root_layout.addWidget(self.start_button, 3, 3, 1, 1)

        self.log_widget = QTreeWidget(GameValidatorWidget)
        QTreeWidgetItem(self.log_widget)
        QTreeWidgetItem(self.log_widget)
        self.log_widget.setObjectName(u"log_widget")
        self.log_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.log_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.log_widget.setTextElideMode(Qt.ElideNone)
        self.log_widget.header().setStretchLastSection(True)

        self.root_layout.addWidget(self.log_widget, 2, 0, 1, 4)


        self.retranslateUi(GameValidatorWidget)

        self.verbosity_combo.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(GameValidatorWidget)
    # setupUi

    def retranslateUi(self, GameValidatorWidget):
        GameValidatorWidget.setWindowTitle(QCoreApplication.translate("GameValidatorWidget", u"Game Validator", None))
        self.verbosity_label.setText(QCoreApplication.translate("GameValidatorWidget", u"<html><head/><body><p>Log Verbosity</p></body></html>", None))
        self.verbosity_combo.setItemText(0, QCoreApplication.translate("GameValidatorWidget", u"Silent", None))
        self.verbosity_combo.setItemText(1, QCoreApplication.translate("GameValidatorWidget", u"Normal", None))
        self.verbosity_combo.setItemText(2, QCoreApplication.translate("GameValidatorWidget", u"High", None))
        self.verbosity_combo.setItemText(3, QCoreApplication.translate("GameValidatorWidget", u"Extreme", None))

        self.status_label.setText(QCoreApplication.translate("GameValidatorWidget", u"Not started", None))
        self.start_button.setText(QCoreApplication.translate("GameValidatorWidget", u"Start", None))
        ___qtreewidgetitem = self.log_widget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("GameValidatorWidget", u"Steps", None));

        __sortingEnabled = self.log_widget.isSortingEnabled()
        self.log_widget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.log_widget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("GameValidatorWidget", u"To view the playthrough, it's necessary to run the solver.", None));
        ___qtreewidgetitem2 = self.log_widget.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("GameValidatorWidget", u"Press the Start button at the bottom-right and wait for it to finish.", None));
        self.log_widget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

