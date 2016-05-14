#include "myclient.h"
#include "myserver.h"
#include "interfacecollection.h"

MyClient::MyClient(QObject *parent) :
    QObject(parent)
{
    QThreadPool::globalInstance()->setMaxThreadCount(15);
}

void MyClient::SetSocket(int Descriptor)
{
    socket = new QTcpSocket(this);

    connect(socket,SIGNAL(disconnected()),this,SLOT(disconnected()));
    connect(socket,SIGNAL(readyRead()),this,SLOT(readyRead()));

    socket->setSocketDescriptor(Descriptor);

    qDebug() << "client connected";

}

void MyClient::disconnected()
{
    qDebug() << "client disconnected";
}

void MyClient::readyRead()
{
    QString received = socket->readAll().simplified();

    if(received != "")
    {
        qDebug() << received;

        //Initialize a task
        MyTask *mytask = new MyTask(received, mode);
        mytask->setAutoDelete(true);
        connect(mytask,SIGNAL(Result(QByteArray)),SLOT(TaskResult(QByteArray)), Qt::QueuedConnection);

        //Connect to the other interfaces
        InterfaceCollection *ic = qobject_cast<InterfaceCollection *>(this->parent());
        connect(mytask,SIGNAL(UARTsend(QByteArray)),ic->Uart,SLOT(writeData(QByteArray)));

        //Start the task
        QThreadPool::globalInstance()->start(mytask);
    }
}

void MyClient::TaskResult(QByteArray rData)
{
    //Send the data straight to the client
    socket->write(rData);
}

void MyClient::setVerbose(uint level)
{

}

void MyClient::setMode(uint level)
{

}
