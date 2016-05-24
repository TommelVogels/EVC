#include "mydbus.h"

MyDbus::MyDbus(QObject *parent) :
    QObject(parent)
{
    if (!QDBusConnection::sessionBus().isConnected()) {
        qDebug() << "Cannot connect to the D-Bus session bus.";
        exit(1);
    }

    if (!QDBusConnection::sessionBus().registerService(SERVICE_NAME)) {
        fprintf(stderr, "%s\n", qPrintable(QDBusConnection::sessionBus().lastError().message()));
        qDebug() << "error";
        exit(1);
    }
    else
    {
        QDBusConnection::sessionBus().registerObject(PP_OBJECT_PATH, &ext, QDBusConnection::ExportScriptableSlots);
        qDebug() << "Dbus Started";
    }
}

int MyDbus::test(QString str)
{
    return str.isEmpty() ? 1 : 0;
}

QString Dbus_ext::push(const QString &arg)
{
    qDebug() << "received: " << arg;
    QMetaObject::invokeMethod(QCoreApplication::instance(), "quit");
    return QString("ping(\"%1\") got called").arg(arg);
}

QString Dbus_ext::pop(const QString &arg)
{
    qDebug() << "received: " << arg;
    return QString("vlees(\"%1\") got called").arg(arg);
}
