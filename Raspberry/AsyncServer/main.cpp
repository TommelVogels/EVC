#include <stdio.h>
#include <stdlib.h>

#include <QtCore/QCoreApplication>
#include <QDebug>

#include "interfacecollection.h"
#include "globaldefines.h"

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    QStringList arguments = QCoreApplication::arguments();

    InterfaceCollection ic(arguments);
    ic.startInterfaces();
    a.exec();

    return 0;
}
