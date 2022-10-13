// Activate Featericons
feather.replace();

// Active class in current page
var page = window.location.href
var allLinks = document.getElementsByTagName('a');

for (var i = 0; i < allLinks.length; i++) {
    if (allLinks[i].href == page) {
        allLinks[i].classList.add('active');
    }
}
