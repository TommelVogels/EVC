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

    connect(Dbus,SIGNAL(busWrite(QByteArray,uint)),Uart,SLOT(queueData(QByteArray,uint)));
    connect(Dbus,SIGNAL(MotorSignal(bool,bool,int,int)),Uart,SLOT(setMotor(bool,bool,int,int)));
    connect(Dbus,SIGNAL(TurretAngleSignal(bool,bool,int,int)),Uart,SLOT(setTurretAngle(bool,bool,int,int)));
    connect(Dbus,SIGNAL(LaserSignal(bool)),Uart,SLOT(setLaser(bool)));
    connect(Uart,SIGNAL(notification(QVariantMap,uint)),Server,SLOT(sendNotifications(QVariantMap,uint)));

    int port = 0;
    if(args.length() > 1)
        port = args[1].toInt();

    Server->StartServer(port?port:1234);
}


