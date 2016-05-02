#include "myclient.h"
#include "myserver.h"

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
    QString received = socket->readAll().trimmed();

    if(received != "")
    {
        qDebug() << received;
        MyTask *mytask = new MyTask(received);
        mytask->setAutoDelete(true);
        connect(mytask,SIGNAL(Result(QByteArray)),SLOT(TaskResult(QByteArray)), Qt::QueuedConnection);

        connect(mytask,SIGNAL(UARTsend(QByteArray)),qobject_cast<MyServer *>(this->parent())->uart,SLOT(writeData(QByteArray)));
        //connect(mytask,SIGNAL(UARTsend(QByteArray)),qobject_cast<MyServer *>(this->parent())->uart,writeData(QByteArray));
        QThreadPool::globalInstance()->start(mytask);
    }
}

void MyClient::TaskResult(QByteArray rData)
{
    socket->write(rData);
}
