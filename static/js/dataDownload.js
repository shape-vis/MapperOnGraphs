
    function downloadText(text, filename) {
        var a = document.createElement('a');
        a.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        a.setAttribute('download', filename);
        a.click()
    }

    function downloadJson(obj, filename) {
        downloadText(JSON.stringify(obj), filename);
    }
