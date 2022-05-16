int main (void) {
  init();
  pinMode(10, OUTPUT);
  pinMode(A0, INPUT); //v gen
  pinMode(A4, INPUT); // v hall
  Serial3.begin(9600); // pin 15 RX e 14 TX
  Serial.begin(9600);

  int f = 20; //numero di n misure in semiperiodo
  float V_ard_low[f], V_ard_high[f];
  float V_hall_high[f], V_hall_low[f];
  float dV_hall, dV_ard;
  float incremento_corrente = 0.1;
  float I_max = 0.2;
  Serial3.println("OP1 1 LF");
  Serial3.println("I1 0 LF");
  Serial3.println("V1 30 LF");

  delay(200);
  
  for(float I=0; I <= I_max ; I+= incremento_corrente){
    Serial.println("CORRENTE");
    Serial.println(I);
    
    for(int M = 0; M <= 2 ; M += 1){ // M misure di un "periodo"

      for (int N = 0 ; N < f ; N += 1){ //N misure 5V
        digitalWrite(10, HIGH);
        V_ard_high[N] = analogRead(A0)*5/1023; //float(map(analogRead(A0), 0, 1023, 0, 5000))/1000;
        V_hall_high[N] = analogRead(A4)*5/1023; //float(map(analogRead(A4), 0, 1023, 0, 5000))/1000;
      }

      for(int K=0 ; K < f ; K += 1){ //N misure 0V
        digitalWrite(10, LOW);
        V_ard_low[K] = analogRead(A0)*5/1023; //float(map(analogRead(A0), 0, 1023, 0, 5000))/1000;
        V_hall_low[K] = analogRead(A4)*5/1023; //float(map(analogRead(A4), 0, 1023, 0, 5000))/1000;
      }

      Serial.println("VARD");
      for ( int T = 0 ; T < f ; T++){
        dV_ard = (V_ard_high[T]-V_ard_low[T]);
        String vard = String(dV_ard) + " ";
        Serial.print(vard);  // PRINTO N VALORI
      }
      Serial.println(" ");
      delay(100);

      Serial.println("VHALL");
      for ( int T = 0 ; T < f ; T++){
        dV_hall = (V_hall_high[T]-V_hall_low[T]);
        String vhall = String(dV_hall) + " ";
        Serial.print(vhall); //PRINTO N VALORI 
      }
      Serial.println(" ");
      delay(100);
    }
    delay(100);
    String corrente = "I1 " + String(I) + " LF";
    Serial3.println(corrente);
  }
  delay(100);
  Serial.println("BREAK");
  delay(100);
  
  return 0;
}
