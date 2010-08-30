 function quicklook(question_id, service){
        var jQuerydialog = jQuery('<div>loading <img src="/images/indicator.gif"/></div>');
         jQuerydialog.dialog({
			title: '[Q]uicklook',
			width: '650px',
			modal: true,
			position: ['center', 95]});
		jQuerydialog.load('/quicklook?question='+ question_id +'&service='+service,'', function (responseText, textStatus, XMLHttpRequest) {
        	}
        );
        return false;
    }