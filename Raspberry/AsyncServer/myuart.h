#ifndef MYUART_H
#define MYUART_H

#include <QObject>
#include <QSerialPort>
#include <QSerialPortInfo>
#include <QDebug>

class MyUART : public QObject
{
    Q_OBJECT
public:
    explicit MyUART(QObject *parent = 0);
    void getPortInfo();

signals:

public slots:
    void serialReceived();
    void writeData(QByteArray data);

private:
    QSerialPort *serialPort;
    QSerialPortInfo *portInfo;


};

#endif // MYUART_H
