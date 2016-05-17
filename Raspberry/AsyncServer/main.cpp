#include <QtCore/QCoreApplication>
#include "interfacecollection.h"
#include "globaldefines.h"

uint mode = MODE_MANUAL;

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    QStringList arguments = QCoreApplication::arguments();

    InterfaceCollection ic(arguments);
    ic.startInterfaces();

    return a.exec();
}
