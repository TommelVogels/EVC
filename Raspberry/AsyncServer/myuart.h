#ifndef MYUART_H
#define MYUART_H

#include <QObject>
#include <QSerialPort>
#include <QSerialPortInfo>
#include <QDebug>
#include <QQueue>
#include <QTimer>

class MyUART : public QObject
{
    Q_OBJECT
public:
    explicit MyUART(QObject *parent = 0);

signals:
    void notification(QByteArray data, uint verbosity = 1);

public slots:
    void serialReceived();
    void timeOut();
    void queueData(QByteArray data, uint function = 0);


private:
    void writeData();
    QTimer *timer;
    QSerialPort *serialPort;
    QSerialPortInfo *portInfo;
    QQueue<QByteArray> queue;
    QByteArray receivedData;
    QByteArray lastCommand;
    bool waitingForAck;




};

#endif // MYUART_H
