#ifndef MYUART_H
#define MYUART_H

#include <QObject>
#include <QSerialPort>
#include <QSerialPortInfo>
#include <QDebug>
#include <QQueue>
#include <QTimer>
#include <QPair>

class MyUART : public QObject
{
    Q_OBJECT
public:
    explicit MyUART(QObject *parent = 0);
    QByteArray pop(void);

signals:
    void notification(QVariantMap noti, uint verbosity = 1);

public slots:
    void serialReceived();
    void timeOut();
    void queueData(QByteArray data, uint function = 0);
    void setMotor(bool left, bool right, int l = 0, int r = 0);
    void setTurretAngle(bool horizontal, bool vertical, int h = 0, int v = 0);
    void fireMissile(bool t1, bool t2, bool all);
    void setLaser(bool on);

private:
    void writeData();
    QTimer *timer;
    QSerialPort *serialPort;
    QSerialPortInfo *portInfo;
    QQueue<QPair<QByteArray, uint>> queue;
    QQueue<QByteArray> receivedQueue;
    QByteArray receivedData;
    QByteArray lastCommand;
    bool waitingForAck;




};

#endif // MYUART_H
