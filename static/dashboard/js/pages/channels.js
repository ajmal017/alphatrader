window.ATChannels = ( function( window, document, $ ){

	var atchannels = {};

	atchannels.init = function(){
		atchannels.username = atlocalised.username;
		atchannels.chname = atlocalised.chname;

		console.log(atlocalised.username)


		$(".plus_btn").on('click',function(){
				$(".message_menu").show();
				$('.plus_btn').addClass('plus_btn_focus');


		});	
		$(".channels_btn").on('click',function(evt){
			    evt.preventDefault();

				$(".channel_list").show();

		});	

		$(".enlarge_sidebar").on('click',function(evt){
			    evt.preventDefault();
			    if($(".ch_sidebar_parent").hasClass('col-lg-3')){
			    	$(".ch_sidebar_parent").removeClass('col-lg-3');
			    	$(".ch_message_box_parent").removeClass('col-lg-9');
			    	$(".ch_message_box_parent").addClass('col-lg-3');
					$(".ch_sidebar_parent").addClass('col-lg-9');
			    	$(".enlarge_sidebar i").css('transform','rotate(180deg)');

			    }else{
			    	$(".ch_message_box_parent").removeClass('col-lg-3');

					$(".ch_sidebar_parent").removeClass('col-lg-9');
			    	$(".ch_sidebar_parent").addClass('col-lg-3');
			    	$(".ch_message_box_parent").addClass('col-lg-9');
			    	$(".enlarge_sidebar i").css('transform','rotate(0deg)');

			    }

		});					
		$(document).on('click touch', function(event) {
		  if (!$(event.target).parents().addBack().is('.plus_btn')) {
		    $('.message_menu').hide();
		    $('.plus_btn').removeClass('plus_btn_focus');

		  }
		  if (!$(event.target).parents().addBack().is('.channels_btn')) {
		    $('.channel_list').hide();
		  }		  
		});

		atchannels.fix_channel_responsive();

		atchannels.update_scroll();

		atchannels.init_websocket();

		atchannels.init_messenger();
		// atchannels.init_channels();



	};

	atchannels.fix_channel_responsive = function(){
		var height_of_browser = $(window).height();
		console.log(height_of_browser)

		// $(".ch_message_box").height(height_of_browser);
		$(".ch_sidebar").height(height_of_browser);
		$(".ch_message_box_parent").height(height_of_browser);
		$(".page-inner").height(height_of_browser-66);

	}
	atchannels.init_websocket = function(){
		// Correctly decide between ws:// and wss://
		var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
		var ws_path = ws_scheme + '://' + window.location.host + "/chat/room1/";
		console.log("Connecting to " + ws_path);
		atchannels.socket = new ReconnectingWebSocket(ws_path);
		atchannels.socket.debug = true;
		atchannels.socket.timeoutInterval = 5400;
		// Helpful debugging
		atchannels.socket.onopen = function () {
		    console.log("Connected to chat socket");
		};

		atchannels.socket.onclose = function () {
		    console.log("Disconnected from chat socket");
		};

		atchannels.socket.onmessage = function (message) {
		    // Decode the JSON
		    console.log("Got websocket message " + message.data);
		    var data = JSON.parse(message.data);
		    // Handle errors
		    if (data.error) {
		        alert(data.error);
		        return;
		    }
			
			if (data.message || data.msg_type != 0) {
			    var msgdiv = $("#channel-" + data.channel_id + " .messages");
			    var ok_msg = "";
			    // msg types are defined in chat/settings.py
			    // Only for demo purposes is hardcoded, in production scenarios, consider call a service.
			    switch (data.msg_type) {
			        case 0:
			            // Message
			            atchannels.add_message(data)
			            break;
			        case 1:
			            // Warning/Advice messages
			            atchannels.add_message(data);
			            atchannels.update_scroll();
			            break;
			        default:
			            console.log("Unsupported message type!");
			            return;
			    }
			    // msgdiv.append(ok_msg);
			    // msgdiv.scrollTop(msgdiv.prop("scrollHeight"));
			} else {
				// ...
			  console.log("Cannot handle message!");
	
			}
		};

	};

	atchannels.update_scroll = function (){
		console.log("Updating scroll");
	    var element = $(".message_area");
	    element.scrollTop(element[0].scrollHeight);
	};

	atchannels.init_messenger = function(){
		$('.message_text textarea').keypress(function (e) {
		  if (e.which == 13) {
		    $(".send_btn button").trigger('click');
		    return false;    //<---- Add this line
		  }
		});		
		$(".send_btn button").on('click',function(evt){
			    evt.preventDefault();

				var message = $(".message_text textarea").val();
				console.log(message);
				if(message != ""){
					atchannels.send_message(message,atchannels.chname);
					$(".message_text textarea").val("");					
				}


		});	
	};


	// atchannels.init_channels = function(){
	// 	$("li.channel-link").click(function () {
	// 	    channel_id = $(this).attr("data-channel-id");
	// 	    if (atchannels.in_channel(channel_id)) {
	// 	        // Leave room
	// 	        $(this).removeClass("joined");
	// 	        socket.send(JSON.stringify({
	// 	            "command": "leave",  // determines which handler will be used (see chat/routing.py)
	// 	            "channel": channel_id
	// 	        }));
	// 	    } else {
	// 	        // Join room
	// 	        $(this).addClass("joined");
	// 	        socket.send(JSON.stringify({
	// 	            "command": "join",
	// 	            "channel": channel_id
	// 	        }));
	// 	    }
	// 	});
	// };

	atchannels.send_message = function(message,channel_id){
		atchannels.socket.send(JSON.stringify({
            "command": "send",  // determines which handler will be used (see chat/routing.py)
            "message": message,
            "channel": channel_id,
            "username": atchannels.username
        }));
	};

	atchannels.add_message = function(data){
		var div;
		// data.message = atchannels.parse_message(data.message);
		var message_area = "#channel-"+data.channel_id
		if(data.username == atchannels.username){
			div = "<div class='message self'>"+
							"<div class='user_icon'><img src='"+data.icon_link+"'></div>"+
							"<div class='msg_main'>"+
								"<div class='meta'>"+
									"<p class='username'>@"+data.username+"</p>"+
									"<p class='message_posted'>"+data.posted_at+"</p>"+
								"</div>"+
								"<p class='message_content'>"+data.message+"</p>"+
							"</div>"+
						"</div>";
		}else{
			div = "<div class='message'>"+
							"<div class='user_icon'><img src='"+data.icon_link+"'></div>"+
							"<div class='msg_main'>"+
								"<div class='meta'>"+
									"<p class='username'>@"+data.username+"</p>"+
									"<p class='message_posted'>"+data.posted_at+"</p>"+
								"</div>"+
								"<p class='message_content'>"+data.message+"</p>"+
							"</div>"+
						"</div>";
		}

		$(message_area).append(div);				

	};

	atchannels.parse_message = function(){

	};

	atchannels.in_channel = function(channel_id){
		return $("#channel-" + channel_id).length > 0;
	};

    // atchannels.start_full_trader = function(evt){
    //   evt.preventDefault();

    //       var post_data = {
    //           action     : 'at_full_start',
    //           enable_analyst: 0,

    //          'csrfmiddlewaretoken': _at.csrf_token

    //          // nonce: nonce,
    //       };

    //       $.ajax({
    //         type: "POST",
    //         url: alphatrader._url,
    //         data: post_data,
    //         success: alphatrader.process_response,
    //         dataType: 'json',
    //         error: alphatrader.process_error,
    //         timeout : 40000

    //       });


    // };


	$(document).ready( atchannels.init );

	return atchannels;

})( window, document, jQuery );