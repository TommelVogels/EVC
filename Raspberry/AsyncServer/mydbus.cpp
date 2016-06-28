#include "mydbus.h"
#include "interfacecollection.h"
#include "globaldefines.h"

MyDbus::MyDbus(QObject *parent) :
    QObject(parent)
{
    ext = new Dbus_ext(this);

    bool success = QDBusConnection::sessionBus().isConnected();
    if (!success)
        qDebug() << "D-Bus: \tCannot connect to the D-Bus session bus.";

    if (success && !QDBusConnection::sessionBus().registerService(SERVICE_NAME1)) {
        qDebug() << "D-Bus: \tCould not register service";
        success = false;
    }

    if(success)
    {
        success = QDBusConnection::sessionBus().registerObject(ECHO_OBJECT_PATH1, ext, QDBusConnection::ExportAllContents);
        if(success)
            qDebug() << "D-Bus: \tStarted without errors";
        else
            qDebug() << "D-Bus: \tDid not start correctly";
    }
}

Dbus_ext::Dbus_ext(MyDbus *parent) :
    QObject(parent)
{
}

void Dbus_ext::push(const QByteArray &arg, const quint8 &commandID)
{
    qDebug() << "D-Bus: \tReceived: " << arg;
    if(sysState.operatingMode == MODE_MANUAL)
        return;

    QByteArray data = arg;
    char cid = commandID;

    MyDbus *dbus = qobject_cast<MyDbus *>(this->parent());
    emit dbus->busWrite(data, cid);
}

QByteArray Dbus_ext::pop(void)
{
    InterfaceCollection *ic = qobject_cast<InterfaceCollection *>(this->parent()->parent());
    return ic->Uart->pop();
}

void Dbus_ext::SetMotor(const bool &left, const bool &right, const int &l, const int &r)
{
    MyDbus *dbus = qobject_cast<MyDbus *>(this->parent());
    emit dbus->MotorSignal(left,right,l,r);
}

void Dbus_ext::setTurretAngle(const bool &horizontal, const bool &vertical, const int &h, const int &v)
{
    MyDbus *dbus = qobject_cast<MyDbus *>(this->parent());
    emit dbus->TurretAngleSignal(horizontal,vertical,h,v);
}

void Dbus_ext::fireMissile(const bool &t1, const bool &t2, const bool &all)
{
    MyDbus *dbus = qobject_cast<MyDbus *>(this->parent());
    emit dbus->MissileSignal(t1,t2,all);
}

void Dbus_ext::setLaser(const bool &on)
{
    MyDbus *dbus = qobject_cast<MyDbus *>(this->parent());
    emit dbus->LaserSignal(on);
}
