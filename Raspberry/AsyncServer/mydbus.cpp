#include "mydbus.h"

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

int MyDbus::test(QString str)
{
    return str.isEmpty() ? 1 : 0;
}

QString Dbus_ext::push(const QString &arg)
{
    qDebug() << "D-Bus: \tReceived: " << arg;
    QMetaObject::invokeMethod(QCoreApplication::instance(), "quit");
    return QString("ping(\"%1\") got called").arg(arg);
}

QString Dbus_ext::pop(const QString &arg)
{
    qDebug() << "D-Bus: \tReceived: " << arg;
    return QString("vlees(\"%1\") got called").arg(arg);
}
