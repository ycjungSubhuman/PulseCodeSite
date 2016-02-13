function pad(number, space){
	var numstring = number+"";
	for(var i=numstring.length; i<space; i++){
		numstring = '0'+numstring;
	}
	return numstring;
}