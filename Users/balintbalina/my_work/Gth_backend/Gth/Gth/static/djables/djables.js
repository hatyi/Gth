var filterUrl,
    defaultQuery = window.location.search,
    orderBy = "",
    doneTypingInterval = 1000,
    typingTimer,
    rows = {},
    pageButtons = {},
    specialInput = {};

var $input = $(".djable-search-input"), $tableBody = $("#djable_body"), filterIcon = $("#djable_special_toggle");
$tableBody.removeClass("hidden");

//FILTER
function emptyElement(element) {
    var i = element.childNodes.length;
    while (i--) {
        element.removeChild(element.lastChild);
    }
}

function resetRows(ids) {
    if (ids.length === 0)
        return;
    pageCount = ids.length;
    ids.forEach(function(item) {
        var btnIndex = "page-button-" + item.page;
        if (pageButtons.hasOwnProperty(btnIndex))
            pageButtons[btnIndex].removeClass("hidden");

        for (var index in item.items) {
            if (item.items.hasOwnProperty(index)) {
                var id = item.items[index];
                var current = rows["djable_" + id];
                current.removeClass("table-row-even");
                current[0].setAttribute("djable-page", item.page);
                $tableBody.append(current);
            }
        }
    });
    changePage(1);
}

function filterTableRequest() {
    $("#djable_body").addClass("hidden");
    $("#djable_loading_body").removeClass("hidden");

    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState === 4 && req.status === 200) {
            var reply = JSON.parse(req.responseText);
            emptyElement($tableBody[0]);
            for (var key in pageButtons) {
                if (pageButtons.hasOwnProperty(key)) {
                    pageButtons[key].addClass("hidden");
                }
            }
            resetRows(reply.ids);
            $tableBody.removeClass("hidden");
            $("#djable_loading_body").addClass("hidden");
        }
    };

    var any = false;
    var base = filterUrl + defaultQuery;
    var searchChar = defaultQuery !== "" ? "&" : "?";
    var url = base +
        searchChar + "query=" + $input[0].value +
        "&order=" + orderBy;
    for (var item in specialInput) {
        if (specialInput.hasOwnProperty(item)) {
            if (specialInput[item] !== "") {
                url += "&" + item + "=" + specialInput[item];
                any = true;
            }
        }
    }
    
    req.open("GET", url, true);
    req.send();
    changeFilterIcon(any);
}

function changeFilterIcon(any) {
    if (any) {
        filterIcon.removeClass("djable-filter-inactive");
        filterIcon.addClass("djable-filter-active");
    } else {
        filterIcon.removeClass("djable-filter-active");
        filterIcon.addClass("djable-filter-inactive");
    }
}
function specialResetClick() {
    $(".djable-special-input").val("");
    for (var item in specialInput) {
        if (specialInput.hasOwnProperty(item)) {
            specialInput[item] = "";
        }
    }
    filterTableRequest();
}



$(".table-row").each(function() {
    rows[$(this).attr("id")] = $(this);
});
$(".table-page-button").each(function() {
    pageButtons[$(this).attr("id")] = $(this);
});
//AUTOFILTER
$input.on("keyup", function() {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(filterTableRequest, doneTypingInterval);
});
$input.on("keydown", function(e) {
    if (e.key === "Enter")
        filterTableRequest();
    else
        clearTimeout(typingTimer);
});

//ORDERING
$(".table-header-orderable").click(function(event) {
    var target = event.target;
    var state = target.getAttribute("data-state");
    if (state === "" || state === "desc") {
        $(".table-header").removeClass("asc");
        $(".table-header").removeClass("desc");
        target.className = "table-header asc";
        target.setAttribute("data-state", "asc");
        orderBy = target.getAttribute("djable-ordering-name");
    } else {
        $(".table-header").removeClass("asc");
        $(".table-header").removeClass("desc");
        target.className = "table-header desc";
        target.setAttribute("data-state", "desc");
        orderBy = "-" + target.getAttribute("djable-ordering-name");
    }
    filterTableRequest();
});


