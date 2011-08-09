#include <stdio.h>
#include <stdlib.h>
int main() {
char* school ;
char* name ;
float age ;
name = "mark";
age = 22;
school = "wentworth";
int y = 10;for (y;y <= 20;y++)
 {
printf("%d", y);
 printf( "\n");
}

if (age >= 21)  {
float x ;
x = age;
 printf( "you are ");
 printf("%f", x);
 printf( "\nyou can drink!\n");
}

 else if (age > 18)  {
float c ;
printf( "can smoke!\n");
 c = 10;
}

 else  {
printf( "you shall not pass\n");
}

if (age > 50)  {
printf( "hey old man");
}

 else  {
printf( "hey young guy");
}

}