#include "mydbus.h"

MyDbus::MyDbus(QObject *parent) :
    QObject(parent)
{
    QDBusConnection dbus = QDBusConnection::sessionBus();
    dbus.registerObject("/interfacedescription", this);
    dbus.registerService("com.dbus.example.interface");


}

int MyDbus::test(QString str)
{
    if(str == QString("via ctor"))
    {
        qDebug() << "ctor";
    }
    else if(str == QString("via setPartent"))
    {
        qDebug() << "setParent";
    }

    return 0;

}
