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
    
function Print(){
    document.body.offsetHeight;window.print()
};

function StyleCode() 
{
    if (typeof disableStyleCode != "undefined") 
    {
        return;
    }

    var a = false;

    jQuery("pre code").parent().each(function() 
    {
        if (!jQuery(this).hasClass("prettyprint")) 
        {
            jQuery(this).addClass("prettyprint");
            a = true
        }
    });
    
    if (a) { prettyPrint() } 
}