$("main").addClass("pre-enter").removeClass("with-hover");
setTimeout(function(){
	$("main").addClass("on-enter");
}, 500);
setTimeout(function(){
	$("main").removeClass("pre-enter on-enter");
	setTimeout(function(){
		$("main").addClass("with-hover");
	}, 50);
}, 2000);

$(".flip, .back a").click(function(){
	$(".player").toggleClass("playlist");
});

$(".bottom a").not(".flip").click(function(){
	$(this).toggleClass("active");
});

var audcon = document.getElementById('audio1');

var time_of_current = document.getElementById('time_of_current');
var duration_of_audio = document.getElementById('duration_of_audio');

var plbar = document.getElementById('plbar')
var aud_dur = 0.0;

function loop() {

    var aud_cur = audcon.currentTime;

    time_of_current.innerHTML = aud_cur;

    plbar.style.width = (200 * aud_cur / aud_dur).toFixed(2) + '%';

    setTimeout(loop, 50);
}
loop();

// html5media enables <video> and <audio> tags in all major browsers
// External File: http://api.html5media.info/1.1.8/html5media.min.js


// Add user agent as an attribute on the <html> tag...
// Inspiration: http://css-tricks.com/ie-10-specific-styles/
var b = document.documentElement;
b.setAttribute('data-useragent', navigator.userAgent);
b.setAttribute('data-platform', navigator.platform);


// HTML5 audio player + playlist controls...
// Inspiration: http://jonhall.info/how_to/create_a_playlist_for_html5_audio
// Mythium Archive: https://archive.org/details/mythium/
jQuery(function ($) {
    var supportsAudio = !!document.createElement('audio').canPlayType;
    if (supportsAudio) {
        var index = 0,
            playing = false,
            trackCount = tracks.length,
            npAction = $('#npAction'),
            npTitle = $('#npTitle'),
            audio = $('#audio1').bind('play', function () {
                playing = true;
                npAction.text('Now Playing...');
            }).bind('pause', function () {
                playing = false;
                npAction.text('Paused...');
            }).bind('ended', function () {
                npAction.text('Paused...');
                if (index + 1 < trackCount) {
                    index = index + 1;
                    loadTrack(index);
                    audio.play();
                } else {
                    audio.pause();
                    index = 0;
                    loadTrack(index);
                }
            }).get(0),
            btnPrev = $('#btnPrev').click(function () {
                audio.pause();
                if (index - 1 > -1) {
                    index = index - 1;
                    loadTrack(index);
                    if (playing) {
                        audio.play();
                    }
                } else {
                    index = 0;
                    loadTrack(index);
                    audio.play();
                }
            }),
			btnPlay = $('#btnPlay').click(function() {
					if (playing == true) {
					    audio.pause();
					} else {
					    audio.play();
					}
			}),
            btnNext = $('#btnNext').click(function () {
                audio.pause();
                if (index + 1 < trackCount) {
                    index = index + 1;
                    loadTrack(index);
                    if (playing) {
                        audio.play();
                    }
                } else {
                    var btn = document.getElementById('mrkUlim');

                    index = 0;
                    loadTrack(index);
                    audio.play();
                    if (btn.className != 'active') {
                        audio.pause();
                    }
                }
            }),
            li = $('#plList li').click(function () {
                var id = parseInt($(this).index());
                if (id !== index) {
                    playTrack(id);
                }
            }),
            loadTrack = function (id) {
                $('.plSel').removeClass('plSel');
                $('#plList li:eq(' + id + ')').addClass('plSel');
                npTitle.text(tracks[id].name);
                index = id;
                aud_dur = tracks[id].length;
                audio.src = tracks[id].path;
                duration_of_audio.innerHTML = aud_dur;
            },
            playTrack = function (id) {
                loadTrack(id);
                audio.play();
            };
        extension = audio.canPlayType('audio/mpeg') ? '.mp3' : audio.canPlayType('audio/ogg') ? '.ogg' : audio.canPlayType('audio/mp4') ? '.mp4' : '';
        loadTrack(index);
    }
});