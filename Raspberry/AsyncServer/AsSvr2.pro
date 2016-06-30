#-------------------------------------------------
#
# Project created by QtCreator 2011-04-22T11:50:43
#
#-------------------------------------------------

QT       += core
QT       += network
QT       -= gui
QT       += serialport
QT       += dbus

TARGET = AsSvr2
CONFIG   += console
CONFIG   += c++11
CONFIG   -= app_bundle
CONFIG(release, debug|release):DEFINES += QT_NO_DEBUG_OUTPUT

TEMPLATE = app


SOURCES += main.cpp \
    tcp/myserver.cpp \
    tcp/myclient.cpp \
    tcp/mytask.cpp \
    json.cpp \
    myuart.cpp \
    mydbus.cpp \
    interfacecollection.cpp


HEADERS += \
    tcp/myserver.h \
    tcp/myclient.h \
    tcp/mytask.h \
    json.h \
    myuart.h \
    globaldefines.h \
    mydbus.h \
    interfacecollection.h

