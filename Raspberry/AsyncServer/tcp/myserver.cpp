#include "myserver.h"
#include "json.h"

MyServer::MyServer(QObject *parent) :
    QTcpServer(parent)
{
}

void MyServer::StartServer(int port)
{
    if(listen(QHostAddress::Any,port))
    {
        qWarning() << "TCP: \tStarted without errors (on port " << QString::number(port) << ")";
    }
    else
    {
        qWarning() << "TCP: \tDid not start";
    }
}

void MyServer::incomingConnection(int handle)
{
    MyClient *client = new MyClient(this->parent());
    connect(client,SIGNAL(sendNotification(QVariantMap,uint)),this,SLOT(sendNotifications(QVariantMap,uint)));
    clientList.append(client);
    client->SetSocket(handle);
}

void MyServer::sendNotifications(QVariantMap notification, uint verbosity)
{
    if(verbosity == 0)
        return;

    notification["jsonrpc"] = "2.0";
    QByteArray data = QtJson::serialize(notification);

    foreach(MyClient *client, clientList)
        if(verbosity & client->verbositylevel)
            client->sendData(data);
}

void MyServer::clientDisconnected()
{
    MyClient *client = qobject_cast<MyClient *>(sender()->parent());

    if(!client)
        return;

    clientList.removeAll(client);
    client->deleteLater();
}
