#-------------------------------------------------
#
# Project created by QtCreator 2016-06-01T15:09:00
#
#-------------------------------------------------

QT       += core gui
QT       += network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = evc_control
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    mysocket.cpp \
    myqframe.cpp

HEADERS  += mainwindow.h \
    mysocket.h \
    json.h \
    myqframe.h

FORMS    += mainwindow.ui
