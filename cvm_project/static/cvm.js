//Django CSRF stuff
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

var cvmManager = {
    candidate_img : ["bachmann.png", "gingrich.png", "huntsman.png", "obama.png", "paul.png", "perry.png", "romney.jpg", "santorum.png"],
    random_img : ["noun_project_1025.png", "noun_project_1566.png", "noun_project_2165.png", "noun_project_2732.png", "noun_project_541.png", "noun_project_104.png", "noun_project_1580.png", "noun_project_2172.png", "noun_project_2755.png", "noun_project_3198.png", "noun_project_598.png", "noun_project_1067.png", "noun_project_1618.png", "noun_project_2211.png", "noun_project_2823.png", "noun_project_31.png", "noun_project_605.png", "noun_project_10.png", "noun_project_2313.png", "noun_project_2849.png", "noun_project_322.png", "noun_project_644.png", "noun_project_1142.png", "noun_project_2324.png", "noun_project_2886.png", "noun_project_325.png", "noun_project_671.png", "noun_project_1144.png", "noun_project_1680.png", "noun_project_2406.png", "noun_project_289.png", "noun_project_328.png", "noun_project_69.png", "noun_project_1160.png", "noun_project_171.png", "noun_project_2409.png", "noun_project_293.png", "noun_project_330.png", "noun_project_761.png", "noun_project_1169.png", "noun_project_2416.png", "noun_project_2957.png", "noun_project_3325.png", "noun_project_1202.png", "noun_project_1822.png", "noun_project_2443.png", "noun_project_296.png", "noun_project_337.png", "noun_project_776.png", "noun_project_1248.png", "noun_project_1844.png", "noun_project_2455.png", "noun_project_3013.png", "noun_project_338.png", "noun_project_804.png", "noun_project_1253.png", "noun_project_188.png",  "noun_project_3018.png", "noun_project_339.png", "noun_project_805.png", "noun_project_1993.png", "noun_project_2472.png", "noun_project_3054.png", "noun_project_403.png", "noun_project_814.png", "noun_project_1.png", "noun_project_253.png", "noun_project_3066.png", "noun_project_410.png", "noun_project_815.png", "noun_project_1332.png", "noun_project_2023.png", "noun_project_2569.png", "noun_project_3077.png", "noun_project_416.png", "noun_project_818.png", "noun_project_137.png", "noun_project_2044.png", "noun_project_2597.png", "noun_project_3129.png", "noun_project_428.png", "noun_project_819.png", "noun_project_1434.png", "noun_project_2066.png", "noun_project_2613.png", "noun_project_3132.png", "noun_project_460.png", "noun_project_861.png", "noun_project_1527.png", "noun_project_2146.png", "noun_project_2636.png", "noun_project_3178.png", "noun_project_49.png", "noun_project_1564.png", "noun_project_2163.png", "noun_project_2666.png", "noun_project_3181.png", "noun_project_4.png"],

    sources : ['article', 'editorial', 'blog post', 'discussion thread', 'campaign email'],
    qualities : ['very high', 'high', 'low', 'very low'],
    codebooks : ['facts, sources, and evidence', 'objective tone', 'public import', 'infotainment', 'emotional reactions', 'divisiveness', 'respect for others', 'emotional appeals', 'divisiveness', 'respect for others'],
    usernames : [],
    //urls : ['the dailykos', 'whitehouse.gov', 'the NYTimes', 'the WSJ', 'the Washington Post', 'gawker.com', 'Michelle Malkin', 'usenet'],
    //These are popular political sites identified in a focused crawl of the web.
    urls : ["adisgruntledrepublican.com", "americablog.com", "americanthinker.com", "nlt.ashbrook.org", "barkbarkwoofwoof.com", "batr.org", "baumbach.org", "biased-bbc.blogspot.com", "biopsychiatry.com", "sabbah.biz", "blacks4barack.com", "consul-at-arms2.blogspot.com", "jailhouselawyersblog.blogspot.com", "wolfhowling.blogspot.com", "biased-bbc.blogspot.com", "smalltalkwitht.blogspot.com", "socraticgadfly.blogspot.com", "kennethdfranks.blogspot.com", "afrikaner-genocide-achives.blogspot.com", "grayee.blogspot.com", "traditional-catholic-prayers.blogspot.com", "daisysdeadair.blogspot.com", "saberpoint.blogspot.com", "shimronletters.blogspot.com", "blogfromonhigh.blogspot.com", "historyscoper-islamwatch.blogspot.com", "metaphysicalperegrine.blogspot.com", "bookerrising.net", "bookninja.com", "bradblog.com", "pithy.butnowyouknow.net", "cagle.com", "cahsrblog.com", "cato.org", "pjmedia.com", "wn.com", "whitehouse12.com", "likethedew.com", "ansionnachfionn.com", "townhall.com", "fullmetalpatriotblog.com", "wattsupwiththat.com", "biggovernment.com", "dailycaller.com", "pajamasmedia.com", "nofrakkingconsensus.com", "michellemalkin.com", "order-order.com", "donklephant.com", "scaredmonkeys.com", "politicalbyline.com", "organizationsandmarkets.com", "veracityvoice.com", "ethicsforadversaries.com", "frontpagemag.com", "offthekuff.com", "majorityinms.com", "definingthenarrative.com", "reflectionsofarationalrepublican.com", "noplaceforsheep.com", "endtimestoday.com", "superfrenchie.com", "21stcenturywire.com", "thedisorderofthings.com", "catholiclane.com", "twawki.com", "footnotes2plato.com", "vox-nova.com", "cifwatch.com", "underthemountainbunker.com", "lettingfreedomring.com", "howtheuniversityworks.com", "indiancountrytodaymedianetwork.com", "volokh.com", "crimefilenews.com", "topics.dailycaller.com", "dailykos.com", "dumpbachmann.com", "economist.com", "eureferendum.blogspot.com", "everydaycitizen.com", "feministlawprofessors.com", "firstthings.com", "foreignpolicy.com", "gaypatriot.net", "gnxp.com", "healingcombattrauma.com", "blog.heritage.org", "hoover.org", "humanevents.com", "irishhistorypodcast.ie", "williambowles.info", "infowars.com", "intellectualconservative.com", "israeli-occupation.org", "jihadwatch.org", "jpost.com", "kennethdurden.com", "blog.kentforliberty.com", "mars2earth.blogspot.com", "usconstitution.meetup.com", "politics.meetup.com", "liberty.meetup.com", "freedom.meetup.com", "localpolitics.meetup.com", "tea-party.meetup.com", "conservative.meetup.com", "libertarian.meetup.com", "mypetjawa.mu.nu", "ace.mu.nu", "nationaljournal.com", "global.nationalreview.com", "nationalreview.com", "alternativenewsreport.net", "dprogram.net", "butnowyouknow.net", "photonicportal.net", "nzclimatescience.net", "nannystateliberationfront.net", "andrewroman.net", "yourdaddy.net", "chicagoboyz.net", "video.nytimes.com", "opednews.com", "constitutionclub.org", "thecampofthesaints.org", "thinkprogress.org", "politicalvelcraft.org", "jonathanturley.org", "platypus1917.org", "intelnews.org", "bellacaledonia.org.uk", "kafila.org", "stephaniemcmillan.org", "rmiglobal.org", "ansnuclearcafe.org", "spectator.org", "orlytaitzesq.com", "patheos.com", "peter-ould.net", "politico.com", "politicususa.com", "politikditto.com", "powerlineblog.com", "prolifeblogs.com", "qando.net", "rawstory.com", "realclearpolitics.com", "realzionistnews.com", "redstate.com", "riehlworldview.com", "ronpaul.com", "rumormillnews.com", "saberpoint.blogspot.com", "sajaforum.org", "salon.com", "samefacts.com", "sarah-palin-2012.blogspot.com", "singularity2050.com", "slate.com", "socialistparty.org.uk", "state.gov", "stoptheaclu.com", "store.tcpress.com", "blogs.telegraph.co.uk", "theatlantic.com", "theblaze.com", "thecenterlane.com", "andrewsullivan.thedailybeast.com", "thedissidentfrogman.com", "thegatewaypundit.com", "thejidf.org", "thelibertypapers.org", "themaritimesentry.com", "thenation.com", "theodoresworld.net", "theotherrussia.org", "think-israel.org", "thinking-catholic-strategic-center.com", "thunderrun.us", "rodonline.typepad.com", "atlasshrugs2000.typepad.com", "marcmasferrer.typepad.com", "weaselzippers.us", "vanguardnewsnetwork.com", "washingtonmonthly.com", "washingtontimes.com", "weeklystandard.com", "whitehouse.gov", "wolfhowling.blogspot.com", "maboulette.wordpress.com", "sadbastards.wordpress.com", "thisblksistaspage.wordpress.com", "danieljmitchell.wordpress.com", "loveandgarbage.wordpress.com", "robertlindsay.wordpress.com", "openparachute.wordpress.com", "elmsprogressivemedia.wordpress.com", "msrb.wordpress.com", "thedaleygator.wordpress.com", "fma7.wordpress.com", "sentient.wordsof.org"],
    tags : ['objective', 'factual', 'divisive', 'angry', 'respectful', 'storytelling', 'quantitative'],
    
    sluggify : function (text){
		return text.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();;
	},
	
    getRandomArrayVal : function(A){
		return A[Math.floor(Math.random() * A.length)];
	},

	getRandomImage : function(){
		return "/static/img/random/"+cvmManager.random_img[Math.floor(Math.random() * cvmManager.random_img.length)];
	},
    
    getRandomSource : function(){
        return cvmManager.sources[Math.floor(Math.random()*cvmManager.sources.length)]
    },

    getRandomUrl : function(){
        return cvmManager.urls[Math.floor(Math.random()*cvmManager.urls.length)]
    },
    
    getRandomQuality: function(){
        return cvmManager.qualities[Math.floor(Math.random()*cvmManager.qualities.length)]
    },

    getRandomCodebook : function(){
        return cvmManager.codebooks[Math.floor(Math.random()*cvmManager.codebooks.length)]
    },
    
    getRandomTags : function(n){
        var a = cvmManager.tags;
        for(var j, x, i = a.length; i; j = parseInt(Math.random() * i), x = a[--i], a[i] = a[j], a[j] = x);
        return a.slice(0,n).join(", ");//cvmManager.tags[Math.floor(Math.random()*cvmManager.tags.length)]
    }    
};


