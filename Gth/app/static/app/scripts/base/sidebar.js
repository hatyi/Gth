function resize() {
    sideBar.style.height = (window.innerHeight - 70) + "px";
}

var sideBar = document.getElementById("sideBar");
resize();
window.onresize = resize;