$(document).ready(function(){
	//audio player action define
	//big 'play' button
	$(document).on('click', '.audiobutton-overlapped', function(){
		var audio = $(this).parent().find('audio');
		$(this).hide();
		$(this).parent().find('.entity-player-small').show();
		$(this).parent().find('audio').load();
		$(this).parent().find('audio').trigger('audio:play');

		//event firing
		audio[0].loaded_updator = setInterval(function(){
			audio.trigger('updator:loading');
			return false;
		}, 500);
		audio[0].played_updator = setInterval(function(){
			audio.trigger('updator:playing');
			return false;
		}, 100);
	});
	//timebar & timedigit
	$(document).on('updator:loading', 'audio', function(e){
		var audio = e.target;
		var duration = audio.duration;
		var buffered;
		for(var i=0; i<audio.buffered.length; i++){
			buffered = buffered>audio.buffered.end(i) ? buffered:audio.buffered.end(i);
		}
		var width_full = parseInt($(audio).parent().find('.scrubber-background').css('width'), 10);
		var loaded_length = width_full * buffered/duration;
		$(audio).parent().find('.scrubber-loaded').css('width', loaded_length);
	});
	function keepTrackPlayed(e){
		var audio = e.target;
		var duration = audio.duration;
		var current = audio.currentTime;
		var width_full = parseInt($(audio).parent().find('.scrubber-background').css('width'), 10);
		var played_length = width_full * current/duration;
		var digit_current = pad(parseInt(current/60, 10), 2) + ':' + pad(parseInt(current)%60, 2);

		$(audio).parent().find('.scrubber-played').css('width', played_length);
		$(audio).parent().find('.playtime').text(digit_current);

		if(current == duration){
			$('audio').trigger('audio:pause');
			audio.currentTime = 0;
		}

	}
	$(document).on('updator:playing', 'audio', keepTrackPlayed);

	$(document).on('mousemove click', '.scrubber-nav', function(e){
		$(document).off('updator:playing');	

		var audio = $(e.target).parents('[role="player"]').find('audio')[0]
		var offset = $(this).offset();
		var mousepos = e.pageX - offset.left;
		var width_full = parseInt($(audio).parent().find('.scrubber-background').css('width'), 10);
		var duration = audio.duration;
		var navtime = duration * mousepos/width_full;
		var navtext = pad(parseInt(navtime/60, 10), 2) + ':' + pad(parseInt(navtime)%60, 2);

		$(e.target).parents('[role="player"]').find('.scrubber-played').css('width', mousepos).css('background-color', '#333355')
		$(e.target).parents('[role="player"]').find('.playtime').text(navtext).css('color', '#7777dd');

		if(e.type == 'click'){
			audio.currentTime = navtime;
		}
	});
	$(document).on('touchstart', '.scrubber-nav', function(e){
		var audio = $(e.target).parents('[role="player"]').find('audio')[0]
		var touch = e.originalEvent.touches[0];
		var offset = $(this).offset();
		var mousepos = touch.pageX - offset.left;
		var width_full = parseInt($(audio).parent().find('.scrubber-background').css('width'), 10);
		var duration = audio.duration;
		var navtime = duration * mousepos/width_full;

		audio.currentTime = navtime;
		return false;
	});
	$(document).on('mouseout', '.scrubber-nav', function(e){
		$(e.target).parents('[role="player"]').find('.scrubber-played').css('background-color', '#333333');
		$(e.target).parents('[role="player"]').find('.playtime').css('color', '#ffffff');
		$(document).on('updator:playing', 'audio', keepTrackPlayed);
		$(e.target).parents('[role="player"]').find('audio').trigger('updator:playing');

	});

	//player button control
	$(document).on('audio:pause', 'audio', function(e){
		var audio = e.target;
		audio.pause();
		$(this).parent().find('[role="pause"]').hide();
		$(this).parent().find('[role="play"]').show();
	});
	$(document).on('audio:play', 'audio', function(e){
		var audio = e.target;
		audio.play();
		$(this).parent().find('[role="pause"]').show();
		$(this).parent().find('[role="play"]').hide();
	});
	$(document).on('click', '[role="pause"]', function(e){
		var audio = $(e.target).parents('[role="player"]').find('audio');
		audio.trigger('audio:pause');
	});
	$(document).on('click', '[role="play"]', function(e){
		var audio = $(e.target).parents('[role="player"]').find('audio');
		audio.trigger('audio:play');
	});
});