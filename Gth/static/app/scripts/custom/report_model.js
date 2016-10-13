//  ---BASIC FUNCTIONS---
var isLoading = false, pageBody = $("#page_body"), loadingBody = $("#loading_body");
function changeLoadingState(){
    isLoading = !isLoading;
    if(isLoading){
        pageBody.addClass("hidden");
        loadingBody.removeClass("hidden");
    } else {
        pageBody.removeClass("hidden");
        loadingBody.addClass("hidden");
    }
}
function request(url, callback, changeState) {
    var state = changeState !== false;
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
            if(state)
                changeLoadingState();
        }
    };
    req.open("GET", url, true);
    if(state)
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

                    resetClick(inputRemoveButtons(), inputRemoveNamespace, removeInputClickHandler);
                    resetClick(inputDetailButtons(), inputDetailsNamespace, inputDetailsClickHandler);
                    resetClick(selectInputButtons(), selectInputNamespace, selectInputClickHandler);
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
pageDuplicateNamespace= "click.duplicate_page",
addGroupNamespace = "click.add_group",
selectInputNamespace = "click.select_input",

modalCancelNamespace = "click.cancel_modal",
modalSaveNamespace = "click.save_modal"
;
//  ---END CLICK NAMESPACES---



//  ---JQUERY ELEMENTS---
function basicInfoModal(){return $("#basic_info_modal");}
function basicInfoSaveButton(){return $("#basic_info_save");}
function basicInfoCancelButton(){return $("#basic_info_cancel");}
function addPageButton(){return $("#add_page_button");}
function reportTitleItem(){return $("#report_title");}
function inputTypeSelectButton() { return $("#input_type_select"); }

function topPagination() { return $("#pagination_top"); }
function bottomPagination() { return $("#pagination_bottom"); }

function pageRemoveButtons(){return $(".page-remove-button");}
function pageDirectionButtons(){return $(".page-direction-button");}
function pageDetailButtons() { return $(".page-details-button"); }
function pageDuplicateButtons() { return $(".page-duplicate-button"); }
function addGroupButtons() { return $(".page-add-group-button"); }

function selectInputButtons() { return $(".select-input-button"); }
function inputSelectModal() { return $("#input_type_modal"); }
function reportDetailsModalButton() { return $("#basic_info_modal_button"); }

function inputRemoveButtons() { return $(".input-remove-button"); }
function inputDetailButtons() { return $(".input-details-button"); }

function modalCancelButtons() { return $(".modal-cancel-button"); }
function modalSaveButtons() { return $(".modal-save-button"); }
function modalFormBody() { return $(".modal-form-body"); }
function modalLoadingBody() { return $(".modal-form-loading"); }
//  ---END JQUERY ELEMENTS---




