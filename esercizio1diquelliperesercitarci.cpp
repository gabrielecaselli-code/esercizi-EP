/*gabriele caselli
3einf
25/11/2026
Scrivere un programma che inseriti da tastiera due numeri interi da tastiera ne stampi il maggiore; se i due numeri sono uguali deve essere stampata la somma dei due numeri.*/

#include <iostream>
using namespace std;

int main(){

    double a,b;
    double risultato;

    cout<<"inserire il primo numero:\n";
    cin>>a;

    cout<<"inserire il secondo numero:\n";
    cin>>b;

    if(a>b){
        cout<<a<<endl;
    }
    else if(b>a){
        cout<<b<<endl;
    }
    else{
        risultato=a+b;
        cout<<risultato<<endl;
    }

    return 0;

}