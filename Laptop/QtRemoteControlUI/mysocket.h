#ifndef MYSOCKET_H
#define MYSOCKET_H

#include <QObject>
#include <QDebug>
#include <QTcpSocket>
#include <QAbstractSocket>

class MySocket : public QObject
{
    Q_OBJECT
public:
    explicit MySocket(QObject *parent = 0);
    void connectToPi(QString address, int port);
    void writeBytes(QByteArray data);
    QTcpSocket *socket;
    bool connected = false;

signals:
    void receivedData(QByteArray data);
    void disconnectSignal();

public slots:
    void disconnected();
    void readyRead();

private:

};

#endif // MYSOCKET_H
