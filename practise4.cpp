#include <iostream>
#include <math.h>
#include <iomanip>

using namespace std;

int main(){

int x = 1;
float y1,y2,y3,y4,y5,y6;
float h = 0.1;
float hmin = pow(10, -19);
float diff1,diff2;
float f1,f2,f3,f4,n1,n2;
float h1 = pow(2,-4);
float h1min = pow(2,-21);
float fprimeReal = 3.0;

//Question 1
while(h > hmin){
	y1= (pow((x + h) , 2) - pow(x,2))/h;
	cout <<setprecision(15)<< y1 << endl;
	h/=10;
}
cout << endl << endl;
h = 0.1;
while(h > hmin){
	y2= ((pow((x + h) , 2) + pow(10,8)));// - (pow(x,2) + pow(10,8)))/h;
	y4 = (pow(x,2) + pow(10,8));
	diff1 = (y2 - y4)/h;
	cout <<setprecision(15)<< diff1 << endl;

	h/=10;
}

cout << endl << endl;
h = 0.1;
while(h > hmin){
	y3= (pow((x + h) , 2) - pow((x-h),2))/(2*h);
	cout <<setprecision(15)<< y3 << endl;
	h/=10;
}
cout << endl << endl;
h = 0.1;
while(h > hmin){
	y5= pow((x + h) , 2) + pow(10,8); 
	y6= pow((x-h),2) + pow(10,8);
	diff2 = (y5 - y6)/(2*h);
	cout <<setprecision(15)<< diff2 << endl;
	h/=10;
}


//Question 2
while(h1 > h1min){
	f1= (pow((x + h1) , 3) - pow(x,3))/h1;
	f2= (pow((x +(2*h1)) , 3) - pow(x,3))/(2*h1);
	f3= (-(pow((x +(2*h1)) , 3))/(2*h1)) - ((3*(pow(x,3)))/(2*h1)) + (2*(pow((x + h1) , 3)))/h1;
	f4= (pow((x +(4*h1)) , 3) - pow(x,3))/(4*h1);
	n1 = (fprimeReal - f2)/ (fprimeReal - f1);
	n2 = (f4 - f2)/(f2 - f1);

	cout << "f1  "<<setprecision(15)<< f1 << endl << endl;
	cout << "f2  "<<setprecision(15)<< f2 << endl << endl;
	cout << "f3  "<<setprecision(15)<< f3 << endl << endl;
	cout << "n1  "<<setprecision(15)<< n1 << endl << endl;
	cout << "n2  "<<setprecision(15)<< n2 << endl << endl;
	h1/=2;
}
cout << endl << endl;







}