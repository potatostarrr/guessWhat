function myFunction(x) {
	$.post( "/postmethod", {
		highscore: x,
		user: $("#username").text()
	});
}



//callback function to return google suggestion
function addScript(u){ 
   var s=document.createElement('script'); 
  s.src=u;  
  document.getElementsByTagName('*')[1].appendChild(s);
 }
function getQueryGoogle(term, callback){
   var id="i"+Math.random().toString(36).slice(2);
   getQueryGoogle[id]=function(data){ callback(data);delete getQueryGoogle[id];};
   addScript( "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20json%20where%20url%3D%22https%3A%2F%2Fsuggestqueries.google.com%2Fcomplete%2Fsearch%3Fclient%3Dfirefox%26q%3D"+
   encodeURIComponent(term)+
  "%22%20&format=json&callback=getQueryGoogle."+id );
}

//global array variable answer
answer = []
//global index variable to indicate current question
var questionIndex = 0 ;
//global variable score
var score = 0;
//gloabl variable fail times
var chance = 10;
//global variable indiating current correct answer number
var cnumber = 0;

//set replace all function to parse search query
String.prototype.replaceAll = function(str1, str2, ignore) 
{
    return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
} 


//update answer columns
function update(){
		$("#top5").empty();
		$("#top10").empty();
		
		
		
		for(i= 0; i < Math.min(answer.length, 5); i++){
			s = "_";for (j = 1;j<answer[i].length;j++){s += " _"};
			$("#top5").append("<li class= 'list-group-item list-group-item-info' id=" + i.toString() + ">"+ s +  "</li>");	
		};
		for(i= 5; i < Math.min(answer.length, 10); i++){
			s = "_";for (j = 1;j<answer[i].length;j++){s += " _"};
			$("#top10").append("<li class= 'list-group-item list-group-item-info' id=" + i.toString() + ">"+s+  "</li>");	
		};
}


$(function() {
	//initialnize answer column
	getQueryGoogle(question[questionIndex], function(d){
		answer = d.query.results.json.json[1].json
		q = question[questionIndex].replaceAll("%20", " ")
		for (i=0; i < answer.length; i++){
			answer[i]  =answer[i].replace(q, "")
			answer[i]  =answer[i].replace(" ", "")
		}
		update();
	
	});
	
	//initialnize question column
	$("#question").text(question[questionIndex].replaceAll("%20", " "))
	
	//add click event for skip button, change question and answer column
	$('#skip').click( function () {
			chance--;
			cnumber = 0;
			questionIndex += 1;
			$("#chance").text(chance.toString());
			$("#question").text(question[questionIndex].replaceAll("%20", " "))
			getQueryGoogle(question[questionIndex], function(d){
				answer = d.query.results.json.json[1].json
				q = question[questionIndex].replaceAll("%20", " ")
				for (i=0; i < answer.length; i++){
					answer[i]  =answer[i].replace(q, "")
					answer[i]  =answer[i].replace(" ", "")
				}
				update();
			});
		});
	
	//add click event for submit button, check if it's a correct answer, if yes then reveal answer and add score by 1 or 2
	//if wrong, minus current chance and if change is 0 change a question,
	$('#submitanswer').click( function () { 
			useranswer = $("#useranswer").val()
			if (useranswer == ""){
				$("#useranswer" ).attr("placeholder", "Plase enter answer!!!")
			}
			else{
				i = answer.indexOf(useranswer)
				if (i == -1){
					chance--;
					$("#chance").text(chance.toString());
					if (chance == 0){
						$("#answerArea").toggleClass("show hidden");
						$("#restartArea").toggleClass("hidden show");
					}
					else{
						$("#useranswer" ).val('');
						$("#useranswer" ).attr("placeholder", "Wrong... Try Again!")
						}
				}
				else {
					$("#useranswer" ).val('');
					$("#useranswer" ).attr("placeholder", "Enter Answer")
					$('#'+i.toString()).text(answer[i])
					answer[i] = ""
					score ++;
					if (i< 5){score++;}
					$("#score").text("Current Score: " + score.toString())
					if (score > highscore){
						highscore = score;
						$("#highscore").text(score.toString())
						myFunction(score);
					}
					cnumber++;
					if (cnumber == answer.length){
						chance++;
						$('#skip').click();
					}
					$("#useranswer" ).val('');
				}
			}	
		});
		
	$("#restart").click(function(){
		$("#restartArea").toggleClass("show hidden");
		$("#answerArea").toggleClass("hidden show");
		score = 0;
		cnumber = 0;
		questionIndex++;
		chance = 11;
		
		$("#chance").text(chance.toString());
		$('#skip').click();
		$("#useranswer" ).val('');
	})

		
	
})















