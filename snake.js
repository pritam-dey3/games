class Snake {

  constructor() {
    this.len = 1;
    this.body = [];
    this.body[0] = createVector(0, 0);
    this.xdir = 0;
    this.ydir = 0;
  }

  setDir(x, y) {
    this.xdir = x;
    this.ydir = y;
  }

  eat(pos) {
    let x = this.body[0].x;
    let y = this.body[0].y;
    if (x == pos.x && y == pos.y) {
      return true;
      this.grow();
    }
    return false;
  }

  grow() {
    this.len++;

  }

  update() {
    this.body[0].x += this.xdir;
    this.body[0].y += this.ydir;

  }

  show() {
    for (let i = 0; i < this.body.length; i++) {
      fill(0);
      rect(this.body[i].x, this.body[i].y, 1, 1);
    }
  }
}
