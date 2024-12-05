//==================
// Dark & Light Mode
function toggleTheme() {
  var darkModeEnabled = getCookie("darkModeEnabled");
  if (darkModeEnabled == "on") {
      setCookie("darkModeEnabled", "off", 365)
      document.getElementsByTagName('body')[0].classList.remove("theme-dark");
      document.getElementsByTagName('body')[0].classList.add("theme-light");
      document.getElementsByTagName('body')[0].dataset.bsTheme = "light";
  } else {
      setCookie("darkModeEnabled", "on", 365)
      document.getElementsByTagName('body')[0].classList.remove("theme-light");
      document.getElementsByTagName('body')[0].classList.add("theme-dark");
      document.getElementsByTagName('body')[0].dataset.bsTheme = "dark";
  }
}

//==========================
// Load Cookie at Page Start
var darkModeEnabled = getCookie("darkModeEnabled");
if (darkModeEnabled == "on") {
  document.getElementsByTagName('body')[0].classList.add("theme-dark");
  document.getElementsByTagName('body')[0].dataset.bsTheme = "dark";
} else {
  document.getElementsByTagName('body')[0].classList.add("theme-light");
  document.getElementsByTagName('body')[0].dataset.bsTheme = "light";
}

//==========
// FUNCTIONS
function setCookie(name, value, days) {
  if (days) {
      const date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 *1000));
      var expires = "; expires=" + date.toGMTString();
  } else {var expires = ""}
  document.cookie = name + "=" + value + expires + "; path=/";
}

function getCookie(name) {
  let cname = name + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(cname) == 0) {
      return c.substring(cname.length, c.length);
    }
  }
  return "";
}

