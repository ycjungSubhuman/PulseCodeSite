var logpos = []; /*an array of logvalues that are used to scale the -frequency- axis of the visualizer*/
				 /*initial value is "empty", fill this in by calling 'makeLogPositionArray'*/


//a prototype for a complex number
function Complex(re, im){
	this.re = re;
	this.im = im;
	this.addWith = function(right){
		if(typeof(right)=="object")
			return new Complex(this.re+right.re, this.im+right.im);//thank you GC :)
		else
			return new Complex(this.re+right, this.im);
	}
	this.subWith = function(right){
		if(typeof(right)=="object")
			return new Complex(this.re-right.re, this.im-right.im);
		else
			return new Complex(this.re-right, this.im);
	}
	this.mulWith = function(right){
		if(typeof(right)=="object")
			return new Complex(this.re*right.re - this.im*right.im, this.re*right.im + this.im*right.re);
		else
			return new Complex(this.re*right, this.im*right);
	}
	this.divWith = function(right){
		if(typeof(right)=="object"){
			if(right.re === 0 && right.im === 0){
				console.log("Complex : div by 0 detected");
				return new Complex(0, 0);
			}
			else{
				return new Complex((this.re*right.re + this.im*right.im)/(right.re*right.re + right.im*right.im),
						(this.im*right.re - this.re*right.im)/(right.re*right.re + right.im*right.im)); 
			}
		}
		else{
			if(right === 0){
				console.log("Complex : div by 0 detected");
				return new Complex(0, 0);
			}
			else{
				return new Complex(this.re/right, this.im/right);
			}
		}
	}
	this.negate = function(){
		return new Complex(-this.re, -this.im);
	}
	this.conjugate = function(){
		return new Complex(this.re, -this.im);
	}
	this.pow = function(n){
		var result = new Complex(1, 0);
		for(var i=0; i<n; i++){
			result = this.mulWith(result);
		}
		return result;
	}
	this.toString = function(){
		if(this.im>=0)
			return this.re + "+" + this.im + "i";
		else
			return this.re + "" + this.im + "i";
	}
}
function makeLogPositionArray(normalval, buffersize){//in: normalizing value, the size of freqencyBinCount
	//init an array
	var arr = [];
	var log_max = Math.log(buffersize);//used to normalize the value

	//push log values 
	for(var i=0; i<buffersize; i++){
		arr.push(normalval* Math.log(i+1)/log_max);
	}
	//returns the array
	return arr;
}
function diminishFrequencyData(data){
	for(var i=0; i<data.length; i++){
		data[i] = data[i]/(i+1);
	}
}

function initCanvas(){//initiallize the canvas(for TESTING CANVAS DRAW)
	//get canvas
	var canvas = document.getElementById("visual");

	if(canvas.getContext){//if successfully loaded
		//init canvas context as "2d"
		var ctx = canvas.getContext("2d");

		//draw a red, opaque square
		ctx.fillStyle = "rgb(200, 0, 0)";
		ctx.fillRect(10, 10, 55, 50);

		//draw a blue, transparent square
		ctx.fillStyle = "rgba(0, 0, 200, 0.5)";
		ctx.fillRect(30, 30, 55, 50);

		drawWaveFunction(Math.cos, 0, 0, canvas.width, canvas.height);	
	}
}

