let snake;
let rez = 20;

function setup() {
  createCanvas(600, 400);
  w = floor(width / rez);
  h = floor(height / rez);
  frameRate(5);
  snake = new Snake();
  foodLocation();
}

function foodLocation() {
  let x = floor(random(w));
  let y = floor(random(h));
  food = createVector(x, y);
}

function keyPressed() {
  if (keyCode === LEFT_ARROW) {
    snake.setDir(-1, 0);
    // print("left")
  } else if (keyCode === RIGHT_ARROW) {
    snake.setDir(1, 0);
  } else if (keyCode === DOWN_ARROW) {
    snake.setDir(0, 1);
  } else if (keyCode === UP_ARROW) {
    snake.setDir(0, -1);
  } else if (keyCode === TAB) {
    snake.setDir(0, 0);
  }
}

function draw() {
  scale(rez);
  background(220);
  if(snake.eat(food)){
    foodLocation();
  }
  snake.update();
  snake.show();

  noStroke();
  fill(200,0,210);
  rect(food.x, food.y, 1, 1)
}
