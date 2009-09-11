function todayStr() {
     var today=new Date()
     day=today.getDate()+''
     month=(today.getMonth()+1)+''
     if (day.length==2) {
      day=day }
     else {
      day="0"+day}
     if (month.length==2) {
      month=month }
     else {
      month="0"+month}


     return (today.getYear() + 1900) +"-"+month+"-"+day
/*     return today.getMonth()+1+"/"+today.getDate()+"/"+(today.getYear() + 1900)*/
   }


var Dom = {
	get: function(el) {
		if (typeof el === 'string') {
			return document.getElementById(el);
		} else {
			return el;
		}
	},
	add: function(el, dest) {
		var el = this.get(el);
		var dest = this.get(dest);
		dest.appendChild(el);
	},
	remove: function(el) {
		el.parentNode.removeChild(el);
	}
};


var Event = {
	add: function() {
		if (window.addEventListener) {
			return function(el, type, fn) {
				Dom.get(el).addEventListener(type, fn, false);
			};
		} else if (window.attachEvent) {
			return function(el, type, fn) {
				var f = function() {
					fn.call(Dom.get(el), window.event);
				};
				Dom.get(el).attachEvent('on' + type, f);
			};
		}
	}()
};

// Add imgs-input-boxes at will

Event.add(window, 'load', function() {
	var i = 0;
	var n = 0;
	Event.add('add-date', 'click', function() {
	var del = document.createElement('span');
	del.innerHTML = '<img src="/images/minus.png"> ';
	Dom.add(del, 'dates');
	var el = document.createElement('span');
	el.innerHTML = '<input name="date'+ ++i +'" type="text" value='+todayStr()+' /> <br />';
	Dom.add(el, 'dates');
		Event.add(del, 'click', function(e) {
			Dom.remove(el);
			Dom.remove(this);
		});
	});

});