function updateVisualizer_BassMorph(frequencyData, bufferlength){//in:ByteFreqData, Buffer size
	//get canvas from HTML
	var canvas = document.getElementById("visual");

	if(canvas.getContext){//if successfully loaded
		//init canvas context ad "2d" and get context
		var ctx = canvas.getContext("2d");
		var midpos = logpos[0]/2;
		var parity = 1;//for +- inversion of values

		//clear canvas
		ctx.clearRect(0, 0, canvas.width, canvas.height);

		ctx.strokeStyle = "rgb(40, 40, 40)";
		//draw curve line according to the data
		ctx.beginPath();
		//initial posotion is left; middle;
		ctx.moveTo(-30, canvas.height/2);
		for(var i=0; i<bufferlength/2-1; i++){//the highest-freq data will be ignored
			if(parity == 1){
				ctx.quadraticCurveTo(midpos, Math.pow(frequencyData[i]*10/canvas.height, 3)+200, logpos[i], canvas.height/2);
			}
			else{
				ctx.quadraticCurveTo(midpos, (-1) * Math.pow(frequencyData[i]*10/canvas.height,3)+200, logpos[i], canvas.height/2);
			}
			midpos = (logpos[i]+logpos[i+1])/2;//set next curve pos;
			parity = -parity;
		}
		//draw
		ctx.stroke();
	}

}
function drawWaveFunction(wavefunc, x, y, width, height){
	var canvas = document.getElementById("visual");

	if(canvas.getContext){
		var ctx = canvas.getContext("2d");
		ctx.translate(0.5, 0.5);//translate a little bit to fit into the actual pixel
		var vmidx = x;//vertical midposition; x
		var vmidy = y+height/2;//vortical midposition; y
		var samplechunk = 1;//sample width = 1px

		//move the pen to the midposition
		ctx.strokeStyle = "rgb(40, 40, 40)";
		ctx.beginPath();
		ctx.moveTo(vmidx, vmidy);

		for(var i=0; i<width; i+=samplechunk){
			ctx.lineTo(i, vmidy+10*wavefunc(i));
		}
		ctx.lineTo(i, vmidy);
		ctx.stroke();
	}
}

//note that this fft is only for size = 2^n
function fft(data, size){//y = Fc. returns y
	if(size > 1){
		//split the data into two arrays of equal length: even and odd
		var even=[], odd=[];
		for(var i=0; i<size; i++){
			if(i%2 == 0) even.push(data[i]);
			else odd.push(data[i]);
		}
		//get fft-ed result for each array and reconstruct original data from them
		var evenResult, oddResult;
		var result = new Array(size);
		evenResult = fft(even, size/2);
		oddResult = fft(odd, size/2);
		
		//Reconstruct with Sooley&Tukey Method. 
		//data[j] = even[j]+(w_n)^j*odd[j] for j=0, 1, 2 ... m-1
		//data[j+m] = even[j] - (w_n)^j*odd[j] (n == 2m, w_n == (n-th root of 1), n==size)
		var w = new Complex(Math.cos(2*Math.PI/size), Math.sin(2*Math.PI/size)); //get size-th root of 1
		for(var i=0; i<size/2; i++){
			result[i] = w.pow(i).mulWith(oddResult[i]).addWith(evenResult[i]);
			result[i+size/2] = w.pow(i).mulWith(oddResult[i]).negate().addWith(evenResult[i]);
		}
		return result;
	}
	else{//size == 1
		var w = 1;
		var result = new Array(1);
		result[0] = w * data[0];
		return result;
	}
}
function ifft(data, size){//(invF)y = c, returns c
	//first get fft
	var ffted = fft(data, size);

	//then get result for (inverse F)
	//note that we can construct inverse of F by using (conjugate of w) instead of (w)
	//and divide all by size
	ffted[0] = ffted[0].divWith(size);
	ffted[size/2] = ffted[size/2].divWith(size);
	for(var i=1; i<size/2; i++){
		var tmp = ffted[i].divWith(size);
		ffted[i] = ffted[size-i].divWith(size);
		ffted[size-i] = tmp;
	}
	return ffted;
}
window.onload = function(){
	var ctx = new AudioContext();
	var audio = document.getElementById("tangential");
	var audioSrc = ctx.createMediaElementSource(audio);
	var analyser = ctx.createAnalyser();
	var canvas = document.getElementById("visual");

	//connect to destinations
	audioSrc.connect(analyser);
	analyser.connect(ctx.destination);

	//frequencyBinCount : number of values
	frequencyData = new Uint8Array(analyser.frequencyBinCount);

	//loop to update frequency data
	function renderFrame(){
		requestAnimationFrame(renderFrame);
		analyser.getByteFrequencyData(frequencyData);

		/*implement rendering here*/
		//updates canvas according to the frequencyData
		updateVisualizer_BassMorph(frequencyData, analyser.frequencyBinCount);

	}

	//initiallize a global array that is used for x-axis-scaling of the visualizer
	logpos = makeLogPositionArray(visual.width, analyser.frequencyBinCount/2);
	//init canvas(for canvas drawing TEST)
	initCanvas();

	audio.play();//play audio
	renderFrame();//render animation frame recursively
};

