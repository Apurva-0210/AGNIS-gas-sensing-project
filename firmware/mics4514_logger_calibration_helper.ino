// =============================================
// MiCS-4514 — CODE 0: CALIBRATION HELPER
// UPDATED: STANDARD OX formula confirmed
// COATED:   R0_RED=320431.2, R0_OX=143.4
// UNCOATED: R0_RED=469174.0, R0_OX=7361.8
// Commands: B U C T H G P K F
// =============================================
#define RED_PIN     25
#define NOX_PIN     14
#define VCC         3.3f
#define ADC_MAX     4095.0f
#define RLOAD_RED   100000.0f
#define RLOAD_NOX   220.0f

float R0_RED       = 469174.0f;
float R0_OX        = 7361.8f;
float baseline_red = 469174.0f;
float baseline_ox  = 7361.8f;
String sensor      = "UNCOATED";
float temperature  = 27.2f;
float humidity     = 50.0f;
float certifiedPpm = 0.0f;
String currentGas  = "CO";
bool flipOX        = true;

float getRs_RED(int raw) {
    float v = raw * (VCC / ADC_MAX);
    if (v <= 0.01f) v = 0.01f;
    return RLOAD_RED * (VCC - v) / v;
}

float getRs_OX(int raw) {
    float v = raw * (VCC / ADC_MAX);
    if (v <= 0.01f) v = 0.01f;
    if (v >= 3.29f) v = 3.29f;
    if (flipOX)
        return RLOAD_NOX * (VCC - v) / v;  // STANDARD
    else
        return RLOAD_NOX * v / (VCC - v);  // INVERTED
}

void handleCommands() {
    if (!Serial.available()) return;
    char c = Serial.read();
    if (c=='B'||c=='b') {
        baseline_red = getRs_RED(analogRead(RED_PIN));
        baseline_ox  = getRs_OX(analogRead(NOX_PIN));
        R0_RED = baseline_red;
        R0_OX  = baseline_ox;
        Serial.println("=== ZERO AIR R0 LOCKED ===");
        Serial.print("R0_RED = "); Serial.print(R0_RED,1); Serial.println(" Ω");
        Serial.print("R0_OX  = "); Serial.print(R0_OX, 1); Serial.println(" Ω");
        Serial.println("==========================");
    }
    if (c=='U'||c=='u') {
        R0_RED = 469174.0f; R0_OX = 7361.8f;
        baseline_red = R0_RED; baseline_ox = R0_OX;
        sensor = "UNCOATED";
        Serial.println("UNCOATED — R0_RED=469174.0 R0_OX=7361.8");
    }
    if (c=='C'||c=='c') {
        R0_RED = 320431.2f; R0_OX = 143.4f;
        baseline_red = R0_RED; baseline_ox = R0_OX;
        sensor = "COATED";
        Serial.println("COATED — R0_RED=320431.2 R0_OX=143.4");
    }
    if (c=='T'||c=='t') {
        Serial.println("Enter temperature (e.g. 27.2):");
        delay(3000);
        if (Serial.available()) {
            temperature = Serial.parseFloat();
            Serial.print("Temp: "); Serial.print(temperature,1); Serial.println(" °C");
        }
    }
    if (c=='H'||c=='h') {
        Serial.println("Enter humidity (e.g. 50.0):");
        delay(3000);
        if (Serial.available()) {
            humidity = Serial.parseFloat();
            Serial.print("Humidity: "); Serial.print(humidity,1); Serial.println(" %RH");
        }
    }
    if (c=='G'||c=='g') {
        Serial.println("Enter gas: 1=CO 2=NO2 3=NH3 4=ETH");
        delay(3000);
        if (Serial.available()) {
            int g = Serial.parseInt();
            if (g==1)      currentGas="CO";
            else if (g==2) currentGas="NO2";
            else if (g==3) currentGas="NH3";
            else if (g==4) currentGas="ETH";
            Serial.print("Gas set: "); Serial.println(currentGas);
        }
    }
    if (c=='P'||c=='p') {
        Serial.println("Enter certified ppm from IITM machine:");
        delay(3000);
        if (Serial.available()) {
            certifiedPpm = Serial.parseFloat();
            Serial.print("Certified ppm: "); Serial.println(certifiedPpm,3);
        }
    }
    if (c=='F'||c=='f') {
        flipOX = !flipOX;
        Serial.print("OX formula switched to: ");
        Serial.println(flipOX ? "STANDARD" : "INVERTED");
        // Recalculate baseline with new formula
        baseline_ox = getRs_OX(analogRead(NOX_PIN));
        R0_OX = baseline_ox;
        Serial.print("R0_OX updated: "); Serial.println(R0_OX,1);
    }
    if (c=='K'||c=='k') {
        int rR = analogRead(RED_PIN);
        int nR = analogRead(NOX_PIN);
        float rs_r = getRs_RED(rR);
        float rs_o = getRs_OX(nR);
        float rat_r = rs_r / R0_RED;
        float rat_o = rs_o / R0_OX;
        float S_r = (baseline_red - rs_r) / baseline_red;
        float S_o = (rs_o - baseline_ox)  / baseline_ox;
        Serial.println("==== CALIBRATION POINT ====");
        Serial.print("Gas:           "); Serial.println(currentGas);
        Serial.print("Sensor:        "); Serial.println(sensor);
        Serial.print("Formula OX:    "); Serial.println(flipOX ? "STANDARD" : "INVERTED");
        Serial.print("Certified ppm: "); Serial.println(certifiedPpm,3);
        Serial.print("Temp:          "); Serial.print(temperature,1); Serial.println(" °C");
        Serial.print("Rs_RED:        "); Serial.print(rs_r,1);        Serial.println(" Ω");
        Serial.print("Rs_OX:         "); Serial.print(rs_o,1);        Serial.println(" Ω");
        Serial.print("Ratio_RED:     "); Serial.println(rat_r,4);
        Serial.print("Ratio_OX:      "); Serial.println(rat_o,4);
        Serial.print("S_RED:         "); Serial.println(S_r,4);
        Serial.print("S_OX:          "); Serial.println(S_o,4);
        Serial.print("CALPOINT,");
        Serial.print(currentGas);      Serial.print(",");
        Serial.print(sensor);          Serial.print(",");
        Serial.print(certifiedPpm,3);  Serial.print(",");
        Serial.print(temperature,1);   Serial.print(",");
        Serial.print(humidity,1);      Serial.print(",");
        Serial.print(rs_r,1);          Serial.print(",");
        Serial.print(rs_o,1);          Serial.print(",");
        Serial.print(rat_r,4);         Serial.print(",");
        Serial.print(rat_o,4);         Serial.print(",");
        Serial.print(S_r,4);           Serial.print(",");
        Serial.println(S_o,4);
        Serial.println("===========================");
    }
}

