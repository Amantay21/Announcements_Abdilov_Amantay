async function makeRequest(url, method = 'GET') {
        let response = await fetch(url, {method});

        if (response.ok) {  // нормальный ответ
            return await response.json();
        } else {            // ошибка
            let error = new Error(response.statusText);
            error.response = response;
            throw error;
        }

}

    async function onClick2(e){
        e.preventDefault()
        let b = e.target;
        let data = await makeRequest(b.dataset['test']);
        console.log(data);
    }

    function onLoad() {
            let button = document.getElementById('button1');
            button.addEventListener('click', onClick2)
        }

    window.addEventListener('load', onLoad);