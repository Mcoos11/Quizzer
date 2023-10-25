function passwordToggle() {
  var x = document.getElementById("pass_name");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}