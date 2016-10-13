function resize() {
    var width = parseInt(window.innerWidth);
    if(width >= 992)
        sideBar.style.height = (window.innerHeight - 70) + "px";
    else
        sideBar.style.height = "";
}

var sideBar = document.getElementById("sideBar");
resize();
window.onresize = resize;