//DATE, DATETIME, INT INPUT
$(".djable-input-date").on("keyup", function(e) {
    if (e.keyCode === 8 || e.keyCode === 46)
        return;
    var raw = $(this).val().replace(/\//g, "");
    var years = raw.substring(0, 4);
    var months = raw.substring(4, 6);
    var days = raw.substring(6, 8);
    var result = years;
    if (years.length === 4)
        result += "/" + months;
    if (months.length === 2)
        result += "/" + days;

    $(this).val(result);
});
$(".djable-input-datetime").on("keyup", function(e) {
    if (e.keyCode === 8 || e.keyCode === 46)
        return;
    var raw = $(this).val().replace(/\//g, "").replace(/\s/g, "").replace(/:/g, "");
    var year = raw.substring(0, 4);
    var month = raw.substring(4, 6);
    var day = raw.substring(6, 8);
    var hour = raw.substring(8, 10);
    var min = raw.substring(10, 12);


    var result = year;
    if (year.length === 4)
        result += "/" + month;
    if (month.length === 2)
        result += "/" + day;
    if (day.length === 2)
        result += " " + hour;
    if (hour.length === 2)
        result += ":" + min;
    $(this).val(result);
});
$(".djable-special-input.djable-input-date").on("keyup", function() {
    var val = $(this).val();
    if (/^[1-2][0-9][0-9][0-9]\/(0[1-9]|1[0-2])\/([0-2][1-9]|3[0-1])$/.test(val)) {
        specialInput[$(this).attr("id")] = val.replace(/\//g, "-");
    } else {
        specialInput[$(this).attr("id")] = "";
    }
});
$(".djable-special-input.djable-input-datetime").on("keyup", function() {
    var val = $(this).val();
    if (/^[1-2][0-9][0-9][0-9]\/(0[1-9]|1[0-2])\/([0-2][1-9]|3[0-1]) [0-2][0-9]:[0-5][0-9]$/.test(val)) {
        specialInput[$(this).attr("id")] = val.replace(/\//g, "-").replace(" ", "-").replace(":", "-");
    } else {
        specialInput[$(this).attr("id")] = "";
    }
});
$(".djable-special-input.djable-input-int").on("keyup", function() {
    var val = $(this).val();
    if (/^[0-9]+$/.test(val)) {
        specialInput[$(this).attr("id")] = val;
    } else {
        specialInput[$(this).attr("id")] = "";
    }
});

//TEXT
$(".djable-special-input.djable-input-text").on("keyup", function () {
    specialInput[$(this).attr("id")] = $(this).val();
});

//CHOICE
$(".djable-special-choice").on("click", function() {
    $(".djable-special-choice").removeClass("active");
    $(this).addClass("active");
    var val = $(this).attr("djable-choice-value");
    if (val !== "-")
        specialInput[$(this).attr("djable-choice-key")] = val;
    else
        delete specialInput[$(this).attr("djable-choice-key")];
});


//MAIN
var page = 1, pageCount, itemsPerPage, pagesVisible;

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

    $("#page-button-" + page).removeClass("active");
    $("#page-button-" + targetPage).addClass("active");
    $(".paged-table-row").each(function() {
        if ($(this).attr("djable-page") !== "" + targetPage)
            $(this).addClass("hidden");
        else
            $(this).removeClass("hidden");
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

    $(".table-page-button").each(function() {
        var id = parseInt($(this).attr("id").split("-")[2]);
        if (visiblePages.indexOf(id) !== -1)
            $(this).removeClass("hidden");
        else
            $(this).addClass("hidden");
    });
}

var modelName, specialVisible = false;
function initPages(pagesLength, itemsOnPage, pageButtonsVisible, djablesModelName) {
    pageCount = parseInt(pagesLength);
    itemsPerPage = parseInt(itemsOnPage);
    pagesVisible = parseInt(pageButtonsVisible);
    modelName = djablesModelName;
    filterUrl = "/djables_filter/" + modelName;
    changePage(1);
}

function toggleSpecialFilters(sender) {
    var div = $("#djable_special_filters");
    if (specialVisible) {
        div.hide();
        sender.removeClass("fa-caret-up");
        sender.addClass("fa-caret-down");
    } else {
        div.show();
        div.removeClass("hidden");
        sender.removeClass("fa-caret-down");
        sender.addClass("fa-caret-up");
    }
    specialVisible = !specialVisible;
}