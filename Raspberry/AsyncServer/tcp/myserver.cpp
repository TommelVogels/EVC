#include "myserver.h"

MyServer::MyServer(QObject *parent) :
    QTcpServer(parent)
{
}

void MyServer::StartServer(int port)
{
    if(listen(QHostAddress::Any,port))
    {
        qDebug() << "started on port " << QString::number(port);
    }
    else
    {
        qDebug() << "not started!";
    }
}

void MyServer::incomingConnection(int handle)
{
    MyClient *client = new MyClient(this->parent());
    client->SetSocket(handle);
}
