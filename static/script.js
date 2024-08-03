function clk(newImg) {
    let getImg = document.getElementById("imgs");
    getImg.src = newImg.src;
}

function wcqib_refresh_quantity_increments() {
    jQuery("div.quantity:not(.buttons_added), td.quantity:not(.buttons_added)").each(function (a, b) {
        var c = jQuery(b);
        c.addClass("buttons_added"), c.children().first().before('<input type="button" value="-" class="minus" />'), c.children().last().after('<input type="button" value="+" class="plus" />')
    })
}
String.prototype.getDecimals || (String.prototype.getDecimals = function () {
    var a = this,
        b = ("" + a).match(/(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/);
    return b ? Math.max(0, (b[1] ? b[1].length : 0) - (b[2] ? +b[2] : 0)) : 0
}), jQuery(document).ready(function () {
    wcqib_refresh_quantity_increments()
}), jQuery(document).on("updated_wc_div", function () {
    wcqib_refresh_quantity_increments()
}), jQuery(document).on("click", ".plus, .minus", function () {
    var a = jQuery(this).closest(".quantity").find(".qty"),
        b = parseFloat(a.val()),
        c = parseFloat(a.attr("max")),
        d = parseFloat(a.attr("min")),
        e = a.attr("step");
    b && "" !== b && "NaN" !== b || (b = 0), "" !== c && "NaN" !== c || (c = ""), "" !== d && "NaN" !== d || (d = 0), "any" !== e && "" !== e && void 0 !== e && "NaN" !== parseFloat(e) || (e = 1), jQuery(this).is(".plus") ? c && b >= c ? a.val(c) : a.val((b + parseFloat(e)).toFixed(e.getDecimals())) : d && b <= d ? a.val(d) : b > 0 && a.val((b - parseFloat(e)).toFixed(e.getDecimals())), a.trigger("change")
});

function check_size() {
    var getSelectedValue = document.querySelector('input[name="size"]:checked');
    const popover = document.getElementById('popsovers');
    if (getSelectedValue == null) {
        popover.style.transition = 'opacity 0.2s ease-in-out';
        popover.style.opacity = '1';
        setTimeout(function () {
            popover.style.transition = 'opacity 0.2s ease-in-out';
            popover.style.opacity = '0';
        }, 5000);
        const position = popover.getBoundingClientRect().top + window.scrollY - 100;
        window.scrollTo({
            top: position,
            behavior: 'smooth'
        });
        event.preventDefault();
    }
}

function isValidPinCode() {
    console.log('Hi')
    let regex = new RegExp(/^[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}$/);
    zip = document.getElementById('inputZip').value
    if (zip == null) {
        return false;
    }

    if (regex.test(zip) == true) {
        return true;
    }
    else {
        return false;
    }
}

document.getElementById('addAddressForm').addEventListener('submit', function (event) {
    if (!isValidPinCode()) {
        event.preventDefault();
        alert('Invalid ZIP Code');
    }
});


// document.addEventListener("DOMContentLoaded", function(event) {
//     $(function() {
//         $('.jscroll').jscroll({
//             autoTrigger: true,
//             padding: 2000,
//             nextSelector: "a:last"
//         });
//     });
//   });