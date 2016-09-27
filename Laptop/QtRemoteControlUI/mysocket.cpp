#include "mysocket.h"
#include <QThread>

MySocket::MySocket(QObject *parent) :
    QObject(parent)
{
    socket = new QTcpSocket(this);

    connect(socket,SIGNAL(disconnected()), this, SLOT(disconnected()));
    connect(socket,SIGNAL(readyRead()), this, SLOT(readyRead()));
}

void MySocket::connectToPi(QString address, int port)
{
    socket->connectToHost(address,port);

    if(!socket->waitForConnected(5000))
    {
       qDebug() << "Error: " <<  socket->errorString();
    }
    else
    {
        connected = true;
    }
}

void MySocket::writeBytes(QByteArray data)
{
    //qDebug() << "sending:" << data;
    data.append("\r\n\r\n");
    socket->write(data);
}


void MySocket::disconnected()
{
    qDebug() << "Disconnected!";
    connected = false;
    emit disconnectSignal();
}


void MySocket::readyRead()
{
    //qDebug() << "Reading...";
    QByteArray data = socket->readAll();
    emit receivedData(data);
}
