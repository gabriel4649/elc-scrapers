var urls = [];

function getLinks(urls) {
    for (var i= document.links.length; i-->0;) {
        var link = document.links[i].href;
        var index = urls.indexOf(link);
        if (index == -1) {
            console.log("Inserting:" + link);
            urls.push(link);
        }
    }

    return;
}

function copyToClipboard(text) {
    window.prompt ("Copy to clipboard: Ctrl+C, Enter", text);
}

//copyToClipboard(urls);

setInterval("getLinks(urls)", 1000);
