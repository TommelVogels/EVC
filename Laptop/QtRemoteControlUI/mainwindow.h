#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "mysocket.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

    void setSteeringEnabled(bool enabled);

public slots:
    void leftChanged(int);
    void rightChanged(int);
    void speedChanged(int);
    void dialChanged(int);
    void resetSpeed(bool);
    void goStraight(bool);
    void fireSingleT1(bool);
    void fireSingleT2(bool);
    void fireAllT1(bool);
    void fireAllT2(bool);
    void fireAllT12(bool);
    void connectToPi(bool);
    void connected(void);
    void turretAngle(int h, int v);
    void turretHChanged(int h);
    void turretVChanged(int v);
    void verboseChanged(bool);
    void changeMode(bool val);
    void dumpData(QByteArray data);

    void flipLaser(bool);
    void socketDisconnected();

    //void keyPressEvent( QKeyEvent* event );
    bool eventFilter( QObject *o, QEvent *e );

private:
    void motorDataChanged(bool left, bool right);
    void turretDataChanged(bool h, bool v);
    Ui::MainWindow *ui;
    int left = 0, right = 0, speed = 0, dial = 0;
    MySocket *socket;
};

#endif // MAINWINDOW_H
