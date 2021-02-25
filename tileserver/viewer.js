class VRect {
  constructor(){
    this.left = 0;
    this.right = 1;
    this.top = 0;
    this.bottom = 1;
    console.log(`initialized zoom rect at ${[this.left,this.right,this.top,this.bottom]}`);
  }
}

class Viewer {
  constructor(viewerId,tileSource,pyramid,initRect,draw,resolution) {
    this.tileSource = tileSource;
    this.pyramid = pyramid;
    this.canvas = document.getElementById(viewerId);
    this.rect = document.getElementById(viewerId).getBoundingClientRect();
    this.width = this.rect.right - this.rect.left;
    this.height = this.rect.bottom - this.rect.top;
    if(resolution==null)
      resolution = this.width/2;
    this.resolution = resolution;
    this.zoom = 0;
    if(initRect==null) {
      initRect = new VRect();
      initRect.left = 0;
      initRect.right = this.width - 1;
      initRect.top = 0;
      initRect.bottom = this.height - 1;
    };
    this.zoomRect = initRect;
    if(draw==null)
      draw = function(context,img,square){context.drawImage(img,square[0],square[1],square[2],square[2])};
    this.draw = draw;
    console.log(`initialized Viewer ${viewerId} at ${this.rect.left},${this.rect.top}`);
  }

  getLocal(x,y) {
    return [x - this.rect.left, y - this.rect.top];
  }

  inBounds(x,y) {
    return ((0 <= x && x < this.width) && (0 <= y && y < this.height));
  }

  getZoomXOffset() {
    return (this.width / (2**this.zoom));
  }

  getZoomYOffset() {
    return (this.height / (2**this.zoom));
  }

  getZ() {
    return Math.max(0,Math.floor(this.zoom));
  }

  getZoomRow(z,y) {
    return Math.floor(((2**z)*y)/this.height);
  }

  getZoomCol(z,x) {
    return Math.floor(((2**z)*x)/this.width);
  }

  getVisibleRows(z) {
    const leftRow = this.getZoomRow(z,this.zoomRect.top);
    const rightRow = this.getZoomRow(z,this.zoomRect.bottom);
    //console.log(`visibleRows [${leftRow},${rightRow}]`);
    return [...Array(rightRow - leftRow+2).keys()].map(i => i + leftRow - 1);
  }

  getVisibleCols(z) {
    const leftCol = this.getZoomCol(z,this.zoomRect.left);
    const rightCol = this.getZoomCol(z,this.zoomRect.right);
    //console.log(`visibleCols [${leftCol},${rightCol}]`);
    return [...Array(rightCol - leftCol+2).keys()].map(i => i + leftCol - 1);
  }

  getVisibleTiles(z) {
    //console.log(z);
    const rows = this.getVisibleRows(z);
    const cols = this.getVisibleCols(z);
    const tileCoords = [];
    for(let i=0; i<rows.length; i+=1){
      for(let j=0; j<cols.length; j+=1){
        if(0 <= rows[i] && rows[i] < 2**z && 0 <= cols[j] && cols[j] < 2**z)
          tileCoords.push([cols[j],rows[i]])
      }
    }
    return tileCoords;
  }

  // deprecated
  drawTile(z,i,j,callback) {
    const scaledWidth = this.resolution / (2**(z - this.zoom - 1));
    const x = (i/(2**z))*this.width;
    const dx = ((x - this.zoomRect.left)/this.getZoomXOffset()) * this.width;
    const y = (j/(2**z))*this.height;
    const dy = ((y - this.zoomRect.top)/this.getZoomYOffset()) * this.height;
    const psqUrl = `${this.tileSource}/psq/${this.pyramid}/${z}_${i}_${j}_${this.resolution}`;
    var tileImg = new Image();
    tileImg.onload = function(){
      callback(tileImg,dx,dy,scaledWidth);
    };
    tileImg.src = psqUrl;
  }

  getTileQuery(l,i,j) {
    return `${this.tileSource}/psq/${this.pyramid}/${l}_${i}_${j}_${this.resolution}`;
  }

  getTileSquare(z,i,j) {
    const scaledWidth = this.width / (2**(z - this.zoom));
    const x = (i/(2**z))*this.width;
    const y = (j/(2**z))*this.height;
    const dx = ((x - this.zoomRect.left)/this.getZoomXOffset()) * this.width;
    const dy = ((y - this.zoomRect.top)/this.getZoomYOffset()) * this.height;
    return [dx,dy,scaledWidth];
  }

  drawVisibleTiles() {
    const z = this.getZ();
    const visible = this.getVisibleTiles(z);
    const context = this.canvas.getContext("2d");
    let draw = this.draw;
    for(let i=0; i<visible.length; i+=1){
      const x = visible[i][0];
      const y = visible[i][1];
      //this.drawTile(z,x,y,function(img,x,y,w){
      //  context.drawImage(img, x, y, w, w);
      //});
      const tileQuery = this.getTileQuery(z,x,y);
      const tileSquare = this.getTileSquare(z,x,y);
      const tileImg = new Image();
      tileImg.onload = function(){
        draw(context,tileImg,tileSquare);
      };
      tileImg.src = tileQuery;
    }
  }

  doZoom(x,y,zvel) {
    x = (x/this.width)*this.getZoomXOffset() + this.zoomRect.left;
    y = (y/this.height)*this.getZoomYOffset() + this.zoomRect.top;
    this.zoom += zvel;
    if(this.zoom > 0){
      const zX = (this.zoomRect.left+this.zoomRect.right)/2;
      const zY = (this.zoomRect.top+this.zoomRect.bottom)/2;
      const zoomWidth = this.width / (2**this.zoom);
      const zoomHeight = this.height / (2**this.zoom);
      this.zoomRect.left = zX - (zoomWidth/2);
      this.zoomRect.right = zX + (zoomWidth/2);
      this.zoomRect.top = zY - (zoomHeight/2);
      this.zoomRect.bottom = zY + (zoomHeight/2);
    }
    else{
      this.zoom = 0;
    }
  }

  doPan(xvel,yvel) {
    this.zoomRect.left += xvel/(2**this.zoom);
    this.zoomRect.right += xvel/(2**this.zoom);
    this.zoomRect.top += yvel/(2**this.zoom);
    this.zoomRect.bottom += yvel/(2**this.zoom);
  }

  correctZoomRect() {
    if(this.zoomRect.left < 0){
      const xCorrection = -this.zoomRect.left;
      this.zoomRect.left += xCorrection;
      this.zoomRect.right += xCorrection;
    }
    if(this.zoomRect.right >= this.width){
      const xCorrection = this.width - this.zoomRect.right;
      this.zoomRect.left += xCorrection;
      this.zoomRect.right += xCorrection;
    }
    if(this.zoomRect.top < 0){
      const yCorrection = -this.zoomRect.top;
      this.zoomRect.top += yCorrection;
      this.zoomRect.bottom += yCorrection;
    }
    if(this.zoomRect.bottom >= this.height){
      const yCorrection = this.height - this.zoomRect.bottom;
      this.zoomRect.top += yCorrection;
      this.zoomRect.bottom += yCorrection;
    }
    if(this.zoom == 0){
      this.zoomRect.left = 0;
      this.zoomRect.right = this.width;
      this.zoomRect.top = 0;
      this.zoomRect.bottom = this.height;
    }
  }
}
