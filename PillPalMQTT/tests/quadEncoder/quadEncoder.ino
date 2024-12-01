const int    C1 = 22; // Entrada de la señal A del encoder.
const int    C2 = 21; // Entrada de la señal B del encoder.

volatile int  n    = 0;
volatile byte ant  = 0;
volatile byte act  = 0;

unsigned long lastTime = 0;  // Tiempo anterior
unsigned long sampleTime = 100;  // Tiempo de muestreo

double P = 0;
//double R = 937.2;
double R = 890;
//double R = 360;

void setup()
{
  Serial.begin(9600);

  pinMode(C1, INPUT);
  pinMode(C2, INPUT);

  attachInterrupt(digitalPinToInterrupt(C1), encoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(C2), encoder, CHANGE);
  
  Serial.println("Numero de conteos");

}

void loop() {
  if (millis() - lastTime >= sampleTime || lastTime==0)
  {  // Se actualiza cada sampleTime (milisegundos)
      lastTime = millis();
      P = (n*360.0)/R;
      Serial.print("Posicion en grados: ");Serial.println(P);
   }
}

// Encoder precisión cuádruple.
void encoder(void)
{

  ant=act;
  
  if(digitalRead(C1)) bitSet(act,1); else bitClear(act,1);            
  if(digitalRead(C2)) bitSet(act,0); else bitClear(act,0);
  
  
  
  if(ant == 2 && act ==0) n++;
  if(ant == 0 && act ==1) n++;
  if(ant == 3 && act ==2) n++;
  if(ant == 1 && act ==3) n++;
  
  if(ant == 1 && act ==0) n--;
  if(ant == 3 && act ==1) n--;
  if(ant == 0 && act ==2) n--;
  if(ant == 2 && act ==3) n--;    
    

}