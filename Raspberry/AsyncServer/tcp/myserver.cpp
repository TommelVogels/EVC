#include "myserver.h"

MyServer::MyServer(QObject *parent) :
    QTcpServer(parent)
{
}

void MyServer::StartServer(int port)
{
    if(listen(QHostAddress::Any,port))
    {
        qDebug() << "TCP: \tStarted on port " << QString::number(port);
    }
    else
    {
        qDebug() << "TCP: \tNot started!";
    }
}

void MyServer::incomingConnection(int handle)
{
    MyClient *client = new MyClient(this->parent());
    client->SetSocket(handle);
}
