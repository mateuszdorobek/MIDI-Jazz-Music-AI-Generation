/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.12.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QListWidget>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include "widget.h"

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    Widget *imageWidget;
    QWidget *layoutWidget;
    QVBoxLayout *verticalLayout;
    QSlider *sliderProgress;
    QHBoxLayout *horizontalLayout;
    QPushButton *buttonPlay;
    QPushButton *buttonStop;
    QLabel *label;
    QSlider *sliderVolume;
    QListWidget *listWidget;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(682, 508);
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindow->sizePolicy().hasHeightForWidth());
        MainWindow->setSizePolicy(sizePolicy);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        imageWidget = new Widget(centralWidget);
        imageWidget->setObjectName(QString::fromUtf8("imageWidget"));
        imageWidget->setGeometry(QRect(270, 10, 400, 400));
        layoutWidget = new QWidget(centralWidget);
        layoutWidget->setObjectName(QString::fromUtf8("layoutWidget"));
        layoutWidget->setGeometry(QRect(270, 420, 401, 61));
        verticalLayout = new QVBoxLayout(layoutWidget);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        sliderProgress = new QSlider(layoutWidget);
        sliderProgress->setObjectName(QString::fromUtf8("sliderProgress"));
        sliderProgress->setPageStep(100);
        sliderProgress->setOrientation(Qt::Horizontal);

        verticalLayout->addWidget(sliderProgress);

        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setSpacing(6);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        buttonPlay = new QPushButton(layoutWidget);
        buttonPlay->setObjectName(QString::fromUtf8("buttonPlay"));

        horizontalLayout->addWidget(buttonPlay);

        buttonStop = new QPushButton(layoutWidget);
        buttonStop->setObjectName(QString::fromUtf8("buttonStop"));

        horizontalLayout->addWidget(buttonStop);

        label = new QLabel(layoutWidget);
        label->setObjectName(QString::fromUtf8("label"));

        horizontalLayout->addWidget(label);

        sliderVolume = new QSlider(layoutWidget);
        sliderVolume->setObjectName(QString::fromUtf8("sliderVolume"));
        sliderVolume->setValue(99);
        sliderVolume->setOrientation(Qt::Horizontal);

        horizontalLayout->addWidget(sliderVolume);


        verticalLayout->addLayout(horizontalLayout);

        listWidget = new QListWidget(centralWidget);
        listWidget->setObjectName(QString::fromUtf8("listWidget"));
        listWidget->setGeometry(QRect(15, 11, 251, 471));
        listWidget->setHorizontalScrollBarPolicy(Qt::ScrollBarAsNeeded);
        listWidget->setAutoScroll(false);
        listWidget->setVerticalScrollMode(QAbstractItemView::ScrollPerPixel);
        listWidget->setHorizontalScrollMode(QAbstractItemView::ScrollPerPixel);
        MainWindow->setCentralWidget(centralWidget);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", nullptr));
        buttonPlay->setText(QApplication::translate("MainWindow", "PLAY", nullptr));
        buttonStop->setText(QApplication::translate("MainWindow", "STOP", nullptr));
        label->setText(QApplication::translate("MainWindow", "Volume", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
