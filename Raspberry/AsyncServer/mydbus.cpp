#include "mydbus.h"
#include "interfacecollection.h"

MyDbus::MyDbus(QObject *parent) :
    QObject(parent)
{
    bool success = QDBusConnection::sessionBus().isConnected();
    if (!success)
        qDebug() << "D-Bus: \tCannot connect to the D-Bus session bus.";

    if (success && !QDBusConnection::sessionBus().registerService(SERVICE_NAME1)) {
        qDebug() << "D-Bus: \tCould not register service";
        success = false;
    }

    if(success)
    {
        success = QDBusConnection::sessionBus().registerObject(ECHO_OBJECT_PATH1, &ext, QDBusConnection::ExportScriptableSlots);
        if(success)
            qDebug() << "D-Bus: \tStarted without errors";
        else
            qDebug() << "D-Bus: \tDid not start correctly";
    }
}

QByteArray Dbus_ext::push(const QByteArray &arg, const QByteArray &commandID)
{
    qDebug() << "D-Bus: \tReceived: " << arg;

    //QString stringData = arg;
    QByteArray data = arg;
    char cid = (uint)commandID[0];
    emit busWrite(data, cid);

    QByteArray push;
    push.append("A501A5A");
    return push;
}

QByteArray Dbus_ext::pop(void)
{
    QByteArray pop;
    pop.append("A501A5A");
    return pop;
}
