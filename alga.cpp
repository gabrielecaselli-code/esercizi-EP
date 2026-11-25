/*gabriele caselli
3einf 
25/11/2026
Si supponga che l’andamento della popolazione di un’alga si sviluppi nel seguente modo: un anno raddoppia l’anno successivo cala di un terzo.
Creare un programma che dato un valore iniziale della popolazione e un valore da raggiungere di popolazione dica quanti anni ci mette quella popolazione a raggiungere o superare quel valore.*/

#include <iostream>
using namespace std;

int main(){

    double popolazione_iniziale;
    double popolazione_finale;
    int anni=0;

    //chiedo un input da tastiera
    cout<<"inserire la popolazione inziale:\n";
    cin>>popolazione_iniziale;

    cout<<"inserisci la popolazione finale:\n";
    cin>>popolazione_finale;

    //condizione per cui non deve inserire 0
    if(popolazione_iniziale<=0 || popolazione_finale<=0){

        cout<<"NON CI RIPROVARE MAI PIU";

        return 0;
    }

    //creo il ciclo con la condizione di permanenza
    while(popolazione_iniziale<popolazione_finale){

        anni++;

        //verifico se un anno dispari
        if (anni % 2 != 0) {
            // Anno dispari (1°, 3°, 5°...): raddoppia
            popolazione_iniziale = popolazione_iniziale * 2.0;
        }
        //verifico se per soddisfare la condizione del ciclo e un anno pari 
        else {
            popolazione_iniziale = popolazione_iniziale * 2.0 / 3.0;


        }

    }

    cout<<"ecco l'obbiettivo raggiunto\n"<<popolazione_iniziale<<endl<<"anni necessari\n"<<anni<<endl;

    return 0;

}