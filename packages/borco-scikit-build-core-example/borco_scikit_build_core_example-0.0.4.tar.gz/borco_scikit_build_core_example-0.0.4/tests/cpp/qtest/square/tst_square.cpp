#include <QCoreApplication>
#include <QtTest>

// add necessary includes here
#include "square.h"

class TestSquare : public QObject
{
    Q_OBJECT

public:
    TestSquare() {}
    ~TestSquare() {}

private slots:
    void initTestCase() {}
    void cleanupTestCase() {}

    void test_square() {
        QVERIFY(square(2) == 4);
    }
};


QTEST_MAIN(TestSquare)

#include "tst_square.moc"
