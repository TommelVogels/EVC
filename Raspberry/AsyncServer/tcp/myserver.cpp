#include "myserver.h"

MyServer::MyServer(QObject *parent) :
    QTcpServer(parent)
{
}

void MyServer::StartServer(int port)
{
    if(listen(QHostAddress::Any,port))
    {
        qDebug() << "TCP: \tStarted without errors (on port " << QString::number(port) << ")";
    }
    else
    {
        qDebug() << "TCP: \tDid not start";
    }
}

void MyServer::incomingConnection(int handle)
{
    MyClient *client = new MyClient(this->parent());
    clientList.append(client);
    client->SetSocket(handle);
}

void MyServer::sendNotifications(QByteArray data, uint verbosity)
{
    if(verbosity == 0)
        return;

    foreach(MyClient *client, clientList)
        if(verbosity & client->verbositylevel)
            client->sendData(data);
}
