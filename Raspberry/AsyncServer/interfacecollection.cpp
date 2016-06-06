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

    connect(&(Dbus->ext),SIGNAL(busWrite(QByteArray,uint)),Uart,SLOT(queueData(QByteArray,uint)));
    connect(Uart,SIGNAL(notification(QByteArray,uint)),Server,SLOT(sendNotifications(QByteArray,uint)));

    int port = 0;
    if(args.length() > 1)
        port = args[1].toInt();

    Server->StartServer(port?port:1234);
}


