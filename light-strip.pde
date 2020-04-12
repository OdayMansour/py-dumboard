int squares = 83;
int size = 20;
color[] colors = {color(149, 137, 211), color(150, 209, 216), color(129, 204, 197), color(103, 180, 186), 
color(95, 143, 197), color(80, 140, 62), color(121, 146, 28), color(171, 161, 14), color(223, 177, 6), 
color(243, 150, 6), color(236, 95, 21), color(190, 65, 18), color(138, 43, 10)};

void setup() {

  size(1680, 40);
  colorMode(RGB, 255);
  background(color(0));
  //frameRate(10);
  
}

void draw() {

  noStroke();
  for (int i=0; i<squares; i++) {
    fill(colors[i%13]);
    ellipse((i+1)*size, size, size, size); 
  }
  noLoop();
}

