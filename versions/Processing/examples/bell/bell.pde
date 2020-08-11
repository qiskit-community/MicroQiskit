String[] quantumCorpusLoad;
String[] finalQuantumArray;
color black = color(0);
color white = color(255);
int bottom = 1000; //how far down the bottom canvas should start. there are 1000 shots, so start 1000px down

void setup() {
  size(50,40);
  loadPixels();
  createReadings();
  colorPixels();
  
  //export image to same folder as this file
  //note that the export will be tiny (50px by 40px).  
  //Scale it up in photoshop using nearests neighboring resampling to get nice hard edges.
  save("pixel_art.png");
  println("exported!");
}


void createReadings() {
  Simulator simulator = new Simulator(0.1);
  
  QuantumCircuit phiPlus = new QuantumCircuit(2, 2);
  phiPlus.h(0);
  phiPlus.cx(0, 1);
  phiPlus.measure(0, 0);
  phiPlus.measure(1, 1);

  List<String> measurements = new ArrayList();
  for (int i = 0; i < 1000; i++) {
    Map<String,Integer> counts = (Map)simulator.simulate(phiPlus, 1, "counts");
    String firstKey = counts.keySet().iterator().next();
    measurements.add(firstKey);
  }
  finalQuantumArray = measurements.toArray(new String[0]);
}


//Color the pixels based on the corpus. The 0th qubit (right digit)
//determines the position, being either the top canvas or the bottom canvas.
//the 1st qubit (left digit) determines the color of the qubit.
//I admit the code below is a lazy way achieving the desired effect, but it works.
void colorPixels() {
  for (int i = 0; i < finalQuantumArray.length; i = i+1) {
    if (finalQuantumArray[i].equals("00")) {
      pixels[i] = black;
    } else if (finalQuantumArray[i].equals("11")) {
      pixels[i + bottom] = white;
    }
     else if (finalQuantumArray[i].equals("01")) {
      pixels[i + bottom] = black;
    }
     else if (finalQuantumArray[i].equals("10")) {
      pixels[i] = white;
    }
  }
  updatePixels();
}
