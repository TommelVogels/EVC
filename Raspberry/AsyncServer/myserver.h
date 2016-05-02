#ifndef MYSERVER_H
#define MYSERVER_H

#include <QTcpServer>
#include <QTcpSocket>
#include <QAbstractSocket>
#include "myclient.h"
#include "myuart.h"

class MyServer : public QTcpServer
{
    Q_OBJECT
public:
    explicit MyServer(QObject *parent = 0);
    void StartServer(int port);
    MyUART *uart;

protected:
    void incomingConnection(int handle);

signals:

public slots:


};

#endif // MYSERVER_H
