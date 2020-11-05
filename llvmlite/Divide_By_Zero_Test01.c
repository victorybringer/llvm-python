/*
 * Copyright (c) Huawei Technologies Co., Ltd. 2019-2020. All rights reserved.
 *
 * @description 除零错误
 *
 * @good GoodCase01;GoodCase02;GoodCase03;GoodCase04;GoodCase05;GoodCase06
 *
 * @bad BadCase01;BadCase02;BadCase03;BadCase04;BadCase05;BadCase06;BadCase07;BadCase08
 *
 * @label Coverity:DIVIDE_BY_ZERO;SecBrella:SecA_DivideByZero
 *
 * @author c00297271
 *
 * @date 2020-06-01
 *
 */


int cond01(int p1)
{
    if (p1 > 5) {
        return 1;
    } else {
        return 0;
    }
}

// @scene 路径敏感， if 条件不成立时，出现除零错误
int BadCase01(p1)
{
    int x = 0;
    if (cond01(p1)<1) {
        x = 1;
    }
    // POTENTIAL FLAW: 除零错误
    return 1 / x;
}


int foo02(int y)
{
    if (y < 0) {
        return 0;
    }
    return y;
}

// @scene 函数返回值做除数，并且该函数的返回值可能为零。         
void BadCase02(int y)
{
    // POTENTIAL FLAW: 除零错误
    int z = 1 / foo02(y);
}
// @scene 来自入参的除数可能为零         
void BadCase03(int y)
{
    // POTENTIAL FLAW: 除零错误
    int z = 1 / y;
}
void Outer01() {
	int p1 = 6;
	int y = 1;
    if(p1 > 5)  
        y = 0; 
	
	// y 值做参数，调用 BadCase03
	BadCase03(y);
}








#define SUB_FILE_MICRO(NUM) ((NUM) - 5)

// @scene 宏展开后的表达式返回值做除数，并且该返回值可能为零。
float BadCase04(int num)
{
    // POTENTIAL FLAW: 除零错误
    float ret = num / SUB_FILE_MICRO(5);
    return ret;
}


void GoodCase01(int actCnt, float lossTot)
{
    int i;
    for (i = 0; i < actCnt; i++) {
    }

    float lossAvg;
    if (i != 0) {
        lossAvg = lossTot / i;//good
    } else {
        lossAvg = 0;
    }
}


// @scene 除数来自外部输入，可能会出现除零错误。
void BadCase05()
{
    int a;
    scanf("%d", &a);
    // POTENTIAL FLAW: 除零错误
    int z = 1 / a;  // 目前clang不跟踪污点所以漏报
}

// @scene 除数来自外部输入，虽然经过条件判断，仍有可能为0
void BadCase06(int b)
{

    if (b < 10) {
        // POTENTIAL FLAW: 除零错误
        int z = 1 / b;
    }

}



typedef double double_t;
// @scene 除数为 chart、int 、long或者其他整形类型，且值等于零
// 
void BadCase07(int flag)
{
    char i1 = 0;
    int i2 = 0;
    unsigned long long i3 = 0;

    float i4 = 0.0;
    double_t i5 = 0.0;

    double valueA = 1.0;
    double valueC = 0.0;

    if (flag == 0) {
        // POTENTIAL FLAW: 除零错误
        100 / i1;
    } else if (flag == 10) {
        // POTENTIAL FLAW: 除零错误
        100 / i2;
    } else if (flag == 100) {
        // POTENTIAL FLAW: 除零错误
        100 / i3;
    } else if (flag == 1000) {
        // 华为c语言编程规范v5.0，只检查整形除法或者余数预算，不要求检查浮点型运算
        100 / i4;
    } else if (flag == 1001) {
        // 华为c语言编程规范v5.0，只检查整形除法或者余数预算，不要求检查浮点型运算
        100 / i5;
    } else if (flag == 1002) {
        // 华为c语言编程规范v5.0，只检查整形除法或者余数预算，不要求检查浮点型运算
        valueC = valueA / i5;
    } else if (flag == 1003) {
        // 华为c语言编程规范v5.0，只检查整形除法或者余数预算，不要求检查浮点型运算
        valueA / i5;
    }

}

//https://secsolar-szv.clouddragon.huawei.com/portal/workspace/projectDefectsView?projectName=UAC3000_V500R020C10_SecBrella_acu&cid=211533
//误报
//工具无法判断浮点型当前取值范围，无法优化
#define  ZERO_DOUBLE                0.0000000001
void GoodCase02(double rateo1, double rateo2, double meterval_o, int flag)
{
    double rateo = 0.0, rated = 0.0;

    if (flag == 0) {
        rateo = rateo1;
        rated = rateo2;
    }

    if (rateo < ZERO_DOUBLE || rated < ZERO_DOUBLE) {
        return;
    }

    double retl = meterval_o * rateo / rated;//good
}


void GoodCase03(int lo)
{
    int numEntries, totalProbe;
    numEntries = totalProbe = 0;

    for (int i = 0; i < lo; i++) {
        numEntries++;
    }

    // 华为c语言编程规范v5.0，只检查整形除法或者余数预算，不要求检查浮点型运算
	// POTENTIAL FLAW: 除零错误
    float f1 = (float)totalProbe / (float)numEntries;
}


void GoodCase04(int lo)
{
    float b = 0;
    float a = 1;
    a = b;
    // 华为c语言编程规范v5.0，只检查整形除法或者余数预算，不要求检查浮点型运算
	// POTENTIAL FLAW: 除零错误
    (float)10.0 / a;//error
}



#define UINT32 unsigned int 
#define DOUBLE double 
#define FLOAT float 

void GoodCase05()
{
    UINT32 client_rate = 1;
    UINT32 time_slot = 0;
    UINT32 target_cgen_m = 0;

    // 华为c语言编程规范v5.0，只检查整形除法或者余数预算，不要求检查浮点型运算
	// POTENTIAL FLAW: 除零错误
    target_cgen_m = (UINT32)((DOUBLE)((DOUBLE)(client_rate) * 1000) / (DOUBLE)(25 * time_slot));
}

typedef unsigned long VOS_UINT32;
typedef float VOS_FLOAT;
void Goodcase06(int u)
{
    VOS_UINT32 u32ESM1Number = 0;
    VOS_FLOAT f32ESM1PortVoltage = 0;
    VOS_FLOAT  f32ESM1TotalVoltage = 0;
    for (int i = 0; i < u; i++) {
        u32ESM1Number++;
        f32ESM1TotalVoltage += 0.1;
    }
    if (0 != u32ESM1Number) {
        f32ESM1PortVoltage = f32ESM1TotalVoltage / u32ESM1Number; // good
    }
}

int  ReadByte();
// @scene 取余预算，除数可能为0
void BadCase08()
{
    int a = ReadByte();
    // POTENTIAL FLAW: 除零错误
    int b = 1000 / a; //a可能是0    
    // POTENTIAL FLAW: 除零错误
    int c = 1000 % a;//a 可能是0    
}
