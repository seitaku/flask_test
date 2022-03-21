
window.addEventListener('load',() =>{
    console.log('hello world')
})
baseData = {}
$(async function(){

    $('#queryBtn').click(query)

    async function query() {
        let cusCode = $('#cusCode').val()
        let prdName = $('#prdName').val()

        let obj = {
            cusCode: cusCode,
            prdName: prdName
        }

        let params = urlEncode(obj).slice(1)
        let api = '/nq?'

        response = 
            await fetch(basePath + api + params, {method:'GET'})
                    .then(res => {
                        return res.json()
                    })
                    .then(data => { 
                        return JSON.parse(data.res)
                    })
                    .catch(err => console.log(err))
                    // JSON.parse(response)
        
        console.log('response:', response)
    }//query end

    function render(result) {
    }
})//IIFE end