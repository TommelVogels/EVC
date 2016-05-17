#ifndef MYCLIENT_H
#define MYCLIENT_H

#include <QObject>
#include <QTcpSocket>
#include <QDebug>
#include <QThreadPool>
#include "mytask.h"

class MyClient : public QObject
{
    Q_OBJECT

public:
    explicit MyClient(QObject *parent = 0);
    void SetSocket(int Descriptor);

signals:

public slots:
    void disconnected();
    void readyRead();
    void TaskResult(QByteArray rData);
    void setVerbose(uint level);
    void setMode(uint mode);

private:
    QTcpSocket *socket;
    uint verbositylevel;
};

#endif // MYCLIENT_H
