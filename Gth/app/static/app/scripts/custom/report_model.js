//  ---BASIC FUNCTIONS---
var isLoading = true, pageBody = $("#page_body"), loadingBody = $("#loading_body");
function changeLoadingState(){
    isLoading = !isLoading;
    if(isLoading){
        pageBody.removeClass("hidden");
        loadingBody.addClass("hidden");
    } else {
        pageBody.addClass("hidden");
        loadingBody.removeClass("hidden");
    }
}
function request(url, callback, changeState = true) {
    if(isLoading)
        return;
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
            if(changeState)
                changeLoadingState();
        }
    };
    req.open("GET", url, true);
    if(changeState)
        changeLoadingState();
    req.send();
}
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
                    var detailButtons = inputDetailButtons();
                    
                    removeButtons.off(inputRemoveNamespace, removeInputClickHandler);
                    removeButtons.on(inputRemoveNamespace, removeInputClickHandler);
                    detailButtons.off(inputDetailsNamespace, inputDetailsClick);
                    detailButtons.on(inputDetailsNamespace, inputDetailsClick);
                }
            });
        });
}
function resetClick(obj, clickNamespace, func){
    obj.off(clickNamespace, func);
    obj.on(clickNamespace, func);
}
//  ---END BASIC FUNCTIONS---

//  ---PAGING---
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
//  ---END PAGING---



//  ---CLICK NAMESPACES---
var 
inputRemoveNamespace = "click.remove_input",
inputDetailsNamespace = "click.details_input",

pageRemoveNamespace = "click.remove_page",
pageDirectionNamespace = "click.direction_page",
pageDetailsNamespace = "click.details_page",
addGroupNamespace = "click.add_group"
;
//  ---END CLICK NAMESPACES---



//  ---JQUERY ELEMENTS---
function basicInfoModal(){return $("#basic_info_modal");}
function basicInfoSaveButton(){return $("#basic_info_save");}
function basicInfoCancelButton(){return $("#basic_info_cancel");}
function addPageButton(){return $("#add_page_button");}
function reportTitleItem(){return $("#report_title");}

function pageRemoveButtons(){return $(".page-remove-button");}
function pageDirectionButtons(){return $(".page-direction-button");}
function pageDetailButtons(){return $(".page-details-button");}
function addGroupButtons(){return $(".add-group-button");}

function inputRemoveButtons(){return $(".input-remove-button");}
function inputDetailButtons(){return $(".input-details-button");}

function topPagination(){return $("#pagination_top");}
function bottomPagination(){return $("#pagination_bottom");}

//  ---END JQUERY ELEMENTS---




//  ---START LOGIC---
window.onload = function () {
    if (window.location.pathname.indexOf("new") !== -1)
        basicInfoModal().modal("show");

    makeSortable();
    addPageButton().click(addPageClickHandler);
    resetClick(pageRemoveButtons(), pageRemoveNamespace, removePageClickHandler);
    resetClick(inputRemoveButtons(), inputRemoveNamespace, removeInputClickHandler);
    
    resetClick(pageDetailButtons(), pageDetailsNamespace, pageDetailsClickHandler);
    resetClick(inputDetailButtons(), inputDetailsNamespace, inputDetailsClickHandler);
    
    resetClick(directionButton(), pageDirectionNamespace, directionClickHandler);
    
    resetClick(addGroupButtons(), addGroupNamespace, addGroupClickHandler);
};
var firstOpen = true, saveClick = false;
basicInfoSaveButton().click(function () {
    saveClick = true;
});
basicInfoModal().on("hidden.bs.modal", function () {
    if (window.location.pathname.indexOf("new") !== -1 && firstOpen && !saveClick) {
        window.location = "/models";
    }
    firstOpen = false;
});
//  ---END START LOGIC---



//TODO unified logic on save and cancel click






function addPageClickHandler() {
    request("/models/get_new_page/" + pageCount, function (result) {
        pageCount += 1;
        $("#pages-inner-container").append(result);

        var topPaginationItem = topPagination(), bottomPaginationItem = bottomPagination();
        var topLastButton = topPaginationItem.children("li").last(), bottomLastButton = bottomPaginationItem.children("li").last();

        topLastButton.remove();
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
        topPaginationItem.append(li);
        topPaginationItem.append(topLastButton);
        bottomPaginationItem.append(li.clone(true));
        bottomPaginationItem.append(bottomLastButton);

        resetClick(pageRemoveButtons(), pageRemoveNamespace, removePageClickHandler);
        resetClick(pageDirectionButtons(), pageDirectionNamespace, directionClickHandler);
        resetClick(addGroupButtons(), addGroupNamespace, addGroupClickHandler);

        changePage(pageCount);
    });
}
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
    topPagination().children("li").eq(-2).remove();
    bottomPagination().children("li").eq(-2).remove();
    pageCount -= 1;
    if (pageCount === 0)
        return;
    if (pageCount === 1)
        changePage(1);
    else
        changePage(pageNumber - 1 === 0 ? 1 : pageNumber - 1);
}
function removeInputClickHandler() {
    var parent = $(this).parents("li").eq(1);
    parent.remove();
}

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

function pageDetailsClickHandler() {
    var commonParent = $(this).closest(".page-panel");
    var modal = commonParent.children(".modal");
    modal.modal("show");
}
function inputDetailsClickHandler() {
    var commonParent = $(this).closest(".input-panel-container");
    var modal = commonParent.children(".modal");
    modal.modal("show");
}

function addGroupClickHandler() {
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