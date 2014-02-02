int a = 0, b = 0, c = 0;

int fact2(int x) {
    int c = 1, res = 1;

    repeat
        res = res * c;
        c = c + 1;
    until c > x;
    return res;
}

int fib(int nth){
    if(nth <= 1){
        return 1;
    } else {
        return fib(nth-1) + fib(nth-2);
    }
}

print fact2(6);


while(a < 100 ) {
    if(a==15)
        break;
    print a;
    a = a + 1;
}

a = 0;

repeat {
    a = a + 1;
    if(a%5!=0)
        continue;
    print a;
} until (a>100);

a = 0;
repeat {
    a = a + 1;
    print fib(a);
} until (a>5);