//  ---START LOGIC---
window.onload = function () {
    if (window.location.pathname.indexOf("new") !== -1)
        basicInfoModal().modal("show");

    makeSortable();

    addPageButton().click(addPageClickHandler);
    resetClick(pageRemoveButtons(), pageRemoveNamespace, removePageClickHandler);
    resetClick(pageDuplicateButtons(), pageDuplicateNamespace, duplicateClickHandler);
    resetClick(pageDirectionButtons(), pageDirectionNamespace, directionClickHandler);
    resetClick(pageDetailButtons(), pageDetailsNamespace, pageDetailsClickHandler);

    inputTypeSelectButton().click(addInputClickHandler);
    reportDetailsModalButton().click(reportDetailsClickHandler);
    resetClick(inputRemoveButtons(), inputRemoveNamespace, removeInputClickHandler);
    resetClick(inputDetailButtons(), inputDetailsNamespace, inputDetailsClickHandler);
    
    
    resetClick(addGroupButtons(), addGroupNamespace, addGroupClickHandler);
    resetClick(selectInputButtons(), selectInputNamespace, selectInputClickHandler);

    resetClick(modalCancelButtons(), modalCancelNamespace, modalCancelClickHandler);
    resetClick(modalSaveButtons(), modalSaveNamespace, modalSaveClickHandler);

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



//  ---MODAL FORMS---
function showModal(selector, context) {
    if (selector.indexOf("#") !== -1)
        $(selector).modal("show");
    else
        context.closest(selector).children(".modal").modal("show");
}
function getModalFromButton(context) {
    return context.closest(".modal");
}

function getForm(context) {
    var container = context.parent().prev();
    return {
        'container': container,
        'form': container.children("form").first()
    }
}
function reportDetailsClickHandler() {
    showModal("#basic_info_modal");
}
function pageDetailsClickHandler() {
    showModal(".page-panel", $(this));
}
function inputDetailsClickHandler() {
    showModal(".input-panel-container", $(this));
}

var isModalLoading = false, currentRequest, currentForm, currentErrors;
function modalCancelClickHandler() {
    var self = $(this);
    var modal = getModalFromButton(self);
    if (isModalLoading) {
        if (currentRequest)
            currentRequest.abort();
        modalFormBody().removeClass("hidden");
        modalLoadingBody().addClass("hidden");
        isModalLoading = false;
    } else {
        modal.modal("hide");
    }
    var tmpForm = getForm(self),
            form = tmpForm['form'],
            formContainer = tmpForm["container"];
    if (currentErrors) {
        form.remove();
        currentForm[0].reset();
        formContainer.append(currentForm);
    } else {
        form[0].reset();
    }
    currentForm = null;
    currentErrors = false;
}
function modalSaveClickHandler() {
    if (isLoading)
        return;
    var self = $(this), tmpForm = getForm(self),
        formContainer = tmpForm['container'],
        target = self.attr("target"), modal = getModalFromButton(self),
        title = modal.prev().children(".panel-heading").children(".panel-title:first");
    currentForm = tmpForm['form'];
    isModalLoading = true;
    modalFormBody().addClass("hidden");
    modalLoadingBody().removeClass("hidden");
    currentForm.ajaxSubmit({
        type: "POST",
        url: "validate_form/" + target,
        success: function (result) {
            
            currentForm.remove();
            formContainer.append(result.html);
            currentErrors = !result.success;


            modalFormBody().removeClass("hidden");
            modalLoadingBody().addClass("hidden");
            isModalLoading = false;
            if (!result.success)
                return;
            modal.modal("hide");
            title.html(currentForm.find("#id_title").val() + "*");

        }, error: function (e) { console.log(e) }
    });
}
//  ---END MODAL FORMS---





//  ---INPUT---
function addGroupClickHandler() {
    var page = $(this).closest(".panel");
    request("/models/get_new_group", function (result) {

        var list = page.children(".panel-body").children("ol");
        var li = $(document.createElement("li"));
        li.append(result);
        list.append(li);

        resetClick(inputRemoveButtons(), inputRemoveNamespace, removeInputClickHandler);
        resetClick(inputDetailButtons(), inputDetailsNamespace, inputDetailsClickHandler);
        resetClick(modalCancelButtons(), modalCancelNamespace, modalCancelClickHandler);
        resetClick(modalSaveButtons(), modalSaveNamespace, modalSaveClickHandler);
        makeSortable();
    });
}

var currentInputCallback;
function selectInputClickHandler() {
    inputSelectModal().modal("show");
    var self = $(this);
    var li = $(document.createElement("li")),
        ol = self.attr("source") === "page"
        ? $(".page-panel").not(".hidden").find(".panel-body").closest("ol").first()
        : self.closest(".input-panel-container").find("ol").first();
    currentInputCallback = function (result) {
        li.append(result);
        ol.append(li);
    }
}

function addInputClickHandler() {
    var types = $(".input-select-radio"), selected = 0;
    for (input in types) {
        if (types.hasOwnProperty(input)) {
            var current = $(types[input]);
            if (current.is(":checked"))
                selected = current.attr("type-value");
        }
    }
    request("/models/get_new_input/" + selected, function (result) {
        if (currentInputCallback)
            currentInputCallback(result);
        resetClick(inputRemoveButtons(), inputRemoveNamespace, removeInputClickHandler);
        resetClick(inputDetailButtons(), inputDetailsNamespace, inputDetailsClickHandler);
        resetClick(modalCancelButtons(), modalCancelNamespace, modalCancelClickHandler);
        resetClick(modalSaveButtons(), modalSaveNamespace, modalSaveClickHandler);
        makeSortable();
    });
}
function removeInputClickHandler() {
    var parent = $(this).parents("li").eq(1);
    parent.remove();
}
//  ---END INPUT---


//  ---PAGE---
function addPageClickHandler() {
    request("/models/get_new_page/" + pageCount, function (result) {
        addPageCommon(result);
    });
}
function duplicateClickHandler() {
    var page = $(this).closest(".page-panel");
    var clone = page.clone(true);
    clone.attr("page", pageCount + 1);
    addPageCommon(clone);
}

function addPageCommon(pageHtml) {
    pageCount += 1;
    $("#pages-inner-container").append(pageHtml);

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
    resetClick(selectInputButtons(), selectInputNamespace, selectInputClickHandler);
    resetClick(modalCancelButtons(), modalCancelNamespace, modalCancelClickHandler);
    resetClick(modalSaveButtons(), modalSaveNamespace, modalSaveClickHandler);

    changePage(pageCount);
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
function directionClickHandler() {
    var self = $(this);
    var dir = self.attr("direction");
    var pageDiv = $(this).parents("div[page]");
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
//  ---END PAGE---