void setup() {
    Serial.begin(115200);
    analogSetPinAttenuation(RED_PIN, ADC_11db);
    analogSetPinAttenuation(NOX_PIN, ADC_11db);
    Serial.println("=============================================");
    Serial.println("   CODE 0: CALIBRATION HELPER");
    Serial.println("   GPIO 25=RED  GPIO 27=NOX");
    Serial.println("   COATED R0:   320431.2 / 143.4");
    Serial.println("   UNCOATED R0: 469174.0 / 7361.8");
    Serial.println("---------------------------------------------");
    Serial.println("   B=baseline  U=uncoated  C=coated");
    Serial.println("   T=temp  H=humidity");
    Serial.println("   G=gas  P=certified ppm  K=record");
    Serial.println("   F=flip OX formula");
    Serial.println("=============================================");
    Serial.println("Warming up 3 minutes...");
    delay(180000);
    Serial.println("Ready!");
    Serial.println("Time(s),Sensor,Gas,CertPPM,Temp,Humidity,RED_Raw,NOX_Raw,Rs_RED,Rs_OX,Ratio_RED,Ratio_OX");
}

unsigned long t0 = 0;
void loop() {
    handleCommands();
    if (!t0) t0 = millis();
    unsigned long t = (millis() - t0) / 1000;

    int rR = analogRead(RED_PIN);
    int nR = analogRead(NOX_PIN);
    float rs_r = getRs_RED(rR);
    float rs_o = getRs_OX(nR);
    float rat_r = rs_r / R0_RED;
    float rat_o = rs_o / R0_OX;
    float S_r   = (baseline_red - rs_r) / baseline_red;
    float S_o   = (rs_o - baseline_ox)  / baseline_ox;

    Serial.println("--------------------------------------------");
    Serial.print("Time: ");        Serial.print(t);            Serial.println(" s");
    Serial.print("Sensor: ");      Serial.print(sensor);
    Serial.print("  Gas: ");       Serial.print(currentGas);
    Serial.print("  CertPPM: ");   Serial.println(certifiedPpm,3);
    Serial.print("Formula OX: ");  Serial.println(flipOX ? "STANDARD" : "INVERTED");
    Serial.print("Temp: ");        Serial.print(temperature,1);
    Serial.print(" °C  Hum: ");    Serial.print(humidity,1);   Serial.println(" %");
    Serial.print("Rs_RED: ");      Serial.print(rs_r,1);
    Serial.print(" Ω  Rs_OX: ");   Serial.print(rs_o,1);       Serial.println(" Ω");
    Serial.print("Ratio_RED: ");   Serial.print(rat_r,4);
    Serial.print("  Ratio_OX: ");  Serial.println(rat_o,4);
    Serial.print("S_RED: ");       Serial.print(S_r,4);
    Serial.print("  S_OX: ");      Serial.println(S_o,4);
    Serial.println("Press K to record calibration point");

    Serial.print("CSV,");
    Serial.print(t);              Serial.print(",");
    Serial.print(sensor);         Serial.print(",");
    Serial.print(currentGas);     Serial.print(",");
    Serial.print(certifiedPpm,3); Serial.print(",");
    Serial.print(temperature,1);  Serial.print(",");
    Serial.print(humidity,1);     Serial.print(",");
    Serial.print(rR);             Serial.print(",");
    Serial.print(nR);             Serial.print(",");
    Serial.print(rs_r,1);         Serial.print(",");
    Serial.print(rs_o,1);         Serial.print(",");
    Serial.print(rat_r,4);        Serial.print(",");
    Serial.println(rat_o,4);
    delay(2000);
}