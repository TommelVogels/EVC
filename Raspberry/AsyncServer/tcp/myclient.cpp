#include "myclient.h"
#include "myserver.h"
#include "interfacecollection.h"

MyClient::MyClient(QObject *parent) :
    QObject(parent)
{
    QThreadPool::globalInstance()->setMaxThreadCount(15);
    setVerbose(5);
}

void MyClient::SetSocket(int Descriptor)
{
    socket = new QTcpSocket(this);

    connect(socket,SIGNAL(disconnected()),this,SLOT(disconnected()));
    connect(socket,SIGNAL(readyRead()),this,SLOT(readyRead()));

    socket->setSocketDescriptor(Descriptor);

    qDebug() << "TCP: \tClient connected";

}

void MyClient::disconnected()
{
    qDebug() << "TCP: \tClient disconnected";
}

void MyClient::readyRead()
{
    QString received = socket->readAll().simplified();

    if(received != "")
    {
        qDebug() << "TCP: \tReceived: " << received;

        //Initialize a task
        MyTask *mytask = new MyTask(received, mode);
        mytask->setAutoDelete(true);
        connect(mytask,SIGNAL(Result(QByteArray)),SLOT(sendData(QByteArray)), Qt::QueuedConnection);

        //Connect to the other interfaces
        InterfaceCollection *ic = qobject_cast<InterfaceCollection *>(this->parent());
        connect(mytask,SIGNAL(UARTsend(QByteArray,uint)),ic->Uart,SLOT(queueData(QByteArray,uint)));

        //Start the task
        QThreadPool::globalInstance()->start(mytask);
    }
}

void MyClient::sendData(QByteArray rData)
{
    //Send the data straight to the client
    socket->write(rData.append("\r\n"));
}

void MyClient::setVerbose(uint level)
{
    verbositylevel = 0xFFFFFFFF;
}

void MyClient::setMode(uint level)
{

}
