int squares = 83;
int size = 20;
color[] colors = new color[46];

void setup() {

  size(1680, 40);
  colorMode(HSB, 360, 100, 100);
  background(color(0));
  //frameRate(10);
colors[0] = color(280, 100, 100);
colors[1] = color(280, 100, 100);
colors[2] = color(280, 100, 100);
colors[3] = color(280, 100, 100);
colors[4] = color(280, 100, 100);
colors[5] = color(210, 100, 100);
colors[6] = color(207, 100, 100);
colors[7] = color(204, 100, 100);
colors[8] = color(201, 100, 100);
colors[9] = color(198, 100, 100);
colors[10] = color(195, 100, 100);
colors[11] = color(192, 100, 100);
colors[12] = color(189, 100, 100);
colors[13] = color(186, 100, 100);
colors[14] = color(183, 100, 100);
colors[15] = color(180, 100, 100);
colors[16] = color(177, 100, 100);
colors[17] = color(174, 100, 100);
colors[18] = color(171, 100, 100);
colors[19] = color(168, 100, 100);
colors[20] = color(165, 100, 100);
colors[21] = color(154.5, 100, 100);
colors[22] = color(144, 100, 100);
colors[23] = color(133.5, 100, 100);
colors[24] = color(123, 100, 100);
colors[25] = color(112.5, 100, 100);
colors[26] = color(102, 100, 100);
colors[27] = color(91.5, 100, 100);
colors[28] = color(81, 100, 100);
colors[29] = color(70.5, 100, 100);
colors[30] = color(60, 100, 100);
colors[31] = color(54, 100, 100);
colors[32] = color(48, 100, 100);
colors[33] = color(42, 100, 100);
colors[34] = color(36, 100, 100);
colors[35] = color(30, 100, 100);
colors[36] = color(24, 100, 100);
colors[37] = color(18, 100, 100);
colors[38] = color(12, 100, 100);
colors[39] = color(6, 100, 100);
colors[40] = color(0, 100, 100);
colors[41] = color(0, 100, 100);
colors[42] = color(0, 100, 100);
colors[43] = color(0, 100, 100);
colors[44] = color(0, 100, 100);
colors[45] = color(0, 100, 100);
}

void draw() {

  noStroke();
  for (int i=0; i<squares; i++) {
    fill(colors[i%46]);
    ellipse((i+1)*size, size, size, size);
    fill(0);
    text((i%46)-5,(i+0.7)*size, size*1.2);
  }
  noLoop();
}
