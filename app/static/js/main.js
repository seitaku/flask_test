
window.addEventListener('load',() =>{
    console.log('hello world')
})
baseData = {}
$(async function(){

    $(".left_menu_btn").click(function(){

        $(".left_menu_method").removeClass("show")
        // $(this).removeClass("active")
        // $(this).addClass("active")
        if ( $(this).hasClass("active") )
            $(this).removeClass("active")
        else
            $(".left_menu_btn").removeClass("active")
            $(this).addClass("active")
    });

    // $('#loginBtn').click(login)

    async function login() {
        let account = $('#account').val()
        let password = $('#password').val()

        let obj = {
            account: account,
            password: password
        }

        let headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            // "Authorization": `Bearer ${token}`,
        }

        let params = urlEncode(obj).slice(1)
        let api = '/login'
        console.log(obj)
        response = 
            await fetch(basePath + api, { method: 'POST',headers: headers, body: JSON.stringify(obj) })
                    .then(res => {
                        console.log('stp1')
                        console.log(res) 
                        
                        // console.log(res.text()) 
                        let view = res.text()
                        // console.log(view)
                        // $('.container').html(view)
                        return view

                        // return res.json()
                    })
                    .then(tables => {
                        console.log(tables)
                        // $('html').html(tables)
                    })
                    // .then(tables => {
                    //     console.log(tables)
                    //     $('.container').html(tables)}
                    // )
                    // .then(data => { 
                    //     console.log('stp2')
                    //     console.log(data)
                    //     if (data.code == 999) 
                    //     {
                    //         alert(data.msg)
                    //     }
                    //     else 
                    //     {
                    //         // call 登入成功頁面
                    //         // location.href='./qPage'
                    //     }
                    // })
                    .catch(err => {
                        console.log(err)
                    })
                    // JSON.parse(response)
        baseData = response
        console.log('response:', response)
    }//query end

    function render(result) {
    }
})//IIFE end