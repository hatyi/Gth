function request(url, callback) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState === 4 && req.status === 200) {
            try {
                var reply = JSON.parse(req.responseText);
                if (callback)
                    callback(reply);
            } catch (e) {
                callback(req.responseText);
            } 
            
        }
    };
    req.open("GET", url, true);
    req.send();
}

window.onload = function () {
    if(window.location.pathname.indexOf("new") !== -1)
        $("#basic_info_modal").modal("show");

    var firstOpen = true, saveClick = false, reportTitle, reportDescription;
    $("#basic_info_save").click(function () {
        reportTitle = null;
        reportDescription = null;
        var title = $("#id_title").val();
        if (!title)
            return;
        $("#report_title").html(title);
        $("#basic_info_modal").modal("hide");
        saveClick = true;
    });
    $("#basic_info_cancel").click(function() {
        if (reportTitle && reportDescription) {
            $("#id_title").val(reportTitle);
            $("#id_description").val(reportDescription);
        }
    });
    $("#basic_info_modal").on("shown.bs.modal", function() {
        reportTitle = $("#id_title").val();
        reportDescription = $("#id_description").val();
    });
    $("#basic_info_modal").on("hidden.bs.modal", function() {
        if (window.location.pathname.indexOf("new") !== -1 && firstOpen && !saveClick) {
            window.location = "/models";
        }
        firstOpen = false;
    });

    makeSortable();
};

function makeSortable() {
    Array.prototype.forEach.call(
        document.getElementsByClassName("sortable-list"), function(item) {
            Sortable.create(item, {
                group: { name: "sortable", pull: true, put: true },
                onAdd: function(e) {
                    var from = $(e.from), to = $(e.to), input = $(e.item);
                    if (!(!from.hasClass("sortable-list-group")
                        && to.hasClass("sortable-list-group")
                        && input.attr("input-type") === "group"))
                        return;
                    input.remove();
                    var children = from.children();
                    if (children.length > 1)
                        children.eq(e.oldIndex).after(input);
                    else
                        children.eq(e.oldIndex - 1).after(input);
                    $(".input-remove-button").off("click.remove_input", removeInputClickHandler);
                    $(".input-remove-button").on("click.remove_input", removeInputClickHandler);
                    $(".input-details-button").off("click.input_details", inputDetailsClick);
                    $(".input-details-button").on("click.input_details", inputDetailsClick);
                }
            });
        });
}


//PAGING
var page = 1, pageCount, pagesVisible;
function initPages(pagesLength, pageButtonsVisible) {
    pageCount = parseInt(pagesLength);
    pagesVisible = parseInt(pageButtonsVisible);
    $(".page-button-" + 1).addClass("active");
}
function changePage(param) {
    var targetPage;
    if (param === "next")
        targetPage = page + 1;
    else if (param === "prev")
        targetPage = page - 1;
    else
        targetPage = parseInt(param);

    if (targetPage < 1 || targetPage > pageCount)
        return;

    $(".page-button-" + page).removeClass("active");
    $(".page-button-" + targetPage).addClass("active");

    var animDuration = 300, animSpeed = 100;
    $(".page-panel").each(function () {
        var self = $(this);
        var inc = 1 / animSpeed;
        
        if ($(this).attr("page") !== "" + targetPage) {
            self.addClass("hidden");
        } else {
            var animIn = setInterval(function () {
                var current = parseFloat(self.css("opacity"));
                self.css({ "opacity": current + inc });
            }, animDuration / animSpeed);
            self.css({ "opacity": 0 });
            self.removeClass("hidden");
            setTimeout(function () {
                clearInterval(animIn);
                self.css({ "opacity": 1 });
            }, animDuration);
        }
    });
    page = targetPage;


    var visiblePages = [], i;
    if (page <= Math.ceil(pagesVisible / 2)) {
        for (i = 1; i <= pagesVisible; i++) {
            visiblePages.push(i);
        }
    } else if (page >= pageCount - Math.floor(pagesVisible / 2)) {
        for (i = pageCount; i > pageCount - pagesVisible; i--) {
            visiblePages.push(i);
        }
    } else {
        for (i = page - Math.floor(pagesVisible / 2) ; i <= page + Math.floor(pagesVisible / 2) ; i++) {
            visiblePages.push(i);
        }
    }

    $(".table-page-button").each(function () {
        var id = parseInt($(this).attr("data-page"));
        if (visiblePages.indexOf(id) !== -1)
            $(this).removeClass("hidden");
        else
            $(this).addClass("hidden");
    });
}

