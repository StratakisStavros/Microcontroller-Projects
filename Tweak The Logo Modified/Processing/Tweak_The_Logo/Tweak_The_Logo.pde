import processing.serial.*;
// === Global Variables ===
Serial myPort;
PImage logo;
int sensorValue = 0;
int bgcolor = 0;
// Scale factor για το logo
float logoScale = 0.5;
PrintWriter logger;
boolean isLogging = false;

void setup() {
  // Αρχικό dummy μέγεθος (απαραίτητο για Processing)
  size(100, 100);
  // Φόρτωση εικόνας
  logo = loadImage("arduino_logo.png");
  // Ρύθμιση τελικού παραθύρου ώστε να χωράει scaled logo + gauge
  int canvasWidth = int(logo.width * logoScale);
  int canvasHeight = int(logo.height * logoScale) + 60;
  surface.setSize(canvasWidth, canvasHeight);
  // Χρωματικός χώρος HSB
  colorMode(HSB, 255);
  // Σύνδεση στη σειριακή θύρα (αν χρειαστεί άλλαξε το COM3)
  myPort = new Serial(this, "COM3", 9600);
  myPort.bufferUntil('\n');  // Περιμένει ολόκληρη γραμμή (string + newline)
  // Δημιουργία CSV αρχείου με timestamp στο όνομα
  logger = createWriter("Recording.csv");
  logger.println("Time(ms);SensorValue;Percentage");
}

void draw() {
  // Μετατροπή τιμής A0 (0–1023) σε Hue (0–255)
  bgcolor = int(map(sensorValue, 0, 1023, 0, 255));
  background(bgcolor, 255, 255);
  // Προβολή scaled λογότυπου
  image(logo, 0, 0, logo.width * logoScale, logo.height * logoScale);
  // Προβολή ράβδου gauge
  drawGaugeBar(sensorValue);
}

void drawGaugeBar(int value) {
  // Διαστάσεις παραθύρου
  int barWidth = width - 40;
  int barHeight = 20;
  int x = 20;
  // Y position: ακριβώς κάτω από το scaled logo
  int y = int(logo.height * logoScale) + 20;
  // Υπολογισμός συμπληρωμένου πλάτους
  float fillWidth = map(value, 0, 1023, 0, barWidth);
  // Σχεδίαση πλαισίου
  stroke(0);
  noFill();
  rect(x, y, barWidth, barHeight);
  // Συμπληρωμένο μέρος
  noStroke();
  fill(0, 0, 200);  // μπλε
  rect(x, y, fillWidth, barHeight);
  // Ποσοστό
  fill(0);
  textAlign(CENTER, CENTER);
  textSize(12);
  int percentage = int(map(value, 0, 1023, 0, 100));
  text(percentage + "%", x + barWidth/2, y + barHeight + 14);
}

void serialEvent(Serial myPort) {
  String inString = myPort.readStringUntil('\n');
  if (inString != null) {
    inString = trim(inString);
    if (inString.matches("\\d+")) {
      sensorValue = int(inString);
      println(sensorValue);
      if (isLogging) {
        int percentage = int(map(sensorValue, 0, 1023, 0, 100));
        logger.println(millis() + ";" + sensorValue + ";" + percentage);
        logger.flush();
      }
    }
  }
}

void keyPressed() {
  if (key == 'l' || key == 'L') {
    isLogging = !isLogging;
    if (isLogging) {
      println("📥 Logging ENABLED");
    } else {
      println("📤 Logging DISABLED");
    }
  }
}
