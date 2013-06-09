var TaskManager = function( game_session_id, csrf_token ){
    this.game_session_id = game_session_id;
    this.csrf_token = csrf_token;
    this.batch_index = null;  //Index of the currently visible document

    this.init = function(){
        this.initControls();
        this.initCodebook();
        
        var self = this;
        $.post(
            '/tasks/ajax/get-first-task/',
            //JSON.stringify({'gs_id': game_session_id, 'csrfmiddlewaretoken': csrf_token }),
            {'gs_id': this.game_session_id, 'csrfmiddlewaretoken': this.csrf_token },
            function(data){
                self.showDocument(data.document);
                self.markupGameStats(data.game_stats);
                self.activateSubmitBtn();
            },
            'json'
        );
    };
    
    this.submitTask = function(){
        var labels = {};
        
        var formVals = $('#codebook-form').serializeArray();
        for (i in formVals)
            labels[formVals[i].name] = formVals[i].value;
        
        //Disable subtmit button
        $("#submit-btn")
            .addClass("disabled")
            .off("click");

        var self = this;
        $.post(
            '/tasks/ajax/submit-task/',
            JSON.stringify({
                'game_session_id': self.game_session_id,
                'csrfmiddlewaretoken': self.csrf_token,
                'document_id': self.document_id,
                'labels': labels
            }),
            function(data){
                self.showMessage(data.game_stats);
                self.markupGameStats(data.game_stats);
                self.next_doc = data.next_document;
                
                if( data.status == "success" ){
                    self.nextTask();
                    
                    /*
                    //If the last task was *un*scored
                    if( data.game_stats.last_score == null ){
                        //...just keep going to the next task.
                        self.nextTask();
                    }else{
                        //Otherwise, pause for codebook markup.
                        self.markupCodebook(data.codebook_markup);
                        $("#submit-btn").fadeOut(function(){$("#next-btn").fadeIn();});
                    }
                    */
                }else{
                    alert(data.msg);
                }
            },
            'json'
        );
                    
        return false;
    };

    this.nextTask = function(){
        var self = this;
        //Toggle next and submit buttons
        $("#next-btn").fadeOut(function(){
            self.activateSubmitBtn();
        });

        //Clear codebook
        this.clearCodebook();
        
        //Load next document
        this.showDocument( this.next_doc );
        this.next_doc = null;
    };
    
    this.showDocument = function(doc){
		//Update batch_index
        this.document_id = doc.document_id;

        //Show the document
        $("#doc-box").html(doc.content);

        //Update navigation
        //this.updateControls();
    };
    
    this.activateSubmitBtn = function(){
        $("#submit-btn")
            .removeClass("disabled")
            .fadeIn()
            .click(function(){taskManager.submitTask();});
    };
    
    this.initControls = function(){        
        $("#next-btn")
            .hide()
            .click(function(){taskManager.nextTask(); });
        
        $("#submit-btn")
            .hide();
    };

    this.initCodebook = function(){
        //$(".shim-graph").hide();
    
        $(".clickable")
            .mouseover( function(){ $(this).addClass('mouseoverCell'); })
            .mouseout( function(){ $(this).removeClass('mouseoverCell'); })
            .click( function(event){
                if( event.target.type != 'checkbox' && event.target.type != 'radio' ){
                    $('input', this).trigger("click");
                }
    //            return false;
            });
    };
    
    this.clearCodebook = function(){
        $form = $("#codebook-form");
        $form.find('input:text, input:password, input:file, select, textarea').val('');
        $form.find('input:radio, input:checkbox')
             .removeAttr('checked').removeAttr('selected');  
    };

    this.showMessage = function(game_stats){
        var last_score = game_stats.last_score,
            avg_score = Math.floor(game_stats.avg_score * 10)/10,
            feedback = "Good work. ",
            alert_type = '';

        if( last_score == null ){
            msg = feedback+'That task was unscored, so your average is still ' + avg_score + '.'

        }else{
            var badge_type = '';

            if( last_score > 75 ){
                feedback = cvmManager.getRandomArrayVal(['Excellent','Great work','Fantastic','Superb','Super accurate'])+'! ';
                alert_type = 'alert-success';
                badge_type = 'badge-success';

            }else if( last_score > 50 ){
                feedback = cvmManager.getRandomArrayVal(['Very good','Great','Nice','Well done','Very accurate'])+'! ';                
                alert_type = 'alert-success';
                badge_type = 'badge-success';

            }else if( last_score > 25 ){
                feedback = cvmManager.getRandomArrayVal(['Nice','Good job','Well done','Good','Not bad'])+'! ';                
                alert_type = 'alert-success';
                badge_type = 'badge-success';
                
            }else if( last_score <= 25 ){
                feedback = cvmManager.getRandomArrayVal(['Uh oh','Ouch','Not so good','Hm'])+'. ';
                alert_type = 'alert-error';
                badge_type = 'badge-warning';
        
            }
            
            msg = feedback+' You scored <span class="badge '+badge_type+'">'+last_score+'</span> on that task, making your average ' + Math.floor(game_stats.avg_score * 10)/10 + '.'
        }
        
        $('<div class="alert '+alert_type+'"><button class="close" data-dismiss="alert">×</button>'+msg+'</div>')
            .hide()
            .prependTo( $('#messages') )
            .slideDown(200);
        $('#messages div.alert:gt(4)').each(function(i,alert_div){
            $alert_div = $(alert_div);
            $alert_div.fadeOut(function(){$alert_div.remove();});
        });
    };

    this.markupGameStats = function( game_stats ){
        $("#breadcrumb-total-score").html( Math.floor( game_stats.total_score * 10)/10 );
        $("#breadcrumb-avg-score").html( Math.floor(game_stats.avg_score * 10)/10 );
        $("#breadcrumb-tasks-completed").html( game_stats.tasks_completed );
        $("#breadcrumb-bonus-credits").html( game_stats.bonus_credits );
        
        $("#modal-total-score").html( Math.floor( game_stats.total_score * 10)/10 );
        $("#modal-exchange-rate").html( game_stats.exchange_rate );
        $("#modal-avg-score").html( Math.floor(game_stats.avg_score * 10)/10 );
        $("#modal-next-bonus").html( game_stats.tasks_until_next_bonus );
        $("#modal-tasks-completed").html( game_stats.tasks_completed );
        $("#modal-bonus-size").html( game_stats.bonus_size );
        $("#modal-bonus-credits").html( game_stats.bonus_credits );
        $("#modal-tasks-remaining").html( game_stats.tasks_remaining );
    };
    
    this.markupCodebook = function( codebook_markup ){};
};    

$(function(){
    $(".clickable")
        .mouseover( function(){ $(this).addClass('mouseoverCell'); })
        .mouseout( function(){ $(this).removeClass('mouseoverCell'); })
        .click( function(event){
            if( event.target.type != 'checkbox' && event.target.type != 'radio' ){
                x = $('input', this).trigger("click");
            }
        });
});