$(function(){
    $('.modal').on('show', function(e) {
        var modal = $(this);
        modal.css({
            'position': 'fixed'
        });

 //       modal.click(function(){$(this).modal('hide')});
        return this;
    });
//    .hide();

    //.open-modal buttons open modal dialogs
    //The dialog must be the next element in the DOM after the button
    $(".open-modal").click(function(){
      $(this).next().modal({'backdrop': 'static'});
    });

	//"Cancel" buttons in modals
    $("button[type='cancel']").click(function(){
      //event.preventDefault();
      //Get the first ancsetor modal to this button, and hide it
      $(this).parents(".modal:first").modal('hide');
      return false;
    });

/*
    //.open-modal buttons open modal dialogs
    //The dialog must be the next element in the DOM after the button
    $(".open-modal").click(function(){
      $(this).next().modal({'backdrop': 'static'});
    });
*/

    $("#sign-in-btn").click(function(){
      $("#sign-in-modal").modal({'backdrop': 'static'});
    });

/*
    //"Cancel" buttons in modals
    $("button[type='cancel']").click(function(){
      //event.preventDefault();
      //Get the first ancsetor modal to this button, and hide it
      $(this).parents(".modal:first").modal('hide');
      return false;
    });
*/

    $('form:not(.tb-basic)').submit(function() {
        //event.preventDefault();
        var form = $(this);
        //console.log(form.serializeArray());
        $.post(
            form.attr('tb-href'),
            form.serializeArray(),
            function(data){

                //If the AJAx call succeeded
                if( data.status == "success" ){

                  //...and the form has "tb-redirect"
                  if( form.attr("tb-redirect") ){
                    //Redirect to the designated url
                    location.href = form.attr("tb-redirect");

                  //...or if the AJAX response designates a redirect target URL
                  }else if( data.redirect ){
                    //Redirect to the designated url
                    location.href = data.redirect;
                  }

                //If the AJAX call failed
                }else{
                  //! Give some kind of alert
                  alert( data.msg );
                }
                //alert(JSON.stringify(data));
            },
            'json'
        );
        return false;
    });



	//Add quick-links
	$("#mini-blocks h3").each(function(i,t){
		var tag = $(t);
		var text = tag.html();
		var slug = cvmManager.sluggify(text);

		tag.parent().attr("id", slug);
		$("#quick-links").append("<li><a href='#"+slug+"'>"+text+"</a></li>");
	})
	
	//Add random pictures
	$("#mini-blocks div.well:not(:has(img))").each(function(i,b){
		$(b).prepend('<img src="'+cvmManager.getRandomImage()+'" class="flavor-pic"></img>');
	});
	
	//Add corner-right divs to mini-block flavor-pics
	$("#mini-blocks div.well img.flavor-pic").each(function(i,b){
		var $b = $(b);
		var img = b.outerHTML;
		$b.replaceWith( '<div class="corner-right">'+img+'</div>');
	});
	
	//Hide remaining yes-do-this buttons
	$(".yes-do-this").hide();
	
	/*
	$("#mini-blocks div.well img.flavor-pic").each(function(i,b){
		var $b = $(b);
		var img = b.outerHTML;
		$b.replaceWith( '<div class="corner-right">'+img+'<br/><span class="label yes-do-this">Good idea!</span></div>');
	});
	$("span.yes-do-this").parent()
		.css({cursor:"pointer"})
		.hover(
			function(event){
				$(".yes-do-this", this).addClass("label-important");
				return false;
			},
			function(event){
				$(".yes-do-this", this).removeClass("label-important");
				return false;
			}
		)
		.click(function(){
			$(".yes-do-this", this).addClass("label-info");
		});
	*/
	
/*		.mouseover( function(event){
			event.stopPropagation();
			$(".yes-do-this", event.target).addClass("label-info");
		})
		.mouseout( function(event){
			event.stopPropagation();
			$(".yes-do-this", event.target).removeClass("label-info");
		});
*/
	
	//Add popover triggers to quick-links entries
	/*
	$("#quick-links li").click(function(event){
		var div = $($(event.target).attr("href"));
		
		div.popover({
				title:"Here it is!",
				//content:"Here it is!",
				placement:'top',
				trigger:'None',
				delay:200
				
			})
			.popover('show')
			.mouseover(function(){
				$(this).popover('hide')
			});
	});
	*/
    
    //Clickable table rows have "href" attributes    
    $('tr[href], .cvm-big-button')
        .hover(function(){
            $(this).addClass("tr-hilight");
        }, function(){
            $(this).removeClass("tr-hilight");
        })
/*        .click(function(){
            location.href = $(this).attr('href');
        });
*/
	//Use h4 headers as toggles for following content
	$("h4")
		.css({"cursor":"pointer"})
		.each(function(i,h){ $(h).html('<a class="">'+$(h).html()+'</a>')})
		.click(function(){
			$(this).next().slideToggle();
		})
		.next().hide();
	
	//Set up AB test on the appeals dialog
	var current_domain =  document.location.hostname;
	/*
	var referring_domain =  document.referrer.split('/')[2];
	console.log(referring_domain);
	console.log(current_domain);
	console.log(referring_domain == current_domain);
	*/
	
	/*
	//Put a random appeal-blurb in the help-funding modal.
	$(".appeal-blurb")
		.hide()
		.each(function(i,b){
			$(b).data("slug", cvmManager.sluggify($("strong:first", b).html()) );
		});
	var blurbs = $(".appeal-blurb").get().sort(function(){ 
			return Math.round(Math.random())-0.5
		});
	$(blurbs[0]).show();
	//console.log($(blurbs[0]).data("slug"));
	*/

/*
	//Add GAnalytics instrumentation to everything
	if( !current_domain.match(/localhost/) ){
		$("h4").click(function(){
			
		})
	}
*/

	//Add lorem as needed
	$("p").each(function(i,p){
		if( $(p).html() == "..." ){
			$(p).lorem({ type: 'words',amount:(Math.round(Math.random()*30)+8),ptags:true});
		}
	});

	//Masonify pages after all images load.
	$('#mini-blocks').imagesLoaded( function(){
		$('#mini-blocks').masonry({
			itemSelector : 'div.cvm-masonry',
			columnWidth: 290
		});
	});

	//Plug in a random suggestion tweet
	var tweets = [
		'Neat @knightfnd #newschallenge entry: a "@civilometer" for tracking civility in news and politics.',
		'Check out the @civilometer: data tools for political civility and accountability. @knightfnd #newschallenge',
		'Check out this @knightfnd #newschallenge project: A political @civilometer, just in time for election season!',
		'I support the political @civilometer in the @knightfnd #newschallenge.  RT if you like it too!',
		'Prototype page for a political @civilometer.  RT and like so they can get funding from the @knightfnd #newschallenge!',
		'This project will monitor civility in US media. Check it out! @civilometer #newschallenge',
		'Cool concept: data tools for political civility. @civilometer #newschallenge'
		]
     $("#twitter-btn").attr("data-text", tweets[Math.floor(Math.random()*tweets.length)]);

    //Automagically trigger "auto" actions
    $(".auto").click(); 	
});



