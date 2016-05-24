#include "interfacecollection.h"

InterfaceCollection::InterfaceCollection(QStringList arguments, QObject *parent) :
    QObject(parent)
{
    args = arguments;
}

void InterfaceCollection::startInterfaces()
{
    Uart = new MyUART(this);
    Server = new MyServer(this);
    Dbus = new MyDbus(this);

    int port = 0;
    if(args.length() > 1)
        port = args[1].toInt();

    Server->StartServer(port?port:1234);
    //Dbus->StartBus();
}


