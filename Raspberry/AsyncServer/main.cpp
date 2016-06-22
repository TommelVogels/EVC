#include <stdio.h>
#include <stdlib.h>

#include <QtCore/QCoreApplication>
#include <QDebug>
#include "interfacecollection.h"
#include "globaldefines.h"

uint mode = MODE_MANUAL;
SystemState sysState;

int main(int argc, char *argv[])
{
    sysState.laser = false;
    sysState.mototSpeedLeft = 0;
    sysState.motorSpeedRight = 0;
    sysState.turretHorizontal = 0;
    sysState.turretVertical = 0;
    sysState.operatingMode = MODE_AUTONOMOUS;

    QCoreApplication a(argc, argv);
    QStringList arguments = QCoreApplication::arguments();
    InterfaceCollection ic(arguments);
    ic.startInterfaces();
    a.exec();

    return 0;
}
