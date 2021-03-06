﻿function request(url, callback) {
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

//JQUERY ELEMENTS
function basicInfoModal(){return $("#basic_info_modal");}
function basicInfoSaveButton(){return $("#basic_info_save");}
function basicInfoCancelButton(){return $("#basic_info_cancel");}
function inputRemoveButtons(){return $(".input-remove-button");}
function inputDetailButtons(){return $(".input-details-button");}

//CLICK NAMESPACES
var 
inputRemoveNamespace = "click.remove_input",
inputDetailsNamespace = "click.details_input";


window.onload = function () {
    if (window.location.pathname.indexOf("new") !== -1)
        basicInfoModal().modal("show");
    makeSortable();
};



function makeSortable() {
    Array.prototype.forEach.call(
        document.getElementsByClassName("sortable-list"), function (item) {
            Sortable.create(item, {
                group: { name: "sortable", pull: true, put: true },
                onAdd: function (e) {
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
                    var removeButtons = inputRemoveButtons();
                    var detailButtons = inputRemoveButtons();
                    
                    removeButtons.off(inputRemoveNamespace, removeInputClickHandler);
                    removeButtons.on(inputRemoveNamespace, removeInputClickHandler);
                    detailButtons.off(inputDetailsNamespace, inputDetailsClick);
                    detailButtons.on(inputDetailsNamespace, inputDetailsClick);
                }
            });
        });
}

var firstOpen = true, saveClick = false, reportTitle, reportDescription;
basicInfoSaveButton().click(function () {
    reportTitle = null;
    reportDescription = null;
    var title = $("#id_title").val();
    if (!title)
        return;
    $("#report_title").html(title);
    $("#basic_info_modal").modal("hide");
    saveClick = true;
});
basicInfoCancelButton().click(function () {
    if (reportTitle && reportDescription) {
        $("#id_title").val(reportTitle);
        $("#id_description").val(reportDescription);
    }
});
$("#basic_info_modal").on("shown.bs.modal", function () {
    reportTitle = $("#id_title").val();
    reportDescription = $("#id_description").val();
});
$("#basic_info_modal").on("hidden.bs.modal", function () {
    if (window.location.pathname.indexOf("new") !== -1 && firstOpen && !saveClick) {
        window.location = "/models";
    }
    firstOpen = false;
});



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
        for (i = page - Math.floor(pagesVisible / 2); i <= page + Math.floor(pagesVisible / 2); i++) {
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

        $(".add-group-button").off("click.add_group", addGroupToPage);
        $(".add-group-button").on("click.add_group", addGroupToPage);


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
    var parent = $(this).parents("li").eq(1);
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

$(".page-details-button").on("click.page_details", pageDetailsClick);
function pageDetailsClick() {
    var commonParent = $(this).closest(".page-panel");
    var modal = commonParent.children(".modal");
    modal.modal("show");
}

$(".input-details-button").on(inputDetailsNamespace, inputDetailsClick);
function inputDetailsClick() {
    var commonParent = $(this).closest(".input-panel-container");
    var modal = commonParent.children(".modal");
    modal.modal("show");
}

$(".add-group-button").on("click.add_group", addGroupToPage);
function addGroupToPage() {
    var page = $(this).closest(".panel");
    canClick = false;
    $("#page_body").addClass("hidden");
    $("#loading_body").removeClass("hidden");
    request("/models/get_new_group", function (result) {

        var list = page.children(".panel-body").children("ol");
        var li = $(document.createElement("li"));
        li.append(result);
        list.append(li);

        $(".input-remove-button").off("click.remove_input", removeInputClickHandler);
        $(".input-remove-button").on("click.remove_input", removeInputClickHandler);
        $(".input-details-button").off(inputDetailsNamespace, inputDetailsClick);
        $(".input-details-button").on(inputDetailsNamespace, inputDetailsClick);
        makeSortable();

        $("#loading_body").addClass("hidden");
        $("#page_body").removeClass("hidden");
        canClick = true;
    });
}

$("#input_type_select").click(function () {
    var page = $(".page-panel").not(".hidden");
    canClick = false;
    $("#page_body").addClass("hidden");
    $("#loading_body").removeClass("hidden");
    var types = $(".input-select-radio"), selected = 0;
    for (input in types) {
        if (types.hasOwnProperty(input)) {
            var current = $(types[input]);
            if (current.is(":checked"))
                selected = current.attr("type-value");
        }
    }
    request("/models/get_new_input/" + selected, function (result) {

        var list = page.find(".panel-body").closest("ol").first();
        var li = $(document.createElement("li"));
        li.append(result);
        list.append(li);

        $(".input-remove-button").off("click.remove_input", removeInputClickHandler);
        $(".input-remove-button").on("click.remove_input", removeInputClickHandler);
        $(".input-details-button").off(inputDetailsNamespace, inputDetailsClick);
        $(".input-details-button").on(inputDetailsNamespace, inputDetailsClick);

        $("#loading_body").addClass("hidden");
        $("#page_body").removeClass("hidden");
        canClick = true;
    });
});