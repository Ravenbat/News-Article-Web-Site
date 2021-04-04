fetch('https://api.exchangeratesapi.io/latest?base=USD')
.then(response => {
    return response.json();
})
.then(users =>{
    var newStr2 = JSON.stringify(users)
    var newStr3 = newStr2.substring(10, 180)
    document.querySelector('#json').innerHTML = newStr3;
})
let x = document.querySelector("#location");
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  x.innerHTML = "Latitude: " + position.coords.latitude +
  "<br>Longitude: " + position.coords.longitude;
}
document.querySelectorAll('#editButton').forEach(button =>{
    let commentText = button.previousElementSibling;   // Getting the comment text and saving it to variable
    button.onclick = function() {
        document.querySelector('#editArea').style.display = "block";    // Showing the textarea
        document.querySelector('#saveButton').onclick = function(button) {
            let saveButton = button.target                                     // target getting the element being clicked on
            let commentId = saveButton.previousElementSibling;                 // using previousElementSibling to go back to previous element to get id, comment
            let editedComment = commentId.previousElementSibling;
            document.querySelector('#editArea').style.display = "none";
            editComment(commentId.innerHTML, editedComment.value);
            commentText.innerHTML = editedComment.value;
        }
    }
})
function editComment(id, newComment){
    fetch(`comment/update/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            newComment: newComment
        })})
      .then(response => response.json())
      .then(comment => {
          console.log(comment)
      })
          // ... Updating comment ...
      }
    

            
