#ifndef MYSERVER_H
#define MYSERVER_H

#include <QTcpServer>
#include <QTcpSocket>
#include <QAbstractSocket>
#include <QList>
#include "myclient.h"
#include "myuart.h"

class MyServer : public QTcpServer
{
    Q_OBJECT
public:
    explicit MyServer(QObject *parent = 0);
    void StartServer(int port);

protected:
    void incomingConnection(int handle);
    QList<MyClient *> clientList;
signals:

public slots:
    void sendNotifications(QByteArray data, uint verbosity);
    void clientDisconnected();
};

#endif // MYSERVER_H