var canClick = true;
$("#add_page_button").click(function () {
    if (!canClick)
        return;
    canClick = false;
    $("#page_body").addClass("hidden");
    $("#loading_body").removeClass("hidden");
    request("/models/get_new_page/" + pageCount, function (result) {
        pageCount += 1;
        $("#pages-inner-container").append(result);
        var topLastButton = $("#pagination_top li").last();
        topLastButton.remove();
        var bottomLastButton = $("#pagination_bottom li").last();
        bottomLastButton.remove();
        var li = $(document.createElement("li"));
        li.attr("data-page", pageCount);
        li.addClass("page-button-" + pageCount + " table-page-button");
        var a = $(document.createElement("a"));
        a.html(pageCount);
        var currentCount = pageCount;
        a.click(function () {
            changePage(currentCount);
        });
        li.append(a);
        $("#pagination_top").append(li);
        $("#pagination_top").append(topLastButton);
        $("#pagination_bottom").append(li.clone(true));
        $("#pagination_bottom").append(bottomLastButton);
        $(".btn-danger.panel-button").off("click.remove_page");
        $(".btn-danger.panel-button").on("click.remove_page", removePageClickHandler);
        $(".btn-info.panel-button").off("click.move_page");
        $(".btn-info.panel-button").on("click.move_page", directionClickHandler);
        $(".page-panel #id_title").off("input.title_input");
        $(".page-panel #id_title").on("input.title_input", titleInputHandler);
        $("#loading_body").addClass("hidden");
        $("#page_body").removeClass("hidden");
        changePage(pageCount);
        canClick = true;
    });
});
$(".page-remove-button").on("click.remove_page", removePageClickHandler);
function removePageClickHandler() {
    var pageDiv = $(this).closest(".page-panel");
    var pageNumber = parseInt(pageDiv.attr("page"));
    $(".page-panel").each(function () {
        var self = $(this);
        var current = parseInt(self.attr("page"));
        if (current > pageNumber)
            self.attr("page", current - 1);
    });
    pageDiv.remove();
    $("#pagination_top li").eq(-2).remove();
    $("#pagination_bottom li").eq(-2).remove();
    pageCount -= 1;
    if (pageCount === 0)
        return;
    if (pageCount === 1)
        changePage(1);
    else
        changePage(pageNumber - 1 === 0 ? 1 : pageNumber - 1);
}


$(".input-remove-button").on("click.remove_input", removeInputClickHandler);
function removeInputClickHandler() {
    var parent = $(this).closest("li");
    parent.remove();
}

$(".btn-info.panel-button").on("click.move_page", directionClickHandler);
function directionClickHandler() {
    var self = $(this);
    var dir = self.attr("direction");
    var pageDiv = $(this).parent().parent().parent();
    var pageNumber = parseInt(pageDiv.attr("page"));
    var targetPosition;
    if (dir === "left")
        targetPosition = pageNumber - 1;
    else
        targetPosition = pageNumber + 1;
    if (targetPosition === 0 || targetPosition > pageCount)
        return;
    $("div[page='" + targetPosition + "']").attr("page", pageNumber);
    pageDiv.attr("page", targetPosition);
    changePage(targetPosition);
}

$(".page-panel #id_title").on("input.title_input", titleInputHandler);
function titleInputHandler() {
    var self = $(this);
    if(self.val())
        $("div[page='" + page + "'] > div > div > h2").html(self.val());
    else
        $("div[page='" + page + "'] > div > div > h2").html("Edit title");
}

$(".page-details-button").on("click.page_details", pageDetailsClick);
function pageDetailsClick() {
    var commonParent = $(this).closest(".page-panel");
    var modal = commonParent.children(".modal");
    modal.modal("show");
}

$(".input-details-button").on("click.input_details", inputDetailsClick);
function inputDetailsClick(){
    var commonParent = $(this).closest(".input-panel-container");
    var modal = commonParent.children(".modal");
    modal.modal("show");
}
