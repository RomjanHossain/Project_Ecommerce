$(document).ready(function() {

    // Contact Form Handler

    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action") // /abc/

    function displaySubmitting(submitBtn, defaultText, doSubmit) {
        if (doSubmit) {
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
        } else {
            submitBtn.removeClass("disabled")
            submitBtn.html(defaultText)
        }
    }
    contactForm.submit(function(event) {
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmitting(contactFormSubmitBtn, "", true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function(data) {
                contactForm[0].reset()
                // jQuery.confirm({
                // 	title: "Success!",
                // 	content: data.message,
                // 	theme: "supervan",
                // });
                alert('Success', data.message)
                setTimeout(function() {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            },
            error: function(error) {
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ""
                $.each(jsonData, function(key, value) { // key, value  array index / object
                    msg += key + ": " + value[0].message
                })
                //   $.alert({
                //     title: "Oops!",
                //     content: msg,
                //     theme: "supervan",
                // });
                // $.alert({
                // 	title: 'Alert!',
                // 	content: 'Simple alert!',
                // });
                alert(msg)
                setTimeout(function() {
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)

            }
        })
    })
    // Auto Search

    var searchForm = $('#search_mini_form')
    var searchInput = searchForm.find('[name="q"]')
    var searchBtn = searchForm.find("[type='submit']")
    var typingTimer;
    var typingInterval = 500 // .5 seconds

    searchInput.keyup(function(event) {
        // console.log(searchInput.val())
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })
    searchInput.keydown(function(event) {
        clearTimeout(typingTimer)
    })

    function doSearch() {
        searchBtn.addClass('disabled')
        searchBtn.html("<i class=fa fa-spin fa-spinner></i> Searching....")
    }

    function performSearch() {
        doSearch()
        var query = searchInput.val()
        setTimeout(function() {
            window.location.href = '/search/?q=' + query
        }, 10000)
    }
    // cart + add Product
    var productForm = $(".FormProductAjax")
    productForm.submit(function(event) {
        event.preventDefault();
        //console.log('form is not sending!')
        var thisForm = $(this)
        var actionEndpoint = thisForm.attr('data-endpoint');
        var httpmethod = thisForm.attr('method');
        var formData = thisForm.serialize();
        $.ajax({
            url: actionEndpoint,
            method: httpmethod,
            data: formData,
            success: function(data) {
                console.log('sucess')
                console.log(data)
                var submitSpan = thisForm.find('.addtocart__actions')
                console.log(submitSpan.html())
                if (data.added) {
                    submitSpan.html('<button class="tocart" type="submit" title="Remove">Remove</button>')
                } else {
                    submitSpan.html('<button class="tocart" type="submit" title="Add to Cart">Add to Cart</button>')
                }
                var navbarCount = $('.product_qun')
                navbarCount.text(data.cartItemCount)
                var currentPath = window.location.href
                // console.log(currentPath)
                if (currentPath.indexOf('cart') != -1) {
                    refreshCart()
                }
            },
            error: function(errorData) {
                // $.alert({
                // 	title: 'Opps@!',
                // 	context: 'An error occorred',
                // 	theme: 'modern',
                // });
                alert('An error occorred!')
                // console.log('error')
                // console.log(errorData)
            }
        })
    })

    function refreshCart() {
        console.log('in current cart')
        var taka = $('.amountChange')
        var cartTable = $('.cart-table')
        var cartBody = cartTable.find('.cart-body')
        // cartBody.html('<h1>Changed</h1>') <= this works
        var productRows = cartBody.find(".cart-product")
        // productRows.html('<tr><td>Coming Soon</td></tr>') <== this works too
        var currentUrl = window.location.href

        var refreshCartUrl = '/api/cart/'
        var refreshCartMethod = 'GET';
        var data = {};
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function(data) {
                var hiddenCartItemRemoveForm = $('.cart-item-remove-form')
                console.log('success')
                console.log(data)
                if (data.products.length > 0) {
                    productRows.html('') //<= this not works , shit
                    $.each(data.products, function(index, value) {
                        // console.log(value)
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone() //cart-item-productId
                        // console.log(newCartItemRemove.find('.cart-item-productId').val(value.id))
                        newCartItemRemove.css('display', 'block')
                        newCartItemRemove.find('.cart-item-productId').val(value.id)
                        // console.log(newCartItemRemove.find('.cart-item-productId').val(value.id).html())
                        cartBody.prepend("<tr>" +
                            '<td class="product-thumbnail"><a href="' + value.url + '"><img src="' + value.image + '" alt="product img"></a></td>' +
                            '<td class="product-name"><a href="' + value.url + '">' + value.name + '</a></td>' +
                            "<td class='product-price'>" +
                            value.price + "</td>" +
                            "<td class='product-quantity'><input type='number' value='1'>" + "</td>" +
                            "<td class='product-price'>" +
                            value.price + "</td>" + "<td>" +
                            newCartItemRemove.html() + "</td>" +
                            "</td>" + "</tr>")
                    })
                    // cartBody.prepend('<tr><td>Coming Soon</td></tr>')
                    taka.find('.cart-subtotal').text(data.subtotal)
                    taka.find('.cart-total').text(data.total)
                } else {
                    window.location.href = currentUrl
                }
            },
            error: function(errorData) {
                // $.alert({
                // 	title: 'Opps@!',
                // 	context: 'An error occorred',
                // 	theme: 'modern',
                // });
                alert('An error Occorred')

            }
        })
    }
})
