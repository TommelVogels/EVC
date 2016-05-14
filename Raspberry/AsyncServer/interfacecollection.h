#ifndef INTERFACECOLLECTION_H
#define INTERFACECOLLECTION_H

#include <QObject>
#include "tcp/myserver.h"
#include "myuart.h"
#include "mydbus.h"

class InterfaceCollection : public QObject
{
    Q_OBJECT
public:
    explicit InterfaceCollection(QStringList arguments, QObject *parent = 0);
    void startInterfaces();
    QStringList args;
    MyUART *Uart;
    MyServer *Server;
    MyDbus *Dbus;

signals:

public slots:

};

#endif // INTERFACECOLLECTION_H
