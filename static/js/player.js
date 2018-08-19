// entry
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
// end entry

// animation
$(".flip, .back a").click(function(){
	$(".player").toggleClass("playlist");
});

$(".bottom a").not(".flip").click(function(){
	$(this).toggleClass("active");
});
// end animation

// playbar animation
var aud = document.getElementById('audio1');

var time_cur = document.getElementById('time_of_current');
var dur_aud = document.getElementById('duration_of_audio');

var plbar = document.getElementById('plbar');
var aud_cur = 0.0;
var aud_dur = 0.0;
var cmn = 0;
var nmn = 0;

function loop(){
    aud_cur = aud.currentTime;
    time_cur.innerHTML = aud_cur;
    plbar.style.width = (200 * aud_cur / aud_dur).toFixed(2) + '%';
    setTimeout(loop, 50);
}
loop();
// playbar animation

// audio player
    // Add user agent as an attribute on the <html> tag...
    // Inspiration: http://css-tricks.com/ie-10-specific-styles/
var b = document.documentElement;
b.setAttribute('data-useragent', navigator.userAgent);
b.setAttribute('data-platform', navigator.platform);
    // end add user agent

    // html5 audio player + playlist controls
jQuery(function ($) {
    var supportsAudio = !!document.createElement('audio').canPlayType;
    if (supportsAudio) {
        var index = 0,
            playing = false,
            trackCount = tracks.length,
            npNext = document.getElementById('npNext'),
            npTitle = document.getElementById('npTitle'),
			btnPlay = $('#btnPlay'),
			btnPause = $('#btnPause'),
			mrkUlim = $('#mrkUlim'),
			mrkRand = $('#mrkRand'),
			player = document.getElementById('player'),
			albart = document.getElementById('albumart'),
            audio = $('#audio1').bind('play', function () {
                playing = true;
                btnPlay.css('display', 'none');
                btnPause.css('display', 'block');
            }).bind('pause', function () {
                playing = false;
                btnPause.css('display', 'none');
                btnPlay.css('display', 'block');
            }).bind('ended', function () {
                if (index + 1 < trackCount) {
                    index = index + 1;
                    loadTrack(index);
                    audio.play();
                } else {
                    audio.pause();
                    index = 0;
                    loadTrack(index);
                    if (mrkUlim.hasClass('active')) {
                        audio.play();
                    }
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
                    index = tracks.length - 1;
                    loadTrack(index);
                    audio.play();
                }
            }),
			btnPlayfunc = btnPlay.click(function() {
					if (playing == false) {
					    audio.play();
					}
			}),
			btnPausefunc = btnPause.click(function(){
			        if (playing == true) {
			            audio.pause();
			        }
			}),
            btnNext = $('#btnNext').click(function () {
                audio.pause();
                if (mrkRand.hasClass('active')) {
                    index = Math.floor(Math.random() * tracks.length);
                    loadTrack(index);
                    audio.play();
                } else {
                    if (index + 1 < trackCount) {
                        index = index + 1;
                        loadTrack(index);
                        if (playing) {
                            audio.play();
                        }
                    } else {
                        index = 0;
                        loadTrack(index);
                        audio.play();
                    if (!mrkUlim.hasClass('active')) {
                        audio.pause();
                    }
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
                npTitle.innerHTML = tracks[id].name;

                if (mrkRand.hasClass('active')) {
                    npNext.innerHTML = 'Unknown.';
                } else {
                    if (id + 1 < trackCount) {
                        npNext.innerHTML = tracks[id + 1].name;
                    } else {
                        if (mrkUlim.hasClass('active')) {
                            npNext.innerHTML = tracks[0].name;
                        } else {
                            npNext.innerHTML = 'Fin.';
                        }
                    }
                }

                npTitle.className = 'curmusic';
                npNext.className = 'nxtmusic';
                npTitle.style.marginLeft = '0px';
                npNext.style.marginLeft = '0px';
                cmn = 0;
                nmn = 0;

                cmn = npTitle.offsetWidth - player.offsetWidth + 24;
                nmn = npNext.offsetWidth - player.offsetWidth + 24;

                if (cmn > 0) {
                    npTitle.classList.add('curmusicname');
                    npTitle.style.marginLeft = -1 * cmn + 'px';
                } else {
                    npTitle.style.marginLeft = '0px';
                }
                if (nmn > 0) {
                    npNext.classList.add('nxtmusicname');
                    npNext.style.marginLeft = -1 * nmn + 'px';
                } else {
                    npNext.style.marginLeft = '0px';
                }

                index = id;
                aud_dur = tracks[id].length;
                audio.src = "/player/" + tracks[id].name;  // Set Audio Location
                albart.src = "/picture/" + tracks[id].name; // Set AlbumArt
                duration_of_audio.innerHTML = aud_dur;
            },
            playTrack = function (id) {
                loadTrack(id);
                audio.play();
            };
        loadTrack(index);
    }
});
