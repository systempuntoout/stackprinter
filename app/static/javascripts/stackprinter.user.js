// ==UserScript==
// @name           Stack Overflow: StackPrinter
// @namespace      http://userscripts.org/users/gangsta75
// @description    Add Printer-Friendly button to question
// @include        http://stackoverflow.com/questions/*
// @include        http://serverfault.com/questions/*
// @include        http://superuser.com/questions/*

// ==/UserScript==

function wait() {
	if(typeof unsafeWindow.jQuery != 'function') { 
		window.setTimeout(wait, 100); 
	} else {
	        var linkTokens = window.location.href.split('/');
	        var domainTokens= linkTokens[2].split('.');
	        var service = domainTokens[0];     
	        unsafeWindow.jQuery('#question .vote:first').append('<div id="PrinterFriendly" style="margin-top:8px"><a alt="Printer-Friendly" title="Printer-Friendly" href="javascript:(function(){f=\'http://stackprinter.appspot.com/export?format=HTML&service='+service+'&question='+unsafeWindow.jQuery('.vote').find('input[type=hidden]:first').val()+'\';a=function(){if(!window.open(f))location.href=f};if(/Firefox/.test(navigator.userAgent)){setTimeout(a,0)}else{a()}})()"><img width="33px" height="33px" src="http://stackprinter.appspot.com/images/printer.gif"</img></a></div>');		
	}
}
wait();

