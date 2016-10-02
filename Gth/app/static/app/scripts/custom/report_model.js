function request(url, callback) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState === 4 && req.status === 200) {
            var reply = JSON.parse(req.responseText);
            if(callback)
                callback(reply);
        }
    };
    req.open("GET", url, true);
    req.send();
}

window.onload = function () {
    //if(window.location.pathname.indexOf("new") !== -1)
    //    $("#basic_info_modal").modal("show");

    var firstOpen = false, saveClick = false;
    //var firstOpen = true, saveClick = false;
    $("#basic_info_save").click(function() {
        var title = $("#id_title").val();
        if (!title)
            return;
        var errorHandler= function(reply) {
            console.log(reply);
        };
        $("#basic_info_form").ajaxSubmit({
            url: window.location.pathname + "/report", type: "post",
            success: function (reply) {
                if (reply.success) {
                    $("#report_title").html(title);
                    $("#basic_info_modal").modal("hide");
                    saveClick = true;
                } else {
                    errorHandler(reply);
                }
            },
            error: errorHandler
        });
    });
    $("#basic_info_modal").on("hidden.bs.modal", function() {
        if (window.location.pathname.indexOf("new") !== -1 && firstOpen && !saveClick) {
            window.location = "/models";
        }
        firstOpen = false;
    });
};